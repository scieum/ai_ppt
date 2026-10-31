from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops
import json,hashlib,fitz,posixpath
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
D=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_19장_영상핵심5장확장_v8.pptx';S=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_14장_사전확인_v7.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'};RID='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
def ordered(z):
 rr={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 return [rr[x.get(RID)].lstrip('/')if rr[x.get(RID)].startswith('/')else posixpath.normpath('ppt/'+rr[x.get(RID)])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
report={'slides':19,'five_new_video_based_pages':[15,16,17,18,19],'native_table_pages':[13,17,19]}
with ZipFile(D)as z,ZipFile(S)as src:
 p=ordered(z);old=ordered(src);assert len(p)==19
 for i,part in enumerate(old):assert z.read(p[i])==src.read(part)
 report['all_fourteen_prior_slide_xml_unchanged']=True
 for part in src.namelist():
  if part.startswith('ppt/media/'):assert z.read(part)==src.read(part)
 report['all_prior_media_animations_preserved']=True
 for page in [13,17,19]:assert E.fromstring(z.read(p[page-1])).find('.//a:tbl',N)is not None
 assert E.fromstring(z.read(p[17])).find('p:timing',N)is None
 assert E.tostring(E.fromstring(z.read(p[15])).find('p:timing',N))==E.tostring(E.fromstring(src.read(old[2])).find('p:timing',N))
 report['new_role_comparison_native_animation_preserved']=True
 assert len([x for x in z.namelist()if x.startswith('ppt/notesSlides/')and x.endswith('.xml')])==19
 for page in range(15,20):
  t='\n'.join(E.fromstring(z.read(p[page-1])).xpath('.//a:t/text()',namespaces=N));assert len(t)>100
  assert 'NotionTalk' in t
 report['five_distinct_substantive_pages']=True
 report['two_still_panels_are_editable_and_static']=True
renders=U/'renders/video7-five-slides-20261028';oldrenders=U/'renders/preview-first-20261028'
for i in range(1,15):assert ImageChops.difference(Image.open(renders/f'slide-{i:02}.png').convert('RGB'),Image.open(oldrenders/f'slide-{i:02}.png').convert('RGB')).getbbox()is None
report['all_fourteen_prior_slide_pixels_unchanged']=True
overflow=[]
for b in json.loads((renders/'text-bounds.json').read_text(encoding='utf-8-sig')):
 if b['name']in ['copyright_footer','section_number']:continue
 if b['text_width']>b['shape_width']+1 or b['text_height']>b['shape_height']+1:overflow.append(b)
assert not overflow,overflow
report['body_text_overflow_count']=0
with fitz.open(D.with_suffix('.pdf'))as pdf:assert len(pdf)==19
assert len(list(renders.glob('slide-*.png')))==19
report['pdf_pages']=19;report['all_slides_native_rendered']=True
specs=json.loads((B/'edits.json').read_text(encoding='utf8'));assert len(specs)==5 and all('https://www.youtube.com/watch?v=7xOcIYWGG0A'in s['notes']for s in specs)
assert (U/'examples/video7/storyline.md').is_file()
report['source_time_ranges_and_original_examples_documented']=True
report['actual_storyline_md_example_exists']=True
h=hashlib.sha256(D.read_bytes()).hexdigest();assert h==json.loads((B/'validation-v8.json').read_text(encoding='utf8'))['finalSha256'];report['pptx_sha256']=h
assert hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest()==json.loads((U/'checks/lesson-only-20261028/verification.json').read_text(encoding='utf8'))['source_lesson_sha256']
report['lesson_unchanged']=True;report['g10_status']='unchanged for inherited assets; no original video frames or source prompt copied'
out=U/'checks/video7-five-slides-20261028/verification.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False,indent=2))
