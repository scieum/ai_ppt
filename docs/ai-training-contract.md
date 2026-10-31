# AI 연수용 실행 데이터 계약 2.2.0

2026-10-27. 기본 규칙은 `harness/rules.json`, 실행은 [사용 안내](../harness/README.md)를 따른다. 경로는 별도 언급이 없으면 해당 강의 폴더 기준이다. 규칙 수치·유형·허용값의 단일 기준은 규칙 JSON이다.

G10 추가: `rights/inventory.json`, `scan.json`, `review.json`, `open-issues.json`이 필요하다. 모든 출처·자산을 빠짐없이 연결하고 현재 계획·출력의 해시에 묶은 사람의 검토를 요구한다. 전체 필드와 갱신 절차는 [저작권 검토 계약](copyright-review.md)에 있다. 전체 제작 종료·검수 전후·Figma 게시·최종화에서 확인하며 기존 G01~G09를 대체하지 않는다.

## 1. 입력과 계획

`input.json`의 필수 필드는 다음과 같다. 전체 편집 예시는 [input.json](../harness/templates/ai-training/input.json)과 [plan.md](../harness/templates/ai-training/plan.md)에 있다. 예시에는 실제 승인이나 유효한 근거 해시가 없다.

| 필드 | 값 |
|---|---|
| profile | `ai_training` |
| unit, audience | 강의 식별자와 청중 설명 |
| format | `workshop`, `demo`, `lecture` |
| environment | product, version, os, ui_language, account의 비어 있지 않은 문자열 |
| objectives | id, action(수행 행동), result(결과물)을 가진 고유 항목 배열 |
| target_slides, minutes | 양의 정수 장수, 양의 유한한 총시간 |
| deliverables | pdf, figma, exercises를 모두 명시한 불리언 객체 |
| branding | brand_id, copyright, mode, label, logos 배열 |

새 강의를 시작할 때 브랜드 지정이 없으면 항상 **“이번에는 사이음/노션톡 중 무엇인가요?”**라고 질문한다. `brand_id`는 사이음=`scieum`, 노션톡=`notiontalk` 중 사용자가 선택한 값이다. null·누락·다른 값은 G01에서 차단한다. 이전 강의의 선택을 새 강의에 자동 적용하지 않는다.

`copyright`에는 `template`과 `year`를 둔다. template에는 `{holder}`를 정확히 한 번 쓰고 필요한 경우 `{year}`를 한 번 쓴다. holder는 사이음일 때 `Sci_eum`, 노션톡일 때 `NotionTalk`으로 해석한다. 브랜드를 바꿔도 연도·기호·접두·접미 문구는 유지한다. 예시는 `{"template":"© {year}. {holder}. All rights reserved.","year":2026}`다.

자산 위치 확인 전에는 mode=`text`, logos=[]로 근거 분석·계획 초안을 작성할 수 있다. 로고를 준비해야 G04 이후를 진행할 수 있다. 실제 제작은 mode=`logo`, logos 한 항목을 요구한다. role은 `sci_eum_logo` 또는 `notiontalk_logo`로 선택과 일치하고, file은 원본 자산의 증빙, slides는 1부터 전체 장수까지의 배열이다. 모든 장표 우측 상단에 사용한다. 필요하면 variants에 white/black 증빙을 등록하고 배경 대비에 맞는 원본을 사용한다. 미등록 로고·다른 브랜드는 거절한다.

원본 자산은 [assets/branding](../assets/branding/README.md)에 보존한다. 사이음 원본은 현재 체크아웃에서 미확보 상태이므로 실제 사이음 제작 전에 원본을 확인해야 한다. 임의 재제작·텍스트 대체로 자산 준비를 통과시키지 않는다.

강의별 `plan.md`에는 `harness-plan` JSON 블록이 정확히 하나 있어야 한다. JSON은 위 입력과 같은 필드에 design(디자인 기준 설명/경로), slides, exercises, supplementary를 더한다. break_minutes는 생략 시 0이다. links는 수강생 배포용 HTTP(S) 주소 배열이며 생략 시 빈 배열이다.

슬라이드 필드:

