from pathlib import Path
import shutil
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';H=U/'history/challenge-calendar-20261029';H.mkdir(parents=True,exist_ok=True)
prefix='''## 최신 후속 챌린지 캘린더 — 2026-10-29

현재 강의는 `output/webinar-knowledge-only/NotionTalk_모션그래픽_챌린지일정추가_41장_v24.pptx`와 PDF다. 사용자 요청으로 롤백 기준 v22 40장 끝에 노션톡 웨비나 챌린지 일정 한 장을 추가했다. 기존 40장 XML·PDF 출력 픽셀·미디어·노트를 보존한다. v23 준비물·.md 카드·내레이션 변경은 계속 취소 상태다.

41쪽은 후속 활동 캘린더다. 2026년 11월 1일(일)~11월 7일(토)은 1차 사이클, 11월 8일(일)~11월 14일(토)은 2차 사이클이다. 양 끝 날짜를 포함해 각각 7일, 총 14일이다. 과제·제출 장소·마감 시각은 지정되지 않았으므로 넣지 않는다. 기존 40쪽 마무리 뒤에 배치하며 새 Part나 목차 항목을 늘리지 않는다.

기존 L18 일정 에셋의 출처 R01 99쪽·R03 42쪽을 다시 시각 검토했다. 원본의 요일 7칸·주차별 가로행·어두운 날짜 셀·기간을 가로지르는 색 띠를 편집 가능한 객체로 구성한다. NotionTalk 로고·푸터·Pretendard·검정 바탕·주황 강조를 유지한다. 두 번째 기간 띠는 낮은 채도의 파랑으로 구분한다. 날짜·문구는 노션톡 일정으로 새로 썼고 원본 PDF 화면을 붙이지 않는다.

검증은 단원 `checks/challenge-calendar-20261029/verification.json`, 렌더는 `renders/challenge-calendar-20261029/`다. lesson.md와 하네스 기본 구조·상속 G10 상태는 유지한다. 아래 40장 버전은 이번 추가 직전 이력이다.

'''
for p in [R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md',U/'part-4.md']:
 backup=H/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(p,backup)
 content=p.read_text(encoding='utf-8-sig')
 if not content.startswith('## 최신 후속 챌린지 캘린더'):p.write_text(prefix+content,encoding='utf-8')
(U/'follow-up-challenge.md').write_text('''# 노션톡 웨비나 챌린지 후속 활동

2026년 11월 1일~11월 14일, 총 2주.

| 구간 | 시작 | 종료 | 기간 |
|---|---|---|---|
| 1차 사이클 | 11월 1일(일) | 11월 7일(토) | 7일 |
| 2차 사이클 | 11월 8일(일) | 11월 14일(토) | 7일 |

현재 웨비나의 마지막 41쪽에서 안내한다. 날짜는 양 끝을 포함한다. 과제·제출 방식·마감 시각은 아직 정하지 않았다.

디자인: R01 99쪽 및 R03 42쪽의 달력 구조. 일~토 7열, 1·2주차 2행, 어두운 셀과 각 주를 가로지르는 사이클 띠. 브랜드와 날짜를 노션톡에 맞춰 적용했다.
''',encoding='utf-8')
print('Updated current deck pointer and follow-up calendar plan.')
