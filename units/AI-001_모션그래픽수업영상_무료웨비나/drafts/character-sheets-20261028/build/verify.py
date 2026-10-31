from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops,ImageDraw
import json,hashlib,posixpath,fitz
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1];O=R/'output/webinar-knowledge-only';F=O/'NotionTalk_모션그래픽_캐릭터시트적용_21장_v14.pptx';S=O/'NotionTalk_모션그래픽_톤과움직임확장_21장_v13.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def ordered(z):
 rel=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'));paths={x.get('Id'):x.get('Target').lstrip('/') if x.get('Target').startswith('/')else posixpath.normpath(posixpath.join('ppt',x.get('Target')))for x in rel};return [paths[x.get('{'+N['r']+'}id')]for x in E.fromstring(z.read('ppt/presentation.xml')).findall('p:sldIdLst/p:sldId',N)]
def serial(x):return E.tostring(x)if x is not None else None
changed=[4,6,16,17,18,19,21];used=[];oldcount=0;gifs=0
specs=json.loads((B/'edits.json').read_text(encoding='utf-8'))
with ZipFile(F)as z,ZipFile(S)as s:
 final=ordered(z);source=ordered(s);assert len(final)==len(source)==21
 for n,(fp,sp) in enumerate(zip(final,source),1):
  a=E.fromstring(z.read(fp));b=E.fromstring(s.read(sp));assert a.xpath('.//a:t/text()',namespaces=N)==b.xpath('.//a:t/text()',namespaces=N),n
  assert serial(a.find('p:timing',N))==serial(b.find('p:timing',N)),n
  assert [serial(x)for x in a.findall('.//a:tbl',N)]==[serial(x)for x in b.findall('.//a:tbl',N)]
  if n not in changed:assert z.read(fp)==s.read(sp),n
  oldcount+=sum(x.find('p:nvPicPr/p:cNvPr',N).get('name','').startswith('mascot-')for x in b.findall('.//p:pic',N))
  assert not any(x.find('p:nvPicPr/p:cNvPr',N).get('name','').startswith('mascot-')for x in a.findall('.//p:pic',N)),n
  for pic in a.findall('.//p:pic',N):
   name=pic.find('p:nvPicPr/p:cNvPr',N).get('name','')
   if name.startswith('character-pose-'):
    im=next(x['images'][0]for x in specs if x['page']==n);rect=pic.find('p:blipFill/a:srcRect',N);assert all(int(rect.get(k))==round(im['crop'][v]*100000)for k,v in [('l','left'),('t','top'),('r','right'),('b','bottom')]);used.append({'page':n,'pose':im['id'],'crop':dict(rect.attrib)})
 for path in s.namelist():
  if path.endswith('.gif'):assert z.read(path)==s.read(path);gifs+=1
 media=[z.read(n)for n in z.namelist()if n.startswith('ppt/media/')]
 for path in (U/'assets/character-sheets-20261028').glob('*.png'):assert path.read_bytes()in media
assert [x['page']for x in used]==[4,16,17,21]
render=U/'renders/character-sheets-20261028';prior=U/'renders/video-tones-20261028'
for n in range(1,22):
 if n not in changed:assert ImageChops.difference(Image.open(render/f'slide-{n:02}.png'),Image.open(prior/f'slide-{n:02}.png')).getbbox()is None,n
assert len(fitz.open(F.with_suffix('.pdf')))==21
poses=json.loads((U/'assets/character-sheets-20261028/poses.json').read_text(encoding='utf-8'));assert len(poses)==9
for path in (U/'assets/character-sheets-20261028').glob('*.png'):
 im=Image.open(path);assert im.mode=='RGBA'and im.getchannel('A').getextrema()==(0,255)
bounds=json.loads((render/'text-bounds.json').read_text(encoding='utf-8-sig'));issues=[]
for t in bounds:
 if t['name']!='copyright_footer'and(t['text_left']+t['text_width']>t['shape_left']+t['shape_width']+2 or t['text_top']+t['text_height']>t['shape_top']+t['shape_height']+2):issues.append([t['slide'],t['name']])
assert not issues,issues
receipt=json.loads((B/'validation-v14.json').read_text());sha=hashlib.sha256(F.read_bytes()).hexdigest();assert receipt['finalSha256']==sha
assert hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest()=='845e711e86e7017598b9f98ff43760d1cc485d9becbf29c0c27cc477feedc471'
report={'slides':21,'pdf_pages':21,'sheet_count':3,'pose_count':9,'old_body_character_instances':oldcount,'new_body_character_instances':len(used),'used':used,'all_21_slides_visible_text_tables_and_timing_preserved':True,'all_original_gif_parts_unchanged':gifs,'14_unmodified_slides_pixel_identical':True,'all_sheet_png_bytes_embedded_unchanged':True,'native_transparent_crops_verified':True,'body_text_overflow':issues,'lesson_unchanged':True,'finalizer_pass':True,'final_sha256':sha,'new_assets_rights_record':'user-owned character references, built-in generated pose sheets; inherited G10 status unchanged'}
check=U/'checks/character-sheets-20261028';check.mkdir(parents=True,exist_ok=True);(check/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
sheet=Image.new('RGB',(1600,1080),'#333333');draw=ImageDraw.Draw(sheet)
for k in range(21):
 im=Image.open(render/f'slide-{k+1:02}.png').convert('RGB');im.thumbnail((320,180));x=k%5*320;y=k//5*216;sheet.paste(im,(x,y));draw.text((x+6,y+185),str(k+1),fill='white')
sheet.save(B/'contact-sheet.jpg',quality=92)
print(json.dumps(report,ensure_ascii=False,indent=2))
