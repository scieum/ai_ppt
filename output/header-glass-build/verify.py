from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from copy import deepcopy
import json,hashlib,fitz,numpy as np
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
audit=json.loads((B/'source-audit.json').read_text(encoding='utf-8'));changes=json.loads((B/'changes.json').read_text(encoding='utf-8'))
src=Path(audit['source']);out=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_헤더확대_글라스로고_43장_v27.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
names={x['name'] for x in changes['headers']};canon=lambda e:E.tostring(e,method='c14n')
with ZipFile(src) as a,ZipFile(out) as b:
 modified=set(changes['modified_slide_parts']+[changes['prep_relationships']])
 untouched=[n for n in a.namelist() if n not in modified]
 assert all(a.read(n)==b.read(n) for n in untouched)
 assert set(b.namelist())-set(a.namelist())=={f'ppt/media/header-glass-{n}.png' for n in ['claude','codex','higgsfield']}
 for i,part in enumerate(audit['parts'],1):
  old=E.fromstring(a.read(part));new=E.fromstring(b.read(part))
  assert old.xpath('//a:t/text()',namespaces=N)==new.xpath('//a:t/text()',namespaces=N)
  for sp in new.findall('.//p:sp',N):
   name=sp.find('p:nvSpPr/p:cNvPr',N).get('name')
   if name in names:
    for el in sp.xpath('.//*[@sz]'):el.set('sz',str(int(el.get('sz'))-200))
   if name=='section_number':
    ext=sp.find('p:spPr/a:xfrm/a:ext',N);ext.set('cx',str(int(ext.get('cx'))-76200))
   if name=='section_heading':
    off=sp.find('p:spPr/a:xfrm/a:off',N);ext=sp.find('p:spPr/a:xfrm/a:ext',N)
    off.set('x',str(int(off.get('x'))-76200));ext.set('cx',str(int(ext.get('cx'))+76200))
   if i==3 and name=='required':
    prior=next(s for s in old.findall('.//p:sp',N) if s.find('p:nvSpPr/p:cNvPr',N).get('name')=='required')
    sp.replace(sp.find('p:spPr',N),deepcopy(prior.find('p:spPr',N)))
  assert canon(old)==canon(new),part
 media=[n for n in a.namelist() if n.startswith('ppt/media/')]
 notes=[n for n in a.namelist() if n.startswith('ppt/notesSlides/')]
 timing=[i for i,p in enumerate(audit['parts'],1) if E.fromstring(b.read(p)).find('p:timing',N) is not None]
pdf_before=fitz.open(src.with_suffix('.pdf'));pdf_after=fitz.open(out.with_suffix('.pdf'))
assert len(pdf_before)==len(pdf_after)==43
comparison=[]
for i in range(43):
 p=pdf_before[i].get_pixmap();q=pdf_after[i].get_pixmap()
 x=np.frombuffer(p.samples,np.uint8).reshape(p.height,p.width,p.n);y=np.frombuffer(q.samples,np.uint8).reshape(q.height,q.width,q.n)
 diff=np.any(x!=y,axis=2);bbox=None
 if diff.any():
  yy,xx=np.where(diff);bbox=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]
 if i!=2:assert not diff[115:].any(),(i+1,bbox)
 if audit['parts'][i] not in changes['modified_slide_parts']:assert not diff.any(),i+1
 comparison.append({'slide':i+1,'changed_pixels_bbox':bbox,'body_unchanged':bool(not diff[115:].any())})
bounds=json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig'))
target=[x for x in bounds if x['name'] in names or x['name']=='required']
overflow=[x for x in target if x['text_width']>x['shape_width']+1 or x['text_height']>x['shape_height']+1]
assert not overflow,overflow
result={'source':str(src),'output':str(out),'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'slide_count':43,'headers_changed':len(changes['headers']),'header_owner_slides':len(changes['modified_slide_parts']),'font_delta_pt':2,'all_text_preserved':True,'only_requested_shape_changes':True,'original_media_preserved':len(media),'original_note_parts_preserved':len(notes),'timing_owner_slides':timing,'header_text_overflow':overflow,'pdf_comparison':comparison}
dest=U/'checks/header-glass-20261030';dest.mkdir(parents=True,exist_ok=True)
(dest/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='pdf_comparison'},ensure_ascii=False,indent=2))
