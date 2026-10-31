from pathlib import Path
import shutil
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';H=U/'history/header-glass-20261030'
prefix='''## 최신 상단 글자 확대·유리 질감 로고 — 2026-10-30

현재 강의는 `output/webinar-knowledge-only/NotionTalk_모션그래픽_헤더확대_글라스로고_43장_v27.pptx`와 PDF다. v26에 대한 사용자 주석을 반영했다. 43장 구성과 본문·사이클 일정·활동 내용은 그대로 유지한다.

- 36개 장표의 상단 Part 표기·섹션 번호·섹션 제목 108개를 v26보다 정확히 2pt 확대했다. Part 12→14pt, 12.75→14.75pt, 16→18pt; 섹션 21→23pt, 22→24pt다. 이후 편집 시 이 증가분을 다시 누적하지 않는다. 표지·파트 구분의 큰 제목·본문·푸터는 대상이 아니다.
- 기존 section_number는 확대된 두 자리 숫자가 들어가도록 폭을 8px 넓히고 section_heading은 오른쪽으로 8px 옮겨 기존 오른쪽 끝을 유지한다. 다른 레이아웃은 유지한다.
- 준비물 3쪽의 클로드·코덱스·힉스필드 타일은 주황 장식을 없앤 중성 회색 유리 질감과 흰 로고로 교체했다. `assets/tool-logos/glass-v3/`에 세 PNG와 ImageGen 생성 프롬프트·원본 경로 기록을 보관한다. 이전 주황 자산은 보존한다.
- ‘유료 계정 필수’ 문구에 #242424 배경·#454545 테두리의 편집 가능한 둥근 텍스트 상자를 적용했다. 기존 문구와 주황 텍스트는 유지한다.

준비물은 클로드 또는 코덱스 유료 계정 필수, 힉스필드 선택 안내를 유지한다. 취소된 v23 도구·문서 카드 변경을 복원하지 않는다. 검증은 단원 `checks/header-glass-20261030/verification.json`, 렌더는 `renders/header-glass-20261030/`다. 아래 내용은 이전 이력이다.

'''
for p in [R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md',U/'part-0.md']:
 assert p.exists(),p
 backup=H/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(p,backup)
 s=p.read_text(encoding='utf-8-sig')
 if not s.startswith('## 최신 상단 글자 확대·유리 질감 로고'):p.write_text(prefix+s,encoding='utf-8')
print('Saved current v27 rules and archived prior documentation.')
