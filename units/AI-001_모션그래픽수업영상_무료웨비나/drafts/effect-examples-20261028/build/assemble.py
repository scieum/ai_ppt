from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json,posixpath
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
SRC=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_10장_v2.pptx'
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PK='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types';N={'p':P,'a':A}
def target(p,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(x):return E.tostring(x,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 rs={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 return [target('ppt/presentation.xml',rs[x.get('{'+REL+'}id')]) for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
with ZipFile(SRC) as src,ZipFile(B/'roundtrip.pptx') as authored:
 files={x:src.read(x) for x in src.namelist()};sp=ordered(src);ep=ordered(authored)
 for spec in json.loads((B/'edits.json').read_text(encoding='utf8')):
  page=spec['page'];part=sp[page-1];base=E.fromstring(files[part]);edit=E.fromstring(authored.read(ep[page-1]));tree=base.find('p:cSld/p:spTree',N)
  current={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in base.findall('.//p:sp',N)}
  changed={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in edit.findall('.//p:sp',N)}
  for name in spec['remove']:
   x=current[name];x.getparent().remove(x)
  for name in spec['edits']:
   a=current[name].find('p:txBody',N);b=changed[name].find('p:txBody',N)
   for q in list(a.findall('a:p',N)):a.remove(q)
   for q in b.findall('a:p',N):a.append(deepcopy(q))
  nextid=max(int(x.get('id')) for x in base.findall('.//p:cNvPr',N))+1
  for name,sh in changed.items():
   if not name.startswith('ex-'):continue
   sh=deepcopy(sh);sh.find('p:nvSpPr/p:cNvPr',N).set('id',str(nextid));nextid+=1;tree.append(sh)
  sr=E.fromstring(files[rel(part)])
  for index,im in enumerate(spec['images']):
   pic=next(x for x in edit.findall('.//p:pic',N) if x.find('p:spPr/a:xfrm/a:off',N) is not None and abs(int(x.find('p:spPr/a:xfrm/a:off',N).get('x'))/9525-(200+index*320))<1 and abs(int(x.find('p:spPr/a:xfrm/a:off',N).get('y'))/9525-451)<1)
   pic=deepcopy(pic);prop=pic.find('p:nvPicPr/p:cNvPr',N);prop.set('id',str(nextid));nextid+=1;prop.set('name',im['alt']);prop.set('descr',im['alt'])
   rid='rIdMotion'+im['kind'];pic.find('p:blipFill/a:blip',N).set('{'+REL+'}embed',rid)
   media='ppt/media/motion-example-'+im['kind']+'.gif';files[media]=(B/'assets'/(im['kind']+'.gif')).read_bytes()
   E.SubElement(sr,'{'+PK+'}Relationship',Id=rid,Type=REL+'/image',Target='/'+media);tree.append(pic)
  if page in [7,8]:
   timing=base.find('p:timing',N)
   if timing is not None:base.remove(timing)
  note=target(part,next(x.get('Target') for x in sr if x.get('Type').endswith('/notesSlide')))
  nt=E.fromstring(files[note]);body=next(x.find('p:txBody',N) for x in nt.findall('.//p:sp',N) if x.find('.//p:ph',N)is not None and x.find('.//p:ph',N).get('type')=='body')
  para=E.Element('{'+A+'}p');run=E.SubElement(para,'{'+A+'}r');E.SubElement(run,'{'+A+'}t').text=spec['notes'];body.insert(1,para)
  files[part]=xml(base);files[rel(part)]=xml(sr);files[note]=xml(nt)
 ct=E.fromstring(files['[Content_Types].xml'])
 if not any(x.get('Extension')=='gif' for x in ct):E.SubElement(ct,'{'+CT+'}Default',Extension='gif',ContentType='image/gif')
 files['[Content_Types].xml']=xml(ct)
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as out:
  for name,data in files.items():out.writestr(name,data)
print('Preserved original deck; inserted six animated GIFs and editable snapshots.')
