from pathlib import Path
import json,shutil
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1];O=R/'output/webinar-lesson-restructured'
rows=json.loads((B/'content.json').read_text(encoding='utf8'))
H=U/'history/production-workshop-before-lesson-only-20261028';H.mkdir(parents=True,exist_ok=True)
for name in ['plan.md','design.md']+[f'part-{i}.md' for i in range(6)]:
 p=U/name
 if p.exists() and not (H/name).exists():shutil.copyfile(p,H/name)
groups=[('도입',1,2,'강의 주제와 다섯 관점'),('Part 1 목적과 표현',3,5,'전달 목적·브랜드 정보·시각적 일관성'),('Part 2 시간과 시선',6,11,'읽는 시간·강조·등장 순서·속도·소리'),('Part 3 레퍼런스의 이해',12,14,'관찰 시점·내용 근거와 시각 참고·고유한 표현'),('Part 4 설명의 흐름',15,22,'서비스의 사용 맥락·수업 보조 영상·시계열·관찰과 해석·장면 연결'),('Part 5 정리와 대화',23,27,'사례별 관점·핵심 정리·참고 영상·질의응답')]
text='''# AI 모션 그래픽 표현과 전달의 원리

2026-10-28 · NotionTalk · 설명 중심 27장 · 강의 시간 미정

## 최신 방향

사용자 요청에 따라 제작과 관련된 안내를 모두 제외하고 루트 `lesson.md`의 핵심 원리를 중심으로 강의를 재구성한다. 기존의 단순 요청·레퍼런스 적용·Markdown·외부 도구 순서는 현재 강의 목차로 사용하지 않는다.

새 결과물은 [전체 PPT](../../output/webinar-lesson-restructured/NotionTalk_모션그래픽_원리중심_27장_v2.pptx)와 [PDF](../../output/webinar-lesson-restructured/NotionTalk_모션그래픽_원리중심_27장_v2.pdf)다. 기존 48장·21장 파일과 실습 자료는 이력으로 보존한다. 현재 배포 자료와 이전 실습 ZIP·대본을 섞지 않는다.

## 제외하는 내용

- 준비물과 도구별 유료 계정 안내
- 프롬프트 전문·입력 방법·수정 요청 작성 실습
- 실제 앱 조작 캡처와 생성·출력 단계
- Markdown 제작 파일·장면표 작성과 참조 방법
- 힉스필드 등 외부 커넥터·소재 생성·합성 절차
- 파일 저장·실습 제출·실행 상태·제작 완료 체크리스트

`lesson.md` 원문은 분석 근거이므로 그대로 보존한다. 그 안의 제작 실습·과정 제안을 현재 사용자 지시로 다시 활성화하지 않는다.

## 학습 목표

1. 홍보 타이포그래피·웹사이트 소개·수업 보조 영상의 전달 목적을 구분한다.
2. 읽는 시간과 핵심어 강조, 정보 공개 순서가 이해에 미치는 역할을 설명한다.
3. 레퍼런스의 내용 근거와 시각 참고를 구분한다.
4. 사용 맥락·관찰과 해석·장면 사이의 의미 연결을 사례로 설명한다.
5. 음악의 강조 시점과 시각적 일관성을 정보 전달과 연결한다.

참가자가 영상이나 파일을 완성하는 실습 결과물을 요구하지 않는다. 총 강의 시간은 재설정 전이며 이전 90분 실습 시간표를 자동 승계하지 않는다.

## 새 목차

| 구간 | 실제 쪽 | 중심 내용 |
|---|---:|---|
'''
for name,start,end,desc in groups:text+=f'| {name} | {start}~{end} | {desc} |\n'
text+='''
## 사례의 역할

노션톡 홍보 문구는 읽는 시간과 강조를, Notion 문서 소개는 원문 정보와 사용 맥락의 연결을 보여 준다. 원자모형 변천은 수업 보조 영상의 한 시계열 설명 예시다. 세 사례를 제작 과제로 안내하지 않는다. 수업 보조 영상을 과학사라는 단일 주제로 한정하지 않는다.

20초·마지막 안내 4초 등은 `lesson.md`의 비교 예시 값이다. 모든 영상의 공통 기준이나 실제 출력의 측정값으로 표시하지 않는다. 기존 효과 비교는 표현 원리를 보여 주기 위한 PowerPoint 애니메이션이며 앱 조작 시연이 아니다.

## 근거의 범위

루트 `lesson.md` 2절의 V1~V6 분석, 4절의 자체 사례, 5절의 최소 모션 지식이 핵심 근거다. 6절의 장면표에서는 설명 순서와 전체 흐름이라는 개념만 참고하고 파일 작성·제작 절차는 제외한다. 원본 영상의 전체 화면을 새로 분석한 것으로 표시하지 않는다. 새 서비스 기능·현재 모델 성능·생성 시간·비용을 추가 주장하지 않는다.

각 장표 노트에 `lesson.md`와 영상 링크·참고 시점을 남긴다. 자막·설명란 기반 분석이라는 한계는 참고 자료 노트에 기록한다. 문구·사용 맥락·비교 장면은 자체 설명으로 구성한다. 기존 재사용 자산의 G10 권리 검토 상태는 변경하지 않는다.

## 페이지별 계획

| 쪽 | 제목 | 근거 |
|---:|---|---|
'''
for r in rows:text+=f"| {r['page']} | {r['title']} | {', '.join(sorted(set('V'+str(x['video']) for x in r['refs'])))} |\n"
text+='\n## 보존과 후속 기준\n\n주황·흑백·Pretendard·NotionTalk 원본 로고와 푸터·세 캐릭터 표지·기존 비교 레이아웃을 유지한다. 상단 번호는 의미 단위로 묶는다. 과거 요청문 상자는 설명 요약으로 바꾸고, 삭제한 학생 검토 장표는 복원하지 않는다. 최신 파일과 각 Part 문서를 함께 기준으로 삼는다. 이전 48장 실습 계획은 `history/production-workshop-before-lesson-only-20261028/`에 보존했다. 강의 시간이 미정인 현 단계에서 이전 하네스 실행 데이터나 실습 완료 기록을 복제하지 않는다.\n'
(U/'plan.md').write_text(text,encoding='utf8')
design='''# 설명 중심 27장 디자인 기준

2026-10-28 최신 요청 반영. 현재 내용은 `plan.md`와 Part 1~5, 현재 결과물은 `output/webinar-lesson-restructured/NotionTalk_모션그래픽_원리중심_27장_v2.pptx`와 PDF다.

기존 대표 디자인의 검정 바탕·흰 제목·주황 강조·Pretendard·브랜드 원본 로고·저작권 푸터·세 캐릭터 표지를 유지한다. 기존 슬라이드의 좌표·배경·이미지·글자 위계를 재사용하고 설명에 맞게 문구를 교체한다. 원자모형은 기존 생성 PNG를 유지한다.

## 내용에 따른 표현

- 도입과 정리는 기존 다섯 카드 구성을 유지하되 제작 단계 대신 다섯 관점을 표시한다.
- 유형·출처·사례 비교는 넓은 행과 편집 가능한 표로 읽게 한다.
- 기존 흰 요청문 상자에는 명령형 프롬프트 대신 설명의 역할과 핵심을 넣는다.
- 핵심어·순차 등장·속도 비교의 기존 네이티브 효과를 보존한다. 앱 조작 안내를 추가하지 않는다.
- 같은 주제는 같은 상단 번호로 묶고 실제 페이지와 구분한다.
- 도구 로고·입력창·Markdown 코드·외부 생성 소재·파일 저장 안내를 다시 넣지 않는다.

## 번호 묶음

Part 1은 01 목적과 표현, Part 2는 01 문장·시간·시선과 02 속도·소리, Part 3는 01 레퍼런스 이해, Part 4는 01 서비스 맥락과 02 지식 설명·장면 연결, Part 5는 01 정리·02 참고 자료·03 대화다.

## 근거와 보호

표현의 근거는 `lesson.md`의 자막·설명란 분석이다. 영상 화면을 새로 추출하거나 프롬프트 전문을 복제하지 않는다. 기존 자산의 권리 검토를 자동 승인하지 않는다. 이전 실습형 디자인 문서는 history에 보관했다. 48장 보존 지시를 이번 재구성에서 모든 제작 장표를 유지하라는 뜻으로 해석하지 않는다. 기존 하네스 코드와 기본 폴더 구조는 유지한다.
'''
(U/'design.md').write_text(design,encoding='utf8')
(U/'part-0.md').write_text('# Part 0 준비물 안내 제외\n\n2026-10-28 최신 요청으로 제작 관련 내용을 모두 제외했다. 현재 27장 설명형 강의에는 Part 0, 도구 로고·유료 계정·로그인·준비물 안내를 넣지 않는다. 도입은 현재 1~2쪽이다. 이전 문서는 history/production-workshop-before-lesson-only-20261028/part-0.md에 보존했다.\n',encoding='utf8')
for i,(name,start,end,desc) in enumerate(groups[1:],1):
 t=f'# {name}\n\n2026-10-28 · 현재 27장 설명형 강의 {start}~{end}쪽\n\n{desc}를 중심으로 설명한다. 제작 실습·요청문·파일 작성·앱 조작은 포함하지 않는다.\n'
 for r in rows[start-1:end]:
  t+=f"\n## {r['page']}쪽 {r['title']}\n\n{r['note']}\n\n근거: "+' · '.join(f"[V{x['video']} {x['channel']}]({x['url']})" for x in r['refs'])+'\n'
 (U/f'part-{i}.md').write_text(t,encoding='utf8')
