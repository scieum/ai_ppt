from pathlib import Path
import copy,json,sys,tempfile
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'harness'))
from test_training import fixture
from gate import read,save,plan
out=root/'harness/templates/ai-training'
out.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as temp:
    e=fixture(Path(temp))
    p=plan(e.unit)
    inp=read(e.unit/'input.json')
for d in [inp,p]:
    d.update(unit='AI-001_안내문 초안 만들기',audience='AI 채팅 도구를 처음 사용하는 성인',
             environment={'product':'선택한 AI 도구명','version':'제작일 확인 필요','os':'Windows',
                          'ui_language':'한국어','account':'사용 계정과 요금제 확인 필요'},
             objectives=[{'id':'O1','action':'일정 메모로 안내문 초안을 만들고 원문과 대조한다','result':'검토한 안내문 텍스트'}],
             branding={'mode':'text','label':'강사명 입력','logos':[]})
p['exercises'][0].update(title='안내문 초안 작성과 대조', start_conditions='선택한 도구에 로그인하고 일정 메모 열기',
    input_location='AI 도구의 새 대화 입력창', instructions=['일정 메모와 프롬프트를 입력한다','출력의 날짜·대상·장소를 원문과 비교한다'],
    expected_result='일정 메모에 근거한 안내문 초안', success_criteria=['날짜·대상·장소가 원문과 일치한다'],
    errors=[{'symptom':'필수 정보 누락','check':'원문과 출력 비교','action':'누락한 항목을 지정해 다시 요청','expected_state':'필수 정보가 모두 포함된 초안'}],
    fallback='강사가 제공한 중간 완성본으로 결과 비교 활동에 합류', customization='자신의 행사 일정으로 메모 교체')
titles=['오늘의 결과물','실습 흐름','수행 목표','진행 순서','입력 자료와 화면','안내문 초안 작성','초안 대조와 수정']
for i,s in enumerate(p['slides']):
    s.update(title=titles[i],message=titles[i]+'의 핵심 메시지 작성',instructor_action='이 페이지의 설명·조작 작성',learner_action='이 페이지에서 수행할 행동 작성')
save(out/'input.json',inp)
(out/'plan.md').write_text('# 강의별 계획 양식\n\n이 파일은 편집용 예시이며 실제 제작 승인·검증 기록이 아니다.\n\n시간과 페이지를 실제 강의에 맞게 수정하고 출처·실습 파일·대표 시안을 준비한다. 승인 증빙은 실제 사용자 응답 이후에만 만든다.\n\n```harness-plan\n'+json.dumps(p,ensure_ascii=False,indent=2)+'\n```\n',encoding='utf-8')
save(out/'sources.json',[{'id':'S1','role':'content','citation':'제공할 일정 메모의 파일명','locator':'해당 위치',
                         'evidence':{'path':'research/source-extract.txt','sha256':'실제 파일 해시로 교체'}},
                        {'id':'D1','role':'design','citation':'선택한 디자인 레퍼런스','locator':'PDF 쪽/PPTX 장',
                         'evidence':{'path':'research/design-extract.txt','sha256':'실제 파일 해시로 교체'}}])
save(out/'content-map.json',[{'id':'C1','kind':'task','scope':'기본','claim':'제공 메모의 정보로 초안을 작성하고 대조한다',
                             'rationale':'수행 목표 O1의 실습 과제','source_ids':['S1'],'objective_ids':['O1']}])
print('Exported editable templates without approvals, verified evidence, or generated deliverables.')
