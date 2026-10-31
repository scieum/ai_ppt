# 모션 그래픽을 이용한 수업 영상 제작하기 — 웨비나 전체 계획

작성: 2026-10-27 · 상태: 전체 구성 검토용 초안 · 브랜드: NotionTalk

## 1. 이번 계획의 기준

사용자가 지정한 순서를 강의의 중심 흐름으로 유지한다.

**단순 프롬프트로 생성 → 레퍼런스로 생성 → 모션 그래픽 관련 지식 → 장면표 등 .md 파일 제작 → 힉스필드와 같은 외부 커넥터로 제작**

처음부터 문서 작성과 이론을 요구하지 않는다. 먼저 짧은 요청으로 실제 움직이는 결과를 만들고, 원하는 결과와 다른 지점을 발견한 뒤 레퍼런스·모션 용어·문서가 왜 필요한지 경험하게 한다. 마지막에는 같은 제작 조건을 외부 서비스 요청으로 옮긴다. 타이포그래피를 기본 실습으로 삼되 인포그래픽·절차 설명·캐릭터 장면까지 함께 다룬다.

| 항목 | 이번 계획 |
|---|---|
| 강의명 | 모션 그래픽을 이용한 수업 영상 제작하기 |
| 형태·청중 | 수업 영상을 만들어 보려는 교사를 위한 무료 웨비나. 짧은 시연과 함께 실습을 반복 |
| 일정 | 2026년 11월 1일(일) 20:00 시작. 제공 홍보 이미지의 정보 |
| 총시간 | **90분 제안**: 도입 5분 + 다섯 단계 70분 + 정리 5분 + 질의응답 10분. 종료 시각은 미확정 |
| 장수 | 42장 제안. 과거 대표 시안의 5장은 전체 강의 분량이 아님 |
| 브랜드 | 노션톡 원본 로고를 모든 장표 우측 상단에 배치 |
| 저작권 | `© 2026. NotionTalk. All rights reserved.` |
| 디자인 | 원본 PDF에서 추출한 구조·슬롯을 유지. 첫 장표는 주황→검정 그라데이션과 새로 생성한 세 캐릭터 장면 |
| 주 실습 도구 | 도구명·버전·UI는 미정. 1~4단계는 자연어 요청과 파일 참조로 모션을 만들고 재생할 수 있는 환경을 사전 리허설로 확정 |
| 기본 구현 제안 | 코드 기반 모션 미리보기를 사용할 경우 AI가 작성한 HTML/CSS/JS를 제공 시작 파일에서 재생. 참가자에게 코드 직접 작성을 요구하지 않음 |
| 외부 생성 후보 | Higgsfield 등 이미지·영상 생성 커넥터. 실제 사용 클라이언트·연결 방식·모델·생성 조건은 사전 검증 후 확정 |
| 결과물 | 네 영상 유형의 실습/관찰 기록, Markdown 3종, 프롬프트 묶음, 완성 예시와 체크리스트 |

시간·장수·구현 경로·영상 길이는 현재 **제안값**이다. 사용자 지정 내용과 같은 확정 상태로 표현하지 않는다. 웨비나 참가가 무료라는 안내를 개별 생성 도구의 무료 이용 보장으로 확대하지 않는다. 이번 작업은 계획서 작성이며 새 영상 생성·외부 업로드·전체 장표 제작·승인 기록 생성은 실행하지 않는다.

## 2. 끝나고 할 수 있게 될 일

| 목표 | 수행 행동 | 확인할 결과 |
|---|---|---|
| O1 | 단순한 자연어 요청으로 모션을 만들고 조건 하나를 바꾸어 수정 | 타이포그래피 최초·수정 결과 또는 관찰 기록 |
| O2 | 레퍼런스에서 유지할 요소와 교체할 내용을 구분 | 인포그래픽 결과와 유지·변경 비교 |
| O3 | 대상·속성·시간·곡선·순서를 사용해 수정 요청 | 모호한 요청을 고친 구체적인 문장 |
| O4 | 브리프·모션 기준·장면표를 파일로 작성하고 대조 | 서로 일치하는 Markdown 3개와 절차 설명 모션 |
| O5 | 장면 하나를 외부 생성 요청으로 옮기고 상태·결과를 확인 | 요청 조건표·작업 상태·검토 기록; 준비된 계정에서는 생성 클립 |

개별 생성 계정이 없는 참가자도 강사 결과·중간 완성본으로 같은 판단 활동을 수행한다. 관찰 경로를 선택했다고 실제 생성이나 내보내기에 성공한 것으로 기록하지 않는다.

## 3. 함께 만들 영상 유형

공통 소재는 교과 지식 검증 부담이 적은 수업 활동 문구 **‘관찰하고, 질문하고, 설명하기’**를 제안한다. 강사가 실제 수업 자료를 정하면 문구를 교체한다. 과학·역사 등의 사실을 새로 만들지 않고 제공한 자료 안에서 작성한다.

| ID·영상 유형 | 제안 길이 | 수업에서 쓰는 위치 | 함께 수행할 작업 | 주된 단계 |
|---|---:|---|---|---|
| V1 키네틱 타이포그래피 | 8초 | 도입·핵심어·정리 | ‘관찰하고 / 질문하고 / 설명하기’의 순차 등장, 유지 시간·강조 수정 | 1단계 생성, 3단계 개선 |
| V2 인포그래픽·비교 모션 | 12초 | 비교·분류·구조 설명 | 같은 문구를 카드/도형의 관계와 등장 순서로 표현. 레퍼런스의 색·배치를 참고 | 2단계 생성, 3단계 개선 |
| V3 절차·활동 안내 모션 | 20초 | 수업 활동이나 제작 절차 안내 | 질문 4초, 자료 확인 10초, 생각 정리 6초의 3장면. 문서로 조건 고정 | 4단계 문서 작성·생성 |
| V4 캐릭터·장면 기반 클립 | 모델 지원 범위 내 짧은 길이; 목표 5~8초 | 도입 장면·전환·설명 삽화 | 기존 세 캐릭터 참고 이미지로 행동 장면을 요청하고, 정확한 글자는 별도 레이어로 조합 | 5단계 외부 생성 |

V4의 길이는 선택 모델이 지원하는 값으로 조정한다. V1~V3의 전체 길이를 외부 서비스에 한 번의 요청으로 반드시 만들 수 있다고 설명하지 않는다. 여러 클립을 조합할 경우 최종 길이는 편집 단계에서 맞춘다.

짧은 자연어 요청의 예시는 다음과 같다. 이는 실제 실행 성공을 확인한 명령어가 아니라 리허설할 실습 초안이다.

> ‘관찰하고, 질문하고, 설명하기’라는 세 문구가 차례로 나타나는 8초 모션을 만들어 줘. 검정 배경과 주황색 강조를 쓰고, 글자를 읽을 시간을 둬. 재생할 수 있는 결과를 보여줘.

레퍼런스를 더할 때에는 다음처럼 요청 범위를 좁힌다.

> 첨부 자료의 색과 카드 배치를 참고해 같은 문구를 12초 인포그래픽 모션으로 만들어 줘. 문구와 내용은 내가 준 자료로 바꾸고, 등장 순서는 문장에 적힌 순서로 해줘. 정지 이미지에 없는 움직임은 새로 제안한 내용으로 구분해 줘.

## 4. 다섯 단계의 진행과 연결

| 구간 | 경과 시간 | 핵심 질문 | 강사·참가자 활동 | 다음 단계로 넘기는 것 |
|---|---|---|---|---|
| 도입 | 0~5분 | 오늘 무엇을 만들까요? | 실제 재생 예시 4종, 수행 목표, 실습·관찰 경로 확인 | 시작 파일과 같은 예제 문구 |
| Part 1 단순 프롬프트 | 5~17분 | 짧게 말해도 어디까지 만들어질까요? | V1 생성·재생·문제 찾기·조건 하나 수정 | 최초 결과와 바꾸고 싶은 조건 |
| Part 2 레퍼런스 | 17~31분 | 원하는 모습을 어떻게 전달할까요? | 참고 범위 분석, 유지·변경 목록, V2 생성·비교 | 시각 기준과 교체할 내용 |
| Part 3 모션 지식 | 31~44분 | 원하는 움직임을 어떤 말로 설명할까요? | V1·V2를 대상으로 대상·속성·시간·곡선·순서, 가독성 진단 | 구체적인 모션 수정 문장 |
| Part 4 Markdown 문서 | 44~62분 | 같은 조건을 다음 작업에도 어떻게 남길까요? | BRIEF·MOTION·STORYBOARD 작성, V3 생성, 한 행 수정 | 재사용할 문서 3개 |
| Part 5 외부 커넥터 | 62~75분 | 문서의 한 장면을 외부 제작에 어떻게 연결할까요? | 지원 입력·생성 조건 확인, V4 요청, 상태·결과 검토, 조합 | 외부 요청 조건과 생성/관찰 기록 |
| 정리 | 75~80분 | 내 수업에는 어떤 방식이 맞을까요? | 처음·중간·최종 결과 비교, 적용 유형 선택, 파일 저장 | 자기 수업 적용 메모 |
| 질의응답 | 80~90분 | 실제 적용에서 무엇이 남았나요? | 공통 문제와 개별 환경 질문 | 다음 제작 한 가지 |

생성 대기는 각 시연 시간에 포함한다. 리허설에서 길게 걸리면 실제 요청 접수까지만 시연하고, 준비된 동일 조건의 완성 결과로 검토한다. 무작정 생성 완료를 기다리며 다음 단계를 미루지 않는다.

