from pathlib import Path
import shutil,json
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
assert (U/'checks/prep-label-spacing-20261030/verification.json').exists()
prefix='''## 최신 준비물 안내 박스·간격 수정 — 2026-10-30

현재 강의는 `output/webinar-knowledge-only/NotionTalk_모션그래픽_준비물안내박스_43장_v30.pptx`와 PDF다. v29에 대한 사용자 주석을 반영해 3쪽 ‘있으면 좋아요’에도 왼쪽 ‘유료 계정 필수’와 같은 #242424 배경·#454545 테두리의 편집 가능한 둥근 텍스트 박스를 적용했다. 오른쪽 기존 폭과 주황 글씨는 유지한다.

양쪽 흰색 안내 문구를 1280×720 기준 y604에서 y616으로 내려 박스와 간격을 확보했다. 나머지 42장, 모든 문구·폰트·로고 색·이미지·표·움직임은 그대로다. v29의 공통 글자 크기와 정렬 기준은 계속 유지한다. 검증은 단원 `checks/prep-label-spacing-20261030/verification.json`, 렌더는 `renders/prep-label-spacing-20261030/`다. 아래는 이전 이력이다.

'''
for p in [R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md',U/'part-0.md']:
 backup=U/'history/prep-label-spacing-20261030'/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(p,backup)
 s=p.read_text(encoding='utf-8-sig')
 if not s.startswith('## 최신 준비물 안내 박스·간격 수정'):p.write_text(prefix+s,encoding='utf-8')
print('Recorded narrow slide-3 correction and retained prior versions.')
