from pathlib import Path
from PIL import Image,ImageChops
from pypdf import PdfReader
import zipfile,json,xml.etree.ElementTree as ET,shutil,re
B=Path(__file__).resolve().parent;U=B.parents[2];ROOT=U.parents[1]
OUT=ROOT/'output/webinar-part01-added'
OLD=OUT/'NotionTalk_대표5장유지_Part0_Part1추가_9장_v1.pptx'
NEW=OUT/'NotionTalk_대표5장유지_Part0_Part1추가_9장_v2.pptx'
pres=json.loads((B/'preservation.json').read_text())
a=zipfile.ZipFile(OLD);b=zipfile.ZipFile(NEW)
for name in a.namelist():
 if name not in pres['allowed_changed_parts']:assert a.read(name)==b.read(name),name
images=U/'renders/prep-tools-v2/powerpoint'
for n in [1,2,4,5,6,7,8,9]:
 x=Image.open(U/f'renders/append-part01/powerpoint/slide-{n:02}.png').convert('RGB')
 y=Image.open(images/f'slide-{n:02}.png').convert('RGB')
 assert ImageChops.difference(x,y).getbbox() is None,n
assert len(PdfReader(NEW.with_suffix('.pdf')).pages)==9
target=ET.fromstring(b.read(pres['edited_part']))
texts=''.join(target.itertext())
assert all(s in texts for s in ['유료 계정 필수','클로드 또는 코덱스 중 하나','있으면 좋아요','없으면 시연을 보세요'])
assert not any(s in texts for s in ['홍보 문장','과학사 주제','인터넷'])
shutil.copy2(images/'slide-03.png',OUT/'준비물_로고형_v2.png')
sheet=Image.new('RGB',(1920,1080),'black')
for i,n in enumerate([3,4,5,6]):sheet.paste(Image.open(images/f'slide-{n:02}.png').convert('RGB').resize((960,540)),((i%2)*960,(i//2)*540))
sheet.save(OUT/'추가4장_미리보기_v2.png')
check=U/'checks/prep-tools-v2';check.mkdir(exist_ok=True)
(check/'verification.json').write_text(json.dumps({'total_slides':9,'pdf_pages':9,'edited_slide':3,'unchanged_other_slides_pixel_identical':8,'requested_logos':['claude-front','codex-front','higgsfield-front'],'prerequisite':'클로드 또는 코덱스 중 하나의 유료 계정 필수','higgsfield':'선택, 없으면 강사 시연 관찰','G10_clearance':False},ensure_ascii=False,indent=2),encoding='utf-8')

part0='''# Part 0 — 오늘의 준비물

2026-10-27 최신 사용자 지시. 추가 장표 미리보기의 첫 번째 준비물 장표이며 전체 PPT에서는 3쪽이다.

## 장표 내용

앞서 제작한 클로드·코덱스·힉스필드 도구 로고를 사용한다. 이전 컴퓨터·문장·웹주소·과학사 주제의 다섯 카드 내용은 준비물 장표에서 제거한다.

| 도구 | 준비 조건 | 화면 문구 |
|---|---|---|
| 클로드 또는 코덱스 | 둘 중 하나의 유료 계정 필수 | 유료 계정 필수 / 클로드 또는 코덱스 중 하나 |
| 힉스필드 | 선택 사항. 계정이 없으면 시연 관찰 | 있으면 좋아요 / 없으면 시연을 보세요 |

두 AI 도구를 모두 결제하거나 힉스필드를 반드시 구매하라는 의미가 아니다. 검정 바탕·주황 강조·노션톡 원본 로고·푸터를 유지한다. 다른 8장은 변경하지 않는다.

현재 파일: `output/webinar-part01-added/NotionTalk_대표5장유지_Part0_Part1추가_9장_v2.pptx`와 같은 이름 PDF. 검증: `checks/prep-tools-v2/verification.json`.
'''
history=U/'history/before-prep-tools-v2-20261027';history.mkdir(exist_ok=True)
if not (history/'part-0.md').exists():shutil.copy2(U/'part-0.md',history/'part-0.md')
(U/'part-0.md').write_text(part0,encoding='utf-8')
helper=U/'drafts/planning/revise_three_cases.py'
txt=helper.read_text(encoding='utf-8')
txt=re.sub(r"PART0 = '''.*?'''(?=\n\nPART1)",lambda m:"PART0 = '''"+part0+"'''",txt,flags=re.S)
helper.write_text(txt,encoding='utf-8')
design=U/'design.md'
d=design.read_text(encoding='utf-8')
d=d.replace('9장_v1.pptx','9장_v2.pptx')
d=d.replace('## 현재 추가본 — 기존 5장 + 요청한 4장','## 최신 준비물 수정\n\n준비물(전체 3쪽)은 사용자 요청으로 다섯 카드와 기존 본문을 제거하고 기존 클로드·코덱스·힉스필드 로고로 바꿨다. 클로드 또는 코덱스 중 하나의 유료 계정은 필수, 힉스필드는 선택이며 없으면 시연을 본다. 기존 대표 5장과 다른 예제 3장은 그대로 보존했다. 검증 근거는 checks/prep-tools-v2/verification.json이다.\n\n## 현재 추가본 — 기존 5장 + 요청한 4장',1)
design.write_text(d,encoding='utf-8')
plan=U/'plan.md';plan.write_text(plan.read_text(encoding='utf-8').replace('9장_v1.pptx','9장_v2.pptx'),encoding='utf-8')
readme=OUT/'읽어주세요.md'
readme.write_text('최신 파일은 9장_v2.pptx와 PDF입니다. 준비물 장표(전체 3쪽)만 기존 도구 로고 3개로 수정했습니다. 클로드 또는 코덱스 중 하나의 유료 계정은 필수, 힉스필드는 선택이며 계정이 없으면 시연을 봅니다. 나머지 8장은 원본 데이터와 PowerPoint 렌더 모두 동일함을 확인했습니다. G10 검토 상태는 유지합니다.\n',encoding='utf-8')
print('PASS: 1 preparation slide changed; other 8 slides pixel-identical; 9 PDF pages.')
