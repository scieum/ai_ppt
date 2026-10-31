from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops,ImageDraw
import json,hashlib,posixpath,subprocess
import numpy as np,fitz,imageio_ffmpeg
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1];O=R/'output/webinar-knowledge-only';F=O/'NotionTalk_모션그래픽_톤과움직임확장_21장_v13.pptx';S=O/'NotionTalk_모션그래픽_준비물복원_17장_v11.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def ordered(z):
 rel=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'));paths={x.get('Id'):x.get('Target').lstrip('/') if x.get('Target').startswith('/') else posixpath.normpath(posixpath.join('ppt',x.get('Target')))for x in rel}
 return [paths[x.get('{'+N['r']+'}id')]for x in E.fromstring(z.read('ppt/presentation.xml')).findall('p:sldIdLst/p:sldId',N)]
order=[1,2,3,4,5,6,None,None,7,8,9,10,None,None,11,12,13,14,15,16,17];specs=json.loads((B/'edits.json').read_text(encoding='utf-8'))
with ZipFile(F)as final,ZipFile(S)as source:
 parts=ordered(final);old=ordered(source);assert len(parts)==21
 for page,original in enumerate(order,1):
  if original:assert final.read(parts[page-1])==source.read(old[original-1])
 for name in source.namelist():
  if name.startswith('ppt/media/'):assert final.read(name)==source.read(name)
 for spec in specs:
  root=E.fromstring(final.read(parts[spec['page']-1]));shapes={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in root.findall('.//p:sp',N)}
  for name,value in spec['edits'].items():assert ''.join(shapes[name].xpath('.//a:t/text()',namespaces=N))==value,(spec['page'],name)
  assert len([x for x in root.findall('.//p:pic',N)if x.find('p:nvPicPr/p:cNvPr',N).get('name','').startswith('tone-demo-')])==3
 media=[final.read(n)for n in final.namelist()if n.startswith('ppt/media/')]
 for path in (U/'assets/video-tones-20261028').glob('*.gif'):assert path.read_bytes() in media
 tablepages=[p+1 for p,part in enumerate(parts)if E.fromstring(final.read(part)).find('.//a:tbl',N)is not None];assert tablepages==[18,20]
render=U/'renders/video-tones-20261028';previous=U/'renders/restore-preparation-20261028'
for page,original in enumerate(order,1):
 if original:assert ImageChops.difference(Image.open(render/f'slide-{page:02}.png'),Image.open(previous/f'slide-{original:02}.png')).getbbox()is None,(page,original)
assert len(fitz.open(F.with_suffix('.pdf')))==21
bounds=json.loads((render/'text-bounds.json').read_text(encoding='utf-8-sig'));issues=[]
for t in bounds:
 if t['slide'] in [7,8,13,14] and t['name']!='copyright_footer':
  dx=t['text_left']+t['text_width']-t['shape_left']-t['shape_width'];dy=t['text_top']+t['text_height']-t['shape_top']-t['shape_height']
  if dx>2 or dy>2:issues.append([t['slide'],t['name'],dx,dy])
assert not issues,issues
receipt=json.loads((B/'validation-v13.json').read_text());sha=hashlib.sha256(F.read_bytes()).hexdigest();assert receipt['finalSha256']==sha
assert hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest()=='845e711e86e7017598b9f98ff43760d1cc485d9becbf29c0c27cc477feedc471'
ff=imageio_ffmpeg.get_ffmpeg_exe();video=B/'playback-reflow.mp4'
def frame(t,name):
 path=B/(name+'.png');subprocess.run([ff,'-y','-loglevel','error','-ss',str(t),'-i',str(video),'-frames:v','1',str(path)],check=True);return np.asarray(Image.open(path).convert('RGB')).astype(int)
playback=[]
for index,page in enumerate([7,8,13,14]):
 a=frame(index*4+.3,f'qa-{page}-a');b=frame(index*4+1.3,f'qa-{page}-b')
 for card in range(3):
  x=196+320*card;region=np.max(abs(a[451:590,x:x+248]-b[451:590,x:x+248]),axis=2);count=int((region>12).sum());assert count>100,(page,card,count);playback.append({'page':page,'example':card+1,'changed_pixels':count})
report={'slides':21,'pdf_pages':21,'new_pages':[7,8,13,14],'new_animated_examples':12,'all_prior_17_slides_xml_media_and_native_pixels_unchanged':True,'all_new_literal_text_verified':True,'new_body_text_overflow':issues,'native_table_pages':tablepages,'native_playback_all_12_examples_changed':playback,'lesson_unchanged':True,'finalizer_pass':True,'final_sha256':sha,'source_basis':'metadata, description and all 199 Korean caption segments; no source video footage/audio reused','inherited_G10_status':'unchanged'}
checks=U/'checks/video-tones-20261028';checks.mkdir(parents=True,exist_ok=True);(checks/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
sheet=Image.new('RGB',(1600,1080),'#333333');d=ImageDraw.Draw(sheet)
for k in range(21):
 im=Image.open(render/f'slide-{k+1:02}.png').convert('RGB');im.thumbnail((320,180));x=k%5*320;y=k//5*216;sheet.paste(im,(x,y));d.text((x+6,y+185),str(k+1),fill='white')
sheet.save(B/'contact-sheet.jpg',quality=92)
print(json.dumps(report,ensure_ascii=False,indent=2))