## 5. 이론의 범위와 설명 방식

이론은 처음부터 독립 강의처럼 길게 설명하지 않고 앞서 만든 V1·V2를 고치는 데 필요한 만큼 다룬다.

| 내용 | 화면에서 비교할 것 | 참가자가 써 볼 수정 문장 |
|---|---|---|
| 대상·속성 | 같은 글자의 위치·크기·투명도 | ‘두 번째 문구의 투명도만 바꾸고 위치는 유지해 줘.’ |
| 지속 시간·지연·순차 등장 | 읽는 구간, 나타나기 전 대기, 요소 간 간격 | ‘문구를 읽는 구간을 늘리고 다음 문구는 그 뒤에 보여줘.’ |
| 이징·속도 변화 | 같은 이동의 일정한 속도와 완만한 시작·끝 | ‘움직임의 시작과 끝에서 속도가 완만하게 바뀌게 해줘.’ |
| 위계·시선 | 동시 등장과 단계별 강조 | ‘지금 설명하는 핵심어 하나만 강조해 줘.’ |
| 타이포그래피 | 정확한 문구·줄바꿈·크기·대비·읽는 시간 | ‘원문을 그대로 쓰고 한 줄이 길면 의미 단위로 줄을 나눠 줘.’ |

모든 글자에 같은 읽기 시간을 정답처럼 적용하지 않는다. 실제 문구와 청중을 기준으로 재생하며 읽을 수 있는지 확인한다. 정지 PDF만으로 원본의 실제 속도·이징·클릭 타이밍을 관찰했다고 주장하지 않는다.

심화로는 루프·전환·마스킹·카메라 이동·음성 싱크·숏폼 비율 변환을 짧은 예시로만 소개한다. 이번 90분안의 필수 실습에는 넣지 않는다. 복잡한 3D·립싱크·모델별 고급 파라미터·긴 서사 영상·계정 설치 전체 과정은 제외한다.

## 6. Markdown 파일 제작 실습

### 6.1 세 문서가 맡을 역할

| 파일 | 적는 내용 | 수정할 때 돌아갈 곳 |
|---|---|---|
| `BRIEF.md` | 청중, 학습 목표 하나, 원자료, 영상 유형, 길이·비율, 최종 결과 | 내용·대상·목적이 달라졌을 때 |
| `MOTION.md` | 대상·속성·시간·순서·이징, 문구 보존, 타이포그래피, 색, 캐릭터 고정 조건 | 반복되는 디자인·동작 문제 |
| `STORYBOARD.md` | 장면별 시작·끝·화면 문구·설명·동작·소재·완료 확인 | 장면 순서·시간·내용 수정 |

파일 이름만 저장하면 AI가 자동으로 읽는다고 가르치지 않는다. 사용하는 도구에서 실제로 파일을 첨부하거나 경로를 참조하고, 어느 파일을 어떤 목적으로 읽을지 요청한다. 서비스가 Markdown을 직접 실행해 주는 것으로 표현하지 않는다.

### 6.2 실습 템플릿에 들어갈 최소 항목

`BRIEF.md`: 대상 / 학습 목표 / 원자료 / 영상 유형 / 총길이 / 비율 / 반드시 포함할 문구 / 완료 기준.

`MOTION.md`: 문구 원문 유지 / 색·글꼴·위계 / 움직일 대상과 속성 / 등장 순서 / 읽는 구간과 전환 / 이징 의도 / 캐릭터 고정 조건 / 바꿔도 되는 조건.

`STORYBOARD.md` 예시:

| 장면 | 시작~끝 | 화면 문구 | 설명·나레이션 초안 | 모션·자료 | 확인할 것 |
|---|---|---|---|---|---|
| S01 | 0~4초 | 무엇이 보이나요? | 자료를 보고 발견한 것을 떠올립니다. | 질문 문구 등장, 자료 자리 유지 | 질문을 읽을 수 있는가 |
| S02 | 4~14초 | 관찰하고, 질문하고 | 자료를 살펴보고 질문 하나를 만듭니다. | 관찰·질문 문구와 관련 도형 순차 강조 | 문구·설명·강조가 같은 순서인가 |
| S03 | 14~20초 | 내 생각을 설명하기 | 자신의 생각을 짧게 정리해 설명합니다. | 요약 문구를 보여 준 뒤 유지 | 마지막 문구가 끝까지 보이는가 |

4+10+6=20초는 실습 예시다. 실제 원자료가 정해지면 문구와 설명을 바꾼다. 시간 구간의 겹침·빈틈, 세 문서의 길이·비율·문구 불일치를 확인한 뒤 생성한다. 충돌이 있으면 AI가 임의로 고르게 두지 않고 문서를 고친다.

### 6.3 문서를 사용한 생성 요청의 골격

> BRIEF.md의 목적과 원자료, MOTION.md의 고정 규칙, STORYBOARD.md의 장면별 시간과 문구를 읽고 모션을 만들어 줘. 먼저 서로 충돌하는 조건을 알려 줘. 충돌이 없으면 장면 순서대로 재생 가능한 미리보기를 만들어 줘. 문구와 학습 내용은 제공 자료 밖에서 추가하지 마.

## 7. 외부 커넥터 실습 설계

Higgsfield는 외부 제작 서비스의 대표 후보로 다룬다. 특정 모델을 강의의 불변 조건으로 두지 않고, 같은 장면표를 지원 입력에 맞춰 요청하는 방법을 가르친다.

1. 강사 계정 연결 상태와 사용 가능한 생성 기능을 읽기 작업으로 확인한다.
2. 선택한 모델이 받는 참조 매체·역할·길이·비율과 현재 생성 조건을 확인한다.
3. 장면표에서 캐릭터 행동 장면 하나를 고르고, 화면·동작·카메라·유지할 외형을 추린다.
4. 로컬 파일 경로·업로드된 매체 ID·참조 URL을 구분하고, 실제 클라이언트에 맞는 전달 방식을 사용한다.
5. 생성할 조건을 검토한 뒤 한 번 요청한다. 접수·대기·완료·실패를 구분한다.
6. 완료 상태뿐 아니라 실제 파일 재생, 길이·비율·인물 외형·원자료와의 일치를 확인한다.
7. 문자 정확성이 필요한 타이포그래피는 별도 텍스트 레이어로 만들고 캐릭터 클립과 조합한다. 사용 모델에서 정확한 문자 표현이 확인된 경우에만 해당 경로를 실습에 포함한다.

외부 커넥터는 `.md`를 임의의 자동 실행 파일로 처리하지 않는다. **AI가 문서를 읽고, 지원하는 프롬프트·참조 매체·길이·비율 등의 요청 필드로 변환**하는 과정이 핵심이다. 실패한 요청을 무조건 반복하지 않고 원인과 상태를 확인한다.

