from pathlib import Path
import shutil
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';H=U/'history/challenge-activities-20261030'
prefix='''## 최신 사이클 활동 안내 — 2026-10-30

현재 강의는 `output/webinar-knowledge-only/NotionTalk_모션그래픽_사이클활동안내_43장_v26.pptx`와 PDF다. 41쪽 캘린더 뒤에 사이클별 활동 안내를 42·43쪽으로 추가했다. 기존 41장의 XML·PDF 출력 픽셀·미디어·노트와 11월 2일 시작 일정은 그대로 유지한다. v23 준비물·.md 카드·내레이션 변경은 계속 취소 상태다.

- 42쪽 / 1차 사이클 / 11월 2일(월)~8일(일): 이번 웨비나 내용을 적용해 수업에서 활용할 영상을 만든다. 수업 주제 선택, 배운 모션 적용, 수업용 영상 완성의 흐름이다.
- 43쪽 / 2차 사이클 / 11월 9일(월)~15일(일): 제공할 추가 자료를 활용해 motion.md·video.md 등 기준 문서를 작성하고 일관성을 유지한 모션그래픽을 만든다. 기준과 대표 장면을 먼저 확인하고 확정 기준을 재사용해 반복 생성과 토큰 낭비를 줄이는 활동이다.

motion.md는 등장·전환·속도·간격, video.md는 화면 비율·배경·전체 영상 톤을 정리하는 작업용 문서로 안내한다. 기존 storyline.md와 design.md 설명은 유지한다. 특정 파일명으로 자동 실행되거나 토큰 절약이 보장된다고 표현하지 않는다. 추가 자료는 제공 예정이며 이미 배포했다고 표시하지 않는다. 제출 채널·영상 길이·마감 시각·채점 기준은 지정되지 않아 추가하지 않았다.

디자인은 기존 L19 과제 안내의 큰 활동 영역과 오른쪽 짧은 설명을 따르고 2차에는 L16 파일 역할 표현을 더했다. 주황·흑백·Pretendard·NotionTalk 브랜드와 02 후속 활동 그룹을 유지한다. 새 이미지나 추가 Part 번호를 늘리지 않는다. 검증은 단원 `checks/challenge-activities-20261030/verification.json`, 렌더는 `renders/challenge-activities-20261030/`다. lesson.md·기본 하네스·상속 G10 상태는 유지하며 아래는 이전 이력이다.

'''
for p in [R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md',U/'part-4.md',U/'follow-up-challenge.md']:
 backup=H/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(p,backup)
 s=p.read_text(encoding='utf-8-sig')
 if p.name=='follow-up-challenge.md':
  s='''# 노션톡 웨비나 챌린지 후속 활동

2026년 11월 2일(월)~11월 15일(일), 총 2주. 43장 v26의 41~43쪽에서 안내한다.

## 1차 사이클 · 11/2~11/8

이번 웨비나에서 배운 내용을 적용해 수업에서 활용할 만한 영상을 제작한다.

1. 수업에서 보여 주고 싶은 주제를 선택한다. 도입·개념 설명·내용 정리 등은 선택 예시다.
2. 배운 모션그래픽 유형과 효과를 적용한다.
3. 수업에 활용할 영상으로 완성한다.

## 2차 사이클 · 11/9~11/15

추가 자료를 제공하고, 기준 문서를 재사용해 반복 생성과 토큰 사용을 줄이는 모션그래픽 제작을 진행한다.

1. 제공할 추가 자료에서 필요한 기준을 확인한다.
2. motion.md·video.md 등을 작성하고 대표 장면으로 톤과 움직임을 확인한다.
3. 확정 기준을 다음 장면에 재사용해 일관성을 유지한 모션그래픽을 만든다.

motion.md에는 등장·전환·속도·간격, video.md에는 화면 비율·배경·전체 영상 톤을 기록한다. 기존 storyline.md는 내용과 장면 순서, design.md는 색·글꼴·배치의 기준으로 유지한다. 문서는 AI에 명시적으로 제공하는 기준 자료이며 이름만으로 자동 적용되지 않는다.

토큰 절약은 반복 생성 범위를 줄이는 목적이며 절감량을 보장하지 않는다. 제출 채널·마감 시각·영상 길이는 아직 지정하지 않았다. 추가 자료가 이미 배포되었다고 표시하지 않는다.
'''
 else:s=prefix+s
 p.write_text(s,encoding='utf-8')
print('Updated activity plan and current deck pointers.')
