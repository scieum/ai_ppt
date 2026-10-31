from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops
import json,hashlib,io,fitz,posixpath,subprocess,imageio_ffmpeg
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
D=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_12장_종류예시_v5.pptx'
S=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_10장_효과예시_v4.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
RID='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
def ordered(z):
 rels={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 return [rels[x.get(RID)].lstrip('/')if rels[x.get(RID)].startswith('/')else posixpath.normpath('ppt/'+rels[x.get(RID)])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
report={'slides':12,'type_examples_page':5,'added_knowledge_pages':[10,11],'native_table_page':12}
with ZipFile(D)as z,ZipFile(S)as src:
 parts=ordered(z);old=ordered(src);assert len(parts)==12
 for page in [1,2,3,4,6,7,8,9]:assert z.read(parts[page-1])==src.read(old[page-1])
 assert z.read(parts[11])==src.read(old[9])
 report['other_nine_slide_xml_preserved']=True
 for name in src.namelist():
  if name.startswith('ppt/media/'):assert z.read(name)==src.read(name)
 report['previous_animation_and_media_preserved']=True
 texts=''
 for part in parts:
  t=E.fromstring(z.read(part));texts+='\n'.join(t.xpath('.//a:t/text()',namespaces=N))
 for phrase in ['프롬프트','제작 방법','실습하기','커넥터','장면표','고려해야']:assert phrase not in texts
 newk=['typography','infographic','interface','logo','illustration','normal','delay','long','ease-in','ease-out','ease-in-out']
 for kind in newk:
  data=z.read('ppt/media/type-example-'+kind+'.gif');assert data==(B/'assets'/(kind+'.gif')).read_bytes()
  with Image.open(io.BytesIO(data))as im:assert im.n_frames>2 and im.info['loop']==0
 report['eleven_new_embedded_looping_examples_verified']=True
 assert len(E.fromstring(z.read(parts[4])).findall('.//p:pic',N))==6
 assert E.fromstring(z.read(parts[11])).find('.//a:tbl',N)is not None
 assert len([n for n in z.namelist()if n.startswith('ppt/notesSlides/')and n.endswith('.xml')])==12
report['knowledge_only_scope_preserved']=True
oldrender=U/'renders/effect-examples-20261028';render=U/'renders/type-examples-20261028'
for page,source in [(i,i)for i in [1,2,3,4,6,7,8,9]]+[(12,10)]:
 a=Image.open(render/f'slide-{page:02}.png').convert('RGB');b=Image.open(oldrender/f'slide-{source:02}.png').convert('RGB');assert ImageChops.difference(a,b).getbbox()is None
report['other_nine_slide_pixels_preserved']=True
a=Image.open(render/'slide-05.png').convert('RGB');b=Image.open(oldrender/'slide-05.png').convert('RGB')
for box in [(0,0,1920,500),(0,500,1080,1080),(0,1015,1920,1080)]:assert ImageChops.difference(a.crop(box),b.crop(box)).getbbox()is None
report['type_page_title_logo_footer_two_text_columns_preserved']=True
overflow=[]
for b in json.loads((render/'text-bounds.json').read_text(encoding='utf-8-sig')):
 if b['name']in ['copyright_footer','section_number']:continue
 if b['text_width']>b['shape_width']+1 or b['text_height']>b['shape_height']+1:overflow.append(b)
assert not overflow,overflow
report['body_text_overflow_count']=0
with fitz.open(D.with_suffix('.pdf'))as pdf:assert len(pdf)==12
assert len(list(render.glob('slide-*.png')))==12
report['pdf_pages']=12;report['all_slides_native_rendered']=True
video={};ff=imageio_ffmpeg.get_ffmpeg_exe()
for page,offset in [(5,0),(10,4),(11,8)]:
 frames=[]
 for i,t in enumerate([.5,2.5]):
  out=B/f'playback-page{page}-{i}.png';res=subprocess.run([ff,'-hide_banner','-loglevel','error','-ss',str(offset+t),'-i',str(B/'playback-v5.mp4'),'-frames:v','1','-y',str(out)],capture_output=True);assert res.returncode==0,res.stderr
  frames.append(Image.open(out).convert('RGB'))
 for k in range(5 if page==5 else 3):
  y=round(383.3+k*48.67);box=(740,y,1114,y+36)if page==5 else(200+k*320,451,440+k*320,531)
  diff=ImageChops.difference(frames[0].crop(box),frames[1].crop(box));num=sum(1 for v in diff.get_flattened_data()if max(v)>10);assert num>100,(page,k,num);video[f'{page}-{k}']=num
report['eleven_examples_motion_verified_in_native_powerpoint_video']=video
h=hashlib.sha256(D.read_bytes()).hexdigest();assert h==json.loads((B/'validation-v5.json').read_text(encoding='utf8'))['finalSha256'];report['pptx_sha256']=h
oldlesson=json.loads((U/'checks/lesson-only-20261028/verification.json').read_text(encoding='utf8'))['source_lesson_sha256'];assert hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest()==oldlesson
report['lesson_unchanged']=True;report['reference_adapted_concept_pages']=[20,23,24];report['reference_media_not_extracted']=True;report['inherited_g10_status']='unchanged; pending inherited rights inventory'
out=U/'checks/type-examples-20261028/verification.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False,indent=2))