| 필드 | 내용 |
|---|---|
| number, title, message | 1부터 이어지는 실제 번호, 제목, 핵심 메시지 |
| content_ids, source_ids | 포함한 내용과 출처의 ID 배열 |
| visual | 시각 자산 ID 배열. 필요 없으면 [] |
| layout, design_type, character | 배치 설명, 기존 7유형 중 하나, 캐릭터가 없으면 `none` |
| minutes, activity | 페이지 소요시간, explanation/demo/guided_practice/practice/check/troubleshooting/summary |
| objective_ids, exercise_ids | 수행 목표와 실습 연결. exercise_ids는 페이지당 0~1개 |
| instructor_action, learner_action | 강사와 청중의 행동을 각각 설명 |

페이지 시간 합계와 휴식 시간이 총시간과 같아야 한다. 한 실습 카드의 시간은 연결된 페이지 시간 합계와 같아야 한다. 관찰형 강의도 목표를 확인할 활동과 `check` 페이지가 필요하다. 실습형 카드에는 `practice` 또는 `guided_practice` 페이지가 있어야 한다. 포함한 내용은 빠짐없이 쓰고 제외 내용은 계획에 넣지 않는다.

실습 카드(exercises 배열)의 필수 필드:

`id`, `title`, `objective_ids`, `mode`(hands_on/observation), `start_conditions`, `input_location`, `instructions`(단계 배열), `expected_result`, `success_criteria`(관찰 가능한 조건 배열), `errors`(symptom/check/action/expected_state 객체 배열), `fallback`, `customization`, `minutes`, `file_ids`, `source_ids`.

`file_ids`는 `assets/manifest.json`에서 실습 파일 종류로 등록한 ID다. 해당 파일이 없으면 []로 쓴다. 카드의 목표는 연결 페이지의 목표에도 들어 있어야 한다. 모든 수행 목표는 실습 또는 관찰 카드와 그 결과 확인에 연결되어야 한다.

## 2. 근거와 검증

모든 파일 증빙은 `{"path":"research/extract.txt","sha256":"실제 SHA-256"}` 형식이다. 절대 경로, `..` 탈출, Windows ADS, 역슬래시를 사용하지 않는다. 상대 경로의 심벌릭 링크가 강의 폴더 밖으로 나가면 거절한다.

`research/sources.json`은 고유 id, role, citation, locator, evidence의 배열이다. role은 official(공식 사용법), content(강의 내용), structure(설명 구성), design(디자인)이다. 내용 근거는 official/content 중 하나 이상, 디자인 근거는 design이 있어야 한다. 선택하지 않은 자료 역할을 채우려고 가짜 출처를 만들지 않는다.

official에는 HTTPS url과 ISO 날짜 checked_on을 더한다. URL을 썼다는 사실만으로 공식성·최신성을 자동 인증하지 않는다. 실제 확인한 내용·조건을 증빙에 남긴다.

`research/content-map.json`은 다음 항목의 배열이다.

- id, kind(concept/technical/task), claim, rationale
- scope: 기본 / 선택·심화 / 제외. 확인 필요는 확정 단계에서 실패한다.
- source_ids, objective_ids
- 선택·심화에는 inclusion_reason, separation을 더하고, 계획의 supplementary에도 같은 내용을 넣는다.
- 포함할 technical에는 공식 출처 ID와 verification을 둔다. verification은 status=`verified`, checked_on, input과 같은 environment, evidence가 필요하다. 단순 메타데이터 기록만으로 실제 재현을 했다고 보고하지 않는다.

G01은 입력 목표만 사용하므로 페이지 계획 파일이 없어도 근거 분석 단계의 검사를 할 수 있다.

## 3. 자산과 실습 파일

`assets/manifest.json` 항목: id, file 증빙, kind, purpose, review=`passed`, reviewer. 계획의 모든 visual 및 실습 file_ids의 합집합과 정확히 일치해야 한다. 동일 파일을 여러 ID로 중복 등록하지 않는다. 같은 자산을 여러 페이지에서 쓰려면 동일 ID를 재사용한다.

