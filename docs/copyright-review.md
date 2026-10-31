# G10 — 저작권·이용 권리·독자성 검토

2026-10-27 · AI 연수 프로필 2.2.0. 기존 G01~G09와 작업 폴더·원본 보호·승인 구조를 유지한다.

## 무엇을 확인하는가

원본의 문장, 예시, 비유, 프롬프트, 전개, 시각 표현을 새 강의에 어떻게 사용했는지 검토한다. 추출 배경·도형·로고, 화면 캡처, 글꼴·음원·영상, 생성 이미지의 참조 자료도 실제 사용하는 자산 목록에 포함한다. 자료 제공이나 출처 표시를 이용 허락의 증거로 대신하지 않는다. 색 변경·이름 변경·재생성만으로 독자성 검토를 생략하지 않는다.

자동 검사는 법적 침해 여부를 확정하지 않는다. 한국 저작권법 제28조도 인용의 목적뿐 아니라 정당한 범위와 공정한 관행을 조건으로 둔다. 교육·무료라는 이유만으로 자동 통과시키지 않는다. [국가법령정보센터 제28조](https://www.law.go.kr/LSW/lsSideInfoP.do?docCls=jo&joBrNo=00&joNo=0028&lsiSeq=283335&urlMode=lsScJoRltInfoR) (2026-10-27 확인).

G10은 전체 제작 종료, 검수 진입·검수 후, Figma 게시 선행 검사와 최종화에 연결된다. 초기 조사·계획은 미확인 상태로 진행할 수 있다. 사용 근거 조사와 자체 표현 설계를 먼저 수행하고, 완성된 출력 묶음에 대한 사람의 검토로 제작 종료를 확인한다. 같은 제작 단계에서 PPTX·대본·PDF를 차례로 쓰는 동안에는 파일마다 검토 승인을 반복하지 않으며, 현재 출력의 G10이 통과해야 제작 완료·검수·배포로 진행한다. 사용 근거가 없으면 해당 자산을 사용 목록에서 빼고 새 표현과 자체 자산으로 교체한다. 기존 결과는 이력으로 보존하고 미확인 상태를 표시한다.

## 파일 계약

모든 경로는 강의 폴더 기준이며 증빙 객체는 `{path, sha256}`이다. `canonical`은 `harness/gate.py`의 JSON 정규화 해시 함수다. 승인·검토를 실제로 받지 않은 상태에서 다음 기록을 `reviewed`로 채우지 않는다.

`rights/inventory.json`:

- `unit`, `intended_uses`, `references`, `materials`.
- `intended_uses`: `live_presentation`, `pdf_distribution`, `exercise_distribution`, `recording_distribution`, `figma_publication` 중 실제 이용 범위. 라이브와 입력에서 선택한 PDF·실습·Figma 범위를 포함한다. 녹화 배포도 한다면 명시한다.
- `references`: `research/sources.json`의 모든 출처 ID를 정확히 한 번 포함한다. 각 행은 `source_id`, `use`, `review_note`를 가진다. `use`는 `analysis_only`, `quoted`, `adapted`, `reproduced`다. 분석용이라고 쓰고 실제로 추출 자산을 사용하는 모순은 사람 검토에서 반려한다.
- `quoted/adapted/reproduced` 출처에는 `basis`, `allowed_uses`, `evidence`가 필요하다. `basis`는 `permission/license/public_domain/exception_review`. 예외 적용을 근거로 할 때는 해당 사례의 `legal_reasoning`도 필요하다.
- `materials`: `assets/manifest.json`의 모든 자산을 정확히 한 번 포함한다. 각 행은 `asset_id`, 등록 자산과 같은 `file`, `use`, `basis`, `rights_holder`, `reason`, `allowed_uses`, `source_ids`, `evidence`를 가진다. `use`는 `original/generated/reproduced/adapted`, `basis`는 위 네 종류 또는 `original/generated`다. 복제·변형 사용을 `original/generated` 근거로 통과시킬 수 없다. 참조한 출처 ID는 등록 목록 안에 있어야 한다. 예외 적용에는 `legal_reasoning`이 필요하다.
- 이용 근거에는 실제 허락·라이선스와 조건, 자체 제작 과정, 생성 프롬프트와 참조 이력 등을 연결한다. `generated` 표기는 서비스 약관·참조 이미지·기존 표현 검토를 대신하지 않는다.

`rights/scan.json`은 실행기가 계산한다:

```powershell
python harness/gate.py --unit units/AI-001_강의명 copyright-scan --report
```

현재 전체 `plan.md`, 페이지·실습 항목, PPTX 본문, DOCX, 등록된 텍스트 실습 파일을 등록 출처와 대조한다. 한글·영숫자만 남겨 대소문자·공백·구두점 차이를 무시한 연속 20자 일치를 선별한다. 이는 검토 후보 기준이며 허용량·안전 비율이 아니다. `findings`는 위치·출처·표본·ID를, `text_unavailable_sources`는 텍스트를 읽을 수 없거나 없는 출처를 기록한다. 이미지 PDF는 별도 OCR 또는 사람이 직접 검토한다. 의미상 바꿔 쓰기, 그림·음원·모션·상표 유사성을 자동 판정하지 않는다.

`rights/review.json`:

- `unit`, `status="reviewed"`, `actor="human"`, `reviewer`, `message_ref`, `checked_on`(YYYY-MM-DD), 실제 검토 증빙 `evidence`.
- `scope_hash`: `copyright_gate.snapshot(engine)['scope_hash']`. 전체 계획·입력, 출처와 자산 목록 및 파일, 존재하는 표준 출력, 디자인 참조·검토와 그 후보·렌더·비교를 묶는다.
- `inventory_hash`: `canonical(inventory)`, `scan_hash`: `canonical(scan)`.
- `criteria`: 아래 여섯 키를 모두 포함하며 각 값은 `status="reviewed"`, `reason`, `evidence`를 가진다. 자동 일치 0건이어도 생략하지 않는다.
- `resolutions`: 모든 `findings`의 ID와 정확히 대응한다. 각 행은 `finding_id`, `decision`, `reason`, `evidence`. decision은 `common_term/permitted_quote/independent_expression` 중 근거에 맞게 선택한다. 해결하지 못한 항목은 통과 처리하지 않는다.

| 검토 키 | 사람이 확인할 내용 |
|---|---|
| text_expression | 원문 문장·독특한 표현의 재사용과 인용 범위 |
| examples_and_prompts | 비유·실습·프롬프트가 이름만 바뀐 사례인지 |
| structure_and_visuals | 고유 전개·도형·배경·비교 구성·이미지·모션의 재현 여부 |
| asset_rights | 실제 사용 자산, 참조 자료, 권리자, 이용 근거와 조건 |
| attribution | 인용·출처·크레디트·변경 고지 등 필요한 표시 |
| distribution_scope | 라이브·PDF·실습 파일·녹화·게시의 허용 범위 |

`rights/open-issues.json`은 검토 중 이슈 배열이다. G10 통과 시에만 `[]`여야 한다. 실제 검토 없이 삭제하여 통과시키지 않는다. 다른 파일에 `simulation=true`가 있으면 실제 모드에서는 거절한다. 테스트용 모의 기록은 실제 승인 근거가 아니다.

## 갱신과 한계

1. 출처와 사용하는 자산을 등록하고 미확인 근거를 이슈로 남긴다.
2. 허락 범위를 확인하거나 새 표현·자체 자산으로 교체한다. 목록에서 뺀 자산이 PPT에 남지 않았는지도 확인한다.
3. 현재 스캔을 저장한 뒤 원본과 결과를 나란히 검토하고 여섯 기준과 각 일치 항목의 근거를 기록한다.
4. `check --gate G10`을 실행한다. 계획·출처·자산·현재 출력이 바뀌면 스캔과 사람 검토를 갱신한다. 제작 전 기록으로 제작 후 결과를 통과시킬 수 없다.

검사기는 기록과 파일 일관성을 확인한다. 검토자 신원·허락의 진위나 누락 자산을 독립적으로 인증하지 않으며 법률 자문·법원의 판단을 대신하지 않는다. 별도로 만든 상세 계획·프롬프트 파일을 제작에 사용한다면 자산 목록에도 등록해 검토 범위에 넣는다.
