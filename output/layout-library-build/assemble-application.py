from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json,posixpath
B=Path(__file__).resolve().parent;R=B.parents[1];SRC=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_캐릭터시트적용_21장_v14.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def target(p,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def ordered(z):
 rel={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};return[target('ppt/presentation.xml',rel[x.get('{'+N['r']+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
def xml(x):return E.tostring(x,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(SRC)as source,ZipFile(B/'application-roundtrip.pptx')as authored:
 files={n:source.read(n)for n in source.namelist()};sp=ordered(source);ep=ordered(authored)
 for spec in json.loads((B/'application-edits.json').read_text(encoding='utf-8')):
  page=spec['page'];part=sp[page-1];base=E.fromstring(files[part]);edit=E.fromstring(authored.read(ep[page-1]));tree=base.find('p:cSld/p:spTree',N)
  shapes={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in tree.findall('p:sp',N)}
  targets={x.get('spid')for x in base.findall('.//p:timing//p:spTgt',N)}
  for name in spec['remove']:
   sh=shapes[name];assert sh.find('p:nvSpPr/p:cNvPr',N).get('id')not in targets,(page,name,'animation target');tree.remove(sh)
  for name,pos in spec['positions'].items():
   sh=shapes[name];xf=sh.find('p:spPr/a:xfrm',N)
   for prop,el,attr in [('left','a:off','x'),('top','a:off','y'),('width','a:ext','cx'),('height','a:ext','cy')]:
    if prop in pos:xf.find(el,N).set(attr,str(round(pos[prop]*9525)))
  for name,style in spec['styles'].items():
   for r in shapes[name].findall('.//a:rPr',N):r.set('sz',str(round(style['fontSize']*75)))
  for name,pos in spec['picture_positions'].items():
   pic=next(x for x in tree.findall('p:pic',N)if x.find('p:nvPicPr/p:cNvPr',N).get('name')==name);xf=pic.find('p:spPr/a:xfrm',N)
   for prop,el,attr in [('left','a:off','x'),('top','a:off','y'),('width','a:ext','cx'),('height','a:ext','cy')]:xf.find(el,N).set(attr,str(round(pos[prop]*9525)))
  nextid=max(int(x.get('id'))for x in base.findall('.//p:cNvPr',N))+1
  for sh in edit.findall('.//p:sp',N):
   if not sh.find('p:nvSpPr/p:cNvPr',N).get('name','').startswith('asset-'):continue
   sh=deepcopy(sh);sh.find('p:nvSpPr/p:cNvPr',N).set('id',str(nextid));nextid+=1;tree.append(sh)
  # The row backgrounds must sit behind the existing animated GIF pictures.
  for pic in list(tree.findall('p:pic',N)):
   if pic.find('p:nvPicPr/p:cNvPr',N).get('name')in spec['picture_positions']:
    tree.remove(pic);tree.append(pic)
  files[part]=xml(base)
 with ZipFile(B/'application-candidate.pptx','w',ZIP_DEFLATED)as out:
  for name,data in files.items():out.writestr(name,data)
print('Updated three slides; preserved all other slide parts, media, crops, tables and native timing.')