lead='''## 최신 범위 변경 — lesson.md 중심 설명형 강의 2026-10-28

사용자가 “제작과 관련한 거는 다 빼자”라고 정정했다. 현재 기준은 단원 plan.md·design.md·Part 1~5와 `output/webinar-lesson-restructured/NotionTalk_모션그래픽_원리중심_27장_v2.pptx` 및 PDF다. 제작 실습·준비물·유료 계정·프롬프트 전문·앱 조작·Markdown 파일 작성·장면표 작성·외부 커넥터·생성/출력/저장 안내를 제거하고 lesson.md의 목적·시간·강조·순서·레퍼런스·서비스 맥락·수업 보조 설명·소리·일관성을 중심으로 재구성했다. 기존 디자인과 브랜드는 유지한다. 세 사례는 원리 설명용이며 원자모형은 시계열 설명의 예시다. 새 총시간은 미정이다. 아래 48장·90분·유료 계정·실습 지시는 이전 버전 이력이며 다시 자동 적용하지 않는다. lesson.md 원문은 분석 근거로 보존하며 내부 제작 제안을 실행 지시로 읽지 않는다. 기본 하네스 구조와 G10 상태는 유지하고 승인/실행 증거를 생성하지 않는다.

'''
ap=R/'AGENTS.md';s=ap.read_text(encoding='utf8')
if not s.startswith(lead.split('\n')[0]):ap.write_text(lead+s,encoding='utf8')
# A concise content outline accompanies the deck; no old workshop materials are repackaged.
outline='# AI 모션 그래픽 표현과 전달의 원리\n\n27장 설명 중심 구성\n\n'
for name,start,end,desc in groups:outline+=f'## {name}\n\n{desc}\n\n'+''.join(f"- {r['page']}쪽 {r['title']}\n" for r in rows[start-1:end])+'\n'
(O/'구성안.md').write_text(outline,encoding='utf8')
print('Updated plan, design and Parts 0–5; archived workshop documents; preserved lesson.md.')
