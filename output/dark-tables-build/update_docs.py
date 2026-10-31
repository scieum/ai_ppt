from pathlib import Path
import shutil
B=Path(__file__).resolve().parent;R=B.parent.parent
U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
H=U/'history/dark-tables-20261029';H.mkdir(parents=True,exist_ok=True)
prefix='''## 최신 표 디자인 정리 — 2026-10-29

현재 강의는 `output/webinar-knowledge-only/NotionTalk_모션그래픽_표디자인정리_40장_v22.pptx`와 PDF다. 사용자 지적에 따라 25·34쪽의 밝은 표 셀을 없애고 R01 20쪽의 어두운 비교표 표현을 적용했다. 머리행 #2D2D2D, 항목열 #303030, 본문 #1E1E1E, 흰 본문과 주황 #FF9228 항목 강조를 사용한다. 구분선은 #454545·0.65px이며 셀 안 여백과 세로 중앙 정렬을 적용한다. 앞으로 비교표에는 흰색 셀이나 갈색 항목열을 기본으로 쓰지 않는다. 밝은 문서 예시 패널은 표와 구분한다.

총 40장과 모든 내용·순서·로고·푸터·이미지·GIF·애니메이션·노트는 유지한다. 기존 어두운 표인 22·33쪽과 나머지 장표는 유지했다. 24·30·38쪽의 큰 설명 이미지도 그대로다. 검증 기록은 단원 `checks/dark-tables-20261029/verification.json`이며 이전 버전은 아래 개정 이력이다. lesson.md·하네스 기본 구조·상속 G10 상태를 변경하지 않는다.

'''
for p in [R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md',U/'part-3.md',U/'part-4.md']:
 assert p.exists(),p
 backup=H/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(p,backup)
 text=p.read_text(encoding='utf-8-sig')
 if not text.startswith('## 최신 표 디자인 정리'):
  p.write_text(prefix+text,encoding='utf-8')
print('Updated current deck pointers and reusable dark-table policy.')
