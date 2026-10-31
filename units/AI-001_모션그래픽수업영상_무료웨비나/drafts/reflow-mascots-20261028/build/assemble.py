from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json,posixpath,hashlib
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
SRC=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_19장_영상핵심5장확장_v8.pptx'
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PK='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types';N={'p':P,'a':A}
def target(p,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(x):return E.tostring(x,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 return [target('ppt/presentation.xml',rs[x.get('{'+REL+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
with ZipFile(SRC)as src,ZipFile(B/'roundtrip.pptx')as authored:
 files={p:src.read(p)for p in src.namelist()};sp=ordered(src);ep=ordered(authored);ct=E.fromstring(files['[Content_Types].xml']);pres=E.fromstring(files['ppt/presentation.xml']);ids=pres.find('p:sldIdLst',N);pr=E.fromstring(files['ppt/_rels/presentation.xml.rels'])
 for x in list(ids):ids.remove(x)
 for x in list(pr):
  if x.get('Type').endswith('/slide'):pr.remove(x)
 for name in list(files):
  if name.startswith(('ppt/slides/','ppt/notesSlides/')):del files[name]
 for x in list(ct):
  if x.get('PartName','').startswith(('/ppt/slides/','/ppt/notesSlides/')):ct.remove(x)
 specs=json.loads((B/'edits.json').read_text(encoding='utf8'));picture_templates={}
 # Repair repeated-image exports by reusing the authored picture for the same file.
 for item in specs:
  ed=E.fromstring(authored.read(ep[item['export_page']-1]))
  for im in item['images']:
   matches=[x for x in ed.findall('.//p:pic',N)if x.find('p:spPr/a:xfrm/a:off',N)is not None and abs(int(x.find('p:spPr/a:xfrm/a:off',N).get('x'))/9525-im['x'])<1 and abs(int(x.find('p:spPr/a:xfrm/a:off',N).get('y'))/9525-im['y'])<1]
   if matches:picture_templates[im['file']]=matches[-1]
 for spec in specs:
  page=spec['page'];old=sp[spec['source_page']-1];part=f'ppt/slides/reflow-{page:02}.xml';note=f'ppt/notesSlides/reflow-{page:02}.xml'
  base=E.fromstring(src.read(old));edit=E.fromstring(authored.read(ep[spec['export_page']-1]));tree=base.find('p:cSld/p:spTree',N)
  if page==2:
   # The inherited logo is baked into a full-canvas source background.
   # Keep its original pixels as a native crop while replacing only the body background.
   pics=tree.findall('p:pic',N);brand=pics[0]
   for other in pics[1:]:tree.remove(other)
   fill=brand.find('p:blipFill',N);crop=fill.find('a:srcRect',N)
   if crop is None:crop=E.Element('{'+A+'}srcRect');fill.insert(1,crop)
   for k,v in {'l':'75000','t':'5556','r':'4167','b':'83333'}.items():crop.set(k,v)
   x=brand.find('p:spPr/a:xfrm',N);of=x.find('a:off',N);ex=x.find('a:ext',N)
   of.set('x',str(960*9525));of.set('y',str(40*9525));ex.set('cx',str(round(400/1.5*9525)));ex.set('cy',str(80*9525))
  cur={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in base.findall('.//p:sp',N)};changed={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in edit.findall('.//p:sp',N)}
  for name in spec['remove']:
   sh=cur[name];sh.getparent().remove(sh)
  for name in set(spec['edits'])|set(spec.get('styles',{})):
   a=cur[name].find('p:txBody',N);b=changed[name].find('p:txBody',N)
   for q in list(a.findall('a:p',N)):a.remove(q)
   for q in b.findall('a:p',N):a.append(deepcopy(q))
   if name in spec['edits']:
    desired=spec['edits'][name];actual='\n'.join(''.join(q.xpath('.//a:t/text()',namespaces=N))for q in a.findall('a:p',N))
    if actual!=desired:
     # Imported slides can share creation IDs; repair stale exported text literally.
     template=deepcopy(a.find('a:p',N));rpr=template.find('.//a:rPr',N)
     for q in list(a.findall('a:p',N)):a.remove(q)
     for line in desired.split('\n'):
      pp=deepcopy(template)
      for child in list(pp):
       if E.QName(child).localname!='pPr':pp.remove(child)
      rr=E.SubElement(pp,'{'+A+'}r')
      if rpr is not None:rr.append(deepcopy(rpr))
      E.SubElement(rr,'{'+A+'}t').text=line;a.append(pp)
  for name,pos in spec.get('positions',{}).items():
   # Preserve untouched source dimensions and replace only explicitly requested values.
   x=cur[name].find('p:spPr/a:xfrm',N);off=x.find('a:off',N);ext=x.find('a:ext',N)
   for key,attr,node in [('left','x',off),('top','y',off),('width','cx',ext),('height','cy',ext)]:
    if key in pos:node.set(attr,str(round(pos[key]*9525)))
  nextid=max(int(x.get('id'))for x in base.findall('.//p:cNvPr',N))+1
  for name,sh in changed.items():
   if not name.startswith('reflow-'):continue
   sh=deepcopy(sh);sh.find('p:nvSpPr/p:cNvPr',N).set('id',str(nextid));nextid+=1;tree.append(sh)
  sr=E.fromstring(src.read(rel(old)));oldnote=target(old,next(x.get('Target')for x in sr if x.get('Type').endswith('/notesSlide')))
  for x in sr:
   if x.get('TargetMode')!='External':x.set('Target','/'+(note if x.get('Type').endswith('/notesSlide')else target(old,x.get('Target'))))
  for j,im in enumerate(spec['images']):
   matches=[x for x in edit.findall('.//p:pic',N)if x.find('p:spPr/a:xfrm/a:off',N)is not None and abs(int(x.find('p:spPr/a:xfrm/a:off',N).get('x'))/9525-im['x'])<1 and abs(int(x.find('p:spPr/a:xfrm/a:off',N).get('y'))/9525-im['y'])<1]
   pic=deepcopy(matches[-1]if matches else picture_templates[im['file']]);prop=pic.find('p:nvPicPr/p:cNvPr',N);prop.set('id',str(nextid));nextid+=1;prop.set('name',im['name']);prop.set('descr',im['name'])
   xf=pic.find('p:spPr/a:xfrm',N);of=xf.find('a:off',N);ex=xf.find('a:ext',N)
   for key,attr,node in [('x','x',of),('y','y',of),('w','cx',ex),('h','cy',ex)]:node.set(attr,str(round(im[key]*9525)))
   rid='rIdReflowImage'+str(j);pic.find('p:blipFill/a:blip',N).set('{'+REL+'}embed',rid);file=Path(im['file']);data=file.read_bytes();media='ppt/media/reflow-'+hashlib.sha256(data).hexdigest()[:16]+'.png';files[media]=data;E.SubElement(sr,'{'+PK+'}Relationship',Id=rid,Type=REL+'/image',Target='/'+media)
   if im['layer']=='back':tree.insert(2,pic)
   else:tree.append(pic)
  nt=E.fromstring(src.read(oldnote))
  if spec.get('notes'):
   body=next(x.find('p:txBody',N)for x in nt.findall('.//p:sp',N)if x.find('.//p:ph',N)is not None and x.find('.//p:ph',N).get('type')=='body')
   # Existing source citations remain available after the new consolidation explanation.
   oldtext='\n'.join(body.xpath('.//a:t/text()',namespaces=N))
   for q in list(body.findall('a:p',N)):body.remove(q)
   for line in (spec['notes']+'\n\n'+oldtext).split('\n'):
    para=E.SubElement(body,'{'+A+'}p');run=E.SubElement(para,'{'+A+'}r');E.SubElement(run,'{'+A+'}t').text=line
  for sh in nt.findall('.//p:sp',N):
   ph=sh.find('.//p:ph',N)
   if ph is not None and ph.get('type')=='sldNum':
    for t in sh.findall('.//a:t',N):t.text=str(page)
  nr=E.fromstring(src.read(rel(oldnote)))
  for x in nr:
   if x.get('TargetMode')!='External':x.set('Target','/'+(part if x.get('Type').endswith('/slide')else target(oldnote,x.get('Target'))))
  files[part]=xml(base);files[rel(part)]=xml(sr);files[note]=xml(nt);files[rel(note)]=xml(nr)
  for pp,typ in [(part,'slide'),(note,'notesSlide')]:E.SubElement(ct,'{'+CT+'}Override',PartName='/'+pp,ContentType='application/vnd.openxmlformats-officedocument.presentationml.'+typ+'+xml')
  rid='rIdReflow'+str(page);E.SubElement(pr,'{'+PK+'}Relationship',Id=rid,Type=REL+'/slide',Target='/'+part);E.SubElement(ids,'{'+P+'}sldId',{'id':str(255+page),'{'+REL+'}id':rid})
 files['ppt/presentation.xml']=xml(pres);files['ppt/_rels/presentation.xml.rels']=xml(pr);app=E.fromstring(files['docProps/app.xml'])
 for x in app.iter():
  if E.QName(x).localname in ['Slides','Notes']:x.text='16'
 files['docProps/app.xml']=xml(app);files['[Content_Types].xml']=xml(ct)
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED)as out:
  for name,data in files.items():out.writestr(name,data)
print('Assembled 16 reordered slides with source motion preserved and embedded transparent character assets.')
