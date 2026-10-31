from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from copy import deepcopy
import json, hashlib, math
import fitz, numpy as np
from PIL import Image, ImageDraw
B=Path(__file__).resolve().parent; R=B.parent.parent
U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
spec=json.loads((B/'spec.json').read_text(encoding='utf-8'))
edits=json.loads((B/'actual-edits.json').read_text(encoding='utf-8'))
src=Path(spec['source']); out=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_폰트간격점검_43장_v29.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(src) as za, ZipFile(out) as zb:
 assert set(za.namelist())==set(zb.namelist())
 changed=[n for n in za.namelist() if za.read(n)!=zb.read(n)]
 assert set(changed)<=set(spec['parts'])
 for part in spec['parts']:
  old=E.fromstring(za.read(part)); new=E.fromstring(zb.read(part))
  assert old.xpath('//a:t/text()',namespaces=N)==new.xpath('//a:t/text()',namespaces=N)
  for e in [e for e in edits if e['part']==part]:
   a=next(s for s in old.findall('.//p:sp',N) if s.find('p:nvSpPr/p:cNvPr',N).get('name')==e['name'])
   b=next(s for s in new.findall('.//p:sp',N) if s.find('p:nvSpPr/p:cNvPr',N).get('name')==e['name'])
   x=b.find('p:spPr/a:xfrm',N);x.getparent().replace(x,deepcopy(a.find('p:spPr/a:xfrm',N)))
   for ael,bel in zip(a.xpath('.//*[@sz]'),b.xpath('.//*[@sz]')):bel.set('sz',ael.get('sz'))
   aa=a.find('p:txBody/a:bodyPr',N);bb=b.find('p:txBody/a:bodyPr',N)
   if 'anchor' in aa.attrib:bb.set('anchor',aa.get('anchor'))
   else:bb.attrib.pop('anchor',None)
  assert E.tostring(old,method='c14n')==E.tostring(new,method='c14n'),part
oldpdf=fitz.open(src.with_suffix('.pdf'));newpdf=fitz.open(out.with_suffix('.pdf'))
assert len(oldpdf)==len(newpdf)==43
page_checks=[]
for i in range(43):
 a=oldpdf[i].get_pixmap(); b=newpdf[i].get_pixmap()
 av=np.frombuffer(a.samples,np.uint8).reshape(a.height,a.width,a.n);bv=np.frombuffer(b.samples,np.uint8).reshape(b.height,b.width,b.n)
 diff=np.any(av!=bv,axis=2); count=int(diff.sum())
 for e in [e for e in edits if e['slide']==i+1]:
  for p in [e['old_position'],e['position']]:
   l=max(0,math.floor(p['left']*.75)-3);t=max(0,math.floor(p['top']*.75)-3)
   rr=min(a.width,math.ceil((p['left']+p['width'])*.75)+3);bt=min(a.height,math.ceil((p['top']+p['height'])*.75)+3)
   diff[t:bt,l:rr]=False
 assert not diff.any(),('Unexpected pixel change',i+1,int(diff.sum()))
 page_checks.append({'slide':i+1,'changed_pixels':count,'pixels_outside_edited_text_frames_unchanged':True})
bounds=json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig'))
overflow=[]; overlaps=[]
for s in bounds:
 if not s['text'].strip():continue
 for axis,dim in [('left','width'),('top','height')]:
  # PowerPoint BoundLeft includes optical overhang on right-aligned footers.
  # Check required text extent against frame capacity and the actual slide edge.
  limit=960 if axis=='left' else 540
  if s['text_'+dim]>s['shape_'+dim]+1 or s['text_'+axis]<-1 or s['text_'+axis]+s['text_'+dim]>limit+1:
   overflow.append((s['slide'],s['name'],axis))
for i,a in enumerate(bounds):
 if not a['text'].strip():continue
 for b in bounds[i+1:]:
  if a['slide']!=b['slide'] or not b['text'].strip():continue
  w=min(a['text_left']+a['text_width'],b['text_left']+b['text_width'])-max(a['text_left'],b['text_left'])
  h=min(a['text_top']+a['text_height'],b['text_top']+b['text_height'])-max(a['text_top'],b['text_top'])
  if w>2 and h>2:overlaps.append((a['slide'],a['name'],b['name']))
assert not overflow,overflow
assert not overlaps,overlaps
record={'slides':43,'output':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'actual_text_objects_adjusted':len(edits),'changed_slide_parts':changed,'all_text_content_preserved':True,'all_media_notes_tables_relationships_and_animations_preserved':True,'only_font_size_text_frame_and_vertical_anchor_changed':True,'native_powerpoint_text_overflow':overflow,'native_powerpoint_text_overlaps':overlaps,'page_checks':page_checks}
dest=U/'checks/typography-qa-20261030';dest.mkdir(parents=True,exist_ok=True)
(dest/'verification.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
render=U/'renders/typography-qa-20261030'
for start in range(1,44,6):
 sheet=Image.new('RGB',(1920,1716),'#444444');d=ImageDraw.Draw(sheet)
 for j,n in enumerate(range(start,min(start+6,44))):
  im=Image.open(render/f'slide-{n:02d}.png').convert('RGB').resize((960,540))
  x=(j%2)*960;y=(j//2)*572;sheet.paste(im,(x,y+28));d.text((x+10,y+6),f'Slide {n:02d}',fill='white')
 sheet.save(B/f'review-{start:02d}.jpg',quality=92)
print(json.dumps({'slides':43,'text_objects_adjusted':len(edits),'overflow':overflow,'overlaps':overlaps,'other_content_and_pixels_preserved':True}))
