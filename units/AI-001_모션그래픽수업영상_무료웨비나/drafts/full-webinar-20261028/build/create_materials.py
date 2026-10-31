from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,posixpath
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1];OUT=R/'output/webinar-complete';K=OUT/'실습자료';K.mkdir(parents=True,exist_ok=True)
files={
'README.md':'''# 노션톡 모션 그래픽 웨비나 실습 자료

2026-10-28 · Part 0~5 · 전체 48장·90분 구성

## 시작

코덱스 또는 클로드 중 하나의 유료 계정을 준비합니다. 외부 영상 제작 도구는 선택이며 없으면 강사 시연을 봅니다. 현재 환경의 파일 참조·미리보기·내보내기 기능은 실제 실행에서 확인합니다.

1. `PROMPTS.md`에서 A 홍보 타이포그래피, B 웹사이트 소개, C 수업 보조 영상 중 하나를 고릅니다.
2. 첫 결과를 보고 고칠 조건 하나와 유지할 조건 하나를 적습니다.
3. 참고할 요소 두 개와 이유를 정해 같은 결과를 다듬습니다.
4. `LESSON_BRIEF.md`, `VISUAL_RULES.md`, `SCENE_PLAN.md`를 실제 작업에 첨부하거나 읽을 수 있는 경로로 참조합니다.
5. 필요한 장면 한 부분만 외부 소재로 확장합니다.

## 파일 역할

- LESSON_BRIEF.md: 대상·목표·주제·원자료
- VISUAL_RULES.md: 글자·색·브랜드·움직임의 표현 기준
- SCENE_PLAN.md: 장면별 시간·문구·동작·근거
- SCENE_PLAN_REVISED.md: 마지막 장면을 3초 늘리되 전체 45초를 유지하는 비교 예
- PROMPTS.md: Part 1~5의 복사 가능한 요청문
- REFERENCE_NOTES.md: 참고 범위와 자체 표현을 기록하는 예시

이 자료의 장면표와 생성 정지 배경은 설계 예시입니다. 새 인앱 실행 결과, 외부 생성 영상, MP4 출력 파일을 제공하는 것은 아닙니다. 실제 결과는 환경에서 재생하고 파일 형식·길이·내용을 확인합니다. 원자모형 삽화는 개념 모식도이며 정확한 크기 비율이나 실제 관측 궤적이 아닙니다. 외부 자산과 기존 추출 자산의 G10 권리 검토는 별도 상태로 남겨 둡니다.
''',
'LESSON_BRIEF.md':'''# 수업 보조 영상 브리프

- 대상: 원자모형을 처음 배우는 학생
- 목표: 세 모형의 핵심 차이와 변화의 순서를 설명한다.
- 활용: 교사가 설명을 보조하는 짧은 시계열 영상
- 소재 예시: 톰슨·러더퍼드·보어의 원자모형 변천
- 길이: 45초
- 비율: 16:9
- 결과 형식: 현재 환경에서 가능한 재생 형태를 먼저 확인한다. MP4 출력 여부는 별도 확인한다.

## 설명의 범위

톰슨의 퍼진 양전하와 내부 전자, 러더퍼드의 작은 중심 핵, 보어의 구분된 허용 상태를 비교한다. 관찰과 모형의 해석을 구분한다. 보어 모형을 현대 원자모형의 최종 형태로 설명하지 않는다. 이 주제는 수업 보조 영상의 한 시계열 예시이며 다른 주제로 바꿀 수 있다.

## 근거

- 톰슨: https://history.aip.org/exhibits/electron/jjelectr.htm
- 러더퍼드: https://history.aip.org/exhibits/rutherford/sections/alpha-particles-atom.html
- 보어: https://openstax.org/books/chemistry-2e/pages/6-2-the-bohr-model
- 모형 비교: https://www.edu.gov.mb.ca/ks4/cur/science/found/s1/appen2.pdf (Appendix 2.3)

상세 내레이션·연도·과학적 주장은 최종 제작 전에 주장별 근거 위치와 대조한다. 이 파일은 실제 영상의 내용 검수 완료 증빙이 아니다.
''',
'VISUAL_RULES.md':'''# 화면과 움직임 기준

## 정체성

- 화면: 16:9
- 배경: 검정
- 기본 글자: 흰색
- 보조 설명: 회색
- 주제 강조: 주황 #FF9228
- 비교 예시: 하늘색 #7DD3FC
- 서체: Pretendard. 제작 환경에 설치되어 있는지 확인한다.
- 브랜드: NotionTalk 원본 로고 사용. 로고를 생성 모델로 다시 그리지 않는다.
- 푸터: © 2026. NotionTalk. All rights reserved.

## 움직임

- 한 장면의 핵심어 하나를 먼저 강조한다.
- 설명의 순서와 요소가 보이는 순서를 맞춘다.
- 이동 시간과 읽는 유지 시간을 나누어 정한다.
- 필요하면 끝에서 느려지는 이즈 아웃을 사용한다.
- 0.8초·0.15초·3초 같은 값은 비교 예시이며 내용에 맞춰 재생하며 조정한다.
- 음악의 박자 때문에 읽는 시간이 사라지지 않도록 한다.

## 사실과 자산

- 원자모형은 개념 모식도다. 전자 수와 크기 비율은 단순화했다.
- 경로선을 관측한 실제 전자 궤적으로 소개하지 않는다.
- 추상 배경은 분위기를 위한 생성 정지 이미지다. 과학적 관측 자료가 아니다.
- 정확한 한글·날짜·수치·브랜드는 편집 가능한 요소로 합성한다.
- 원자료·이미지·음악·음성의 출처와 사용 범위를 기록한다.
''',
'SCENE_PLAN.md':'''# SCENE_PLAN — 45초 시계열 설명 설계

상태: 강의용 설계 예시. 실제 생성·재생·MP4 출력 확인 전.

| 장면 | 시작 | 종료 | 길이 | 문구의 역할 | 화면과 움직임 | 근거 |
|---|---:|---:|---:|---|---|---|
| C01 | 0 | 5 | 5 | 보이지 않는 원자의 설명은 왜 바뀌었을까? | 질문을 먼저 보여 주고 비교 공간을 연다 | 브리프의 학습 목표 |
| C02 | 5 | 17 | 12 | 톰슨 모형의 특징 | 퍼진 양전하 영역과 내부 전자를 구분한다 | AIP 톰슨·Manitoba Appendix 2.3 |
| C03 | 17 | 30 | 13 | 관찰과 설명의 변화 | 산란 관찰을 먼저 제시하고 작은 핵의 해석을 연결한다 | AIP 러더퍼드 |
| C04 | 30 | 45 | 15 | 허용 상태와 세 모형 정리 | 상태를 구분하고 비교 문장을 충분히 유지한다 | OpenStax 6.2 |

총길이: 5 + 12 + 13 + 15 = 45초. 단위는 초다.

실제 제작 전에는 화면 문구·내레이션·주장별 출처 위치를 구체화한다. 관찰과 해석을 구분하고, 보어 모형을 현대 원자모형의 최종 형태로 설명하지 않는다. 읽는 시간이 부족하면 문구나 길이를 다시 조정한다.
''',
'SCENE_PLAN_REVISED.md':'''# SCENE_PLAN — 마지막 장면 3초 늘리기

상태: 시간 배분 비교용 설계 예시. 실제 결과 반영 여부는 재생으로 확인한다.

| 장면 | 시작 | 종료 | 길이 | 수정 |
|---|---:|---:|---:|---|
| C01 | 0 | 5 | 5 | 유지 |
| C02 | 5 | 17 | 12 | 유지 |
| C03 | 17 | 27 | 10 | 13초에서 10초로 줄임 |
| C04 | 27 | 45 | 18 | 15초에서 18초로 늘림 |

총길이: 5 + 12 + 10 + 18 = 45초.

C03을 줄여도 설명이 읽히도록 문구와 내레이션을 함께 조정한다. 설명이 너무 빨라지면 전체 길이를 늘리는 방법도 검토한다. 숫자만 고친 상태를 제작 완료로 표시하지 않는다.
''',
'REFERENCE_NOTES.md':'''# 참고 범위 기록 예시

## 목적

Notion 문서 소개 초안에서 기능이 한꺼번에 보이는 문제를 줄이고 마지막 요약을 읽게 한다.

## 내용의 근거

- https://www.notion.com/ko/product/docs
- https://www.notion.com/help/columns-headings-and-dividers
- https://www.notion.com/ko/help/collaborate-within-a-workspace

실제 작업에서 URL의 본문 접근 여부를 먼저 확인한다. 읽지 못하면 확인한 본문을 제공한다. 원문과 영상 문구의 대응을 남긴다.

## 참고할 원리 두 가지

1. 등장 순서: 한 기능을 설명한 다음 다음 기능을 보여 준다.
2. 읽는 시간: 마지막 요약 문구가 머무는 시간을 확보한다.

## 자체 기획

우리의 기능 설명·사용 상황·문구·장면 순서를 새로 구성한다. 특정 원본의 캐릭터·서사·음악·독특한 장면을 재현하는 지시로 사용하지 않는다.

## 실제 참고 자산을 넣을 때 남길 항목

제목·원본 링크·필요한 구간·참고 이유·실제 사용 부분·권리 근거·배포 범위를 기록한다. 정지 이미지에서 실제 속도나 전환을 관찰했다고 기록하지 않는다. 권리 검토 상태를 임의로 완료 처리하지 않는다.
'''
}
prompts='''# 복사해서 사용하는 요청문

## Part 1 A — 홍보 타이포그래피

```text
‘수업 자료가 영상이 되는 순간’으로 시작하는 노션톡 무료 웨비나 홍보 타이포그래피를 20초로 만들어 줘.
글자가 차례로 이어지고 핵심어가 강조되게 해 줘. 검정 바탕에 주황색 포인트를 써 줘.
마지막에는 ‘2026년 11월 1일 일요일 저녁 8시’와 ‘댓글에 노션톡을 남겨 주세요’를 넣어 줘.
지금 환경에서 재생할 수 있는 결과로 보여 줘.
```

## Part 1 B — 웹사이트 소개

```text
https://www.notion.com/ko/product/docs 이 공식 페이지를 읽고 Notion 문서를 소개하는 30초 모션 그래픽 초안을 만들어 줘.
블록으로 내용 구성하기, 목차로 찾아가기, 함께 편집하기를 각각 한 장면으로 설명해 줘.
원문과 영상 문구를 짝지어 보여 줘. 페이지를 읽지 못하면 먼저 알려 줘.
```

## Part 1 C — 수업 보조 영상의 시계열 설명 예시

```text
톰슨·러더퍼드·보어의 원자모형 변천을 설명하는 45초 모션 그래픽 초안을 만들어 줘.
각 모형의 특징, 이전 설명의 한계, 바뀐 이유를 짧은 문장과 개념 모식도로 보여 줘.
핵심 주장에 사용한 근거를 연결하고 새로 확인해야 할 사실은 따로 표시해 줘.
보어 모형을 현대 원자모형의 최종 형태로 설명하지 마.
```

## Part 2 — 참고 범위 선택

```text
첨부한 레퍼런스의 등장 순서와 장면 전환을 분석해 줘.
참고할 조건 두 가지와 우리 영상에 필요한 이유를 먼저 설명해 줘.
우리 문구와 사례는 유지하고, 선택한 움직임의 원리를 Notion 문서 소개 초안에 적용해 줘.
참고한 부분과 새로 구성한 부분을 나누어 알려 줘.
```

## Part 3 — 마지막 안내 시간 수정

```text
전체 길이는 20초로 유지하고 마지막 안내를 4초 동안 읽을 수 있게 앞 장면의 시간을 조정해 줘.
필수 문구와 일정은 유지해 줘. 수정한 구간을 설명하고 결과를 다시 보여 줘.
```

## Part 4 — 세 문서로 다시 제작

```text
첨부한 LESSON_BRIEF.md, VISUAL_RULES.md, SCENE_PLAN.md를 읽어 줘.
먼저 세 파일에서 적용할 조건과 서로 충돌하는 부분을 정리해 줘.
확인한 내용으로 45초 수업 보조 영상 초안을 구성하고 문구·장면 순서·시간표의 반영을 알려 줘.
파일을 읽지 못했거나 구현하기 어려운 조건은 먼저 알려 줘.
```

## Part 4 — 한 행 수정

```text
SCENE_PLAN_REVISED.md의 시간을 반영해 마지막 장면을 18초로 늘리고 전체 45초를 유지해 줘.
앞 장면의 설명이 너무 빨라지지 않도록 문구와 내레이션도 함께 검토해 줘.
변경한 파일·구간·시간과 결과의 반영 여부를 알려 줘.
```

## Part 5 — 외부 소재 한 장면

```text
현재 연결된 외부 도구의 지원 기능과 계정 조건을 먼저 확인해 줘.
도입에 사용할 5초, 16:9 배경 영상 소재를 만들어 줘.
검정 배경에 주황빛 유리 구체와 얇은 빛의 곡선이 차분하게 움직이고 카메라는 천천히 이동하게 해 줘.
문자와 로고는 별도 편집에서 넣을 수 있게 여백을 남겨 줘.
요청 조건·작업 상태·실제 출력 파일을 확인할 수 있게 알려 줘.
```

외부 소재는 추상 연출이며 실제 과학 관측이나 정확한 원자모형으로 설명하지 않는다. 위 문구는 강의용 예시다. 실제 생성, 비용·권리 조건, 재생과 내보내기는 현재 도구에서 확인한다.
'''
files['PROMPTS.md']=prompts
for name,value in files.items():(K/name).write_text(value,encoding='utf8')
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def target(p,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
with ZipFile(B/'candidate.pptx') as z:
 ids=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N);rs={r.get('Id'):r.get('Target') for r in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};out=['# 노션톡 모션 그래픽 웨비나 — 강사용 진행 원고\n','전체 48장 · 90분 제안\n','Part 0 1~3쪽 5분 / Part 1 4~19쪽 26분 / Part 2 20~26쪽 10분 / Part 3 27~33쪽 10분 / Part 4 34~40쪽 14분 / Part 5 41~45쪽 10분 / 정리 46~48쪽 15분\n'];index=[]
 for i,sid in enumerate(ids,1):
  p=target('ppt/presentation.xml',rs[sid.get('{'+N['r']+'}id')]);s=E.fromstring(z.read(p));title=s.xpath('.//p:sp[p:nvSpPr/p:cNvPr[@name="title"]]//a:t/text()',namespaces=N);title=''.join(title);rels=E.fromstring(z.read(rel(p)));np=target(p,next(r.get('Target') for r in rels if r.get('Type').endswith('/notesSlide')));nt=E.fromstring(z.read(np));body=''
  for sh in nt.findall('.//p:sp',N):
   ph=sh.find('.//p:ph',N)
   if ph is not None and ph.get('type')=='body':body='\n'.join(''.join(x.xpath('.//a:t/text()',namespaces=N)) for x in sh.findall('p:txBody/a:p',N));break
  out.extend([f'## {i:02}. {title}\n',body+'\n']);index.append({'page':i,'title':title})
 (OUT/'강사용_진행원고.md').write_text('\n'.join(out),encoding='utf8');(B/'page-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf8')
print('Created seven workshop Markdown files and a 48-page instructor script.')
