from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,zipfile,re
from pypdf import PdfReader

BUILD=Path(__file__).resolve().parent
UNIT=BUILD.parents[2];ROOT=UNIT.parents[1]
OUT=ROOT/'output/webinar-three-cases-v2'
RENDER=UNIT/'renders/three-cases-v2/powerpoint'
CHECK=UNIT/'checks/three-cases-v2'
CHECK.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf',27)
mapping=['R05-p031.png']*3+['R03-p031.png','R03-p035.png']
for i,src in enumerate(mapping,1):
    # Inspection montage only. Original PDF pages are never used in the PPT.
    im=Image.new('RGB',(1920,590),'#242424');d=ImageDraw.Draw(im)
    d.text((30,13),'제공 레퍼런스 · '+src,fill='white',font=font)
    d.text((990,13),'새 대표 시안 · '+str(i)+'장',fill='#FF9228',font=font)
    left=Image.open(ROOT/'output/reference-analysis'/src).convert('RGB').resize((960,540),Image.Resampling.LANCZOS)
    right=Image.open(RENDER/f'slide-{i:02}.png').convert('RGB').resize((960,540),Image.Resampling.LANCZOS)
    im.paste(left,(0,50));im.paste(right,(960,50));im.save(CHECK/f'comparison-{i:02}.png')
    if i==1:im.save(OUT/'레퍼런스_비교_01.png')

# Native-rendered contact sheet for quick review. Full-size pages remain separate.
sheet=Image.new('RGB',(1920,720),'#111111')
for i in range(1,6):
    frame=Image.open(RENDER/f'slide-{i:02}.png').convert('RGB').resize((640,360),Image.Resampling.LANCZOS)
    sheet.paste(frame,((i-1)*640,0) if i<=3 else (320+(i-4)*640,360))
sheet.save(OUT/'대표장표_미리보기.png')

pdf=OUT/'NotionTalk_Part1_예제와실제시연_v4.pdf'
assert len(PdfReader(pdf).pages)==5
for i in range(1,6):assert Image.open(RENDER/f'slide-{i:02}.png').size==(1920,1080)
media=json.loads((BUILD/'media-verification.json').read_text(encoding='utf-8'))
for row in media:
    file=Path(row['file']);assert hashlib.sha256(file.read_bytes()).hexdigest()==row['sha256']
caps=UNIT/'assets/three-cases-v2/claude'
capdata=json.loads((caps/'captures.json').read_text(encoding='utf-8'))
for row in capdata:
    b=(caps/row['file']).read_bytes();assert hashlib.sha256(b).hexdigest()==row['sha256']
    row['size_pixels']=list(Image.open(caps/row['file']).size)
(CHECK/'verification.json').write_text(json.dumps(dict(pptx_slides=5,pdf_pages=5,native_powerpoint_rendered=5,actual_capture_count=len(capdata),actual_capture_hashes='passed',videos=media,comparison_pages=5,user_design_approval=False,G10_clearance=False),ensure_ascii=False,indent=2),encoding='utf-8')

feedback=dict(actor='user',scope='global',status='open',feedback='실제앱 단계별 캡쳐 졸라 별로야. 레퍼런스 처럼 해달라니깐\n그리고 너가 예시로 넣은 것도 졸라 별로야.',example_direction_reply='이 조합으로 수정',selected_topics=['노션톡 웨비나 홍보 타이포그래피','실제 웹사이트 소개','원자모형 변천 과학사 영상'],design_approval=False,correction_artifact='output/webinar-three-cases-v2/NotionTalk_Part1_예제와실제시연_v4.pptx',remaining=['B·C의 인앱 시연 및 새 Codex 캡처','전체 강의 반영','사용자 디자인 확인','G10 권리 검토'])
(CHECK/'user-feedback.json').write_text(json.dumps(feedback,ensure_ascii=False,indent=2),encoding='utf-8')
readme='''# Part 1 대표 장표·예제 수정 검토본

사용자가 선택한 노션톡 홍보 타이포그래피 / 실제 웹사이트 소개 / 원자모형 변천 조합으로 바꾼 대표 5장입니다. 첫 3장은 예제와 시작 요청, 4~5장은 실제 Claude 요청·아티팩트 결과입니다. 기존 단계별 캡처 PPT는 사용자 거부 상태이며 이 파일도 디자인 승인 전입니다.

- `NotionTalk_Part1_예제와실제시연_v4.pptx` / 같은 이름 PDF: 대표 5장.
- MP4 3종: 코드로 직접 제작한 20·30·45초 무음 예제. PPT에는 정지 프레임이 들어 있으며 영상은 별도 파일입니다. 실제 Claude 결과를 녹화한 영상이 아닙니다.
- `레퍼런스_비교_01.png`: R05 31쪽과 새 1장 좌우 비교. 참고 자료를 포함한 내부 검토용이며 발표·외부 배포 자료가 아닙니다.
- Claude 실제 실행: https://claude.ai/chat/13929648-6e5f-432b-abdc-0ff7440bb057 . 20초 HTML 아티팩트가 생성됐고 재생·처음부터·3초 지점 이동을 확인했습니다. MP4 내보내기 완료를 의미하지 않습니다.
- 실제 앱 원본 캡처와 해시는 단원 `assets/three-cases-v2/claude/`에 보관합니다. B·C의 실제 인앱 요청·수정·재생 및 새 Codex 캡처는 아직 없습니다.
- 웹 내용 근거: https://www.notion.com/ko/product/docs . 과학사 근거: https://history.aip.org/exhibits/rutherford/sections/alpha-particles-atom.html 및 https://www.edu.gov.mb.ca/ks4/cur/science/found/s1/appen2.pdf (Appendix 2.3 A27~A29). 확인일 2026-10-27.
- PDF 추출 배경·도형·로고를 새 PPT에 넣지 않았습니다. 사용자 소유 NotionTalk 로고, 네이티브 텍스트·도형, 직접 제작한 영상 프레임과 실제 앱 캡처를 사용했습니다. Pretendard는 익명 Type3 원문 글꼴의 대체이며 원본과 동일한 폰트라는 뜻이 아닙니다.
- PowerPoint 5장 열기·PDF 변환·개별 PNG 출력, 파일 구조·글꼴·페이지 수, MP4 전체 프레임 디코딩을 확인했습니다. 기술 검사는 디자인 승인·사실 검수 전체·G10 통과를 뜻하지 않습니다. G10은 미완료입니다.
'''
(OUT/'읽어주세요.md').write_text(readme,encoding='utf-8')
files=[OUT/'NotionTalk_Part1_예제와실제시연_v4.pptx',pdf,*[Path(m['file']) for m in media],OUT/'읽어주세요.md']
with zipfile.ZipFile(OUT/'Part1_대표5장_예제영상3종.zip','w',zipfile.ZIP_DEFLATED) as z:
    for file in files:z.write(file,file.name)
print('Verified 5 native slides / 5 PDF pages / 3 fully decoded videos /',len(capdata),'authentic captures. G10 and design approval remain open.')
