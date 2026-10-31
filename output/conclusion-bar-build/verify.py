from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import fitz,numpy as np,json,hashlib,math
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
src=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_논리구조에셋반영_43장_v31.pptx';out=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_결론텍스트바_43장_v32.pptx';spec=json.loads((B/'spec.json').read_text(encoding='utf8'))
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'};rects={}
with ZipFile(src) as a,ZipFile(out) as b:
 assert set(a.namelist())==set(b.namelist());assert {n for n in a.namelist() if a.read(n)!=b.read(n)}=={d['part'] for d in spec}
 for d in spec:
  x=E.fromstring(a.read(d['part']));y=E.fromstring(b.read(d['part']));rects[d['page']]=[]
  for root,isnew in [(x,False),(y,True)]:
   tree=root.find('p:cSld/p:spTree',N)
   for s in list(tree):
    nv=s.find('p:nvSpPr/p:cNvPr',N)
    if nv is None:continue
    name=nv.get('name');selected=name.startswith('conclusion-bar-') if isnew else name in d['remove']
    if not selected:continue
    if isnew and name=='conclusion-bar-message':assert ' '.join(s.xpath('.//a:t/text()',namespaces=N))==d['message']
    f=s.find('p:spPr/a:xfrm',N);o=f.find('a:off',N);e=f.find('a:ext',N);rects[d['page']].append([int(o.get('x'))/12700,int(o.get('y'))/12700,int(e.get('cx'))/12700,int(e.get('cy'))/12700]);tree.remove(s)
  assert E.tostring(x,method='c14n')==E.tostring(y,method='c14n'),d['page']
old=fitz.open(src.with_suffix('.pdf'));new=fitz.open(out.with_suffix('.pdf'));assert len(old)==len(new)==43
for i in range(43):
 a=old[i].get_pixmap();b=new[i].get_pixmap();av=np.frombuffer(a.samples,np.uint8).reshape(a.height,a.width,a.n);bv=np.frombuffer(b.samples,np.uint8).reshape(b.height,b.width,b.n);diff=np.any(av!=bv,axis=2)
 for x,y,w,h in rects.get(i+1,[]):diff[max(0,math.floor(y)-2):min(a.height,math.ceil(y+h)+2),max(0,math.floor(x)-2):min(a.width,math.ceil(x+w)+2)]=False
 assert not diff.any(),i+1
bounds=json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig'));bars=[s for s in bounds if s['name'].startswith('conclusion-bar-')];overflow=[];overlap=[]
for a in bars:
 if a['text_width']>a['shape_width']+1 or a['text_height']>a['shape_height']+1:overflow.append([a['slide'],a['name']])
 for b in bounds:
  if a['slide']!=b['slide'] or a['name']==b['name'] or not b['text'].strip():continue
  w=min(a['text_left']+a['text_width'],b['text_left']+b['text_width'])-max(a['text_left'],b['text_left']);h=min(a['text_top']+a['text_height'],b['text_top']+b['text_height'])-max(a['text_top'],b['text_top'])
  if w>2 and h>2:overlap.append([a['slide'],a['name'],b['name']])
assert not overflow,overflow
assert not overlap,overlap
record={'slides':43,'conclusion_bar_slides':[d['page'] for d in spec],'existing_message_wording_preserved':True,'other_slide_objects_and_media_unchanged':True,'pixels_outside_old_and_new_bar_frames_unchanged':True,'other_32_slides_byte_and_pixel_identical':True,'bar_text_overflow':overflow,'bar_text_overlap':overlap,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'inherited_G10_status':'unchanged'}
dest=U/'checks/conclusion-bar-20261030';dest.mkdir(parents=True,exist_ok=True);(dest/'verification.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(record))
