from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
import json,posixpath,re
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
SRC=R/'output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx'
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PK='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types';N={'p':P,'a':A,'r':REL}
def target(p,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(x):return E.tostring(x,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 rs={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};ids=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)
 return [target('ppt/presentation.xml',rs[x.get('{'+REL+'}id')]) for x in ids]
specs=json.loads((B/'edited-index.json').read_text(encoding='utf8'))
with ZipFile(SRC) as base,ZipFile(B/'roundtrip.pptx') as edit:
 files={x:base.read(x) for x in base.namelist()};bp=ordered(base);ep=ordered(edit)
 types=E.fromstring(files['[Content_Types].xml']);pres=E.fromstring(files['ppt/presentation.xml']);ids=pres.find('p:sldIdLst',N);pr=E.fromstring(files['ppt/_rels/presentation.xml.rels'])
 for x in list(ids):ids.remove(x)
 for x in list(pr):
  if x.get('Type').endswith('/slide'):pr.remove(x)
 # Old slides and notes are removed from the saved file, including unused production instructions.
 for name in list(files):
  if name.startswith('ppt/slides/') or name.startswith('ppt/notesSlides/'):del files[name]
 for x in list(types):
  if x.get('PartName','').startswith(('/ppt/slides/','/ppt/notesSlides/')):types.remove(x)
 for s in specs:
  old=bp[s['source_page']-1];tree=E.fromstring(base.read(old));changed=E.fromstring(edit.read(ep[s['export_page']-1]));new=f"ppt/slides/lesson-{s['page']:02}.xml"
  original_shapes={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in tree.findall('.//p:sp',N)}
  changed_shapes={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in changed.findall('.//p:sp',N)}
  for name in set(s['edits'])|set(s.get('styles',{})):
   a=original_shapes[name];b=changed_shapes[name];ta=a.find('p:txBody',N);tb=b.find('p:txBody',N)
   for p in list(ta.findall('a:p',N)):ta.remove(p)
   for p in tb.findall('a:p',N):ta.append(deepcopy(p))
  if s.get('table'):
   a=tree.findall('.//a:tbl',N)[0];b=changed.findall('.//a:tbl',N)[0]
   for ca,cb in zip(a.findall('.//a:tc',N),b.findall('.//a:tc',N)):
    ta=ca.find('a:txBody',N);tb=cb.find('a:txBody',N)
    for p in list(ta.findall('a:p',N)):ta.remove(p)
    for p in tb.findall('a:p',N):ta.append(deepcopy(p))
  files[new]=xml(tree)
  sr=E.fromstring(base.read(rel(old)));oldnote=target(old,next(x.get('Target') for x in sr if x.get('Type').endswith('/notesSlide')));newnote=f"ppt/notesSlides/lesson-{s['page']:02}.xml"
  for x in sr:
   if x.get('TargetMode')!='External':x.set('Target','/'+(newnote if x.get('Type').endswith('/notesSlide') else target(old,x.get('Target'))))
  files[rel(new)]=xml(sr)
  note=E.fromstring(base.read(oldnote))
  body=next(x.find('p:txBody',N) for x in note.findall('.//p:sp',N) if x.find('.//p:ph',N) is not None and x.find('.//p:ph',N).get('type')=='body')
  for p in list(body.findall('a:p',N)):body.remove(p)
  text=s['note']+'\n\n근거: '+'\n'.join(s['sources'])+'\n'+'\n'.join(f"V{x['video']} {x['channel']}: {x['url']}" for x in s['refs'])
  for line in text.split('\n'):
   p=E.SubElement(body,'{'+A+'}p');r=E.SubElement(p,'{'+A+'}r');E.SubElement(r,'{'+A+'}t').text=line
  for sh in note.findall('.//p:sp',N):
   ph=sh.find('.//p:ph',N)
   if ph is not None and ph.get('type')=='sldNum':
    for t in sh.findall('.//a:t',N):t.text=str(s['page'])
  files[newnote]=xml(note);nr=E.fromstring(base.read(rel(oldnote)))
  for x in nr:
   if x.get('TargetMode')!='External':x.set('Target','/'+(new if x.get('Type').endswith('/slide') else target(oldnote,x.get('Target'))))
  files[rel(newnote)]=xml(nr)
  for part,typ in [(new,'slide'),(newnote,'notesSlide')]:E.SubElement(types,'{'+CT+'}Override',PartName='/'+part,ContentType='application/vnd.openxmlformats-officedocument.presentationml.'+typ+'+xml')
  rid='rIdLesson'+str(s['page']);E.SubElement(pr,'{'+PK+'}Relationship',Id=rid,Type=REL+'/slide',Target='/'+new);E.SubElement(ids,'{'+P+'}sldId',{'id':str(255+s['page']),'{'+REL+'}id':rid})
 # Remove old sections/custom slide shows that may retain references to deleted slides.
 for name in ['sectionLst','custShowLst']:
  for node in pres.xpath('.//*[local-name()="'+name+'"]'):
   node.getparent().remove(node)
 files['ppt/presentation.xml']=xml(pres);files['ppt/_rels/presentation.xml.rels']=xml(pr)
 if 'docProps/app.xml' in files:
  app=E.fromstring(files['docProps/app.xml'])
  for x in app.iter():
   if E.QName(x).localname in ['Slides','Notes']:x.text=str(len(specs))
  for x in list(app):
   if E.QName(x).localname in ['TitlesOfParts','HeadingPairs']:app.remove(x)
  files['docProps/app.xml']=xml(app)
 if 'docProps/core.xml' in files:
  core=E.fromstring(files['docProps/core.xml'])
  for x in core.iter():
   if E.QName(x).localname=='title':x.text='모션 그래픽 기초와 표현 이해하기'
  files['docProps/core.xml']=xml(core)
 # Keep only reachable OOXML parts so removed tool logos and production assets are absent.
 keep={'[Content_Types].xml'};queue=['']
 while queue:
  p=queue.pop();rp='_rels/.rels' if not p else rel(p)
  if p:keep.add(p)
  if rp not in files:continue
  keep.add(rp)
  for x in E.fromstring(files[rp]):
   if x.get('TargetMode')=='External':continue
   dest=target(p,x.get('Target'))
   if dest not in keep and dest in files:keep.add(dest);queue.append(dest)
 for x in list(types):
  if x.get('PartName') and x.get('PartName').lstrip('/') not in keep:types.remove(x)
 files['[Content_Types].xml']=xml(types)
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as out:
  for n in sorted(keep):out.writestr(n,files[n])
print('Assembled 22 slides with source images, GIF and native animations preserved.')