공식 안내에는 클라이언트별 연결 방식이 구분되어 있다. 따라서 웹 AI의 커넥터 설정, 플러그인, 코딩 도구의 CLI 절차를 하나의 동일한 설치법으로 안내하지 않는다. 실제 강의 도구가 정해지면 그 환경의 화면만 캡처해 사용한다. [공식 연결 안내](https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent), [공식 통합 문서](https://higgsfield.ai/enterprise-help-center/platform/integrations). 확인: 2026-10-27.

이 문서에서는 공식 안내와 현재 제공된 도구 명세만 확인했다. 계정 연결·업로드·영상 생성·내보내기를 실환경에서 리허설했다고 기록하지 않는다. 가격·크레딧·지원 길이·모델명은 사전 확인 없이 숫자로 고정하지 않는다.

## 8. 페이지별 제작 계획 — 42장 / 90분 제안

시간은 설명·시연·참가자 대기를 포함한 제안이다. 입력창의 긴 프롬프트와 코드 전체는 배포 문서로 제공하고 장표에는 지금 볼 부분을 보여 준다. 목표·출처·강사/학습자 행동·실습 연결은 아래 표와 문서 끝 실행 초안에 함께 기록한다.

| 장 | 시간(분) | 구간 | 제목 | 화면·활동 | 실습 |
|---:|---:|---|---|---|---|
| 1 | 0.5 | 도입 | 모션 그래픽을 이용한 수업 영상 제작하기 | cover / 주제와 오늘의 범위를 소개한다 · 참가자: 수업에 적용할 상황을 떠올린다 | — |
| 2 | 1.5 | 도입 | 오늘 함께 만들 네 종류의 영상 | comparison / 사전 제작한 실제 재생 예시 4종을 보여준다 · 참가자: 각 유형을 수업 어디에 쓸지 고른다 | — |
| 3 | 1 | 도입 | 다섯 단계로 만드는 수업 영상 | five-elements / 다섯 단계의 입력과 결과를 연결한다 · 참가자: 현재 단계와 다음 단계를 확인한다 | — |
| 4 | 2 | 도입 | 실습 시작 상태와 합류 방법 | checklist / 로그인·시작 파일·관찰 대체 경로를 확인한다 · 참가자: 자기 기기 상태를 확인하고 실습 또는 관찰 경로를 고른다 | — |
| 5 | 0.5 | Part 1 | Part 1 짧은 말로 먼저 만들어 보기 | part / 첫 실습의 화면과 결과를 소개한다 · 참가자: V1 문구를 확인한다 | — |
| 6 | 1 | Part 1 | 첫 요청은 한 문장이면 충분해요 | prompt / 단순 프롬프트를 읽고 바꿀 입력을 표시한다 · 참가자: 복사할 문구를 선택한다 | EX01 |
| 7 | 3 | Part 1 | 타이포그래피 첫 결과 만들기 | prompt / 같은 프롬프트를 실행하고 시작부터 끝까지 재생한다 · 참가자: 생성 과정과 결과의 차이를 관찰한다 | EX01 |
| 8 | 2 | Part 1 | 재생해 보니 무엇이 달랐나요? | comparison / 첫 결과의 문제 한 가지를 구체적으로 짚는다 · 참가자: 문구 누락과 빠른 전환을 찾아 기록한다 | EX01 |
| 9 | 2.5 | Part 1 | 한 가지 조건만 바꾸어 수정하기 | comparison / 문구 유지 시간을 바꾸어 다시 재생한다 · 참가자: 수정 전후에서 달라진 점을 설명한다 | EX01 |
| 10 | 3 | Part 1 | 내 문구로 타이포그래피 만들기 | prompt / 짧은 자기 문구를 넣도록 안내한다 · 참가자: 자기 문구로 생성하거나 제공 결과를 분석한다 | EX01 |
| 11 | 0.5 | Part 2 | Part 2 레퍼런스로 방향 잡기 | part / 레퍼런스를 더한 작업을 소개한다 · 참가자: V2 예시와 비교할 기준을 고른다 | — |
| 12 | 2 | Part 2 | 이미지와 영상 레퍼런스는 다르게 읽어요 | comparison / 색·배치·문구와 실제 움직임의 근거를 나눈다 · 참가자: 각 참고자료에서 알 수 있는 것만 적는다 | EX02 |
| 13 | 2 | Part 2 | 유지할 것과 바꿀 것 정하기 | brief / 유지·변경 목록과 새로운 내용을 함께 요청한다 · 참가자: 유지할 요소 2개와 바꿀 요소 1개를 고른다 | EX02 |
| 14 | 3 | Part 2 | 레퍼런스 기반 인포그래픽 만들기 | prompt / 레퍼런스와 문구를 넣어 V2를 생성한다 · 참가자: 원본과 생성 결과의 같은 점과 다른 점을 관찰한다 | EX02 |
| 15 | 4 | Part 2 | 내 수업 내용으로 바꾸어 보기 | prompt / 실습 자료와 중간 완성본을 안내한다 · 참가자: V2를 자기 문구로 바꾸거나 완성본에서 교체 지점을 표시한다 | EX02 |
| 16 | 2.5 | Part 2 | 레퍼런스 활용 결과 확인 | comparison / 색·배치·읽는 순서와 내용 정확성을 비교한다 · 참가자: 유지·변경 조건이 반영되었는지 체크한다 | EX02 |
| 17 | 0.5 | Part 3 | Part 3 움직임을 설명하는 말 익히기 | part / 이론을 V1·V2의 수정과 연결한다 · 참가자: 고치고 싶은 모션 하나를 고른다 | — |
| 18 | 2 | Part 3 | 대상과 속성 | five-elements / V1에서 움직이는 글자와 속성을 표시한다 · 참가자: 대상과 속성을 구분한다 | — |
| 19 | 2 | Part 3 | 시간과 등장 순서 | comparison / 같은 글자의 시간과 순서를 달리한 예시를 재생한다 · 참가자: duration과 delay·stagger를 구분한다 | — |
| 20 | 2 | Part 3 | 속도 변화와 이징 | comparison / 같은 이동의 속도 변화만 비교한다 · 참가자: 설명에 맞는 속도 변화 이유를 말한다 | — |
| 21 | 2 | Part 3 | 설명의 순서와 시선의 이동 | comparison / V2의 동시 등장과 순차 등장을 비교한다 · 참가자: 첫 번째로 봐야 할 요소를 고른다 | — |
| 22 | 2 | Part 3 | 타이포그래피는 읽을 시간이 필요해요 | comparison / 텍스트의 읽기와 이동 구간을 구분해 재생한다 · 참가자: 가독성 문제를 찾고 수정 조건을 제안한다 | — |
| 23 | 2.5 | Part 3 | 모호한 요청을 구체적인 요청으로 | brief / 짧은 모션 진단 문제를 제시한다 · 참가자: 느낌 표현을 관찰 가능한 수정 문장으로 바꾼다 | EX03 |
| 24 | 0.5 | Part 4 | Part 4 장면표를 파일로 남기기 | part / 이번에 만들 문서 3개의 역할을 소개한다 · 참가자: 저장할 폴더를 확인한다 | — |
| 25 | 1.5 | Part 4 | 세 문서의 역할 | brief / 문서 간 연결과 수정 위치를 설명한다 · 참가자: 어느 조건을 어느 파일에 적을지 고른다 | — |
| 26 | 2.5 | Part 4 | BRIEF.md 만들기 | brief / 학습 목표 하나로 브리프 초안을 만든다 · 참가자: 대상과 자기 자료를 채운다 | EX04 |
| 27 | 2.5 | Part 4 | MOTION.md 만들기 | brief / 세 번째 단계의 수정 조건을 규칙으로 옮긴다 · 참가자: 고정할 문구·색·모션 조건을 채운다 | EX04 |
| 28 | 3 | Part 4 | STORYBOARD.md 만들기 | brief / 20초 3장면 예시를 문서 표로 만든다 · 참가자: 자기 자료로 한 장면을 수정한다 | EX04 |
| 29 | 2 | Part 4 | 장면표가 영상 길이와 맞나요? | brief / 4초·10초·6초의 합과 장면 내용을 확인한다 · 참가자: 겹침·빈 구간·모순 조건을 찾아 고친다 | EX04 |
| 30 | 3 | Part 4 | 세 문서로 절차 설명 모션 만들기 | prompt / 문서의 역할을 지정해 V3를 생성한다 · 참가자: 장면표와 재생 결과를 대응시킨다 | EX04 |
| 31 | 3 | Part 4 | 문서 한 줄을 고쳐 다시 만들기 | comparison / 한 장면만 수정하는 방법을 안내한다 · 참가자: 장면표 한 행을 바꾸어 재생하거나 예상 변화를 적는다 | EX04 |
| 32 | 0.5 | Part 5 | Part 5 외부 커넥터로 장면 확장하기 | part / V4 캐릭터 장면의 역할을 소개한다 · 참가자: 앞서 만든 장면표에서 한 장면을 고른다 | — |
| 33 | 1.5 | Part 5 | AI·커넥터·생성 서비스의 역할 | brief / 문서→요청 조건→외부 작업→결과의 흐름을 설명한다 · 참가자: 어떤 데이터가 외부로 전달되는지 확인한다 | — |
| 34 | 2 | Part 5 | 외부 요청에 필요한 조건 | brief / 연결 상태와 현재 모델 입력 조건을 읽어 보여준다 · 참가자: 장면 하나의 요청 조건을 작성한다 | EX05 |
| 35 | 2 | Part 5 | 장면표의 한 장면을 생성 요청으로 | prompt / 조건을 검토한 후 외부 서비스에 한 번 요청한다 · 참가자: 전달할 문구와 참조 이미지를 대조한다 | EX05 |
| 36 | 2 | Part 5 | 작업 상태와 재생 결과 확인 | comparison / 작업 ID와 완료 상태를 확인하고 결과를 재생한다 · 참가자: 결과의 재생 여부·길이·캐릭터를 확인한다 | EX05 |
| 37 | 2 | Part 5 | 캐릭터 장면과 정확한 글자 결합하기 | comparison / 사전 제작한 장면 조합 결과와 편집 순서를 보여준다 · 참가자: 글자와 캐릭터 장면을 각각 어디서 고칠지 고른다 | EX05 |
| 38 | 3 | Part 5 | 실패했을 때 돌아올 지점 | checklist / 대표 실패 예시와 백업 파일을 제시한다 · 참가자: 자기 요청을 점검하거나 실패 사례의 복구 경로를 고른다 | EX05 |
| 39 | 1.5 | 정리·질문 | 처음 결과와 지금 결과 비교 | comparison / 같은 주제의 결과를 나란히 재생한다 · 참가자: 어느 단계가 어떤 문제를 해결했는지 말한다 | EX06 |
| 40 | 1.5 | 정리·질문 | 내 수업에는 어떤 영상이 맞을까요? | brief / 수업 상황별 선택 질문을 제시한다 · 참가자: 자기 수업 사례와 다음 제작 유형을 적는다 | EX06 |
| 41 | 2 | 정리·질문 | 오늘 만든 파일로 다음 영상 시작하기 | brief / 실제 배포 폴더와 저장 경로를 보여준다 · 참가자: 완성 문서 또는 관찰 기록을 저장한다 | EX06 |
| 42 | 10 | 정리·질문 | 질의응답 | part / 질문을 받아 공통 문제와 개별 상황을 구분한다 · 참가자: 질문하거나 다음 작업 한 가지를 정한다 | — |

## 9. 실습 운영과 합류 경로

| 실습 | 직접 해 볼 일 | 완료 확인 | 준비되지 않은 참가자의 동등 활동 |
|---|---|---|---|
| EX01 | 단순 프롬프트로 V1 생성, 조건 하나 수정 | 문구 3개·순서·읽는 시간과 수정 조건 확인 | 최초/수정 완성본의 차이 표시 |
| EX02 | 유지 2개·변경 1개를 적고 V2 생성 | 참고 범위와 새 내용이 반영됨 | 레퍼런스 분석표와 완성본 대응 |
| EX03 | 모호한 요청을 구체적인 수정 문장으로 변경 | 대상과 시간·순서 등 판단 가능한 조건 포함 | 선택형 예시에서 적절한 수정 요청 고르기 |
| EX04 | 세 문서 작성, V3 생성, 한 장면 수정 | 문서 일치·시간 합계·장면과 결과의 대응 | 중간 완성 문서에서 한 행만 수정 |
| EX05 | 한 장면의 외부 요청 조건 작성, 강사/자기 계정으로 검토 | 매체·요청·상태·실제 결과 대응 | 사전 제작 클립과 실제 작업 기록 분석 |
| EX06 | 결과 비교와 자기 수업 적용 메모 저장 | 다음 수정할 파일과 항목을 말할 수 있음 | 배포 완성본을 자기 수업에 적용할 메모 작성 |

리허설 시 실습별 시작 상태·정확한 입력 위치·실행 내용·정상 결과·오류 복구·백업으로 재합류하는 과정까지 확인한다. 기기·계정·설치 문제는 도입 전 사전 안내로 분리한다. 실시간 생성이 끝나지 않으면 동일 조건의 강사 완성본으로 이어 간다.

## 10. 필요한 자료와 배포 폴더

아래는 **제작 예정 목록**이다. 존재하는 자산과 앞으로 만들 파일을 구분한다. 이 계획서 작성만으로 파일이 완성된 것으로 기록하지 않는다.

| 구분 | 현재 상태 | 준비할 것 |
|---|---|---|
| 표지·브랜드 | 보유 | 노션톡 원본 로고, 주황 표지, 세 캐릭터 생성 PNG·프롬프트·출처 기록 |
| 도구 소개 로고 | 보유 | `../../assets/tool-logos/`의 Claude·Codex·Higgsfield 정면/기울임 배지와 표식. 제공 PDF 벡터 윤곽 기반, 투명 PNG·SVG. Codex는 레퍼런스의 OpenAI 심볼형 |
| 원본 장표 구조 | 일부 보유 | `assets/reference-templates/`의 5유형. 전환·체크리스트·비교 유형은 실제 원본 쪽을 추가 추출 |
| 영상 제작 레퍼런스 | 선정 필요 | 사용 가능한 이미지 1개와 재생 가능한 짧은 영상 1개. 분석 범위·출처·수정할 내용 기록 |
| 실습 문구·원자료 | 제작 필요 | 기본 문구, 교체용 문구, 교과 적용 예시 1개 |
| 프롬프트 | 초안 본문에 있음 | simple / reference / revise / from-md / connector 요청 파일 |
| 문서 템플릿 | 제작 필요 | 빈 BRIEF·MOTION·STORYBOARD와 채운 예시 각 1세트 |
| 영상 예제 | 제작·검증 필요 | V1~V4 실제 재생 파일과 V1·V2 수정 전후. 이미지 한 장을 영상 예제로 표시하지 않음 |
| 외부 제작 증빙 | 리허설 필요 | 실제 요청 조건·작업 상태·완료 결과·실패 복구 캡처 |
| 배포 자료 | 제작 필요 | PPTX·PDF·강사용 대본·실습 파일 묶음·완성 파일·체크리스트 |

제안하는 강의별 배포 구조:

```text
exercises/
  README.md
  prompts/01-simple.md, 02-reference.md, 03-revise.md, 04-from-md.md, 05-connector.md
  templates/BRIEF.md, MOTION.md, STORYBOARD.md
  reference/README.md, reference-image.*, reference-video.*
  starter/                 # 선택한 주 실습 환경의 시작 파일
  checkpoints/             # 단계별 중간 완성본
  completed/               # 재생 검증한 V1~V4와 채운 문서
  review-checklist.md
```

MP4 내보내기는 실제 도구에서 재생·저장까지 성공한 경로를 확인한 뒤 배포 조건으로 확정한다. HTML 등 모션 미리보기와 MP4 파일은 서로 다른 산출물로 표기한다. 실습용 영상 파일명과 경로는 실제 파일을 만든 뒤 배포 목록에 등록한다.

## 11. 디자인과 원본 구조 적용

- 첫 장표: 현재 v3의 제목·일정·브랜드·푸터 좌표와 주황 그라데이션·새 협업 장면 유지. 세 캐릭터의 얼굴·헤어·안경·의상 색을 후속 생성에서도 기준으로 사용한다.
- 본문: 검정 바탕, 흰 제목, 회색 설명, 원본 추출 박스·카드와 실측 슬롯을 사용한다. 새 화면을 임의의 카드 디자인으로 다시 만들지 않는다. 주황은 표지의 확정 색이며 본문 강조색 통일은 전체 시안에서 별도 검토한다.
- 다섯 단계 목차: 기존 4개 꺾임 목차에 다섯 내용을 압축하지 않는다. **R02 PDF 23쪽의 5칸 번호 카드 에셋**에 단계명을 넣어 사용한다. 원본 카드 수·폭·간격을 유지한다.
- 현재 v3의 대표 5장 중 4개 Part 목차와 임시 제목은 이 전체 계획과 맞게 재배치·교체한다. 대표 시안의 번호를 전체 42장의 번호로 오인하지 않는다.
- 전환 장은 R02 PDF 103쪽, 준비 체크는 37쪽의 해당 구조를 추가 추출한다. 비교 화면은 실제 원본의 해당 페이지를 선정·실측한 뒤 쓴다. 아직 없는 에셋을 준비 완료로 표시하지 않는다.
- 태그·박스에 새 문구가 길면 문구를 먼저 줄인다. 원본 슬롯·간격·도형 윤곽을 임의로 바꾸지 않는다.
- 생성 삽화·실제 도구 캡처·재생 가능한 영상·정지 프리뷰를 구분한다. 도구 사용법 장에는 실제 환경의 캡처를 쓰고 캐릭터 삽화로 대신하지 않는다.
- 모든 장의 우측 상단 노션톡 원본 로고와 저작권 문구를 유지한다. 새 강의로 분리할 때 브랜드 미지정이면 기존 하네스의 질문 규칙을 적용한다.

## 12. 사전 준비와 리허설 체크

| 시점 | 해야 할 일 | 완료 증거 |
|---|---|---|
| 교안 제작 전 | 주 실습 도구·클라이언트·버전·OS·UI·계정 조건 확정 | 실제 환경 기록과 시작 화면 |
| 교안 제작 전 | 영상·이미지 레퍼런스, 실습 원자료 선정 | 출처·참고 범위·제공 파일 |
| 실습 파일 제작 | 세 문서 템플릿과 시작·중간·완성본 마련 | 파일 존재와 실제 내용 확인 |
| 리허설 | 같은 예제로 V1~V4를 생성·재생·저장 | 실행 기록과 재생 파일; 미리보기/MP4 구분 |
| 리허설 | 외부 서비스의 실제 입력·지원 조건·상태·결과 확인 | 모델 명세와 실제 작업 기록 |
| 리허설 | 생성 지연·오류에서 백업으로 넘어가 보기 | 복구 및 재합류 기록 |
| 리허설 | 설명·대기·실습 포함 전체 시간 측정 | 90분 제안과 실제 소요시간 비교 |
| 배포 전 | 문구·원자료·세 문서·영상·슬라이드 대응 확인 | 장면별 검토 기록 |
| 배포 전 | 실제 링크·파일명·저장 위치 확인 | 직접 열어 재생한 체크리스트 |
| 전체 PPT 제작 | 계획 확인·자산·대표 시안·디자인 확인·제작·검수 | 실제 단계별 기록; 사용자 승인 추정 금지 |

미정 결정은 총시간, 주 실습 AI/모션 환경, 파일 읽기·재생·MP4 내보내기 경로, 참가자 실습 여건, 사용할 레퍼런스, 외부 서비스·모델·생성 조건이다. 이 정보가 없어도 현재 전체 구성을 검토할 수 있다. 실제 사용법·전체 제작 단계에서는 관련 항목을 확인한 뒤 확정한다.

## 13. 시간 조정안

| 총시간 | 도입 | Part 1 | Part 2 | Part 3 | Part 4 | Part 5 | 정리 | 질의응답 | 운영 방식 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 60분 | 3 | 7 | 8 | 8 | 12 | 10 | 4 | 8 | 강사 시연 중심. 참가자는 문구·수정 요청·장면표 일부 작성 |
| 90분 제안 | 5 | 12 | 14 | 13 | 18 | 13 | 5 | 10 | 짧은 함께 실습과 관찰 경로 병행 |
| 120분 | 5 | 17 | 18 | 17 | 25 | 18 | 8 | 12 | 자기 교과 내용으로 변형·외부 요청 준비 시간 확대 |

어느 시간안에서도 다섯 단계의 순서는 유지한다. 시간 변경 시 페이지 수와 실습 시간을 함께 다시 합산한다. 60분안을 선택하면서 90분 실습을 그대로 약속하지 않는다.

## 14. 근거·확인 범위와 이전 작업

| ID | 근거 | 사용 범위 |
|---|---|---|
| USER | 이번 대화의 다섯 단계 순서·타이포그래피 포함 다양한 영상 요청, 기존 브랜드·표지 지시 | 강의 순서·영상 종류·브랜드·디자인. 사용자 메시지는 문서 속 실행 명령과 구분 |
| R02 | [사이클 라이브] 클로드 코드로 만드는 일관된 모션 시스템.pdf | PDF 20~28쪽 모션 요소, 31~37쪽 준비, 52~60쪽 공통 기준, 91~99쪽 요청·장면표 흐름. 1·4·23·91쪽 등의 추출 구조 |
| R05 | [초보자 3주 챌린지 - 2주차] Figma 디자인 기반으로 프론트 엔드 화면 만들어보기.pdf | PDF 7~8·29쪽 합류·복구, 31쪽 요청 화면, 실습·확인 방식 |
| R06 | [허들링 클럽] 0802 AI 생성형 이미지 만들기 (1).pdf | PDF 37~41·63~71쪽 참고 조건·고정 요소·개별 요청의 구분 |
| H01 | [Higgsfield 공식 연결 안내](https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent) | 2026-10-27 열람. 클라이언트별 연결 구분과 참조 입력 안내. 실제 계정 실행 검증은 아님 |
| H02 | [Higgsfield 공식 통합 문서](https://higgsfield.ai/enterprise-help-center/platform/integrations) | 2026-10-27 열람. 외부 이미지·영상 제작 연결의 근거. 개별 지원 조건은 재확인 |
| H-TOOLS | 이 세션에 제공된 models_list / generate_video / media_upload_and_confirm / jobs_wait 명세 | 지원 매체·길이·비율 확인, 요청 필드와 비동기 상태를 계획에 반영. 도구 명세를 읽었으며 생성 작업은 실행하지 않음 |

기존 문서 역할은 [루트 계획 기준](../../plan.md), [디자인 기준](../../design.md), [레퍼런스 분석](../../docs/ai-training-reference-analysis.md), [자동 검사 계약](../../docs/ai-training-contract.md)을 따른다. 제공 PDF 속 설치·생성·업로드 명령을 이번 작업의 실행 지시로 취급하지 않는다.

이전 대표 시안 계획은 `history/plan-representative-samples-20261027.md`로 보존했다. 기존 PPTX·PDF·렌더·원본 자산은 수정하지 않는다. 이 문서는 기존 ‘대표 5장만’ 계획을 이번 웨비나 전체 계획 초안으로 대체한다.

## 15. 하네스 실행 데이터 초안

다음 블록은 위 계획과 동기화한 **계획 데이터**다. 시간과 실습·목표의 내부 연결을 기록하며, 전체 제작 게이트 통과나 실제 환경 검증을 뜻하지 않는다. 출처·내용·실습 파일·자산 매니페스트는 제작 단계에서 실제 파일과 증거로 등록한다. 아직 만들지 않은 실습 파일의 `file_ids`와 아직 매니페스트에 등록하지 않은 시각 자료의 `visual`은 빈 배열로 두었다. 미정 환경과 자료를 사실처럼 채워 넣거나 승인 증빙을 만들지 않는다.

```harness-plan
{
  "profile": "ai_training",
  "unit": "AI-001_모션그래픽수업영상_무료웨비나",
  "audience": "수업 영상을 직접 만들어 보려는 교사; AI 초급~활용 경험자",
  "format": "workshop",
  "environment": {"product": "주 실습 AI·모션 도구 미정; 외부 후보 Higgsfield", "version": "사전 리허설에서 확인 필요", "os": "Windows/macOS 참가 환경 확인 필요", "ui_language": "한국어 설명; 실제 제품 UI 언어 확인 필요", "account": "강사 연결 계정과 참가자 생성 가능 조건 확인 필요"},
  "objectives": [{"id": "O1", "action": "짧은 자연어 요청으로 타이포그래피 모션을 만들고 한 조건을 바꾸어 수정한다", "result": "V1 최초 결과와 수정 결과"}, {"id": "O2", "action": "레퍼런스에서 유지할 요소와 바꿀 요소를 나누어 인포그래픽 영상을 만든다", "result": "V2 레퍼런스 기반 결과와 비교 메모"}, {"id": "O3", "action": "대상·속성·시간·곡선·순서를 사용해 모션 수정 요청을 구체적으로 작성한다", "result": "모션 진단표와 수정 문장"}, {"id": "O4", "action": "BRIEF.md·MOTION.md·STORYBOARD.md를 작성하고 장면별 길이와 화면 문구를 검토한다", "result": "서로 일치하는 Markdown 문서 3개와 V3 절차 설명 모션"}, {"id": "O5", "action": "장면표의 한 장면을 외부 커넥터용 요청으로 바꾸고 생성 상태와 결과를 확인한다", "result": "V4 요청 조건·작업 상태·검토 기록; 계정 준비 시 생성 클립"}],
  "target_slides": 42,
  "minutes": 90,
  "break_minutes": 0,
  "deliverables": {"pdf": true, "figma": false, "exercises": true},
  "branding": {"brand_id": "notiontalk", "mode": "logo", "label": "NotionTalk", "copyright": {"template": "© {year}. {holder}. All rights reserved.", "year": 2026}, "logos": [{"role": "notiontalk_logo", "file": {"path": "assets/notiontalk-white.png", "sha256": "df7323d6ebf42b7c741488955487378f43dd34921230da2c0ba9f2713b401d21"}, "slides": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]}]},
  "design": "../../design.md; ../../assets/reference-templates/README.md; 현재 강의 plan.md 11절의 표지 변경·5단계 목차 기준",
  "slides": [
    {"number": 1, "title": "모션 그래픽을 이용한 수업 영상 제작하기", "message": "무료 웨비나의 주제와 일정", "content_ids": ["C00"], "source_ids": ["USER", "R02"], "visual": [], "layout": "R02 PDF 1쪽의 두 줄 제목·일정·그림 슬롯; 주황색 변경은 사용자 지시", "design_type": "cover", "character": "three_reference_characters", "minutes": 0.5, "activity": "explanation", "objective_ids": ["O1", "O2", "O3", "O4", "O5"], "exercise_ids": [], "instructor_action": "주제와 오늘의 범위를 소개한다", "learner_action": "수업에 적용할 상황을 떠올린다"},
    {"number": 2, "title": "오늘 함께 만들 네 종류의 영상", "message": "타이포그래피·인포그래픽·절차 설명·캐릭터 장면", "content_ids": ["C00"], "source_ids": ["USER"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 1.5, "activity": "explanation", "objective_ids": ["O1", "O2", "O4", "O5"], "exercise_ids": [], "instructor_action": "사전 제작한 실제 재생 예시 4종을 보여준다", "learner_action": "각 유형을 수업 어디에 쓸지 고른다"},
    {"number": 3, "title": "다섯 단계로 만드는 수업 영상", "message": "단순 요청부터 외부 연결까지 순서대로 확장한다", "content_ids": ["C00"], "source_ids": ["USER", "R02"], "visual": [], "layout": "assets/reference-templates/five-elements: R02 PDF 23쪽의 5칸 구조", "design_type": "contents", "character": "none", "minutes": 1, "activity": "explanation", "objective_ids": ["O1", "O2", "O3", "O4", "O5"], "exercise_ids": [], "instructor_action": "다섯 단계의 입력과 결과를 연결한다", "learner_action": "현재 단계와 다음 단계를 확인한다"},
    {"number": 4, "title": "실습 시작 상태와 합류 방법", "message": "도구가 준비되지 않아도 예시 파일로 함께 진행한다", "content_ids": ["C00"], "source_ids": ["R02", "R05"], "visual": [], "layout": "R02 PDF 37쪽 확인 유형. 실제 제작 전에 에셋 추가 추출", "design_type": "objectives", "character": "none", "minutes": 2, "activity": "check", "objective_ids": ["O1", "O5"], "exercise_ids": [], "instructor_action": "로그인·시작 파일·관찰 대체 경로를 확인한다", "learner_action": "자기 기기 상태를 확인하고 실습 또는 관찰 경로를 고른다"},
    {"number": 5, "title": "Part 1 짧은 말로 먼저 만들어 보기", "message": "문서와 레퍼런스 없이 첫 결과를 경험한다", "content_ids": ["C01"], "source_ids": ["USER"], "visual": [], "layout": "R02 PDF 103쪽 유형. 실제 제작 전에 에셋 추가 추출", "design_type": "part", "character": "none", "minutes": 0.5, "activity": "explanation", "objective_ids": ["O1"], "exercise_ids": [], "instructor_action": "첫 실습의 화면과 결과를 소개한다", "learner_action": "V1 문구를 확인한다"},
    {"number": 6, "title": "첫 요청은 한 문장이면 충분해요", "message": "보여줄 문구와 기본 동작을 짧게 요청한다", "content_ids": ["C01"], "source_ids": ["USER"], "visual": [], "layout": "assets/reference-templates/prompt: R05 PDF 31쪽 입력·결과 슬롯", "design_type": "figure", "character": "none", "minutes": 1, "activity": "explanation", "objective_ids": ["O1"], "exercise_ids": ["EX01"], "instructor_action": "단순 프롬프트를 읽고 바꿀 입력을 표시한다", "learner_action": "복사할 문구를 선택한다"},
    {"number": 7, "title": "타이포그래피 첫 결과 만들기", "message": "요청을 실행하고 실제로 재생한다", "content_ids": ["C01"], "source_ids": ["USER"], "visual": [], "layout": "assets/reference-templates/prompt: R05 PDF 31쪽 입력·결과 슬롯", "design_type": "figure", "character": "none", "minutes": 3, "activity": "demo", "objective_ids": ["O1"], "exercise_ids": ["EX01"], "instructor_action": "같은 프롬프트를 실행하고 시작부터 끝까지 재생한다", "learner_action": "생성 과정과 결과의 차이를 관찰한다"},
    {"number": 8, "title": "재생해 보니 무엇이 달랐나요?", "message": "문구·순서·읽는 시간을 확인한다", "content_ids": ["C01"], "source_ids": ["USER"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 2, "activity": "check", "objective_ids": ["O1"], "exercise_ids": ["EX01"], "instructor_action": "첫 결과의 문제 한 가지를 구체적으로 짚는다", "learner_action": "문구 누락과 빠른 전환을 찾아 기록한다"},
    {"number": 9, "title": "한 가지 조건만 바꾸어 수정하기", "message": "한 번에 하나를 바꾸면 결과를 비교하기 쉽다", "content_ids": ["C01"], "source_ids": ["USER"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 2.5, "activity": "demo", "objective_ids": ["O1"], "exercise_ids": ["EX01"], "instructor_action": "문구 유지 시간을 바꾸어 다시 재생한다", "learner_action": "수정 전후에서 달라진 점을 설명한다"},
    {"number": 10, "title": "내 문구로 타이포그래피 만들기", "message": "문구를 바꾸고 나머지 조건은 유지한다", "content_ids": ["C01"], "source_ids": ["USER"], "visual": [], "layout": "assets/reference-templates/prompt: R05 PDF 31쪽 입력·결과 슬롯", "design_type": "figure", "character": "none", "minutes": 3, "activity": "guided_practice", "objective_ids": ["O1"], "exercise_ids": ["EX01"], "instructor_action": "짧은 자기 문구를 넣도록 안내한다", "learner_action": "자기 문구로 생성하거나 제공 결과를 분석한다"},
    {"number": 11, "title": "Part 2 레퍼런스로 방향 잡기", "message": "참고자료에서 유지할 시각 요소를 고른다", "content_ids": ["C02"], "source_ids": ["USER"], "visual": [], "layout": "R02 PDF 103쪽 유형. 실제 제작 전에 에셋 추가 추출", "design_type": "part", "character": "none", "minutes": 0.5, "activity": "explanation", "objective_ids": ["O2"], "exercise_ids": [], "instructor_action": "레퍼런스를 더한 작업을 소개한다", "learner_action": "V2 예시와 비교할 기준을 고른다"},
    {"number": 12, "title": "이미지와 영상 레퍼런스는 다르게 읽어요", "message": "정지 이미지에서는 움직임의 속도를 알 수 없다", "content_ids": ["C02"], "source_ids": ["R02", "R06"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 2, "activity": "explanation", "objective_ids": ["O2"], "exercise_ids": ["EX02"], "instructor_action": "색·배치·문구와 실제 움직임의 근거를 나눈다", "learner_action": "각 참고자료에서 알 수 있는 것만 적는다"},
    {"number": 13, "title": "유지할 것과 바꿀 것 정하기", "message": "색·레이아웃·리듬의 참고 범위를 구체화한다", "content_ids": ["C02"], "source_ids": ["R06"], "visual": [], "layout": "assets/reference-templates/brief: R02 PDF 91쪽의 3열·3행 구조", "design_type": "table_formula", "character": "none", "minutes": 2, "activity": "explanation", "objective_ids": ["O2"], "exercise_ids": ["EX02"], "instructor_action": "유지·변경 목록과 새로운 내용을 함께 요청한다", "learner_action": "유지할 요소 2개와 바꿀 요소 1개를 고른다"},
    {"number": 14, "title": "레퍼런스 기반 인포그래픽 만들기", "message": "같은 주제를 비교·분류 화면으로 표현한다", "content_ids": ["C02"], "source_ids": ["USER", "R06"], "visual": [], "layout": "assets/reference-templates/prompt: R05 PDF 31쪽 입력·결과 슬롯", "design_type": "figure", "character": "none", "minutes": 3, "activity": "demo", "objective_ids": ["O2"], "exercise_ids": ["EX02"], "instructor_action": "레퍼런스와 문구를 넣어 V2를 생성한다", "learner_action": "원본과 생성 결과의 같은 점과 다른 점을 관찰한다"},
    {"number": 15, "title": "내 수업 내용으로 바꾸어 보기", "message": "참고 배치는 유지하며 문구와 자료를 바꾼다", "content_ids": ["C02"], "source_ids": ["USER"], "visual": [], "layout": "assets/reference-templates/prompt: R05 PDF 31쪽 입력·결과 슬롯", "design_type": "figure", "character": "none", "minutes": 4, "activity": "guided_practice", "objective_ids": ["O2"], "exercise_ids": ["EX02"], "instructor_action": "실습 자료와 중간 완성본을 안내한다", "learner_action": "V2를 자기 문구로 바꾸거나 완성본에서 교체 지점을 표시한다"},
    {"number": 16, "title": "레퍼런스 활용 결과 확인", "message": "복사 여부보다 요청한 기준이 반영됐는지 확인한다", "content_ids": ["C02"], "source_ids": ["USER"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 2.5, "activity": "check", "objective_ids": ["O2"], "exercise_ids": ["EX02"], "instructor_action": "색·배치·읽는 순서와 내용 정확성을 비교한다", "learner_action": "유지·변경 조건이 반영되었는지 체크한다"},
    {"number": 17, "title": "Part 3 움직임을 설명하는 말 익히기", "message": "앞서 만든 결과를 고칠 만큼의 지식을 익힌다", "content_ids": ["C03"], "source_ids": ["USER", "R02"], "visual": [], "layout": "R02 PDF 103쪽 유형. 실제 제작 전에 에셋 추가 추출", "design_type": "part", "character": "none", "minutes": 0.5, "activity": "explanation", "objective_ids": ["O3"], "exercise_ids": [], "instructor_action": "이론을 V1·V2의 수정과 연결한다", "learner_action": "고치고 싶은 모션 하나를 고른다"},
    {"number": 18, "title": "대상과 속성", "message": "무엇의 위치·크기·투명도를 바꾸는가", "content_ids": ["C03"], "source_ids": ["R02"], "visual": [], "layout": "assets/reference-templates/five-elements: R02 PDF 23쪽의 5칸 구조", "design_type": "figure", "character": "none", "minutes": 2, "activity": "explanation", "objective_ids": ["O3"], "exercise_ids": [], "instructor_action": "V1에서 움직이는 글자와 속성을 표시한다", "learner_action": "대상과 속성을 구분한다"},
    {"number": 19, "title": "시간과 등장 순서", "message": "지속 시간과 시작 지연·간격을 구분한다", "content_ids": ["C03"], "source_ids": ["R02"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 2, "activity": "explanation", "objective_ids": ["O3"], "exercise_ids": [], "instructor_action": "같은 글자의 시간과 순서를 달리한 예시를 재생한다", "learner_action": "duration과 delay·stagger를 구분한다"},
    {"number": 20, "title": "속도 변화와 이징", "message": "시작과 끝에서 움직임의 속도를 조절한다", "content_ids": ["C03"], "source_ids": ["R02"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 2, "activity": "explanation", "objective_ids": ["O3"], "exercise_ids": [], "instructor_action": "같은 이동의 속도 변화만 비교한다", "learner_action": "설명에 맞는 속도 변화 이유를 말한다"},
    {"number": 21, "title": "설명의 순서와 시선의 이동", "message": "동시에 움직이는 요소 수와 강조 순서를 정한다", "content_ids": ["C03"], "source_ids": ["R02"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 2, "activity": "explanation", "objective_ids": ["O3"], "exercise_ids": [], "instructor_action": "V2의 동시 등장과 순차 등장을 비교한다", "learner_action": "첫 번째로 봐야 할 요소를 고른다"},
    {"number": 22, "title": "타이포그래피는 읽을 시간이 필요해요", "message": "정확한 문구·줄바꿈·위계·유지 시간을 검토한다", "content_ids": ["C03"], "source_ids": ["USER", "R02"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 2, "activity": "explanation", "objective_ids": ["O3"], "exercise_ids": [], "instructor_action": "텍스트의 읽기와 이동 구간을 구분해 재생한다", "learner_action": "가독성 문제를 찾고 수정 조건을 제안한다"},
    {"number": 23, "title": "모호한 요청을 구체적인 요청으로", "message": "대상·속성·시간·순서를 넣어 수정한다", "content_ids": ["C03"], "source_ids": ["USER", "R02"], "visual": [], "layout": "assets/reference-templates/brief: R02 PDF 91쪽의 3열·3행 구조", "design_type": "table_formula", "character": "none", "minutes": 2.5, "activity": "check", "objective_ids": ["O3"], "exercise_ids": ["EX03"], "instructor_action": "짧은 모션 진단 문제를 제시한다", "learner_action": "느낌 표현을 관찰 가능한 수정 문장으로 바꾼다"},
    {"number": 24, "title": "Part 4 장면표를 파일로 남기기", "message": "반복할 기준과 영상별 요청을 문서로 만든다", "content_ids": ["C04"], "source_ids": ["USER", "R02"], "visual": [], "layout": "R02 PDF 103쪽 유형. 실제 제작 전에 에셋 추가 추출", "design_type": "part", "character": "none", "minutes": 0.5, "activity": "explanation", "objective_ids": ["O4"], "exercise_ids": [], "instructor_action": "이번에 만들 문서 3개의 역할을 소개한다", "learner_action": "저장할 폴더를 확인한다"},
    {"number": 25, "title": "세 문서의 역할", "message": "BRIEF는 목적, MOTION은 규칙, STORYBOARD는 시간 순서", "content_ids": ["C04"], "source_ids": ["R02"], "visual": [], "layout": "assets/reference-templates/brief: R02 PDF 91쪽의 3열·3행 구조", "design_type": "table_formula", "character": "none", "minutes": 1.5, "activity": "explanation", "objective_ids": ["O4"], "exercise_ids": [], "instructor_action": "문서 간 연결과 수정 위치를 설명한다", "learner_action": "어느 조건을 어느 파일에 적을지 고른다"},
    {"number": 26, "title": "BRIEF.md 만들기", "message": "대상·목표·내용·결과 조건을 적는다", "content_ids": ["C04"], "source_ids": ["USER", "R02"], "visual": [], "layout": "assets/reference-templates/brief: R02 PDF 91쪽의 3열·3행 구조", "design_type": "table_formula", "character": "none", "minutes": 2.5, "activity": "guided_practice", "objective_ids": ["O4"], "exercise_ids": ["EX04"], "instructor_action": "학습 목표 하나로 브리프 초안을 만든다", "learner_action": "대상과 자기 자료를 채운다"},
    {"number": 27, "title": "MOTION.md 만들기", "message": "시간·등장·강조·타이포그래피 규칙을 적는다", "content_ids": ["C04"], "source_ids": ["USER", "R02"], "visual": [], "layout": "assets/reference-templates/brief: R02 PDF 91쪽의 3열·3행 구조", "design_type": "table_formula", "character": "none", "minutes": 2.5, "activity": "guided_practice", "objective_ids": ["O4"], "exercise_ids": ["EX04"], "instructor_action": "세 번째 단계의 수정 조건을 규칙으로 옮긴다", "learner_action": "고정할 문구·색·모션 조건을 채운다"},
    {"number": 28, "title": "STORYBOARD.md 만들기", "message": "장면별 시간·문구·설명·동작을 맞춘다", "content_ids": ["C04"], "source_ids": ["USER", "R02"], "visual": [], "layout": "assets/reference-templates/brief: R02 PDF 91쪽의 3열·3행 구조", "design_type": "table_formula", "character": "none", "minutes": 3, "activity": "guided_practice", "objective_ids": ["O4"], "exercise_ids": ["EX04"], "instructor_action": "20초 3장면 예시를 문서 표로 만든다", "learner_action": "자기 자료로 한 장면을 수정한다"},
    {"number": 29, "title": "장면표가 영상 길이와 맞나요?", "message": "시간 합계와 문구·설명의 일치를 확인한다", "content_ids": ["C04"], "source_ids": ["USER"], "visual": [], "layout": "assets/reference-templates/brief: R02 PDF 91쪽의 3열·3행 구조", "design_type": "table_formula", "character": "none", "minutes": 2, "activity": "check", "objective_ids": ["O4"], "exercise_ids": ["EX04"], "instructor_action": "4초·10초·6초의 합과 장면 내용을 확인한다", "learner_action": "겹침·빈 구간·모순 조건을 찾아 고친다"},
    {"number": 30, "title": "세 문서로 절차 설명 모션 만들기", "message": "파일을 근거로 생성하고 장면 순서를 재생한다", "content_ids": ["C04"], "source_ids": ["USER"], "visual": [], "layout": "assets/reference-templates/prompt: R05 PDF 31쪽 입력·결과 슬롯", "design_type": "figure", "character": "none", "minutes": 3, "activity": "demo", "objective_ids": ["O4"], "exercise_ids": ["EX04"], "instructor_action": "문서의 역할을 지정해 V3를 생성한다", "learner_action": "장면표와 재생 결과를 대응시킨다"},
    {"number": 31, "title": "문서 한 줄을 고쳐 다시 만들기", "message": "화면 수정 요청을 다음 작업에도 남긴다", "content_ids": ["C04"], "source_ids": ["USER"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 3, "activity": "practice", "objective_ids": ["O4"], "exercise_ids": ["EX04"], "instructor_action": "한 장면만 수정하는 방법을 안내한다", "learner_action": "장면표 한 행을 바꾸어 재생하거나 예상 변화를 적는다"},
    {"number": 32, "title": "Part 5 외부 커넥터로 장면 확장하기", "message": "외부 생성 서비스를 작업 흐름에 연결한다", "content_ids": ["C05"], "source_ids": ["USER"], "visual": [], "layout": "R02 PDF 103쪽 유형. 실제 제작 전에 에셋 추가 추출", "design_type": "part", "character": "none", "minutes": 0.5, "activity": "explanation", "objective_ids": ["O5"], "exercise_ids": [], "instructor_action": "V4 캐릭터 장면의 역할을 소개한다", "learner_action": "앞서 만든 장면표에서 한 장면을 고른다"},
    {"number": 33, "title": "AI·커넥터·생성 서비스의 역할", "message": "문서 해석과 외부 생성 요청은 서로 다른 단계다", "content_ids": ["C05"], "source_ids": ["H01", "H02"], "visual": [], "layout": "assets/reference-templates/brief: R02 PDF 91쪽의 3열·3행 구조", "design_type": "table_formula", "character": "none", "minutes": 1.5, "activity": "explanation", "objective_ids": ["O5"], "exercise_ids": [], "instructor_action": "문서→요청 조건→외부 작업→결과의 흐름을 설명한다", "learner_action": "어떤 데이터가 외부로 전달되는지 확인한다"},
    {"number": 34, "title": "외부 요청에 필요한 조건", "message": "참조 이미지·지원 길이·비율·한도를 확인한다", "content_ids": ["C05"], "source_ids": ["H01", "H02", "H-TOOLS"], "visual": [], "layout": "assets/reference-templates/brief: R02 PDF 91쪽의 3열·3행 구조", "design_type": "table_formula", "character": "none", "minutes": 2, "activity": "guided_practice", "objective_ids": ["O5"], "exercise_ids": ["EX05"], "instructor_action": "연결 상태와 현재 모델 입력 조건을 읽어 보여준다", "learner_action": "장면 하나의 요청 조건을 작성한다"},
    {"number": 35, "title": "장면표의 한 장면을 생성 요청으로", "message": "문서 내용은 AI가 해석해 지원 필드로 전달한다", "content_ids": ["C05"], "source_ids": ["H01", "H-TOOLS"], "visual": [], "layout": "assets/reference-templates/prompt: R05 PDF 31쪽 입력·결과 슬롯", "design_type": "figure", "character": "none", "minutes": 2, "activity": "demo", "objective_ids": ["O5"], "exercise_ids": ["EX05"], "instructor_action": "조건을 검토한 후 외부 서비스에 한 번 요청한다", "learner_action": "전달할 문구와 참조 이미지를 대조한다"},
    {"number": 36, "title": "작업 상태와 재생 결과 확인", "message": "요청 접수·대기·완료와 실제 파일을 구분한다", "content_ids": ["C05"], "source_ids": ["H-TOOLS"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 2, "activity": "check", "objective_ids": ["O5"], "exercise_ids": ["EX05"], "instructor_action": "작업 ID와 완료 상태를 확인하고 결과를 재생한다", "learner_action": "결과의 재생 여부·길이·캐릭터를 확인한다"},
    {"number": 37, "title": "캐릭터 장면과 정확한 글자 결합하기", "message": "생성 장면과 타이포그래피 레이어를 조합한다", "content_ids": ["C05"], "source_ids": ["USER"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 2, "activity": "demo", "objective_ids": ["O5"], "exercise_ids": ["EX05"], "instructor_action": "사전 제작한 장면 조합 결과와 편집 순서를 보여준다", "learner_action": "글자와 캐릭터 장면을 각각 어디서 고칠지 고른다"},
    {"number": 38, "title": "실패했을 때 돌아올 지점", "message": "계정·참조 입력·대기·문구·형태 문제를 구분한다", "content_ids": ["C05"], "source_ids": ["R05", "H01", "H-TOOLS"], "visual": [], "layout": "R02 PDF 37쪽 확인 유형. 실제 제작 전에 에셋 추가 추출", "design_type": "objectives", "character": "none", "minutes": 3, "activity": "troubleshooting", "objective_ids": ["O5"], "exercise_ids": ["EX05"], "instructor_action": "대표 실패 예시와 백업 파일을 제시한다", "learner_action": "자기 요청을 점검하거나 실패 사례의 복구 경로를 고른다"},
    {"number": 39, "title": "처음 결과와 지금 결과 비교", "message": "프롬프트·레퍼런스·지식·문서·외부 연결의 차이를 확인한다", "content_ids": ["C06"], "source_ids": ["USER"], "visual": [], "layout": "R02 PDF 20~28쪽 비교 유형에서 해당 쪽 실측·추출 후 사용", "design_type": "comparison", "character": "none", "minutes": 1.5, "activity": "check", "objective_ids": ["O1", "O2", "O3", "O4", "O5"], "exercise_ids": ["EX06"], "instructor_action": "같은 주제의 결과를 나란히 재생한다", "learner_action": "어느 단계가 어떤 문제를 해결했는지 말한다"},
    {"number": 40, "title": "내 수업에는 어떤 영상이 맞을까요?", "message": "타이포그래피·인포그래픽·절차·캐릭터 중 용도에 맞게 고른다", "content_ids": ["C06"], "source_ids": ["USER"], "visual": [], "layout": "assets/reference-templates/brief: R02 PDF 91쪽의 3열·3행 구조", "design_type": "table_formula", "character": "none", "minutes": 1.5, "activity": "check", "objective_ids": ["O1", "O2", "O4", "O5"], "exercise_ids": ["EX06"], "instructor_action": "수업 상황별 선택 질문을 제시한다", "learner_action": "자기 수업 사례와 다음 제작 유형을 적는다"},
    {"number": 41, "title": "오늘 만든 파일로 다음 영상 시작하기", "message": "세 문서를 복제하고 내용과 장면표를 바꾼다", "content_ids": ["C06"], "source_ids": ["USER"], "visual": [], "layout": "assets/reference-templates/brief: R02 PDF 91쪽의 3열·3행 구조", "design_type": "table_formula", "character": "none", "minutes": 2, "activity": "summary", "objective_ids": ["O4", "O5"], "exercise_ids": ["EX06"], "instructor_action": "실제 배포 폴더와 저장 경로를 보여준다", "learner_action": "완성 문서 또는 관찰 기록을 저장한다"},
    {"number": 42, "title": "질의응답", "message": "자기 수업에 적용할 때의 질문을 다룬다", "content_ids": ["C06"], "source_ids": ["USER"], "visual": [], "layout": "R02 PDF 103쪽 유형. 실제 제작 전에 에셋 추가 추출", "design_type": "part", "character": "none", "minutes": 10, "activity": "summary", "objective_ids": ["O1", "O2", "O3", "O4", "O5"], "exercise_ids": [], "instructor_action": "질문을 받아 공통 문제와 개별 상황을 구분한다", "learner_action": "질문하거나 다음 작업 한 가지를 정한다"}
  ],
  "exercises": [
    {"id": "EX01", "title": "단순 프롬프트로 V1 타이포그래피 만들기", "objective_ids": ["O1"], "mode": "hands_on", "start_conditions": "주 실습 도구의 새 작업과 시작 폴더; 미준비자는 관찰용 완성본", "input_location": "선정할 주 실습 AI 도구의 대화 입력창", "instructions": ["짧은 프롬프트를 실행한다", "실제로 재생해 문구·순서·읽는 시간을 확인한다", "문구 또는 유지 시간 한 조건을 바꾸어 다시 만든다"], "expected_result": "V1 최초·수정 미리보기 또는 차이를 적은 관찰 기록", "success_criteria": ["지정 문구 3개를 정확히 보여준다", "등장 순서를 설명할 수 있다", "수정한 한 조건을 지목할 수 있다"], "errors": [{"symptom": "정지 화면만 생성됨", "check": "동작과 재생 결과를 요청했는지 확인", "action": "시간에 따라 바뀌는 모션과 재생 가능한 미리보기를 명시", "expected_state": "재생 시 문구가 순서대로 나타남"}], "fallback": "강사 V1 완성본으로 한 조건 수정 전후를 비교", "customization": "자기 교과의 짧은 핵심어 3개로 교체", "file_ids": [], "source_ids": ["USER"], "minutes": 11.5},
    {"id": "EX02", "title": "레퍼런스로 V2 인포그래픽 만들기", "objective_ids": ["O2"], "mode": "hands_on", "start_conditions": "합법적으로 사용할 레퍼런스 이미지와 교체 문구", "input_location": "주 실습 AI 도구의 참조 첨부·대화 입력 위치; 정확한 UI는 도구 확정 후 기록", "instructions": ["참고자료가 정지 이미지인지 재생 영상인지 구분한다", "유지할 것 2개와 바꿀 것 1개를 적는다", "새 문구로 생성하고 원본과 비교한다"], "expected_result": "V2 인포그래픽 모션 또는 유지·변경 비교 기록", "success_criteria": ["참고할 요소를 구체적으로 적는다", "새 수업 문구를 반영한다", "정지 이미지로 알 수 없는 움직임을 원본 관찰 사실로 쓰지 않는다"], "errors": [{"symptom": "참고 이미지가 그대로 복사됨", "check": "참고 범위와 교체할 내용을 구분했는지 확인", "action": "색·배치만 유지하고 내용·구성 목적을 새로 지정", "expected_state": "참고 범위는 보존하고 새 내용이 표시됨"}], "fallback": "분석표와 V2 완성본의 대응을 표시", "customization": "자기 자료의 비교·분류 내용으로 변경", "file_ids": [], "source_ids": ["USER", "R06"], "minutes": 13.5},
    {"id": "EX03", "title": "모션 진단과 구체적인 수정 요청", "objective_ids": ["O3"], "mode": "observation", "start_conditions": "V1·V2의 정상·문제 예시", "input_location": "모션 진단표 또는 메모", "instructions": ["재생 예시의 문제를 찾는다", "대상·속성·시간·순서 중 필요한 조건을 적는다", "수정 요청을 한 문장으로 만든다"], "expected_result": "실행 가능한 수정 문장과 근거", "success_criteria": ["대상을 명시한다", "시간 또는 순서를 구체적으로 적는다", "읽기·설명과 수정 이유를 연결한다"], "errors": [{"symptom": "예쁘게·부드럽게 같은 느낌만 적음", "check": "무엇을 어떻게 바꿀지 관찰 가능한지 확인", "action": "대상과 변화 조건을 추가", "expected_state": "수정 전후를 비교할 수 있는 요청"}], "fallback": "선택형 진단 문장 중 적절한 항목 고르기", "customization": "자기 V1 또는 V2의 문제에 적용", "file_ids": [], "source_ids": ["USER", "R02"], "minutes": 2.5},
    {"id": "EX04", "title": "세 Markdown 문서와 V3 절차 설명 모션", "objective_ids": ["O4"], "mode": "hands_on", "start_conditions": "기본 템플릿·주 실습 작업 폴더·20초 예시", "input_location": "로컬 텍스트 편집기와 주 실습 AI의 파일 참조 위치", "instructions": ["BRIEF.md에 대상·목표·내용을 적는다", "MOTION.md에 공통 모션·타이포그래피 기준을 적는다", "STORYBOARD.md에 시간·문구·설명·동작을 적는다", "세 파일을 근거로 생성하고 장면표 한 행을 수정한다"], "expected_result": "Markdown 3개와 V3 모션 미리보기 또는 검토 기록", "success_criteria": ["세 문서의 대상·길이·비율이 일치한다", "장면 시간 합계가 전체 길이와 같다", "문구와 설명·동작이 서로 대응한다", "수정할 조건을 어느 파일에 적을지 설명한다"], "errors": [{"symptom": "파일 간 길이·문구가 다름", "check": "브리프와 장면표·모션 규칙을 비교", "action": "기준값을 하나로 맞추고 충돌을 제거", "expected_state": "모든 문서가 같은 조건을 가리킴"}], "fallback": "checkpoint의 세 문서로 한 장면만 수정", "customization": "자기 수업 목표 하나와 자료로 내용 교체", "file_ids": [], "source_ids": ["USER", "R02"], "minutes": 16.0},
    {"id": "EX05", "title": "장면 하나를 외부 커넥터 요청으로 바꾸기", "objective_ids": ["O5"], "mode": "hands_on", "start_conditions": "강사 연결 계정·지원 모델 확인·참조 이미지·생성 한도; 미준비자는 관찰 경로", "input_location": "선정한 AI 클라이언트의 외부 커넥터 도구; 로컬 경로와 원격 매체 ID를 구분", "instructions": ["장면표에서 한 장면을 고른다", "지원하는 입력·길이·비율과 현재 생성 조건을 확인한다", "문서 내용을 요청 필드로 옮긴다", "강사 시연 또는 자기 계정에서 작업 상태·실제 결과를 확인한다", "문구와 캐릭터 일관성을 검토한다"], "expected_result": "V4 외부 요청 조건표·상태·검토 기록; 준비 계정은 생성 클립", "success_criteria": ["참조 매체와 요청 문구를 정확히 대응한다", "요청 접수와 완료·실제 재생을 구분한다", "생성 결과를 원래 장면표와 비교한다", "서비스가 지원하지 않는 값은 지원값에 맞추거나 편집 단계로 넘긴다"], "errors": [{"symptom": "작업이 계속 대기함", "check": "같은 작업 ID의 상태를 확인", "action": "중복 재요청하지 않고 백업 클립으로 검토 진행", "expected_state": "대기 작업을 유지한 채 다음 학습 활동에 합류"}, {"symptom": "문구 또는 캐릭터가 변형됨", "check": "참조 입력과 고정 조건을 확인", "action": "참조·움직임 범위를 조정하고 정확한 문구는 별도 텍스트 레이어로 처리", "expected_state": "원본 기준과 비교 가능한 결과"}], "fallback": "사전 제작 V4와 실제 요청·상태 캡처를 분석", "customization": "장면 하나의 행동과 배경만 교체하고 인물 기준은 유지", "file_ids": [], "source_ids": ["H01", "H02", "H-TOOLS"], "minutes": 11},
    {"id": "EX06", "title": "수업 적용 결과 점검과 저장", "objective_ids": ["O1", "O2", "O3", "O4", "O5"], "mode": "observation", "start_conditions": "실습 결과 또는 강사 완성본과 관찰 기록", "input_location": "최종 점검표와 배포 폴더", "instructions": ["처음·중간·최종 결과를 비교한다", "자기 수업의 영상 유형을 고른다", "세 문서와 다음 수정할 내용을 저장한다"], "expected_result": "자기 수업 적용 메모와 재사용 문서 또는 관찰 기록", "success_criteria": ["유형 선택 이유를 말한다", "다섯 단계가 보완한 조건을 설명한다", "다음에 수정할 파일과 항목을 지목한다"], "errors": [{"symptom": "작업 결과가 어디에 있는지 모름", "check": "배포·작업·완성 폴더를 구분", "action": "결과와 세 문서의 저장 위치를 함께 기록", "expected_state": "다음 작업을 다시 시작할 수 있음"}], "fallback": "배포 폴더의 완성본 위치를 표시", "customization": "다음 수업에 적용할 주제 한 가지 기록", "file_ids": [], "source_ids": ["USER"], "minutes": 5.0}
  ],
  "supplementary": {"심화 예시": {"items": ["루프·전환·마스킹", "카메라 이동", "음성 싱크", "숏폼 비율 변환"], "separation": "90분 필수 실습에서 제외. 추가 시간 또는 배포 예시에만 배치"}},
  "links": []
}
```