- screenshot/crop: source_id와 locator가 필요하다.
- screenshot 또는 purpose_type=`tool_ui`: 실제 screenshot/crop만 허용하며 checked_on과 입력과 같은 environment가 필요하다.
- generated/existing 및 실습 파일: provenance가 필요하다.
- exercise_file/prompt/starter/checkpoint: `exercises/` 안의 파일이다.
- 나머지 시각 자산은 `assets/` 안에 둔다.

설명용 그림이 없어도 브랜드 로고는 등록해야 한다. 실습 파일 배포 여부는 input.deliverables.exercises와 정확히 일치해야 한다. 역할 `image`는 승인 후 assets/와 exercises/에만 쓸 수 있다. analysis는 research/, sample은 drafts/representatives/, production은 drafts/를 사용한다. judge는 읽기 전용이다.

## 4. 계획 승인과 해시

`approvals.json`은 unit, actor=`human`, decision=`approve`, message_ref, plan_hash, evidence의 배열이다. 실제 사용자 응답에 연결한다. 모의 기록에는 simulation=true가 필요하며 실제 모드는 이를 거절한다.

연수용 계획 해시는 입력 전체, 목표·납품·브랜드·실습·시간·범위, 페이지의 의미·활동·실습 연결, 내용·출처 기록을 포함한다. 페이지 title/layout/visual/character와 plan.design은 일상적인 표현·배치 수정으로 분리하지만 대표 디자인 확인과 체크포인트 검사는 별도로 무효화될 수 있다. 핵심 메시지·실습 입력·성공 기준 변경은 이전 승인을 사용할 수 없다.

## 5. 대표 디자인과 브랜드

기존 7유형과 G08·G09 확인 구조를 유지한다. 원본과 실제 덱의 번호를 혼동하지 않는다. 대표 시안 7유형을 실제 강의에 모두 넣을 의무는 없다.

`design-review/reference-lock.json`: unit, templates. templates에 각 유형을 정확히 한 번 둔다. 항목은 id, type, slide(참조 PDF 쪽/PPTX 장), source, render, layout, mode다. source/render/layout은 증빙 객체다.

- mode=`exact`: 원본과 시안의 객체 역할·종류·좌표·색·글꼴·굵기·정렬·캐릭터 자산을 직접 대조한다.
- mode=`adopt`: target(artifact/render/layout 증빙)과 recipe를 추가한다. target은 별도로 고정한 연수용 목표 템플릿의 실제 내보내기다. recipe.adopted는 차용 요소, replaced는 교체 설명, adjustments는 `{role, property, reason}` 배열이다. 원본과 목표 사이의 잠긴 속성 변경을 빠짐없이 정확히 명세한다. 객체 추가·삭제는 property=`__role__`로 적는다. 로고는 자산·실제 표시 경계 변경도 명세한다. 시안은 고정한 target과 대조한다.

레이아웃 JSON은 artifact_sha256, render_sha256, exporter, canvas와 objects를 담는다. bbox는 [x,y,width,height]의 0~1 정규화 값이다. canvas는 규칙의 기준 화면이다. 모든 객체는 고유 role과 locked_properties를 담는다. 선택한 로고는 우측 상단 영역의 visible_bbox와 제공 자산 해시가 필요하다. `copyright_footer` 역할에는 실제 문구 text와 하단 영역의 bbox가 필요하다. 수치는 실제 소스에서 내보내고, 검사를 통과시키려고 손으로 맞춘 증빙을 만들지 않는다.

`design-review/review.json`: unit, version, plan_hash, reference_hash(canonical 해시), slides. 각 대표 항목은 id, type, reference_id, slide(대표 시안의 페이지), artifact/render/layout/comparison 증빙, reviewer, reason, criteria다. 로고가 있는 대표 시안은 실제 강의에 적용할 브랜드 배치를 대표하도록 페이지 대응을 정한다. 표지는 1번이며 다른 유형의 원본 참조 쪽을 1쪽으로 강제하지 않는다.

criteria의 목록은 규칙 JSON을 따른다. 각 항목에는 status, reviewer, reason, evidence가 필요하다. 필수 항목은 passed여야 한다. 선택 항목의 not_applicable에도 이유가 필요하며 캐릭터가 실제로 있으면 character_identity를 생략할 수 없다.

