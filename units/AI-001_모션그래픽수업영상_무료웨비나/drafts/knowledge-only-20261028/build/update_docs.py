from pathlib import Path
import json,shutil
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
rows=json.loads((B/'content.json').read_text(encoding='utf8'));H=U/'history/foundations-before-knowledge-only-20261028';H.mkdir(parents=True,exist_ok=True)
for name in ['plan.md','design.md']+[f'part-{i}.md' for i in range(6)]:
 p=U/name
 if p.exists() and not (H/name).exists():shutil.copyfile(p,H/name)
plan='''# 모션 그래픽 기본 지식

2026-10-28 · NotionTalk · 기초 지식만 다루는 10장 · 강의 시간 미정

## 현재 범위

사용자는 모션 그래픽 지식과 종류만 남기고, 어떤 프롬프트를 넣을지와 어떤 영상을 만들려면 무엇을 고려할지에 관한 내용을 모두 제외하도록 요청했다. 기본 개념은 유지하고 제작 조언·목적별 고려사항·분석·검토·실습은 배치하지 않는다.

현재 결과물은 [PPT](../../output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_10장_v2.pptx)와 [PDF](../../output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_10장_v2.pdf)다.

## 남기는 지식

- 모션 그래픽의 뜻과 정지 디자인과의 차이
- 프레임·키프레임·연속된 상태와 움직임
- 키네틱 타이포그래피·인포그래픽·UI/서비스 소개·로고/타이틀·일러스트/캐릭터의 분류
- 위치·크기·각도·불투명도의 의미
- 페이드·슬라이드·줌/스케일의 이름과 변화
- 와이프/리빌·타이프라이터·순차 등장(Stagger)의 의미
- 지속시간·이징·이즈 인/아웃의 정의
- 표현 종류·기본 속성·효과와 시간 규칙의 구분

개념을 보여 주는 기존 GIF와 PPT 네이티브 효과는 유지한다. 특정 영상을 제작하거나 개선하는 실습으로 연결하지 않는다.

## 제외하는 내용

프롬프트·입력 방법·앱 조작·생성·출력·Markdown·장면표·커넥터·저장·제출 실습, 영상 목적별 고려사항, 읽는 시간 확보·강조 우선순위·장면 전환 설계·레퍼런스 분석·음악과 가독성 검토·시각적 일관성 점검은 모두 제외한다. 홍보·웹사이트·원자모형의 제작 사례와 사례별 완료 기준도 넣지 않는다. 효과마다 “어떤 때 쓰면 좋은지” 조언을 덧붙이지 않는다.

종류 장표에 남는 광고·통계·서비스 등은 분류를 설명하는 일반적 예다. 특정 영상의 기획 또는 제작 과제로 설명하지 않는다.

## 페이지 계획

| 쪽 | 내용 |
|---:|---|
'''
for s in rows:plan+=f"| {s['page']} | {s['title']} |\n"
plan+='''
## 디자인과 근거

기존 주황·흑백·Pretendard·NotionTalk 원본 로고와 푸터·세 캐릭터 표지·기초 효과 레이아웃을 유지한다. 상단 번호는 개념 묶음을 나타내며 매 장표마다 증가시키지 않는다. 효과 설명의 노션톡 문구와 하늘색 노션톡 웨비나 챌린지는 유지한다.

기존 기초 자료의 공식 문서 출처는 발표자 노트에 남긴다. lesson.md 원문과 이전 결과물은 이력으로 보존한다. 현재 장표에서 제작 사례나 여섯 영상의 적용안으로 범위를 다시 넓히지 않는다. G10 권리 검토 상태와 기본 하네스 코드·폴더 구조는 유지한다. 이전 22장 계획은 history/foundations-before-knowledge-only-20261028/에 보존했다.
'''
(U/'plan.md').write_text(plan,encoding='utf8')
(U/'design.md').write_text('''# 기본 지식만 남긴 장표 기준

최신 결과물은 output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_10장_v2.pptx와 PDF다. 기존 대표 디자인과 기본 개념 시각화는 유지하며 콘텐츠 범위를 모션 그래픽의 정의·종류·속성·효과·시간 용어로 한정한다.

3쪽 정의 비교, 4쪽 플립북과 내장 GIF, 5쪽 다섯 표현 유형, 6쪽 네 속성, 7쪽 세 등장 효과, 8쪽 글자/순서 효과, 9쪽 지속시간과 이징을 사용한다. 10쪽은 용어의 차이를 편집 가능한 표로 정리한다. 표지와 목차를 포함해 총 10장이다.

7~8쪽에서 효과 사용 목적·추천 상황을 적은 하단 문구는 삭제한다. 9쪽은 읽는 시간에 대한 조언 대신 지속시간과 속도 변화의 정의만 설명한다. 홍보·서비스·원자모형 제작 사례, 프롬프트 상자, 레퍼런스·판단·검토 장표는 다시 넣지 않는다.

기존 주황·흑백·Pretendard·NotionTalk 원본 로고와 푸터를 유지한다. 노션톡 효과 문구와 하늘색 글자 예시, 실제 타이밍과 GIF를 유지한다. 새로운 제작 과정이나 고려사항을 디자인 개선이라는 이유로 추가하지 않는다. G10 상태는 변경하지 않는다.
''',encoding='utf8')
(U/'part-0.md').write_text('# 도입\n\n현재 1~2쪽은 표지와 기본 개념 목차다. 준비물·구독·제작 안내는 포함하지 않는다.\n',encoding='utf8')
groups=[('모션 그래픽의 뜻과 종류',3,5),('기본 속성과 효과 이름',6,8),('지속시간과 이징',9,9),('용어 구분',10,10)]
for i,(name,a,b) in enumerate(groups,1):
 t=f'# {name}\n\n현재 10장 기본 지식 자료의 {a}~{b}쪽.\n'
 for s in rows[a-1:b]:t+=f"\n## {s['page']}쪽 {s['title']}\n\n{s['note']}\n\n근거: "+' · '.join(s['sources'])+'\n'
 (U/f'part-{i}.md').write_text(t,encoding='utf8')
(U/'part-5.md').write_text('# 현재 제외된 구간\n\n기본 지식 10장 구성에는 Part 5와 제작 사례·레퍼런스·검토·실습 구간이 없다. 이전 문서는 history/foundations-before-knowledge-only-20261028/에 보존했다.\n',encoding='utf8')
lead='''## 최신 범위 — 모션 그래픽 자체의 기본 지식만 2026-10-28

사용자는 모션 그래픽 지식과 종류만 남기고 프롬프트와 영상 제작 시 고려사항을 모두 제외하라고 정정했다. 현재 기준은 단원 plan.md·design.md와 output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_10장_v2.pptx 및 PDF다. 뜻·프레임·종류·속성·효과 이름·지속시간·이징·용어 구분만 남긴다. 기본 개념의 GIF·네이티브 효과와 브랜드 디자인은 유지한다. 제작 실습뿐 아니라 홍보/웹사이트/원자모형 사례, 목적별 고려사항, 레퍼런스 분석, 읽는 시간/가독성/일관성 검토, 추천 상황, 제작 조언도 넣지 않는다. 아래 22장·27장·48장 구성은 이력이며 현재 범위로 다시 확장하지 않는다. lesson.md 원문·기본 하네스 구조·G10 상태는 보존한다.

'''
ap=R/'AGENTS.md';txt=ap.read_text(encoding='utf8')
if not txt.startswith(lead.split('\n')[0]):ap.write_text(lead+txt,encoding='utf8')
print('Updated scope and unit documents to basic knowledge only.')
