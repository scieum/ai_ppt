from pathlib import Path
from zipfile import ZipFile
import json,fitz,hashlib,datetime
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';O=R/'output/webinar-knowledge-only'
old=O/'NotionTalk_모션그래픽_표디자인정리_40장_v22.pptx';new=O/'NotionTalk_모션그래픽_챌린지일정추가_41장_v24.pptx'
spec=json.loads((B/'slide-map.json').read_text(encoding='utf-8'))
with ZipFile(old)as a,ZipFile(new)as b:
 for part in spec['source_parts']:assert a.read(part)==b.read(part)
 for n in a.namelist():
  if n.startswith(('ppt/media/','ppt/notesSlides/')):assert a.read(n)==b.read(n)
pdf0,pdf1=fitz.open(old.with_suffix('.pdf')),fitz.open(new.with_suffix('.pdf'));assert len(pdf1)==41
for i in range(40):assert pdf0[i].get_pixmap().samples==pdf1[i].get_pixmap().samples,f'Unexpected change {i+1}'
pdf1[40].get_pixmap(matrix=fitz.Matrix(2,2)).save(B/'calendar-final.png')
assert all(x in ''.join(pdf1[40].get_text().split()) for x in ['1차사이클','2차사이클','11/1','14'])
start=datetime.date(2026,11,1);dates=[start+datetime.timedelta(days=i)for i in range(14)]
assert dates[0].weekday()==6 and dates[6].weekday()==5 and dates[7].weekday()==6 and dates[13]==datetime.date(2026,11,14)
result={'slides':41,'added':41,'original_40_slides_xml_and_pdf_pixels_unchanged':True,'original_media_and_notes_unchanged':True,'cycle_1':['2026-11-01','2026-11-07'],'cycle_2':['2026-11-08','2026-11-14'],'calendar_days_verified':14,'references':['R01 page 99','R03 page 42'],'pptx_sha256':hashlib.sha256(new.read_bytes()).hexdigest()}
check=U/'checks/challenge-calendar-20261029';check.mkdir(parents=True,exist_ok=True);(check/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result))
