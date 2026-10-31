from pathlib import Path
from copy import deepcopy
import re,json
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
plan=U/'plan.md';old=plan.read_text(encoding='utf8');hist=U/'history/plan-before-full-webinar-20261028.md';hist.parent.mkdir(parents=True,exist_ok=True)
if not hist.exists():hist.write_text(old,encoding='utf8')
j=json.loads(re.search(r'```harness-plan\s*(\{.*?\})\s*```',old,re.S).group(1));oldslides={x['number']:x for x in j['slides']}
idx=json.loads((B/'page-index.json').read_text(encoding='utf8'));adds=json.loads((B/'additions.json').read_text(encoding='utf8'));byadd={r['page']:r for r in adds}
mapping=[1,1,3,5,5,6,7,8,9,10,11,12,13,13,14,14,15,15,16,17,18,19,20,20,22,21,23,25,24,27,26,28,29,31,32,33,34,36,37,37,39,40,41,43,44,45,47,48]
minutes=[.5,1.5,3,1,.5,2,1,1.5,1.5,1.5,1,1,2,2,2,2,2.5,2.5,2,.5,1.5,1.5,1.5,1.5,1.5,2,.5,2,1.5,1.5,1.5,1.5,1.5,1,2,2,3,2,2,2,1,2,3,2,2,2.5,2.5,10]
assert len(minutes)==48 and sum(minutes)==90
def stage(n):return 0 if n<=3 else 1 if n<=19 else 2 if n<=26 else 3 if n<=33 else 4 if n<=40 else 5 if n<=45 else 6
actions={0:'필수·선택 계정과 준비물을 확인한다',1:'기초 시연을 보거나 세 사례 중 하나로 첫 요청을 작성한다',2:'참고할 조건 두 가지와 이유를 적고 같은 초안에 적용한다',3:'바꿀 조건과 유지할 조건을 골라 한 번의 수정으로 비교한다',4:'세 Markdown 파일을 자기 주제에 맞게 수정하고 실제 작업에 참조한다',5:'현재 도구 조건·작업 상태·실제 파일을 구분해 확인하거나 시연을 관찰한다',6:'다음 작업에 가져갈 파일과 요청을 정리하고 질문한다'}
slides=[]
for page in range(1,49):
 row=deepcopy(oldslides[mapping[page-1]]);row['number']=page;row['title']=idx[page-1]['title'];row['message']=row['title'];row['minutes']=minutes[page-1];row['learner_action']=actions[stage(page)];row['instructor_action']='해당 장표의 설명·예시·요청을 연결해 제시하고 '+actions[stage(page)]
 row['layout']='기존 대표본과 Part 1 수정본의 검정·흰색·주황·Pretendard·원본 노션톡 로고·푸터를 유지한다. 현재 48장 전체본의 실제 배치를 따른다. 관련 내용은 같은 묶음 번호를 쓴다.'
 if stage(page)==0:row['exercise_ids']=[];row['content_ids']=['C00']
 elif page<=11:row['exercise_ids']=['EX00'];row['content_ids']=['C01'];row['objective_ids']=['O0']
 elif page<=19:row['exercise_ids']=['EX01'];row['content_ids']=['C01'];row['objective_ids']=['O1']
 elif page<=26:row['exercise_ids']=['EX02'];row['content_ids']=['C02'];row['objective_ids']=['O2']
 elif page<=33:row['exercise_ids']=['EX03'];row['content_ids']=['C03'];row['objective_ids']=['O3']
 elif page<=40:row['exercise_ids']=['EX04'];row['content_ids']=['C04'];row['objective_ids']=['O4']
 elif page<=45:row['exercise_ids']=['EX05'];row['content_ids']=['C05'];row['objective_ids']=['O5']
 else:row['exercise_ids']=['EX06'] if page<48 else [];row['content_ids']=['C06']
 if page==1:row['design_type']='cover'
 if page in [2,46]:row['design_type']='contents'
 if page in [21,25,28,33,37,39,40,45]:row['design_type']='brief'
 slides.append(row)
