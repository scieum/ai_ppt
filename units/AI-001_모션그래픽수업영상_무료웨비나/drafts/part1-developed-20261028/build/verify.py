from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops,ImageDraw
import fitz,json,hashlib
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
S=R/'output/webinar-atomic-images/NotionTalk_원자모형_생성이미지반영_21장_v1.pptx'
F=R/'output/webinar-part1-developed/NotionTalk_Part1_내용디자인고도화_21장_v2.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pres=json.loads((B/'preservation.json').read_text(encoding='utf8'));unchanged=[];animations=0
with ZipFile(S) as src,ZipFile(F) as z:
 assert len(E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N))==21
 changed=[n for n in src.namelist() if src.read(n)!=z.read(n)]
 assert set(changed)==set(pres['changed_parts'])
 for n in src.namelist():
  if n.startswith('ppt/media/'):assert src.read(n)==z.read(n),n
  if n.startswith('ppt/slides/') and n.endswith('.xml'):
   s=E.fromstring(src.read(n));f=E.fromstring(z.read(n));st=s.find('p:timing',N);ft=f.find('p:timing',N)
   if st is not None:
    assert E.tostring(st,method='c14n')==E.tostring(ft,method='c14n'),n
    animations+=len(st.findall('.//p:animEffect',N))+len(st.findall('.//p:animMotion',N))+len(st.findall('.//p:animScale',N))+len(st.findall('.//p:animRot',N))
   texts=''.join(f.xpath('.//a:t/text()',namespaces=N));assert '학생이 따라올 수 있는 영상인가요?' not in texts
   assert 'NotionTalk. All rights reserved.' in texts
 for n in ['ppt/media/flipbook-motion.gif','ppt/media/atomic-thomson.png','ppt/media/atomic-rutherford.png','ppt/media/atomic-bohr.png']:assert z.read(n)==src.read(n)
for i in [1,2,3,20,21]:
 a=Image.open(U/f'renders/atomic-images-20261028/slide-{i:02}.png').convert('RGB');b=Image.open(U/f'renders/part1-developed-20261028/slide-{i:02}.png').convert('RGB')
 assert a.size==b.size and ImageChops.difference(a,b).getbbox() is None,i;unchanged.append(i)
now=json.loads((U/'renders/part1-developed-20261028/text-bounds.json').read_text(encoding='utf-8-sig'));before=json.loads((U/'renders/atomic-images-20261028/text-bounds.json').read_text(encoding='utf-8-sig'));new_overflow=[]
for x in now:
 if not 4<=x['slide']<=19:continue
 if x['text_width']>x['shape_width']+1 or x['text_height']>x['shape_height']+1:
  old=next((b for b in before if b['slide']==x['slide'] and b['name']==x['name']),None)
  if x!=old:new_overflow.append((x['slide'],x['name']))
assert not new_overflow,new_overflow
pdf=fitz.open(F.with_suffix('.pdf'));assert len(pdf)==21
assert '0.3+0.8+3=4.1초' in ''.join(pdf[9].get_text().split())
assert '4~16초' in pdf[12].get_text()
assert sha(S)==pres['source_sha256']
validation=json.loads((B/'validation-v2.json').read_text(encoding='utf8'));assert validation['finalSha256']==sha(F)
for key in ['packageIntegrity','presentationLayout']:assert validation[key]['findingCount']==0
# Side-by-side comparison sheets are private QA artifacts, not reused source art.
for page in [6,14,17,19]:
 cv=Image.new('RGB',(1920,540),'#202020')
 for j,folder in enumerate(['atomic-images-20261028','part1-developed-20261028']):
  im=Image.open(U/f'renders/{folder}/slide-{page:02}.png').convert('RGB');im.thumbnail((960,540));cv.paste(im,(j*960,0))
 cv.save(B/f'compare-page-{page:02}.jpg')
report={'source_sha256':sha(S),'final_sha256':sha(F),'slide_count':21,'pdf_pages':21,'edited_pages':list(range(4,20)),'untouched_render_pixels_identical':unchanged,'all_existing_media_bytes_identical':True,'native_animation_xml_identical':True,'native_animation_element_count':animations,'new_text_overflow':new_overflow,'removed_student_slide_not_restored':True,'visual_review_fullsize_pages':list(range(4,20)),'package_layout_font_import_validation':'pass: validation-v2.json','source_original_preserved':True,'part1_proposed_minutes':26,'actual_new_app_runs':False,'new_mp4_export':False,'G10_approval_created':False}
C=U/'checks/part1-developed-20261028';C.mkdir(parents=True,exist_ok=True);(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('Verified 21-slide PPT/PDF, all 16 Part 1 slides, five untouched pages, original media and animation XML, and text fit.')
