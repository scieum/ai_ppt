from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import json,hashlib,posixpath
B=Path(__file__).resolve().parent;R=B.parents[1]
SOURCE=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_레퍼런스표현강화_40장_v20.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'};PK='http://schemas.openxmlformats.org/package/2006/relationships'
def target(p,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(e):return E.tostring(e,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};return[target('ppt/presentation.xml',rs[x.get('{'+N['r']+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
spec=json.loads((B/'additions.json').read_text(encoding='utf8'))
with ZipFile(SOURCE)as z,ZipFile(B/'additions.pptx')as a:
 files={n:z.read(n)for n in z.namelist()};old=ordered(z);new=ordered(a)
 for i,d in enumerate(spec):
  src=new[i];dst=old[d['page']-1];root=E.fromstring(a.read(src));rs=E.fromstring(a.read(rel(src)));oldrs=E.fromstring(files[rel(dst)])
  oldlayout=next(target(dst,r.get('Target'))for r in oldrs if r.get('Type').endswith('/slideLayout'));oldnotes=next(target(dst,r.get('Target'))for r in oldrs if r.get('Type').endswith('/notesSlide'))
  for r in list(rs):
   kind=r.get('Type').split('/')[-1]
   if kind=='image':
    content=a.read(target(src,r.get('Target')));ext=Path(r.get('Target')).suffix;media='ppt/media/image-explain-'+hashlib.sha256(content).hexdigest()[:16]+ext;files[media]=content;r.set('Target','/'+media)
   elif kind=='slideLayout':r.set('Target','/'+oldlayout)
   elif kind=='notesSlide':rs.remove(r)
   else:raise ValueError(kind)
  E.SubElement(rs,'{'+PK+'}Relationship',Id='rIdExplainNotes',Type=N['r']+'/notesSlide',Target='/'+oldnotes)
  files[dst]=xml(root);files[rel(dst)]=xml(rs)
  note=E.fromstring(files[oldnotes]);body=next(sp.find('p:txBody',N)for sp in note.findall('.//p:sp',N)if sp.find('p:nvSpPr/p:nvPr/p:ph',N)is not None and sp.find('p:nvSpPr/p:nvPr/p:ph',N).get('type')=='body')
  for pp in body.findall('a:p',N):body.remove(pp)
  pp=E.SubElement(body,'{'+N['a']+'}p');rr=E.SubElement(pp,'{'+N['a']+'}r');tt=E.SubElement(rr,'{'+N['a']+'}t');tt.text=d['notes']+'\n이미지: 노션톡 교육용 자체 생성 자료. 24쪽은 사용자 소유 캐릭터를 참조했다.';files[oldnotes]=xml(note)
  d['package_part']=dst
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED)as out:
  for name,data in files.items():out.writestr(name,data)
 assert all(files[name]==z.read(name)for name in z.namelist()if name.startswith('ppt/media/'))
 assert all(files[part]==z.read(part)for i,part in enumerate(old,1)if i not in [d['page']for d in spec])
(B/'slide-map.json').write_text(json.dumps({'source':str(SOURCE),'slides':spec,'preserved_slides':37},ensure_ascii=False,indent=2),encoding='utf8')
print('3 replaced; 37 original slide XML and all original media preserved')
