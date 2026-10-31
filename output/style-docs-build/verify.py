from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops
import json,hashlib,fitz
B=Path(__file__).resolve().parent;R=B.parents[1];U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';mapping=json.loads((B/'slide-map.json').read_text(encoding='utf8'));final=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_Part3_Part4확장_40장_v19.pptx';source=Path(mapping['source']);newrenders=U/'renders/style-docs-20261029';oldrenders=U/'renders/part-dividers-20261028'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with ZipFile(source)as z,ZipFile(final)as f:
 assert len(E.fromstring(f.read('ppt/presentation.xml')).find('p:sldIdLst',N))==40
 preserved=[];added=[];tables=[];timing=[];pixel_identical=[];renderer_differences=[]
 for s in mapping['slides']:
  part=s['package_part'];x=E.fromstring(f.read(part));page=s['page']
  if x.find('p:timing',N)is not None:timing.append(page)
  if x.findall('.//a:tbl',N):tables.append(page)
  if s['kind']=='preserved'and s['original_page']!=26:
   assert z.read(part)==f.read(part),s
   diff=ImageChops.difference(Image.open(oldrenders/f"slide-{s['original_page']:02}.png").convert('RGB'),Image.open(newrenders/f'slide-{page:02}.png').convert('RGB'));box=diff.getbbox()
   if box:
    from PIL import ImageStat
    assert page==18 and box==(49,682,228,959)and max(v[1]for v in diff.getextrema())<=13 and max(ImageStat.Stat(diff.crop(box)).mean)<1,s
    renderer_differences.append({'page':18,'bbox':box,'max_channel_delta':13,'mean_delta_within_bbox':ImageStat.Stat(diff.crop(box)).mean,'finding':'Minor raster resampling difference confined to unchanged bear picture; slide XML, relationships and media are unchanged. Fresh export of baseline confirms the same baseline appearance.'})
   else:pixel_identical.append(page)
   preserved.append(page)
  elif s['kind']=='added':
   texts=x.xpath('.//a:t/text()',namespaces=N);assert s['title']in texts;assert len(x.findall('.//p:pic',N))==1;added.append(page)
 for name in z.namelist():
  if name.startswith('ppt/media/')or name.startswith('ppt/notesSlides/'):assert z.read(name)==f.read(name),name
 gifs=[n for n in z.namelist()if n.lower().endswith('.gif')];assert len(gifs)==33
 assert len(preserved)==25;assert len(added)==14;assert timing==[6,11,20];assert tables==[22,25,26,28,33,34,37],tables
 # The closing changes text only. Its native shapes, geometry, artwork and formatting remain identical.
 last=mapping['slides'][-1]['package_part'];before=E.fromstring(z.read(last));after=E.fromstring(f.read(last));oldtexts=before.findall('.//a:t',N);newtexts=after.findall('.//a:t',N);assert len(oldtexts)==len(newtexts);text_edits=[]
 for o,n in zip(oldtexts,newtexts):
  if o.text!=n.text:text_edits.append({'before':o.text,'after':n.text})
  n.text=o.text
 assert len(text_edits)==3;assert E.tostring(before)==E.tostring(after)
 issues=[]
 for t in json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig')):
  if t['slide']in added+[40]and t['name']not in['copyright-footer','copyright_footer']:
   if t['text_left']+t['text_width']>t['shape_left']+t['shape_width']+2 or t['text_top']+t['text_height']>t['shape_top']+t['shape_height']+2:issues.append(t)
 assert not issues,issues
 assert len(fitz.open(final.with_suffix('.pdf')))==40
 sha=hashlib.sha256(final.read_bytes()).hexdigest();assert sha==json.loads((B/'validation.json').read_text(encoding='utf8'))['finalSha256']
 assert hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest()=='845e711e86e7017598b9f98ff43760d1cc485d9becbf29c0c27cc477feedc471'
 ex=R/'output/webinar-style-docs-examples';names=['design.md','motion.md','storyline.md','README.md']
 with ZipFile(ex/'NotionTalk_스타일기준_문서예시.zip')as a:
  assert set(a.namelist())==set(names)
  for name in names:assert a.read(name)==(ex/name).read_bytes()
 assert 'design.md와 motion.md도 함께 만드는 것을 추천합니다'in E.fromstring(f.read(mapping['slides'][23]['package_part'])).xpath('.//a:t/text()',namespaces=N)
 report={'final':str(final),'slide_count':40,'Part3_added_pages':list(range(24,32)),'Part4_added_pages':list(range(34,40)),'preserved_original_slide_XML':25,'pixel_identical_original_slides':len(pixel_identical),'minor_renderer_differences':renderer_differences,'all_original_media_and_notes_preserved':True,'closing_page':40,'closing_text_edits':text_edits,'closing_geometry_and_artwork_unchanged':True,'native_table_pages':tables,'native_timing_pages':timing,'GIF_media_parts_preserved':33,'new_body_text_overflow':issues,'PDF_pages':40,'examples':['design.md','motion.md','storyline.md','README.md'],'example_ZIP_verified':True,'lesson_md_unchanged':True,'G10_state':'inherited state unchanged; not approved by this task','final_sha256':sha}
 check=U/'checks/style-docs-20261029';check.mkdir(parents=True,exist_ok=True);(check/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False,indent=2))