`design-review/approvals.json`: unit, version, review_hash, reference_hash, actor=`human`, decision=`approve_design`, message_ref, evidence의 배열이다. `feedback.json`은 빈 경우에도 []를 기록한다. 의견별 id, scope(global/local), text, message_ref, evidence, status를 둔다. resolved에는 resolution_version, resolution_reason, resolution_evidence가 필요하다. global 의견은 현재 디자인 확인과 같은 confirmation_ref가 있어야 닫는다.

## 6. 제작물·검토·리허설

PPTX는 실제 OOXML 관계 순서의 페이지와 발표자 노트를 읽는다. 각 장의 실제 텍스트에 선택한 브랜드의 전체 푸터 문구가 있어야 한다. 노트에는 설명과 `Source:` 또는 `출처:`가 있어야 한다. DOCX는 `Slide 1`부터 이어지는 구간과 출처를 검사한다. 각 구간에 `발화:`, 시연·실습·오류 대응 장에는 `조작:`, 직접 실습 장에는 `대기:`가 필요하다.

PDF 선택 시 pypdf로 읽을 수 있는 비암호화 파일, 양의 페이지 크기, 전체 PPT 장수와 같은 페이지 수를 요구한다. 내용·줄바꿈의 일치는 아래 사람의 페이지 검토로 확인한다.

`checks/reviews.json`: plan_hash, artifacts, open_issues=[], slides. artifacts는 PPTX·DOCX·선택한 PDF·모든 배포 실습 파일의 상대 경로와 현재 해시 객체다. 각 slides 항목은 number, render 증빙, layout 증빙과 content/learning/visual 검토를 가진다. 검토는 status=`passed`, reviewer, comment, evidence다.

PDF를 선택하면 페이지별 pdf_review도 필요하다. pdf_sha256, page, render 증빙, status=`passed`, reviewer, comment, evidence로 현재 PDF와 대응을 기록한다. 전체 layout은 현재 덱·렌더에 연결하고, 각 장의 로고는 입력의 자산과 적용 페이지 및 해당 유형의 참조 표시 경계와 일치해야 한다.

`checks/rehearsal.json`:

- plan_hash, artifacts: 현재 계획과 배포 파일 해시
- status=`passed`, reviewer, checked_on, environment, evidence
- elapsed_minutes: 설명·실습·대기를 포함한 실제 시간. 총시간을 넘으면 실패
- exercises: 계획 카드별 id, status, reviewer, checked_on, environment, criteria_results, evidence, recovery_evidence, fallback_evidence
- criteria_results는 계획의 success_criteria와 같은 순서의 criterion/status=`passed` 배열
- links: 계획 links의 모든 주소에 대해 url, status=`passed`, evidence

Figma를 선택한 경우에만 `figma/mapping.json`을 요구한다. url, deck_sha256, status=`verified`, reviewer, evidence와 전체 페이지의 고유 slide/node_id 대응을 기록한다. 선택하지 않았는데 Figma 쓰기 선행 명령을 실행하면 거절한다.

모든 모의 검토·리허설·원격 확인에는 simulation=true를 표시한다. 검증 코드는 실제 사용자를 인증하거나 화면·실습·원격 서버를 독립적으로 재현하지 않는다.

## 7. 보호·재개·최종화

G07, 두 사용자 확인 지점, 실패 복귀 단계, 재시도 한도는 유지한다. 입력·규칙·공통 기준 문서·검사 코드·해당 단계의 파일 해시가 달라지면 유효한 지점부터 재검사한다. 실습 파일은 image부터, 리허설은 review부터 영향을 준다. Figma 미선택 강의에는 figma/ 지문을 요구하지 않는다.

최종화는 PPTX·DOCX와 선택한 PDF·실습 파일만 복사하고 이전 결과는 history/에 보존한다. 보호 대상 출력은 쓰기 전에 차단한다. 모의 시험 모드에서는 최종화할 수 없다. 실제로 기록한 자동 검사 결과와 사람의 검토 범위를 나누어 완료를 보고한다.