j['slides']=slides;j['target_slides']=48;j['minutes']=90;j['break_minutes']=0
j['environment']['version']='2026-10-28 강의 설계 기준. 새 인앱 실행·외부 생성·MP4 출력은 미검증이며 강의 전 현재 환경에서 확인한다.'
j['environment']['product']='코덱스 또는 클로드 중 선택한 유료 환경. 외부 제작 도구는 선택이며 현재 지원·연결 상태 확인 후 시연한다.'
j['environment']['ui_language']='한국어 설명과 요청문. 확인하지 않은 앱 메뉴·실행 결과를 생성 화면처럼 표시하지 않는다.'
for o in j['objectives']:
 if o['id']=='O1':o['action']='홍보 타이포그래피·웹사이트 소개·수업 보조 영상 중 한 사례를 선택해 첫 요청과 수정 조건을 기록한다'
 if o['id']=='O4':o['action']='수업 보조 영상의 목적·표현 규칙·장면표를 세 Markdown 파일로 정리하고 문구·시간·근거를 대조한다';o['result']='세 Markdown 파일과 참조·수정 기록'
for ex in j['exercises']:
 totals={'EX00':10,'EX01':16,'EX02':10,'EX03':10,'EX04':14,'EX05':10,'EX06':5}
 if ex['id'] in totals:ex['minutes']=totals[ex['id']]
 for k in ['title','input_location','expected_result','customization']:
  if isinstance(ex.get(k),str):ex[k]=ex[k].replace('역사 설명','수업 보조 영상의 시계열 설명').replace('과학사 영상','수업 보조 영상')
