from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json,hashlib,posixpath
B=Path(__file__).resolve().parent;R=B.parents[1];U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
SOURCE=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_Part3_Part4확장_40장_v19.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'};PK='http://schemas.openxmlformats.org/package/2006/relationships'
def target(p,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(e):return E.tostring(e,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};return[target('ppt/presentation.xml',rs[x.get('{'+N['r']+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
spec=json.loads((B/'additions.json').read_text(encoding='utf8'));poses={x['id']:x for x in json.loads((U/'assets/character-sheets-20261028/poses.json').read_text(encoding='utf8'))}
with ZipFile(SOURCE)as z,ZipFile(B/'additions.pptx')as a:
 files={n:z.read(n)for n in z.namelist()};old=ordered(z);new=ordered(a)
 for i,d in enumerate(spec):
  src=new[i];dst=old[d['page']-1];root=E.fromstring(a.read(src));rs=E.fromstring(a.read(rel(src)));oldrs=E.fromstring(files[rel(dst)])
  oldlayout=next(target(dst,r.get('Target'))for r in oldrs if r.get('Type').endswith('/slideLayout'))
  oldnotes=next(target(dst,r.get('Target'))for r in oldrs if r.get('Type').endswith('/notesSlide'))
  for r in list(rs):
   kind=r.get('Type').split('/')[-1]
   if kind=='image':
    content=a.read(target(src,r.get('Target')));ext=Path(r.get('Target')).suffix;media='ppt/media/reference-style-'+hashlib.sha256(content).hexdigest()[:16]+ext;files[media]=content;r.set('Target','/'+media)
   elif kind=='slideLayout':r.set('Target','/'+oldlayout)
   elif kind=='notesSlide':rs.remove(r)
   else:raise ValueError(kind)
  E.SubElement(rs,'{'+PK+'}Relationship',Id='rIdReferenceNotes',Type=N['r']+'/notesSlide',Target='/'+oldnotes)
  for picture in root.findall('.//p:pic',N):
   nv=picture.find('p:nvPicPr/p:cNvPr',N);desc=nv.get('descr','')
   embed=picture.find('p:blipFill/a:blip',N).get('{'+N['r']+'}embed')
   media_target=next(target(dst,r.get('Target'))for r in rs if r.get('Id')==embed)
   if d['page'] in [24,37]:
    pose_id='woman-explain'if d['page']==24 else'man-review'
    if files[media_target]==Path(poses[pose_id]['file']).read_bytes():desc='pose:'+pose_id;nv.set('descr',desc);nv.set('name',desc)
   if desc.startswith('pose:'):
    pose=poses[desc.split(':',1)[1]];fill=picture.find('p:blipFill',N);crop=fill.find('a:srcRect',N)
    if crop is None:crop=E.Element('{'+N['a']+'}srcRect');fill.insert(1,crop)
    for k,v in [('l','left'),('t','top'),('r','right'),('b','bottom')]:crop.set(k,str(round(pose['crop'][v]*100000)))
    stretch=fill.find('a:stretch',N)
    if stretch is not None and stretch.find('a:fillRect',N)is None:E.SubElement(stretch,'{'+N['a']+'}fillRect')
    # Preserve desired pose dimensions rather than full-sheet aspect fitting.
    xfrm=picture.find('p:spPr/a:xfrm',N);h=263 if d['page']==24 else 245;x=554 if d['page']==24 else 96;y=349 if d['page']==24 else 410
    for el,vals in [('off',{'x':round(x*9525),'y':round(y*9525)}),('ext',{'cx':round(h*pose['aspect_ratio']*9525),'cy':round(h*9525)})]:
     for key,val in vals.items():xfrm.find('a:'+el,N).set(key,str(val))
  files[dst]=xml(root);files[rel(dst)]=xml(rs)
  # Existing educational notes preserved, source references appended in the note body.
  note=E.fromstring(files[oldnotes]);body=next((sp.find('p:txBody',N)for sp in note.findall('.//p:sp',N)if sp.find('p:nvSpPr/p:nvPr/p:ph',N)is not None and sp.find('p:nvSpPr/p:nvPr/p:ph',N).get('type')=='body'),None)
  if body is not None:
   pp=E.SubElement(body,'{'+N['a']+'}p');rr=E.SubElement(pp,'{'+N['a']+'}r');tt=E.SubElement(rr,'{'+N['a']+'}t');tt.text='시각 구성 참고: '+', '.join(d['refs'])+'. R01: 사용자 제공 「기획부터 디자인까지 쭉! AI 디자인 하네스 만들기」 PDF. R03: 사용자 제공 「MCP 적용부터 제작까지 100% 활용하기」 PDF.';files[oldnotes]=xml(note)
  d['package_part']=dst
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED)as out:
  for name,data in files.items():out.writestr(name,data)
 assert all(files[name]==z.read(name)for name in z.namelist()if name.startswith('ppt/media/'))
 assert all(files[part]==z.read(part)for i,part in enumerate(old,1)if i not in [d['page']for d in spec])
(B/'slide-map.json').write_text(json.dumps({'source':str(SOURCE),'slides':spec,'preserved_slides':26},ensure_ascii=False,indent=2),encoding='utf8')
print('14 replaced; 26 slide XML and all original media preserved')
