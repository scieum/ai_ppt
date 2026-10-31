from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import fitz,datetime,json,hashlib,shutil
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';O=R/'output/webinar-knowledge-only'
old='NotionTalk_모션그래픽_챌린지일정추가_41장_v24';new='NotionTalk_모션그래픽_챌린지11월2일시작_41장_v25'
spec=json.loads((B/'slide-map.json').read_text(encoding='utf-8'))
with ZipFile(O/(old+'.pptx'))as a,ZipFile(O/(new+'.pptx'))as b:
 for p in spec['source_parts'][:40]:assert a.read(p)==b.read(p)
 for n in a.namelist():
  if n.startswith('ppt/media/'):assert a.read(n)==b.read(n)
 root=E.fromstring(b.read(spec['source_parts'][40]));texts={}
 for sp in root.xpath('//*[local-name()="sp"]'):
  names=sp.xpath('.//*[local-name()="cNvPr"]/@name')
  if names:texts[names[0]]=''.join(sp.xpath('.//*[local-name()="t"]/text()'))
 assert [texts[f'weekday-{i}']for i in range(7)]==list('월화수목금토일')
 assert [texts[f'date-{i}']for i in range(2,16)]==['11/2']+[str(i)for i in range(3,16)]
p0,p1=fitz.open(O/(old+'.pdf')),fitz.open(O/(new+'.pdf'));assert len(p1)==41
for i in range(40):assert p0[i].get_pixmap().samples==p1[i].get_pixmap().samples
p1[40].get_pixmap(matrix=fitz.Matrix(2,2)).save(B/'calendar-final.png')
assert datetime.date(2026,11,2).weekday()==0 and datetime.date(2026,11,15).weekday()==6
result={'count':41,'changed_page':41,'first_40_xml_and_pdf_pixels_unchanged':True,'all_media_unchanged':True,'cycle_1':['2026-11-02','2026-11-08'],'cycle_2':['2026-11-09','2026-11-15'],'week_starts':'Monday','14_calendar_cells_verified':True,'pptx_sha256':hashlib.sha256((O/(new+'.pptx')).read_bytes()).hexdigest()}
check=U/'checks/challenge-date-fix-20261030';check.mkdir(parents=True,exist_ok=True);(check/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
H=U/'history/challenge-date-fix-20261030'
files=[R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md',U/'part-4.md',U/'follow-up-challenge.md']
for p in files:
 backup=H/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(p,backup)
 s=p.read_text(encoding='utf-8-sig')
 # Correct only the current section; older records stay historical.
 first,sep,rest=s.partition('\n## ')
 for x,y in [(old,new),('2026-10-29','2026-10-30'),('11월 1일(일)','11월 2일(월)'),('11월 7일(토)','11월 8일(일)'),('11월 8일(일)~11월 14일(토)','11월 9일(월)~11월 15일(일)'),('11월 1일~11월 14일','11월 2일~11월 15일'),('11월 14일(토)','11월 15일(일)'),('일~토 7열','월~일 7열'),('checks/challenge-calendar-20261029','checks/challenge-date-fix-20261030'),('renders/challenge-calendar-20261029','renders/challenge-date-fix-20261030')]:first=first.replace(x,y)
 if p.name=='follow-up-challenge.md':first=first.replace('| 2차 사이클 | 11월 8일(일) |','| 2차 사이클 | 11월 9일(월) |')
 first=first.replace('## 최신 후속 챌린지 캘린더','## 최신 후속 챌린지 시작일 정정')
 first+='\n\n사용자 정정: 1차 사이클은 11월 2일 시작이며, 2차는 11월 9일 시작한다. 캘린더 요일은 월요일부터 일요일까지다. 이전 11월 1일 시작 일정은 폐기한다.\n'
 p.write_text(first+(sep+rest if sep else ''),encoding='utf-8')
print(json.dumps(result))
