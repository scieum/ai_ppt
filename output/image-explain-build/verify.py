from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,hashlib,fitz,posixpath
B=Path(__file__).resolve().parent;R=B.parents[1];U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';M=json.loads((B/'slide-map.json').read_text(encoding='utf8'));source=Path(M['source']);final=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_이미지설명강화_40장_v21.pptx';changed={24,30,38}
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};return[(rs[x.get('{'+N['r']+'}id')].lstrip('/')if rs[x.get('{'+N['r']+'}id')].startswith('/')else posixpath.normpath('ppt/'+rs[x.get('{'+N['r']+'}id')]))for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
with ZipFile(source)as z,ZipFile(final)as f:
 old=ordered(z);new=ordered(f);assert old==new and len(new)==40
 for i,name in enumerate(new,1):
  if i not in changed:assert z.read(name)==f.read(name)
 for name in z.namelist():
  if name.startswith('ppt/media/'):assert z.read(name)==f.read(name)
 assert len([n for n in z.namelist()if n.endswith('.gif')])==33
 tables=[];timing=[]
 for i,name in enumerate(new,1):
  x=E.fromstring(f.read(name));texts=x.xpath('.//a:t/text()',namespaces=N)
  if x.findall('.//a:tbl',N):tables.append(i)
  if x.find('p:timing',N)is not None:timing.append(i)
  if i in changed:assert len(x.findall('.//p:pic',N))==2
 assert tables==[22,25,33,34]and timing==[6,11,20]
sha=hashlib.sha256(final.read_bytes()).hexdigest();assert sha==json.loads((B/'final-validation-complete.json').read_text(encoding='utf8'))['finalSha256']
pdf=fitz.open(final.with_suffix('.pdf'));previous=fitz.open(source.with_suffix('.pdf'));assert len(pdf)==40
same=[];diff=[];render=U/'renders/image-explain-20261029/pdf';render.mkdir(parents=True,exist_ok=True)
for i in range(40):
 if i+1 in changed:pdf[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(str(render/f'slide-{i+1:02}.png'))
 else:
  a=previous[i].get_pixmap(matrix=fitz.Matrix(1,1));b=pdf[i].get_pixmap(matrix=fitz.Matrix(1,1));(same if a.samples==b.samples else diff).append(i+1)
assert len(same)==37 and not diff
issues=[]
for t in json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig')):
 if t['slide']in changed and t['name']!='copyright-footer'and(t['text_left']+t['text_width']>t['shape_left']+t['shape_width']+2 or t['text_top']+t['text_height']>t['shape_top']+t['shape_height']+2):issues.append(t)
assert not issues
assert hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest()=='845e711e86e7017598b9f98ff43760d1cc485d9becbf29c0c27cc477feedc471'
report={'final':str(final),'sha256':sha,'pages':40,'image_led_pages':sorted(changed),'unchanged_slides_XML_and_PDF_pixels':37,'all_existing_media_preserved':True,'GIF_parts':33,'native_timing_pages':timing,'native_table_pages':tables,'text_overflow':issues,'generated_assets':['consistent-tone.png','still-and-sequence.png','local-and-shared.png'],'notes_updated':True,'lesson_md_unchanged':True,'G10':'inherited state unchanged; no legal clearance fabricated'}
check=U/'checks/image-explain-20261029';check.mkdir(parents=True,exist_ok=True);(check/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False,indent=2))
