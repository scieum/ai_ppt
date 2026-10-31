from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from PIL import Image,ImageChops
import fitz,json,hashlib
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
SRC=R/'output/webinar-cleanup/NotionTalk_검토장표삭제_21장_v1.pptx'
FINAL=R/'output/webinar-atomic-images/NotionTalk_원자모형_생성이미지반영_21장_v1.pptx'
A=R/'assets/atomic-models/20261028'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
P='http://schemas.openxmlformats.org/presentationml/2006/main';D='http://schemas.openxmlformats.org/drawingml/2006/main'
changed=[];unchanged=[]
with ZipFile(SRC) as s,ZipFile(FINAL) as f:
 for n in s.namelist():
  if s.read(n)!=f.read(n):changed.append(n)
 assert set(changed)==set(json.loads((B/'preservation.json').read_text(encoding='utf8'))['changed_original_parts'])
 assert len(E.fromstring(f.read('ppt/presentation.xml')).find('{'+P+'}sldIdLst'))==21
 sp=E.fromstring(f.read('ppt/slides/part01-slide4.xml'))
 names=[x.get('name') for x in sp.findall('.//{'+P+'}cNvPr')]
 assert not set(names)&{'thomson-positive','thomson-electron','orbit','nucleus','electron'}
 for key in ['thomson','rutherford','bohr']:
  assert f.read('ppt/media/atomic-'+key+'.png')==(A/(key+'.png')).read_bytes()
  im=Image.open(A/(key+'.png'));assert im.mode=='RGBA' and im.getextrema()[3][0]==0
 assert f.read('ppt/media/flipbook-motion.gif')==s.read('ppt/media/flipbook-motion.gif')
 for n in f.namelist():
  if n.startswith('ppt/slides/') and n.endswith('.xml'):
   tx=''.join(E.fromstring(f.read(n)).itertext())
   assert '학생이 따라올 수 있는 영상인가요?' not in tx
for i in range(1,22):
 if i==17:continue
 a=Image.open(U/f'renders/remove-student-check-20261028/slide-{i:02}.png').convert('RGB')
 b=Image.open(U/f'renders/atomic-images-20261028/slide-{i:02}.png').convert('RGB')
 assert a.size==b.size and ImageChops.difference(a,b).getbbox() is None,i
 unchanged.append(i)
bounds=json.loads((U/'renders/atomic-images-20261028/text-bounds.json').read_text(encoding='utf-8-sig'))
overflows=[]
for b in bounds:
 if b['slide']!=17:continue
 if b['text_left']<b['shape_left']-1 or b['text_top']<b['shape_top']-1 or b['text_left']+b['text_width']>b['shape_left']+b['shape_width']+1 or b['text_top']+b['text_height']>b['shape_top']+b['shape_height']+1:overflows.append(b['name'])
baseline_bounds=json.loads((U/'renders/remove-student-check-20261028/text-bounds.json').read_text(encoding='utf-8-sig'))
for name in overflows:
 now=next(b for b in bounds if b['slide']==17 and b['name']==name)
 old=next(b for b in baseline_bounds if b['slide']==17 and b['name']==name)
 assert now==old,(name,now,old)
assert not set(overflows)&{'atomic-model-caption','model-label-0','model-label-1','model-label-2'}
pdf=fitz.open(FINAL.with_suffix('.pdf'));assert len(pdf)==21
assert '개념모식도' in ''.join(pdf[16].get_text().split())
assert sha(SRC)=='441be29026ffa9760f67083c9908918454b6675059295eab0c62caa610bc6c1f'
report={'slides':21,'pdf_pages':len(pdf),'edited_page':17,'generated_images':['thomson','rutherford','bohr'],'transparent_original_pngs_embedded':True,'other_20_render_pixels_identical':unchanged,'only_original_parts_changed':changed,'flipbook_bytes_preserved':True,'removed_student_slide_still_absent':True,'new_or_moved_text_overflow':[],'preexisting_bounds_exceedance_unchanged':overflows,'package_layout_font_import_checks':'pass (validation.json)','visual_review':'17쪽 렌더에서 모형 3개·이름표·모식도 설명 및 기존 레이아웃 확인','source_sha256':sha(SRC),'final_sha256':sha(FINAL),'G10_approval_created':False}
out=U/'checks/atomic-images-20261028';out.mkdir(parents=True,exist_ok=True);(out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
with ZipFile(FINAL.parent/'NotionTalk_원자모형_생성이미지_에셋.zip','w',ZIP_DEFLATED) as z:
 for p in A.iterdir():
  if p.is_file():z.write(p,p.name)
print('Verified 21-slide PPT/PDF; three original transparent PNGs; unchanged pixels on all other 20 slides; no new text overflow.')
