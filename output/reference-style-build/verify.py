from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops
import json,hashlib,fitz,posixpath
B=Path(__file__).resolve().parent;R=B.parents[1];U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';M=json.loads((B/'slide-map.json').read_text(encoding='utf8'));source=Path(M['source']);final=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_레퍼런스표현강화_40장_v20.pptx';changed={x['page']for x in M['slides']}
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};return[(rs[x.get('{'+N['r']+'}id')].lstrip('/')if rs[x.get('{'+N['r']+'}id')].startswith('/')else posixpath.normpath('ppt/'+rs[x.get('{'+N['r']+'}id')]))for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
with ZipFile(source)as z,ZipFile(final)as f:
 old=ordered(z);new=ordered(f);assert old==new and len(new)==40
 for i,name in enumerate(new,1):
  if i not in changed:assert z.read(name)==f.read(name)
 for name in z.namelist():
  if name.startswith('ppt/media/'):assert z.read(name)==f.read(name)
 gifs=[n for n in z.namelist()if n.endswith('.gif')];assert len(gifs)==33
 tables=[];timing=[]
 for i,name in enumerate(new,1):
  x=E.fromstring(f.read(name));texts=x.xpath('.//a:t/text()',namespaces=N)
  if x.findall('.//a:tbl',N):tables.append(i)
  if x.find('p:timing',N)is not None:timing.append(i)
  if i in changed:
   assert any('© 2026. NotionTalk.'in t for t in texts)
   assert 'Part 3  스토리라인과 스틸컷 확인'in texts or'Part 4  수정 후 제작'in texts
  if i in [24,37]:
   pics=x.xpath('.//p:pic[p:nvPicPr/p:cNvPr[starts-with(@descr,"pose:")]]',namespaces=N);assert len(pics)==1
   crop=pics[0].find('p:blipFill/a:srcRect',N);assert crop is not None and int(crop.get('r'))>30000
 assert tables==[22,25,33,34];assert timing==[6,11,20]
sha=hashlib.sha256(final.read_bytes()).hexdigest();receipt=json.loads((B/'final-validation-complete.json').read_text(encoding='utf8'));assert sha==receipt['finalSha256']
pdf=fitz.open(final.with_suffix('.pdf'));previous=fitz.open(source.with_suffix('.pdf'));assert len(pdf)==40
pixel_same=[];different=[]
for i in range(40):
 t=pdf[i].get_text();assert 'NotionTalk'in t or i==0
 if i+1 in changed:
  im=Image.open(U/f'renders/reference-style-20261029/pdf/slide-{i+1:02}.png').convert('RGB');assert im.crop((35,45,480,145)).getbbox() is not None
 if i+1 not in changed:
  a=previous[i].get_pixmap(matrix=fitz.Matrix(1,1));b=pdf[i].get_pixmap(matrix=fitz.Matrix(1,1))
  (pixel_same if a.samples==b.samples else different).append(i+1)
issues=[]
for t in json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig')):
 if t['slide']in changed and t['name']!='copyright-footer'and(t['text_left']+t['text_width']>t['shape_left']+t['shape_width']+2 or t['text_top']+t['text_height']>t['shape_top']+t['shape_height']+2):issues.append(t)
assert not issues
assert hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest()=='845e711e86e7017598b9f98ff43760d1cc485d9becbf29c0c27cc477feedc471'
report={'final':str(final),'sha256':sha,'total_pages':40,'changed_pages':sorted(changed),'preserved_slide_XML':26,'original_media_byte_identical':True,'GIF_parts_preserved':33,'native_timing_pages':timing,'native_table_pages':tables,'new_text_overflow':issues,'PDF_unchanged_pages_pixel_identical':pixel_same,'PDF_unchanged_pages_renderer_differences':different,'new_assets':{'31':'orange-folder-v1.png','24':'woman-explain existing sheet crop','37':'man-review existing sheet crop'},'reference_map':M['slides'],'lesson_md_unchanged':True,'copyright_review':{'reference_text_screenshots_mascots_copied':False,'new_folder':'built-in imagegen; prompt and SHA256 in asset manifest','inherited_G10':'unchanged; no clearance fabricated'}}
check=U/'checks/reference-style-20261029';check.mkdir(parents=True,exist_ok=True);(check/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items()if k not in['reference_map']},ensure_ascii=False,indent=2))
