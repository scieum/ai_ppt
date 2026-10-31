from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import posixpath,json,re,hashlib
B=Path(__file__).resolve().parent;R=B.parents[1]
SOURCE=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_목차수정_21장_v17.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'};PK='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types'
def target(p,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(e):return E.tostring(e,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};return[target('ppt/presentation.xml',rs[x.get('{'+N['r']+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
parts=json.loads((B/'parts.json').read_text(encoding='utf8'))
with ZipFile(SOURCE)as z,ZipFile(B/'dividers.pptx')as a:
 files={n:z.read(n)for n in z.namelist()};old=ordered(z);auth=ordered(a);prs=E.fromstring(files['ppt/presentation.xml']);lst=prs.find('p:sldIdLst',N);oldids=[deepcopy(x)for x in lst];rels=E.fromstring(files['ppt/_rels/presentation.xml.rels']);types=E.fromstring(files['[Content_Types].xml'])
 base_rels=E.fromstring(files[rel(old[0])]);layout=next(target(old[0],r.get('Target'))for r in base_rels if r.get('Type').endswith('/slideLayout'))
 note0=next(target(old[0],r.get('Target'))for r in base_rels if r.get('Type').endswith('/notesSlide'));notesmaster=next(target(note0,r.get('Target'))for r in E.fromstring(files[rel(note0)])if r.get('Type').endswith('/notesMaster'))
 id_max=max(int(x.get('id'))for x in oldids)
 additions={};new_order=[]
 for i,d in enumerate(parts):
  src=auth[i];dst=f'ppt/slides/partDivider{d["part"]}.xml';assert dst not in files;root=E.fromstring(a.read(src));sr=E.fromstring(a.read(rel(src)));newrel=E.Element('{'+PK+'}Relationships',nsmap={None:PK})
  for r in sr:
   kind=r.get('Type').split('/')[-1];rd=deepcopy(r)
   if kind=='slideLayout':rd.set('Target','/'+layout)
   elif kind=='image':
    media='ppt/media/part-divider-notiontalk-original.png';files[media]=(R/'assets/branding/notiontalk-white.png').read_bytes();rd.set('Target','/'+media)
   elif kind=='notesSlide':
    source_note=target(src,r.get('Target'));dest_note=f'ppt/notesSlides/partDivider{d["part"]}.xml';assert dest_note not in files;files[dest_note]=a.read(source_note);nr=E.Element('{'+PK+'}Relationships',nsmap={None:PK});E.SubElement(nr,'{'+PK+'}Relationship',Id='rId1',Type=N['r']+'/notesMaster',Target='/'+notesmaster);E.SubElement(nr,'{'+PK+'}Relationship',Id='rId2',Type=N['r']+'/slide',Target='/'+dst);files[rel(dest_note)]=xml(nr);rd.set('Target','/'+dest_note);E.SubElement(types,'{'+CT+'}Override',PartName='/'+dest_note,ContentType='application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml')
   else:raise RuntimeError('Unexpected relationship '+kind)
   newrel.append(rd)
  files[dst]=xml(root);files[rel(dst)]=xml(newrel);rid='rIdPartDivider'+str(d['part']);E.SubElement(rels,'{'+PK+'}Relationship',Id=rid,Type=N['r']+'/slide',Target='/'+dst);si=E.Element('{'+N['p']+'}sldId',id=str(id_max+i+1));si.set('{'+N['r']+'}id',rid);additions[d['before']]=(si,dst,d);E.SubElement(types,'{'+CT+'}Override',PartName='/'+dst,ContentType='application/vnd.openxmlformats-officedocument.presentationml.slide+xml')
 for x in list(lst):lst.remove(x)
 for i,oldid in enumerate(oldids,1):
  if i in additions:
   si,dst,d=additions[i];lst.append(si);new_order.append({'page':len(new_order)+1,'kind':'divider','part':d['part'],'title':d['title'].replace('\n',' '),'package_part':dst,'layout':'L03'})
  lst.append(oldid);new_order.append({'page':len(new_order)+1,'kind':'preserved','original_page':i,'package_part':old[i-1]})
 files['ppt/presentation.xml']=xml(prs);files['ppt/_rels/presentation.xml.rels']=xml(rels);files['[Content_Types].xml']=xml(types)
 app=E.fromstring(files['docProps/app.xml']);slides=app.find('{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Slides')
 if slides is not None:slides.text=str(len(new_order))
 files['docProps/app.xml']=xml(app)
 assert len(new_order)==26
 assert all(files[p]==z.read(p)for p in old)
 assert all(files[n]==z.read(n)for n in z.namelist()if n.startswith('ppt/media/'))
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED)as out:
  for name,data in files.items():out.writestr(name,data)
 (B/'slide-map.json').write_text(json.dumps({'source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'count':len(new_order),'original_slides_byte_identical':True,'original_media_byte_identical':True,'slides':new_order},ensure_ascii=False,indent=2),encoding='utf8')
print('26 slides: 21 originals preserved byte for byte + 5 L03 dividers.')
