from pathlib import Path
from zipfile import ZipFile
import fitz,json,hashlib
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';O=R/'output/webinar-knowledge-only'
old=O/'NotionTalk_모션그래픽_챌린지11월2일시작_41장_v25.pptx';new=O/'NotionTalk_모션그래픽_사이클활동안내_43장_v26.pptx'
spec=json.loads((B/'slide-map.json').read_text(encoding='utf-8'))
with ZipFile(old)as a,ZipFile(new)as b:
 for p in spec['source_parts']:assert a.read(p)==b.read(p)
 for n in a.namelist():
  if n.startswith(('ppt/media/','ppt/notesSlides/')):assert a.read(n)==b.read(n)
pdf0,pdf1=fitz.open(old.with_suffix('.pdf')),fitz.open(new.with_suffix('.pdf'));assert len(pdf1)==43
for i in range(41):assert pdf0[i].get_pixmap().samples==pdf1[i].get_pixmap().samples,f'Unexpected change {i+1}'
for n in (42,43):pdf1[n-1].get_pixmap(matrix=fitz.Matrix(2,2)).save(B/f'after-{n}.png')
assert '11/2' in pdf1[41].get_text() and '11/8' in pdf1[41].get_text()
assert all(x in pdf1[42].get_text() for x in ['motion.md','video.md','11/9','11/15'])
result={'count':43,'added':[42,43],'original_41_slides_xml_and_pdf_pixels_unchanged':True,'original_media_notes_unchanged':True,'pptx_sha256':hashlib.sha256(new.read_bytes()).hexdigest()}
check=U/'checks/challenge-activities-20261030';check.mkdir(parents=True,exist_ok=True);(check/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result))
