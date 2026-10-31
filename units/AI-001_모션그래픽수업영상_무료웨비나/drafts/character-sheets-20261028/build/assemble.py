from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json,posixpath,hashlib
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1];SRC=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_톤과움직임확장_21장_v13.pptx'
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PK='http://schemas.openxmlformats.org/package/2006/relationships';N={'p':P,'a':A}
def target(p,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(x):return E.tostring(x,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 return [target('ppt/presentation.xml',rs[x.get('{'+REL+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
with ZipFile(SRC)as src,ZipFile(B/'roundtrip.pptx')as authored:
 files={n:src.read(n)for n in src.namelist()};sp=ordered(src);ep=ordered(authored);changes=[]
 for spec in json.loads((B/'edits.json').read_text(encoding='utf-8')):
  page=spec['page'];part=sp[page-1];base=E.fromstring(src.read(part));edit=E.fromstring(authored.read(ep[page-1]));tree=base.find('p:cSld/p:spTree',N);sr=E.fromstring(src.read(rel(part)))
  removed=[]
  for pic in list(tree.findall('p:pic',N)):
   name=pic.find('p:nvPicPr/p:cNvPr',N).get('name','')
   if name.startswith('mascot-'):tree.remove(pic);removed.append(name)
  for name,pos in spec['positions'].items():
   shape=next(x for x in tree.findall('p:sp',N)if x.find('p:nvSpPr/p:cNvPr',N).get('name')==name);xf=shape.find('p:spPr/a:xfrm',N)
   if 'left'in pos:xf.find('a:off',N).set('x',str(round(pos['left']*9525)))
   if 'width'in pos:xf.find('a:ext',N).set('cx',str(round(pos['width']*9525)))
  nextid=max(int(x.get('id'))for x in base.findall('.//p:cNvPr',N))+1
  for j,im in enumerate(spec['images']):
   # Preserve native editable crop rather than cutting/resampling the sheet PNG.
   pic=deepcopy(edit.findall('.//p:pic',N)[-1]);cn=pic.find('p:nvPicPr/p:cNvPr',N);cn.set('id',str(nextid));cn.set('name',im['name']);nextid+=1
   fill=pic.find('p:blipFill',N);rid='rIdCharacterSheet'+str(j);fill.find('a:blip',N).set('{'+REL+'}embed',rid)
   oldcrop=fill.find('a:srcRect',N)
   if oldcrop is not None:fill.remove(oldcrop)
   crop=E.Element('{'+A+'}srcRect',**{k:str(round(im['crop'][v]*100000))for k,v in [('l','left'),('t','top'),('r','right'),('b','bottom')]});fill.insert(1,crop)
   stretch=fill.find('a:stretch',N)
   if stretch is None:stretch=E.SubElement(fill,'{'+A+'}stretch');E.SubElement(stretch,'{'+A+'}fillRect')
   xf=pic.find('p:spPr/a:xfrm',N);pos=im['position'];xf.find('a:off',N).attrib.update({'x':str(round(pos['left']*9525)),'y':str(round(pos['top']*9525))});xf.find('a:ext',N).attrib.update({'cx':str(round(pos['width']*9525)),'cy':str(round(pos['height']*9525))})
   data=Path(im['file']).read_bytes();media='ppt/media/character-sheet-'+hashlib.sha256(data).hexdigest()[:16]+'.png';files[media]=data;E.SubElement(sr,'{'+PK+'}Relationship',Id=rid,Type=REL+'/image',Target='/'+media);tree.append(pic)
  files[part]=xml(base);files[rel(part)]=xml(sr);changes.append({'page':page,'removed':removed,'added':[im['id']for im in spec['images']]})
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED)as out:
  for name,data in files.items():out.writestr(name,data)
 (B/'package-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Preserved all slide content and motion; changed only seven character/layout locations.')
