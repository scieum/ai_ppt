from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json,posixpath
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
SRC=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_13장_표현확장_v6.pptx'
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PK='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types';N={'p':P,'a':A}
def target(p,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(x):return E.tostring(x,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 return [target('ppt/presentation.xml',rs[x.get('{'+REL+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
with ZipFile(SRC)as src,ZipFile(B/'roundtrip.pptx')as authored:
 files={p:src.read(p)for p in src.namelist()};sp=ordered(src);ep=ordered(authored);ct=E.fromstring(files['[Content_Types].xml']);pres=E.fromstring(files['ppt/presentation.xml']);ids=pres.find('p:sldIdLst',N);pr=E.fromstring(files['ppt/_rels/presentation.xml.rels'])
 spec=json.loads((B/'edits.json').read_text(encoding='utf8'))[0];old=sp[6];part='ppt/slides/preview-first.xml';note='ppt/notesSlides/preview-first.xml'
 base=E.fromstring(src.read(old));edit=E.fromstring(authored.read(ep[spec['export_page']-1]));tree=base.find('p:cSld/p:spTree',N)
 cur={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in base.findall('.//p:sp',N)};changed={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in edit.findall('.//p:sp',N)}
 for name in spec['remove']:
  sh=cur[name];sh.getparent().remove(sh)
 for pic in list(tree.findall('p:pic',N)):
  if pic.find('p:nvPicPr/p:cNvPr',N).get('name','').startswith('motion-example-'):tree.remove(pic)
 for name in spec['edits']:
  a=cur[name].find('p:txBody',N);b=changed[name].find('p:txBody',N)
  for q in list(a.findall('a:p',N)):a.remove(q)
  for q in b.findall('a:p',N):a.append(deepcopy(q))
 nextid=max(int(x.get('id'))for x in base.findall('.//p:cNvPr',N))+1
 for name,sh in changed.items():
  if not name.startswith('preview-'):continue
  sh=deepcopy(sh);sh.find('p:nvSpPr/p:cNvPr',N).set('id',str(nextid));nextid+=1;tree.append(sh)
 sr=E.fromstring(src.read(rel(old)));oldnote=target(old,next(x.get('Target')for x in sr if x.get('Type').endswith('/notesSlide')))
 for x in sr:
  if x.get('TargetMode')!='External':x.set('Target','/'+(note if x.get('Type').endswith('/notesSlide')else target(old,x.get('Target'))))
 nt=E.fromstring(src.read(oldnote));body=next(x.find('p:txBody',N)for x in nt.findall('.//p:sp',N)if x.find('.//p:ph',N)is not None and x.find('.//p:ph',N).get('type')=='body')
 for q in list(body.findall('a:p',N)):body.remove(q)
 for line in spec['notes'].split('\n'):
  para=E.SubElement(body,'{'+A+'}p');run=E.SubElement(para,'{'+A+'}r');E.SubElement(run,'{'+A+'}t').text=line
 for sh in nt.findall('.//p:sp',N):
  ph=sh.find('.//p:ph',N)
  if ph is not None and ph.get('type')=='sldNum':
   for t in sh.findall('.//a:t',N):t.text='14'
 nr=E.fromstring(src.read(rel(oldnote)))
 for x in nr:
  if x.get('TargetMode')!='External':x.set('Target','/'+(part if x.get('Type').endswith('/slide')else target(oldnote,x.get('Target'))))
 files[part]=xml(base);files[rel(part)]=xml(sr);files[note]=xml(nt);files[rel(note)]=xml(nr)
 for pp,typ in [(part,'slide'),(note,'notesSlide')]:E.SubElement(ct,'{'+CT+'}Override',PartName='/'+pp,ContentType='application/vnd.openxmlformats-officedocument.presentationml.'+typ+'+xml')
 rid='rIdPreviewFirst';E.SubElement(pr,'{'+PK+'}Relationship',Id=rid,Type=REL+'/slide',Target='/'+part);E.SubElement(ids,'{'+P+'}sldId',{'id':str(max(int(x.get('id'))for x in ids)+1),'{'+REL+'}id':rid})
 files['ppt/presentation.xml']=xml(pres);files['ppt/_rels/presentation.xml.rels']=xml(pr);app=E.fromstring(files['docProps/app.xml'])
 for x in app.iter():
  if E.QName(x).localname in ['Slides','Notes']:x.text='14'
 files['docProps/app.xml']=xml(app);files['[Content_Types].xml']=xml(ct)
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED)as out:
  for name,data in files.items():out.writestr(name,data)
print('Preserved all 13 existing slides and appended the explicitly requested preview-first tip.')
