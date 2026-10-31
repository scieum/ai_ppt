from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops
import fitz,json,hashlib,io
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
D=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_10장_효과예시_v4.pptx'
S=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_10장_v2.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
report={'slides':10,'modified_pages':[6,7,8,9]}
with ZipFile(D)as z,ZipFile(S)as src:
 for page in [1,2,3,4,5,10]:
  part=f'ppt/slides/lesson-{page:02}.xml';assert z.read(part)==src.read(part)
 report['other_slide_xml_unchanged']=True
 for page in [3,6,9]:
  part=f'ppt/slides/lesson-{page:02}.xml';a=E.fromstring(z.read(part)).find('p:timing',N);b=E.fromstring(src.read(part)).find('p:timing',N)
  assert E.tostring(a)==E.tostring(b)
 report['retained_native_animation_pages']=[3,6,9]
 for name in src.namelist():
  if name.startswith('ppt/media/'):assert z.read(name)==src.read(name)
 report['existing_media_preserved']=True
 for kind in ['fade','slide','zoom','reveal','typewriter','stagger']:
  data=z.read('ppt/media/motion-example-'+kind+'.gif')
  assert data==(B/'assets'/(kind+'.gif')).read_bytes()
  with Image.open(io.BytesIO(data))as im:assert im.n_frames>2 and im.info['loop']==0
 report['six_embedded_looping_gifs_verified']=True
 visible=''
 for page in range(1,11):
  tree=E.fromstring(z.read(f'ppt/slides/lesson-{page:02}.xml'))
  visible+='\n'.join(tree.xpath('.//a:t/text()',namespaces=N))
  if page in [6,7,8,9]:assert any(x.get('name','').startswith('ex-')for x in tree.findall('.//p:cNvPr',N))
  if page in [7,8]:
   assert tree.find('p:timing',N)is None
   assert len([x for x in tree.findall('.//p:cNvPr',N)if x.get('name','').startswith('motion-example-')])==3
 assert not any(x in visible for x in ['프롬프트','고려해야','장면표','커넥터','원자모형','제작 방법','실습하기'])
 assert E.fromstring(z.read('ppt/slides/lesson-10.xml')).find('.//a:tbl',N)is not None
 report['knowledge_only_scope_and_native_table_preserved']=True
renders=U/'renders/effect-examples-20261028';old=U/'renders/knowledge-only-20261028'
for page in [1,2,3,4,5,10]:
 assert ImageChops.difference(Image.open(renders/f'slide-{page:02}.png').convert('RGB'),Image.open(old/f'slide-{page:02}.png').convert('RGB')).getbbox()is None
report['other_slide_pixels_unchanged']=True
for page in [6,7,8,9]:
 a=Image.open(renders/f'slide-{page:02}.png').convert('RGB');b=Image.open(old/f'slide-{page:02}.png').convert('RGB')
 assert ImageChops.difference(a.crop((0,0,1920,500)),b.crop((0,0,1920,500))).getbbox()is None
 assert ImageChops.difference(a.crop((0,1015,1920,1080)),b.crop((0,1015,1920,1080))).getbbox()is None
report['changed_slide_header_logo_footer_pixels_unchanged']=True
overflow=[]
for b in json.loads((renders/'text-bounds.json').read_text(encoding='utf-8-sig')):
 if b['name']in ['copyright_footer','section_number']:continue
 if b['text_width']>b['shape_width']+1 or b['text_height']>b['shape_height']+1:overflow.append(b)
assert not overflow,overflow
report['body_text_overflow_count']=0
with fitz.open(D.with_suffix('.pdf'))as doc:assert len(doc)==10
report['pdf_pages']=10
assert len(list(renders.glob('slide-*.png')))==10
report['all_slides_rendered']=True
h=hashlib.sha256(D.read_bytes()).hexdigest()
assert h==json.loads((B/'validation-v4.json').read_text(encoding='utf8'))['finalSha256']
report['pptx_sha256']=h
play=json.loads((B/'playback-verification.json').read_text(encoding='utf8'))
assert len(play)==6 and all(v>150 for v in play.values())
report['six_effects_motion_verified_in_native_powerpoint_video']=play
report['g10_status']='unchanged for inherited assets; new effect assets authored in project code'
out=U/'checks/effect-examples-20261028/verification.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
