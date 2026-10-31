from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
name='NotionTalk_모션그래픽_효과음과움직임확장_48장_v33'
header=f'''## 최신 모션·효과음 확장 — 2026-10-30

현재 강의는 `output/webinar-knowledge-only/{name}.pptx`와 PDF다. 사용자 요청으로 조사 내용을 실제 장표에 반영했다. 기존 검정·주황·흰색, Pretendard, 상단·로고·푸터·결론 텍스트 바를 유지한다. 43장 v32에서 5장을 추가한 48장이다.

- 13쪽: 기존 리빌·순차 등장 설명에 마스크 리빌·스태거 명칭을 통합한다.
- 14쪽: 기존 모핑을 유지하고 입체 회전 안에 카드 플립을 통합한다. 질문 카드가 180도 돌아 답으로 바뀌는 반복 GIF와 상태 세 장을 넣는다.
- 15~16쪽: 스냅 텍스트·블러 인, 카운터·스쿼시 앤 스트레치를 각각 두 개의 움직이는 예시로 설명한다. 새 GIF는 20fps, 92프레임, 4.6초 반복이다.
- 19쪽: 같은 화면의 무음·효과음 4초 영상 두 개를 파일 안에 삽입한다. 슬라이드 쇼에서 각각 클릭해 재생한다. 자체 제작 예시이며 소개 도구의 실제 출력으로 표시하지 않는다.
- 20쪽: Openverse 검색, Clipwing Real SFX 배치, Leonxlnx/earshot 합성·분석을 구분한다. 필수 준비물이나 전부 무료라는 설명을 추가하지 않는다.
- 25쪽: 이미지의 글자·캐릭터·배경을 나누는 개념 도식으로 AE 사례를 연결한다. 선택 심화이며 실제 AE 재현 결과가 아니다. 원문의 Mac 확인·Windows 미검증 조건은 발표자 노트에 기록한다.

기존 41장과 원본 미디어는 보존한다. 기존 결론 바 11개를 유지하며 새 5장에도 같은 컴포넌트를 쓴다. 모든 새 모션·소리는 자체 예시이고 캡처의 원본 영상·음원은 삽입하지 않는다. 기본 하네스와 상속 G10 상태는 유지한다. 영상은 PPTX에서 재생하며 PDF는 정지 화면이다.

현재 순서: 준비물 1~4쪽, Part 1 5~22쪽, Part 2 23~25쪽, Part 3 26~36쪽, Part 4 37~45쪽, 사이클 안내 46~48쪽. 자산은 단원 `assets/motion-audio-20261030/`, 검증은 `checks/motion-audio-20261030/verification.json`, 렌더는 `renders/motion-audio-20261030/`다. 상세 출처는 `docs/motion-effects-audio-ae-20261030.md`. 아래는 이전 버전 이력이다.

'''
def prepend(file,value):
 old=file.read_text(encoding='utf8')
 if not old.startswith(value.split('\n')[0]):file.write_text(value+old,encoding='utf8')
for file in [R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md']:prepend(file,header)
for part,desc in [(1,'5쪽 파트 시작, 본문 6~22쪽. 13~14쪽에 기존 효과를 묶고 15~16쪽에 새 모션, 19~20쪽에 효과음을 추가한다.'),(2,'23쪽 파트 시작, 24쪽 이미지·영상 함께 참고, 25쪽 이미지의 요소를 나누는 AE 선택 사례다.'),(3,'26쪽 파트 시작, 본문 27~36쪽. 기존 내용·디자인은 그대로이며 새 장표 삽입으로 페이지 번호만 이동했다.'),(4,'37쪽 파트 시작, 본문 38~45쪽. 기존 내용·디자인은 그대로이며 새 장표 삽입으로 페이지 번호만 이동했다.')]:
 file=U/f'part-{part}.md'
 if file.exists():prepend(file,f'## 현재 v33 페이지 안내 — 2026-10-30\n\n{desc} 전체 순서는 [현재 장표 목록](slide-order-v33.md)을 따른다. 아래 기존 페이지 표기는 해당 버전 이력이다.\n\n')
mapping=json.loads((B/'slide-map.json').read_text(encoding='utf8'));N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
rows=['# 현재 장표 순서 — 48장 v33','',f'파일: `output/webinar-knowledge-only/{name}.pptx`','', '| 쪽 | 제목 | 반영 |','|---:|---|---|']
with ZipFile(R/f'output/webinar-knowledge-only/{name}.pptx')as z:
 for m in mapping:
  root=E.fromstring(z.read(m['part']));titles=[]
  for el in root.findall('p:cSld/p:spTree/p:sp',N):
   nv=el.find('p:nvSpPr/p:cNvPr',N)
   if nv is not None and nv.get('name')in['title','slot-title','slide-title']:titles+=el.xpath('.//a:t/text()',namespaces=N)
  if not titles:titles=root.xpath('//a:t/text()',namespaces=N)[:3]
  title=' '.join(titles).replace('|','/').replace('\n',' ')
  rows.append(f'| {m["page"]} | {title} | '+{'new':'추가','modified':'기존 설명에 통합','preserved':'유지'}[m['kind']]+' |')
(U/'slide-order-v33.md').write_text('\n'.join(rows)+'\n',encoding='utf8')
summary=R/'docs/motion-effects-audio-ae-20261030.md';old=summary.read_text(encoding='utf8')
notice=f'> 반영 완료(2026-10-30): [{name}.pptx](../output/webinar-knowledge-only/{name}.pptx). 13~14쪽 통합, 15~16·19~20·25쪽 추가. 아래 분석·제안은 조사 당시 기록이며 실제 순서는 [48장 목록](../units/AI-001_모션그래픽수업영상_무료웨비나/slide-order-v33.md)을 따른다.\n\n'
if '> 반영 완료(2026-10-30)'not in old:summary.write_text(old.replace('\n\n','\n\n'+notice,1),encoding='utf8')
asset_readme='''# 자체 제작 모션·효과음 예시

5개 GIF(스냅·블러·카운터·스쿼시 앤 스트레치·플립)는 움직임을 설명하기 위한 자체 시연이다. 20fps, 92프레임, 4.6초 반복으로 정지 화면용 대표 프레임을 앞에 잠깐 둔다.

`silent.mp4`와 `with-sound.mp4`는 같은 4초 화면이며 후자에 자체 합성한 팝·짧은 스윽 소리·알림음을 넣었다. Real SFX나 earshot을 설치·실행한 결과가 아니다. `original-effects.wav`는 사용한 자체 음원이다. 원본 캡처·사이트의 영상이나 음원을 복제하지 않았다.

PPTX의 슬라이드 쇼에서 GIF는 반복되고, 19쪽 영상은 각각 클릭해서 재생한다. PDF에는 정지 프레임만 보인다. PowerPoint 영상 내보내기로 움직임과 음성 트랙을 확인했다.

생성 소스는 `output/motion-audio-build/make-media.mjs` 및 `gif-posters.mjs`, 출처·한계는 루트 `docs/motion-effects-audio-ae-20261030.md`에 있다.
'''
(U/'assets/motion-audio-20261030/README.md').write_text(asset_readme,encoding='utf8')
print('Updated current plan, design, part page mapping and reusable asset notes.')
