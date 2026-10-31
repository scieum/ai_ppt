from pathlib import Path
import shutil,json
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';A=R/'assets/layout-library-20261028/logic-patterns-20261030'
assert (U/'checks/conclusion-bar-20261030/verification.json').exists()
shutil.copy2('C:/Users/User/AppData/Local/Temp/codex-clipboard-d3a467fa-1bea-4ce5-b0da-ebbd80ad7dc8.png',A/'references/conclusion-bar-request.png')
prefix='''## 최신 결론 텍스트 바 — 2026-10-30

현재 강의는 `output/webinar-knowledge-only/NotionTalk_모션그래픽_결론텍스트바_43장_v32.pptx`와 PDF다. 사용자가 특별히 지정한 긴 텍스트 바를 공통 에셋으로 확정했다. 왼쪽 ‘결론’ 라벨과 본문이 한 덩어리로 이어지고, 라벨 안쪽 오른편은 직선이며 바깥쪽만 둥글다. 얇은 테두리와 거의 검정인 본문 배경, 흰 글씨를 쓰고 핑크 대신 노션톡 주황 계열로 적용한다.

6·20·22·23·25·26·36·37·38·39·40쪽의 기존 한 줄 결론 문구 위치에 반영한다. 1280×720 기준 기본 위치 x150/y640, 폭980/높이40이며 왼쪽 라벨 폭은88이다. 6쪽은 기존 곰 캐릭터를 가리지 않도록 x430/폭700으로 두 카드 아래에 맞춘다. 기존 문구는 그대로 유지하며 문구가 없는 표지·파트 구분·준비물·일정 등에 억지로 추가하지 않는다.

결론 바 외의 모든 객체·이미지·애니메이션·노트는 유지했다. 나머지 32장은 XML과 PDF 픽셀 모두 v31과 같다. 재사용 함수는 `assets/layout-library-20261028/logic-patterns-20261030/conclusion-bar.mjs`다. 검증은 단원 `checks/conclusion-bar-20261030/verification.json`, 렌더는 `renders/conclusion-bar-20261030/`다. 기존 G10 상태는 유지한다. 아래는 이전 이력이다.

'''
for p in [R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md']:
 backup=U/'history/conclusion-bar-20261030'/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(p,backup)
 s=p.read_text(encoding='utf-8-sig')
 if not s.startswith('## 최신 결론 텍스트 바'):p.write_text(prefix+s,encoding='utf8')
p=A/'README.md';s=p.read_text(encoding='utf8');addition='''\n## 확정 결론 바 스타일 — v32\n\n사용자가 결론 바를 별도로 지정했다. `conclusion-bar.mjs`를 우선 사용한다. 왼쪽 라벨은 흰 글씨 ‘결론’과 주황 배경, 본문은 거의 검정인 주황 계열 배경과 흰 글씨, 외곽은 얇은 주황 테두리다. 라벨 오른편을 직선으로 이어 별도 캡슐처럼 보이지 않게 한다. 본문 문구를 바꾸지 않고 핵심 요약에만 사용한다. 6쪽은 캐릭터와 겹치지 않게 카드 아래 폭에 맞춘다. 사용자 지정 캡처는 `references/conclusion-bar-request.png`에 내부 참고용으로 보관한다.\n'''
if '## 확정 결론 바 스타일' not in s:p.write_text(s+addition,encoding='utf8')
p=U/'checks/conclusion-bar-20261030/verification.json';v=json.loads(p.read_text(encoding='utf8'));v['full_size_visual_review_slides']=[6,20,22,23,25,26,36,37,38,39,40];p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
print('Saved v32 and canonical conclusion bar preference.')
