from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops
import json,hashlib,io,fitz,posixpath,subprocess,imageio_ffmpeg
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
D=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_13장_표현확장_v6.pptx'
S=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_12장_종류예시_v5.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'};RID='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
def ordered(z):
 rr={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 return [rr[x.get(RID)].lstrip('/')if rr[x.get(RID)].startswith('/')else posixpath.normpath('ppt/'+rr[x.get(RID)])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
report={'slides':13,'added_page':9,'native_table_page':13}
with ZipFile(D)as z,ZipFile(S)as src:
 parts=ordered(z);old=ordered(src);assert len(parts)==13
 for i,oldpart in enumerate(old):assert z.read(parts[i if i<8 else i+1])==src.read(oldpart)
 report['all_twelve_source_slide_xml_preserved']=True
 for name in src.namelist():
  if name.startswith('ppt/media/'):assert z.read(name)==src.read(name)
 report['all_prior_media_animations_preserved']=True
 for kind in ['morph','rotation','gradient']:
  data=z.read('ppt/media/video7-'+kind+'.gif');assert data==(B/'assets'/(kind+'.gif')).read_bytes()
  with Image.open(io.BytesIO(data))as im:assert im.n_frames>10 and im.info['loop']==0
 report['three_embedded_looping_examples_verified']=True
 tree=E.fromstring(z.read(parts[8]));assert len(tree.findall('.//p:pic',N))==13
 assert E.fromstring(z.read(parts[12])).find('.//a:tbl',N)is not None
 text='\n'.join(t for part in parts for t in E.fromstring(z.read(part)).xpath('.//a:t/text()',namespaces=N))
 assert not any(x in text for x in ['프롬프트','제작 방법','실습하기','커넥터','장면표','고려해야'])
 assert len([p for p in z.namelist()if p.startswith('ppt/notesSlides/')and p.endswith('.xml')])==13
report['knowledge_only_scope_preserved']=True
render=U/'renders/video7-concepts-20261028';oldrender=U/'renders/type-examples-20261028'
for i in range(1,13):
 newpage=i if i<=8 else i+1;a=Image.open(render/f'slide-{newpage:02}.png').convert('RGB');b=Image.open(oldrender/f'slide-{i:02}.png').convert('RGB');assert ImageChops.difference(a,b).getbbox()is None
report['all_twelve_source_slide_pixels_preserved']=True
overflow=[]
for b in json.loads((render/'text-bounds.json').read_text(encoding='utf-8-sig')):
 if b['name']in ['copyright_footer','section_number']:continue
 if b['text_width']>b['shape_width']+1 or b['text_height']>b['shape_height']+1:overflow.append(b)
assert not overflow,overflow
report['body_text_overflow_count']=0
with fitz.open(D.with_suffix('.pdf'))as pdf:assert len(pdf)==13
assert len(list(render.glob('slide-*.png')))==13
report['pdf_pages']=13;report['all_slides_native_rendered']=True
ff=imageio_ffmpeg.get_ffmpeg_exe();frames=[]
for i,t in enumerate([.2,1.2]):
 out=B/f'playback-sample-{i}.png';res=subprocess.run([ff,'-hide_banner','-loglevel','error','-ss',str(t),'-i',str(B/'playback-v6.mp4'),'-frames:v','1','-y',str(out)],capture_output=True);assert res.returncode==0,res.stderr;frames.append(Image.open(out).convert('RGB'))
motions={}
for k,kind in enumerate(['morph','rotation','gradient']):
 box=(200+k*320,451,440+k*320,531);diff=ImageChops.difference(frames[0].crop(box),frames[1].crop(box));num=sum(1 for v in diff.get_flattened_data()if max(v)>10);assert num>100,(kind,num);motions[kind]=num
report['motion_verified_in_native_powerpoint_video']=motions
h=hashlib.sha256(D.read_bytes()).hexdigest();assert h==json.loads((B/'validation-v6.json').read_text(encoding='utf8'))['finalSha256'];report['pptx_sha256']=h
source=json.loads((U/'research/youtube-20261028-7xOcIYWGG0A/source-index.json').read_text(encoding='utf8'));report['source_video_id']=source['id'];report['caption_segments_read']=source['segments'];report['source_basis']='complete Korean captions and video description; no source visual footage reused'
oldlesson=json.loads((U/'checks/lesson-only-20261028/verification.json').read_text(encoding='utf8'))['source_lesson_sha256'];assert hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest()==oldlesson;report['lesson_unchanged']=True;report['inherited_g10_status']='unchanged; pending inherited rights inventory'
out=U/'checks/video7-concepts-20261028/verification.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False,indent=2))
