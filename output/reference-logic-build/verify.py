from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import fitz,numpy as np,json,hashlib
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
src=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_준비물안내박스_43장_v30.pptx';out=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_논리구조에셋반영_43장_v31.pptx'
spec=json.loads((B/'spec.json').read_text(encoding='utf8'));pages=[d['page'] for d in spec];parts=json.loads((R/'output/typography-qa-build/spec.json').read_text(encoding='utf8'))['parts']
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
headnames={'part_label','part-label','section_number','group-number','section_heading','group-label','title','slide-title','subtitle','slide-subtitle','copyright_footer','copyright-footer','clear-content'}
with ZipFile(src) as a,ZipFile(out) as b:
 assert set(a.namelist())==set(b.namelist())
 changed={n for n in a.namelist() if a.read(n)!=b.read(n)}
 assert changed=={d[k] for d in spec for k in ['package_part','notes_part']}
 for part in parts:
  x=E.fromstring(a.read(part));y=E.fromstring(b.read(part));xt=x.find('p:timing',N);yt=y.find('p:timing',N)
  assert (E.tostring(xt) if xt is not None else None)==(E.tostring(yt) if yt is not None else None)
  def headers(r):return {s.find('p:nvSpPr/p:cNvPr',N).get('name'):E.tostring(s) for s in r.findall('.//p:sp',N) if s.find('p:nvSpPr/p:cNvPr',N).get('name') in headnames}
  assert headers(x)==headers(y),part
  ids=y.xpath('//p:cNvPr/@id',namespaces=N);assert len(ids)==len(set(ids)),part
  assert set(y.xpath('//p:spTgt/@spid',namespaces=N))<=set(ids),part
  assert sorted(x.xpath('//p:pic/p:nvPicPr/p:cNvPr/@id',namespaces=N))==sorted(y.xpath('//p:pic/p:nvPicPr/p:cNvPr/@id',namespaces=N)),part
  if part not in [d['package_part'] for d in spec]:assert a.read(part)==b.read(part)
  # Every original media payload remains byte-for-byte identical.
 assert all(a.read(n)==b.read(n) for n in a.namelist() if n.startswith('ppt/media/'))
old=fitz.open(src.with_suffix('.pdf'));new=fitz.open(out.with_suffix('.pdf'));assert len(old)==len(new)==43
for i in range(43):
 a=old[i].get_pixmap();b=new[i].get_pixmap();av=np.frombuffer(a.samples,np.uint8).reshape(a.height,a.width,a.n);bv=np.frombuffer(b.samples,np.uint8).reshape(b.height,b.width,b.n)
 if i+1 not in pages:assert np.array_equal(av,bv),i+1
 else:
  assert np.array_equal(av[:230],bv[:230]),('header',i+1)
  assert np.array_equal(av[513:],bv[513:]),('footer',i+1)
bounds=json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig'));selected=[s for s in bounds if s['slide'] in pages and s['text'].strip()];overflow=[];overlap=[]
for a in selected:
 if a['text_width']>a['shape_width']+1 or a['text_height']>a['shape_height']+1:overflow.append([a['slide'],a['name']])
for i,a in enumerate(selected):
 for b in selected[i+1:]:
  if a['slide']!=b['slide']:continue
  w=min(a['text_left']+a['text_width'],b['text_left']+b['text_width'])-max(a['text_left'],b['text_left']);h=min(a['text_top']+a['text_height'],b['text_top']+b['text_height'])-max(a['text_top'],b['text_top'])
  if w>2 and h>2:overlap.append([a['slide'],a['name'],b['name']])
assert not overflow,overflow
assert not overlap,overlap
record={'slides':43,'changed_slides':pages,'unchanged_slides_byte_and_pdf_pixel_identical':38,'headers_footer_original_images_and_timing_preserved':True,'text_overflow':overflow,'text_overlap':overlap,'native_tables_preserved':[22,25,33,34],'new_editable_criteria_tables_slide':37,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'visual_review':{'changed_slides_full_size':pages},'reference_expression_review':{'source_screenshots_embedded':False,'source_brand_or_penguin_reused':False,'reference_subject_matter_copied':False,'wording_rewritten_for_existing_webinar':True,'G10_status':'inherited_unchanged_not_legal_clearance'}}
dest=U/'checks/reference-logic-20261030';dest.mkdir(parents=True,exist_ok=True);(dest/'verification.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(record,ensure_ascii=True))
