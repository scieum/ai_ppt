from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops,ImageDraw
import hashlib,json,posixpath,subprocess
import numpy as np,fitz,imageio_ffmpeg
B=Path(__file__).resolve().parent;R=B.parents[1];U=next((R/'units').glob('AI-001*'));A=R/'assets/layout-library-20261028'
LIB=A/'NotionTalk_상황별레이아웃_20종_v3.pptx';APP=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_레이아웃에셋적용_21장_v16.pptx';OLD=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_캐릭터시트적용_21장_v14.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def ordered(z):
 rel=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'));paths={x.get('Id'):x.get('Target').lstrip('/')if x.get('Target').startswith('/')else posixpath.normpath(posixpath.join('ppt',x.get('Target')))for x in rel};return[paths[x.get('{'+N['r']+'}id')]for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
def serial(x):return E.tostring(x)if x is not None else None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
catalog=json.loads((A/'catalog.json').read_text(encoding='utf-8'));page_map=json.loads((A/'source-page-map.json').read_text(encoding='utf-8'));assert len(catalog['layouts'])==20 and len(page_map)==152
assert len({(x['source_id'],x['page'])for x in page_map})==152
for ref in catalog['source_documents']:assert sha(Path(ref['path']))==ref['sha256']
with ZipFile(LIB)as z:
 parts=ordered(z);assert len(parts)==20;libtable=[];native_shapes=0
 for page,part in enumerate(parts,1):
  x=E.fromstring(z.read(part));native_shapes+=len(x.findall('.//p:sp',N));assert len(x.findall('.//p:pic',N))==1
  if x.find('.//a:tbl',N)is not None:libtable.append(page)
 assert libtable==[6]
 # The only library bitmap is the user's NotionTalk brand asset.
 media=[z.read(n)for n in z.namelist()if n.startswith('ppt/media/')];assert all(m==(R/'assets/branding/notiontalk-white.png').read_bytes()for m in media)
with ZipFile(APP)as z,ZipFile(OLD)as s:
 parts=ordered(z);previous=ordered(s);assert len(parts)==21;characters=[]
 for page,(new,old)in enumerate(zip(parts,previous),1):
  x=E.fromstring(z.read(new));o=E.fromstring(s.read(old))
  if page not in[15,17,21]:assert z.read(new)==s.read(old),page
  assert serial(x.find('p:timing',N))==serial(o.find('p:timing',N)),page
  assert [serial(t)for t in x.findall('.//a:tbl',N)]==[serial(t)for t in o.findall('.//a:tbl',N)]
  for pic in x.findall('.//p:pic',N):
   name=pic.find('p:nvPicPr/p:cNvPr',N).get('name','')
   if name.startswith('character-pose-'):characters.append(page)
  if page==15:
   gifs=[x for x in x.find('p:cSld/p:spTree',N)if E.QName(x).localname=='pic'and x.find('p:nvPicPr/p:cNvPr',N).get('name','').startswith('type-example-')];assert len(gifs)==3
   last3=list(E.fromstring(z.read(new)).find('p:cSld/p:spTree',N))[-3:];assert all(E.QName(x).localname=='pic'for x in last3)
 for n in s.namelist():
  if n.startswith('ppt/media/'):assert z.read(n)==s.read(n)
 assert characters==[4,16,17,21]
renders=U/'renders/layout-assets-20261028';oldrender=U/'renders/character-sheets-20261028'
for page in range(1,22):
 if page not in[15,17,21]:assert ImageChops.difference(Image.open(renders/f'slide-{page:02}.png'),Image.open(oldrender/f'slide-{page:02}.png')).getbbox()is None,page
assert len(fitz.open(APP.with_suffix('.pdf')))==21
body_issues={}
for key in['library','application']:
 issues=[]
 for t in json.loads((B/(key+'-text-bounds.json')).read_text(encoding='utf-8-sig')):
  if t['name']in['copyright-footer','copyright_footer']:continue
  if t['text_left']+t['text_width']>t['shape_left']+t['shape_width']+2 or t['text_top']+t['text_height']>t['shape_top']+t['shape_height']+2:issues.append([t['slide'],t['name']])
 assert not issues,issues;body_issues[key]=issues
for file,receipt in[(LIB,'library-validation-v3.json'),(APP,'application-validation-v16.json')]:assert sha(file)==json.loads((B/receipt).read_text())['finalSha256']
assert sha(R/'lesson.md')=='845e711e86e7017598b9f98ff43760d1cc485d9becbf29c0c27cc477feedc471'
ff=imageio_ffmpeg.get_ffmpeg_exe();video=B/'playback-reflow.mp4'
def frame(t,name):
 path=B/(name+'.png');subprocess.run([ff,'-y','-loglevel','error','-ss',str(t),'-i',str(video),'-frames:v','1',str(path)],check=True);return np.asarray(Image.open(path).convert('RGB')).astype(int)
vqa=[];a=frame(.04,'qa-time-a');b=frame(2.5,'qa-time-b')
for i in range(3):
 y=352+i*96;diff=np.max(abs(a[y:y+80,852:1092]-b[y:y+80,852:1092]),axis=2);count=int((diff>12).sum());assert count>40,(i,count);vqa.append({'page':15,'example':i+1,'sample_times':[.04,2.5],'changed_pixels':count})
a=frame(4.2,'qa-ref-a');b=frame(5.2,'qa-ref-b');count=int((np.max(abs(a[354:410,805:1105]-b[354:410,805:1105]),axis=2)>12).sum());assert count>40,count;vqa.append({'page':17,'native_animated_heading_changed_pixels':count})
report={'classified_source_pages':152,'reusable_native_layouts':20,'native_shapes_in_library':native_shapes,'library_native_table_pages':libtable,'library_only_bitmap':'original user-provided NotionTalk logo','webinar_slide_count':21,'changed_pages':[15,17,21],'18_other_slides_xml_and_pixels_unchanged':True,'all_original_media_tables_and_native_timing_preserved':True,'character_pose_pages_unchanged':characters,'native_playback':vqa,'body_overflow':body_issues,'source_PDFs_unchanged':True,'lesson_unchanged':True,'library_sha256':sha(LIB),'webinar_sha256':sha(APP),'new_native_layouts_not_original_page_rasters':True,'inherited_G10_status':'unchanged'}
check=U/'checks/layout-assets-20261028';check.mkdir(parents=True,exist_ok=True);(check/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
sheet=Image.new('RGB',(1600,1080),'#333333');d=ImageDraw.Draw(sheet)
for k in range(21):
 im=Image.open(renders/f'slide-{k+1:02}.png').convert('RGB');im.thumbnail((320,180));x=k%5*320;y=k//5*216;sheet.paste(im,(x,y));d.text((x+6,y+185),str(k+1),fill='white')
sheet.save(B/'application-contact-final.jpg',quality=92)
print(json.dumps(report,ensure_ascii=False,indent=2))
