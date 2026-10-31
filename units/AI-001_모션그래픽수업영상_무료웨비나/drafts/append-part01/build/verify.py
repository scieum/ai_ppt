from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont
from pypdf import PdfReader
import zipfile,json,hashlib,xml.etree.ElementTree as ET
B=Path(__file__).resolve().parent;U=B.parents[2];ROOT=U.parents[1]
OUT=ROOT/'output/webinar-part01-added'
DECK=OUT/'NotionTalk_대표5장유지_Part0_Part1추가_9장_v1.pptx'
BASE=ROOT/'output/webinar-samples/NotionTalk_모션그래픽_주황포인트_자체사례_v5.pptx'
RENDER=U/'renders/append-part01/powerpoint';SR=U/'renders/append-part01/source'
CHECK=U/'checks/append-part01';CHECK.mkdir(parents=True,exist_ok=True)
old=zipfile.ZipFile(BASE);new=zipfile.ZipFile(DECK)
allowed={'[Content_Types].xml','ppt/presentation.xml','ppt/_rels/presentation.xml.rels','docProps/app.xml'}
for name in old.namelist():
    if name not in allowed:assert old.read(name)==new.read(name),name
rows=[]
font=ImageFont.truetype('C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf',26)
for oldpos,newpos in [(1,1),(2,2),(3,7),(4,8),(5,9)]:
    a=Image.open(SR/f'slide-{oldpos:02}.png').convert('RGB')
    b=Image.open(RENDER/f'slide-{newpos:02}.png').convert('RGB')
    assert a.size==b.size==(1920,1080)
    delta=ImageChops.difference(a,b);bounds=delta.getbbox()
    rows.append({'source_slide':oldpos,'final_slide':newpos,'pixel_identical':bounds is None,'difference_bounds':bounds})
    assert bounds is None,(oldpos,newpos,bounds)
    pair=Image.new('RGB',(1920,590),'#222222');d=ImageDraw.Draw(pair)
    d.text((25,13),f'기존 대표본 {oldpos}장',font=font,fill='white');d.text((985,13),f'추가본 {newpos}쪽 · 기존 장표 그대로',font=font,fill='#FF9228')
    pair.paste(a.resize((960,540)),(0,50));pair.paste(b.resize((960,540)),(960,50));pair.save(CHECK/f'preserved-{oldpos:02}.png')
assert len(PdfReader(DECK.with_suffix('.pdf')).pages)==9
texts={}
for n in range(1,5):
    e=ET.fromstring(new.read(f'ppt/slides/part01-slide{n}.xml'))
    texts[n]=''.join(e.itertext())
assert '코덱스 or 클로드 유료 요금제' in texts[1]
assert all('NotionTalk' in t for t in texts.values())
assert '노션톡' in texts[2] and '타이포그래피' in texts[2]
assert 'notion.com/ko/product/docs' in texts[3]
assert all(s in texts[4] for s in ['원자모형','톰슨','러더퍼드','보어'])
sheet=Image.new('RGB',(1920,1080),'black')
for i,n in enumerate([3,4,5,6]):
    im=Image.open(RENDER/f'slide-{n:02}.png').convert('RGB').resize((960,540),Image.Resampling.LANCZOS)
    sheet.paste(im,((i%2)*960,(i//2)*540))
sheet.save(OUT/'추가4장_미리보기.png')
report={'scope':'original 5 slides preserved, 4 slides added','total_slides':9,'pdf_pages':9,'original_package_parts_unchanged':len(old.namelist())-len(allowed),'native_powerpoint_pixel_comparison':rows,'source_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'final_sha256':hashlib.sha256(DECK.read_bytes()).hexdigest(),'addition_positions':[3,4,5,6],'G10_clearance':False,'new_slide_design_approval':False}
(CHECK/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'읽어주세요.md').write_text('''# 기존 대표 5장 유지 · Part 0/Part 1만 추가

총 9장입니다. 기존 대표 5장의 문구·디자인·이미지·노트는 그대로 보존했습니다.

1~2쪽은 기존 표지와 전체 흐름, 3쪽은 Part 0 준비물, 4~6쪽은 Part 1의 노션톡 홍보 타이포그래피·웹사이트 소개·원자모형 변천 예제, 7~9쪽은 기존 Part 3·4·5 대표 장표입니다.

준비물은 기존 5칸 카드 장표, 예제는 기존 흰 프롬프트 박스 장표를 직접 복제해 추가했습니다. 추가 예제의 글자·도형은 표현 설명이며 실제 앱 캡처로 표시하지 않습니다. 기존 대표본과 이 파일의 해당 5장을 PowerPoint에서 각각 렌더링해 픽셀 단위 동일함을 확인했습니다. 기존 PPTX 파일도 변경하지 않았습니다.

이번 작업은 4장 추가 범위입니다. 전체 42장 강의 제작이나 새로운 인앱 캡처·영상 생성 작업은 포함하지 않습니다. 실제 출처는 추가 장표 노트에 기록했고 기존 G10 권리 검토 상태는 미완료입니다.
''',encoding='utf-8')
print('PASS: 9 PPT/PDF pages; all original 5 native renders pixel-identical; 4 requested slides present.')