summary='''# 모션 그래픽을 이용한 수업 영상 제작하기

2026-10-28 · NotionTalk · 전체 48장 · 90분 제안

## 현재 결과물

[전체 PPT](../../output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx) · [배포 PDF](../../output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pdf) · [강사용 Word 원고](../../output/webinar-complete/NotionTalk_전체웨비나_강사용진행원고.docx) · [실습 자료 폴더](../../output/webinar-complete/실습자료)

기존 21장 수정본의 장표·원본 미디어·발표자 노트·효과는 보존하고 27장을 추가했다. 기존 1~19쪽은 같은 위치, 기존 20쪽은 전체 34쪽, 기존 21쪽은 전체 41쪽이다. 표지의 세 캐릭터·주황 그라데이션, 노션톡 원본 로고·푸터, 6쪽의 일반 활용 예, 8쪽 노션톡·9쪽 하늘색 문구, C의 수업 보조 영상·시계열 예시 표현을 유지한다. 삭제한 학생 관점 체크리스트를 복구하지 않는다.

이번 완성 범위는 강의 장표와 진행 원고·실습 문서다. 실제 인앱 캡처·새 앱 생성 결과·외부 서비스 생성 영상·MP4 출력·리허설 완료를 대신하지 않는다. 강의 화면의 장면 설계·시간표·합성 정지 예시는 실제 결과와 구분했다. G10 권리 검토 상태와 기존 승인 이력은 그대로 유지한다.

## 강의 흐름과 시간

| 구간 | 실제 쪽 | 시간 | 참가자가 할 일 |
|---|---:|---:|---|
| Part 0 준비물 | 1~3 | 5분 | 코덱스 또는 클로드 유료 계정, 외부 도구 선택 조건 확인 |
| Part 1 기초와 첫 요청 | 4~19 | 26분 | 기초 이해 10분, 한 사례 선택·첫 요청·관찰 16분 |
| Part 2 레퍼런스 | 20~26 | 10분 | 참고할 조건 두 가지와 이유를 골라 같은 초안에 적용 |
| Part 3 모션 지식 적용 | 27~33 | 10분 | 읽는 시간·강조·순서·속도 중 한 조건 수정 |
| Part 4 Markdown 문서 | 34~40 | 14분 | 목적·규칙·네 장면 시간표 작성과 한 행 수정 |
| Part 5 외부 소재 | 41~45 | 10분 | 소재 한 장면 선택·요청·상태·실제 파일·합성 경로 확인 |
| 마무리와 질의응답 | 46~48 | 15분 | 문서와 다음 요청 저장, 질문 10분 |

합계 90분. 생성 완료 시간을 보장하는 시간표는 아니며 리허설 전 진행안이다. 세 사례를 모두 생성하도록 요구하지 않고 하나를 먼저 만들며 다른 사례는 관찰한다. 외부 계정이 없으면 시연을 본다. 생성 대기에는 같은 입력의 사전 예시로 이어 가되 현재 실행과 구분한다.

## 다루는 사례

- A: 노션톡 무료 웨비나 홍보 타이포그래피 20초. 필수 문구·일정과 마지막 안내 4초를 연결한다.
- B: Notion 공식 페이지 내용의 30초 소개. 원문 접근·내용의 대응과 새 장면 구성을 구분한다.
- C: 수업 보조 영상 45초. 원자모형 변천은 시간의 흐름을 보여 주는 시계열 설명의 구체 예시다.

표현 형식·입력 방법·활용 목적은 같은 분류가 아니며 한 영상에 여러 표현을 조합할 수 있다.

## 문서와 번호 체계

Part 1은 01 이해하기, 02 움직임과 효과, 03 제작 예제, 04 적용으로 묶는다. Part 2와 Part 3은 각각 두 의미 묶음, Part 4는 목적·규칙 / 장면표·다시 제작 / 재사용, Part 5는 소재·요청 / 합성·상태로 묶는다. 장표마다 숫자를 계속 늘리지 않는다.

상세 설명은 [Part 1](part-1.md), [Part 2](part-2.md), [Part 3](part-3.md), [Part 4](part-4.md), [Part 5](part-5.md)에 있다. 실습 자료의 LESSON_BRIEF.md·VISUAL_RULES.md·SCENE_PLAN.md·수정 시간표·PROMPTS.md를 실제 작업에서 참조한다. 파일 존재와 실제 반영을 구분한다.

## 근거와 원본 보호

기존 `lesson.md`의 영상 6편 자막·설명란 분석과 제공 PDF 7편의 설명·비교·요청 연결 원리를 참고했다. 문구·예제·시간 설계는 자체 작성했다. 원본 PDF·음악·영상의 장면을 새 자산으로 추출하지 않았다. 기존 추출 배경과 브랜드·캐릭터의 권리 상태는 별도 검토 상태다. 새 추상 배경의 생성 프롬프트는 `assets/webinar-full/20261028/provenance.json`에 남겼다.

검수 기록은 `checks/full-webinar-20261028/`에 있다. 원본 대표 5장·직전 21장 파일은 덮어쓰지 않았다. 이전 계획 원문은 `history/plan-before-full-webinar-20261028.md`에 보존했다. 아래 실행 데이터는 실제 48쪽·90분 구성에 맞췄으며, 현재 계획 해시의 승인이나 G10 통과 증빙을 자동 생성하지 않는다.

## 실제 페이지 계획

| 쪽 | 분 | 제목 |
|---:|---:|---|
'''
for row in slides:summary+=f"| {row['number']} | {row['minutes']:g} | {row['title']} |\n"
summary+='\n## 하네스 실행 데이터\n\n```harness-plan\n'+json.dumps(j,ensure_ascii=False,indent=2)+'\n```\n'
plan.write_text(summary,encoding='utf8')
newnotes={r['page']:r for r in json.loads((B/'new-notes.json').read_text(encoding='utf8'))}
stages={2:(20,26,10,'레퍼런스로 방향 잡기'),3:(27,33,10,'첫 결과의 움직임 다듬기'),4:(34,40,14,'Markdown 제작 문서'),5:(41,45,10,'외부 소재 확장')}
for num,(start,end,time,title) in stages.items():
 md=f'# Part {num} {title}\n\n2026-10-28 · NotionTalk · 실제 전체 PPT {start}~{end}쪽 · {time}분 제안\n\n현재 전체본은 [48장 PPT](../../output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx)와 PDF다. 전체 흐름과 시간은 [계획](plan.md)을 따른다. 실제 앱 실행 결과·외부 생성·MP4 출력과 장면 설계 예시를 구분한다.\n\n'
 for page in range(start,end+1):
  md+=f"## {page}쪽 {idx[page-1]['title']}\n\n"
  if page in newnotes:md+=newnotes[page]['body']+'\n\n'
  else:md+='기존 대표 장표의 디자인과 설명을 보존했다. 이 파트의 역할과 다음 요청으로 연결한다.\n\n'
 md+='복사 가능한 요청과 문서는 [실습 자료](../../output/webinar-complete/실습자료)에 있다. 디자인 승인과 G10 권리 검토 증빙은 이번 문서 작성으로 생성하지 않는다.\n';(U/f'part-{num}.md').write_text(md,encoding='utf8')
p=U/'part-1.md';t=p.read_text(encoding='utf8');lead='## 전체 48장 반영\n\n최신 강의는 [48장 전체 PPT](../../output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx)와 PDF다. Part 1의 4~19쪽은 최신 21장 수정본 그대로 유지했다. 기존 뒤 대표 장표 20·21쪽은 전체 34·41쪽으로 이동했다. 아래의 21장 링크·쪽수는 Part 1 수정 이력이다.\n\n';first=t.find('\n\n');t=t[:first+2]+lead+t[first+2:];p.write_text(t,encoding='utf8')
print('Synchronized the full 48-slide / 90-minute plan and Part 2–5 documents without creating approval evidence.')
