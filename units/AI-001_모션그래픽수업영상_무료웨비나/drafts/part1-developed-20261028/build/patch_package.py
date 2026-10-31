from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import posixpath,json,hashlib
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
SOURCE=R/'output/webinar-atomic-images/NotionTalk_원자모형_생성이미지반영_21장_v1.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def relpart(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def target(p,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def slideat(z,n):
 ids=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N);rs=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'));rid=ids[n-1].get('{'+N['r']+'}id');return target('ppt/presentation.xml',next(r.get('Target') for r in rs if r.get('Id')==rid))
def name(n):return n.find('.//p:cNvPr',N).get('name','')
def raw(n):return E.tostring(n,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(SOURCE) as base,ZipFile(B/'edited-roundtrip.pptx') as extra:
 files={n:base.read(n) for n in base.namelist()};original=files.copy();allowed=set();reports=[]
 for page in range(4,20):
  part=slideat(base,page);ep=slideat(extra,page);s=E.fromstring(files[part]);e=E.fromstring(extra.read(ep));st=s.find('p:cSld/p:spTree',N);et=e.find('p:cSld/p:spTree',N)
  original_shapes={name(n):n for n in st.findall('p:sp',N) if name(n)}
  edit_shapes={name(n):n for n in et.findall('p:sp',N) if name(n)}
  animated=set(s.xpath('.//p:spTgt/@spid',namespaces=N));nextid=max(int(n.get('id')) for n in st.findall('.//p:cNvPr',N))+1
  for old in list(st.findall('p:sp',N)):
   key=name(old)
   if key not in edit_shapes:
    assert old.find('.//p:cNvPr',N).get('id') not in animated,(page,key)
    st.remove(old)
   else:
    replacement=deepcopy(edit_shapes[key]);replacement.find('.//p:cNvPr',N).set('id',old.find('.//p:cNvPr',N).get('id'));st.replace(old,replacement)
  for key,new in edit_shapes.items():
   if key not in original_shapes:
    new=deepcopy(new);new.find('.//p:cNvPr',N).set('id',str(nextid));nextid+=1;st.append(new)
  # Existing media, GIFs and background images are kept byte-for-byte.
  if page==17:
   srcpics=[n for n in st.findall('p:pic',N) if name(n).startswith('generated-atomic-')]
   epics=[n for n in et.findall('p:pic',N) if int(n.find('p:spPr/a:xfrm/a:ext',N).get('cx'))<10000000]
   srcpics.sort(key=lambda n:int(n.find('p:spPr/a:xfrm/a:off',N).get('x')));epics.sort(key=lambda n:int(n.find('p:spPr/a:xfrm/a:off',N).get('x')))
   assert len(srcpics)==len(epics)==3
   for sp,epic in zip(srcpics,epics):
    oldxf=sp.find('p:spPr/a:xfrm',N);newxf=deepcopy(epic.find('p:spPr/a:xfrm',N));oldxf.getparent().replace(oldxf,newxf)
  ids={x.get('id') for x in st.findall('.//p:cNvPr',N)};assert animated<=ids,(page,animated-ids)
  assert len(ids)==len(st.findall('.//p:cNvPr',N)),page
  files[part]=raw(s);allowed.add(part)
  rs=E.fromstring(files[relpart(part)]);ers=E.fromstring(extra.read(relpart(slideat(extra,page))))
  np=target(part,next(r.get('Target') for r in rs if r.get('Type').endswith('/notesSlide')))
  enp=target(slideat(extra,page),next(r.get('Target') for r in ers if r.get('Type').endswith('/notesSlide')))
  original_notes=E.fromstring(files[np]);new_notes=E.fromstring(extra.read(enp))
  def body(nt):
   for sh in nt.findall('.//p:sp',N):
    ph=sh.find('.//p:ph',N)
    if ph is not None and ph.get('type')=='body':return sh.find('p:txBody',N)
   raise ValueError('Missing notes body')
  oldbody=body(original_notes);oldbody.getparent().replace(oldbody,deepcopy(body(new_notes)));files[np]=raw(original_notes);allowed.add(np)
  reports.append({'page':page,'part':part,'preserved_animation_targets':sorted(animated),'native_shapes':len(st.findall('p:sp',N))})
 changed=[n for n,v in original.items() if files[n]!=v];assert set(changed)<=allowed
 for n,v in original.items():
  if n not in allowed:assert files[n]==v,n
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as z:
  for n,v in files.items():z.writestr(n,v)
 (B/'preservation.json').write_text(json.dumps({'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'changed_parts':changed,'untouched_pages':[1,2,3,20,21],'all_media_bytes_identical':True,'slides':reports},ensure_ascii=False,indent=2),encoding='utf8')
print('Patched 16 Part 1 slides and notes; all other package parts, media and native animations preserved.')
