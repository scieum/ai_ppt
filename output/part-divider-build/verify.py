from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops
import json,hashlib,fitz,posixpath
B=Path(__file__).resolve().parent;R=B.parents[1];U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';M=json.loads((B/'slide-map.json').read_text(encoding='utf8'))
source=Path(M['source']);final=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_파트구분_26장_v18.pptx';newrenders=U/'renders/part-dividers-20261028';oldrenders=U/'renders/agenda-fix-20261028'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with ZipFile(source)as z,ZipFile(final)as f:
 assert len(E.fromstring(f.read('ppt/presentation.xml')).find('p:sldIdLst',N))==26
 preserved=[];dividers=[]
 for s in M['slides']:
  part=s['package_part'];x=E.fromstring(f.read(part))
  if s['kind']=='preserved':
   assert z.read(part)==f.read(part)
   assert ImageChops.difference(Image.open(oldrenders/f"slide-{s['original_page']:02}.png").convert('RGB'),Image.open(newrenders/f"slide-{s['page']:02}.png").convert('RGB')).getbbox()is None,s
   preserved.append(s['page'])
  else:
   texts=x.xpath('.//a:t/text()',namespaces=N);assert 'Part '+str(s['part'])in texts;assert len(x.findall('.//p:pic',N))==1
   assert any('NotionTalk. All rights reserved.'in t for t in texts)
   assert not any('['in t or 'L03'in t for t in texts)
   dividers.append(s['page'])
 for p in z.namelist():
  if p.startswith('ppt/media/')or p.startswith('ppt/notesSlides/'):assert z.read(p)==f.read(p),p
 gifs=[p for p in z.namelist()if p.lower().endswith('.gif')];assert len(gifs)==33
 timing=[s['page']for s in M['slides']if E.fromstring(f.read(s['package_part'])).find('p:timing',N)is not None];assert timing==[6,11,20],timing
 issues=[]
 for t in json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig')):
  if t['slide']in dividers and t['name']!='copyright-footer':
   if t['text_left']+t['text_width']>t['shape_left']+t['shape_width']+2 or t['text_top']+t['text_height']>t['shape_top']+t['shape_height']+2:issues.append(t)
 assert not issues,issues
 assert len(fitz.open(final.with_suffix('.pdf')))==26
 receipt=json.loads((B/'validation.json').read_text(encoding='utf8'));sha=hashlib.sha256(final.read_bytes()).hexdigest();assert sha==receipt['finalSha256']
 research=U/'research/youtube-top10-20261028';selection=json.loads((research/'selection.json').read_text(encoding='utf8'));assert len(selection['selected'])==10;assert selection['candidate_count']==158
 for e in selection['selected']:
  assert hashlib.sha256((research/'captions'/(e['id']+'.json3')).read_bytes()).hexdigest()==e['caption_sha256']
  assert e['caption_segments']>0
 assert hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest()=='845e711e86e7017598b9f98ff43760d1cc485d9becbf29c0c27cc477feedc471'
 report={'final':str(final),'slide_count':26,'added_divider_pages':dividers,'original_slide_count':21,'all_original_slide_XML_notes_media_unchanged':True,'all_original_slides_pixel_identical':True,'GIF_parts_preserved':len(gifs),'native_timing_pages':timing,'new_slide_body_overflow':issues,'PDF_pages':26,'research_candidates':158,'research_selected':10,'selected_caption_segments':sum(x['caption_segments']for x in selection['selected']),'lesson_md_unchanged':True,'G10_inherited_state':'unchanged, not approved by this task','final_sha256':sha}
 check=U/'checks/part-dividers-20261028';check.mkdir(parents=True,exist_ok=True);(check/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False,indent=2))
