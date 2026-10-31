# 하네스 사용 안내

기본 프로필은 AI 사용법 연수용 `ai_training` 2.0.0이다. G01~G09, 단계별 선행·종료 검사, 계획·디자인 확인, 역할별 쓰기, 원본 보호·이력·재개 구조는 유지한다.

- `rules.json`: 연수용 규칙의 단일 기준
- `training_gate.py`: 수행 목표·실습·시간·캡처·배포본·리허설·브랜드·참조 차용 검사
- `gate.py`, `design_gate.py`: 공통 실행·승인·상태·참조 검사
- `rules-science.json`: 기존 과학 수업용 1.1.0 규칙 보존
- `validate.py`: 외부 원본 없이 실행하는 격리 회귀 검사
- `validate_science.py`: 기존 79건의 과학 수업 회귀 검사와 선택적 원본 복사본 검증
- [데이터 계약](../docs/ai-training-contract.md): JSON 필드와 증빙 형식
- [편집용 양식](templates/ai-training/plan.md): 승인·통과 증빙을 포함하지 않은 예시

## 설치와 실행

Python 3.10 이상을 사용한다. 공통 실행기와 과학 프로필은 표준 라이브러리만 사용한다. 연수용 PDF 검증과 전체 회귀 시험에는 `pypdf`가 필요하다.

```powershell
python -m pip install -r harness/requirements.txt
python harness/gate.py --help
python harness/validate.py
```

회귀 시험은 모의 자료를 임시 폴더에 만들며 실제 강의·승인·Figma 검증을 수행하지 않는다. 상세 로그와 요약은 `harness/validation/<실행ID>/`, 최신 위치는 `harness/validation/latest.json`에 저장한다. 모의 증빙은 실제 모드에서 거절한다.

## 새 연수 준비

`units/AI-001_강의명/` 안에 강의별 자료를 준비한다. 루트 `plan.md`는 공통 지침이며 직접 검사할 실행 계획이 아니다.

편집용 예시는 `harness/templates/ai-training/`에 있다. `input.json`, `plan.md`를 강의 폴더에 복사하고, `sources.json`, `content-map.json`은 그 안의 `research/`에 둔다. 실제 강의의 입력·쪽별 계획·시간·실습으로 수정한다. 양식의 해시 자리표시자는 실제 출처 파일의 SHA-256으로 바꾼다. 승인 파일은 실제 사용자 응답을 확보한 뒤 작성한다.

1. `input.json`에 청중·환경·수행 목표·시간·장수·납품 항목·브랜드를 정한다.
2. `research/`에 출처와 내용·목표 대응, 필요한 공식 사용법 검증을 남긴다.
3. 강의별 `plan.md`에 사람이 읽을 계획과 정확히 하나의 `harness-plan` JSON 블록을 둔다.
4. 원본 보호 기준을 만들고 G01·G02를 검사한다. 실제 계획 확인 응답을 현재 계획 해시에 연결한다.
5. 자산과 실습 파일을 준비하고 G04, 대표 7유형과 G08, 사용자 디자인 확인 G09를 차례로 진행한다.
6. 전체 PPTX·DOCX·선택한 PDF를 제작하고, 페이지별 검토·리허설·필요 시 Figma 대응을 기록한다.

아래 `sources`는 실제 존재하는 읽기 전용 원본 경로로 바꾼다. 원본 없이 빈 보호 기준을 만들거나 기존 기준을 조용히 덮어쓸 수 없다.

```powershell
python harness/gate.py --unit units/AI-001_강의명 baseline --protect sources
python harness/gate.py --unit units/AI-001_강의명 check --gate G01 --gate G02
python harness/gate.py --unit units/AI-001_강의명 plan-hash
python harness/gate.py --unit units/AI-001_강의명 checkpoint research
python harness/gate.py --unit units/AI-001_강의명 checkpoint plan
python harness/gate.py --unit units/AI-001_강의명 preflight image
python harness/gate.py --unit units/AI-001_강의명 write image exercises/prompt.txt --from-file path/to/prepared-prompt.txt
python harness/gate.py --unit units/AI-001_강의명 checkpoint image
python harness/gate.py --unit units/AI-001_강의명 preflight prototype
python harness/gate.py --unit units/AI-001_강의명 check --gate G08 --gate G09
python harness/gate.py --unit units/AI-001_강의명 checkpoint prototype
python harness/gate.py --unit units/AI-001_강의명 checkpoint design_confirmation
python harness/gate.py --unit units/AI-001_강의명 preflight production
python harness/gate.py --unit units/AI-001_강의명 checkpoint production
python harness/gate.py --unit units/AI-001_강의명 checkpoint review
python harness/gate.py --unit units/AI-001_강의명 resume
python harness/gate.py --unit units/AI-001_강의명 finalize
```

각 명령 전에 해당 단계의 실제 파일·검토·승인 증빙을 준비해야 한다. 위 명령을 연속 실행하는 것만으로 증빙이 생성되지 않는다. `check`는 읽기 전용이며 `--report`를 붙이면 검사 기록을 저장한다. `preflight`, `checkpoint`, `resume`, `write`, `finalize`는 상태나 파일을 기록한다. 종료 코드는 0=통과, 1=검사 실패, 2=입력·실행 차단이다.

## 검사 내용

| 게이트 | 연수용 검사 |
|---|---|
| G01 | 수행 목표, 내용·디자인 출처, 기본/심화/제외 판정, 기술 절차의 공식 근거·검증일·환경·증빙 |
| G02 | 입력과 계획 일치, 내용·목표·실습·확인 연결, 페이지/실습/휴식의 시간 합계, 오류 복구·합류 경로 |
| G03 | 실제 사용자 확인, 현재 강의·계획 해시·응답 증빙 연결 |
| G04 | 계획한 이미지·실습 파일의 정확한 목록·해시·검토, 실제 캡처의 환경과 확인일 |
| G05 | PPTX/DOCX 페이지와 출처, 발화·조작·대기 구분, 선택한 PDF 파싱과 페이지 수 |
| G06 | 현재 파일의 내용/목표 적합성/시각 검토, PDF 페이지 대응, 전체 브랜드, 실습 리허설과 링크 확인, 선택한 Figma |
| G07 | 보호 원본의 경로·내용 불변 |
| G08 | 대표 7유형, exact/adopt 참조, 변경 명세와 목표 레이아웃, 현재 비교·검토, 제공 브랜드 |
| G09 | 현재 대표 버전의 실제 사용자 디자인 확인, 미해결 의견 없음 |

일반 이미지가 없는 설명형 강의는 빈 자산 목록을 명시할 수 있다. 목표마다 실습 또는 관찰 활동과 결과 확인이 필요하다. 생성 이미지로 도구 UI 증거를 대체할 수 없다. 로고·캐릭터·T셀파를 일괄 필수로 요구하지 않는다.

대표 시안 7유형은 실제 강의 장수와 별도로 준비한다. `exact`는 원본 레이아웃을 대조한다. `adopt`는 원본에서 무엇을 바꿨는지 전부 명세하고, 별도로 고정한 목표 템플릿과 시안을 대조한다. 두 방식 모두 좌표 허용 오차를 임의로 넓히지 않는다. 참조 변경은 현재 디자인 확인을 무효화한다.

## 선택 산출물과 최종화

`input.json.deliverables`의 `pdf`, `figma`, `exercises`는 모두 명시적인 불리언이다. 선택 변경은 계획 승인 해시에 반영된다.

- PPTX·DOCX는 항상 필요하다. PDF를 선택하면 `drafts/deck.pdf`, 페이지별 PDF 대응 검토가 필요하다.
- 실습 파일을 선택하면 `exercises/` 파일을 자산 목록에 등록한다. `finalize`는 원래 하위 경로를 유지하여 `final/exercises/`로 복사한다.
- Figma를 선택하면 기존 URL·현재 덱 해시·전체 페이지 대응·고유 노드·원격 확인 증빙을 요구한다. 선택하지 않으면 `figma/` 폴더를 요구하지 않으며 Figma 쓰기 선행 명령도 거절한다.
- 최종화는 모든 게이트·체크포인트가 유효할 때만 현재 납품 계약의 파일을 `final/`로 복사한다. 기존 파일은 이력에 보존하며 보호 대상으로 등록한 출력은 덮어쓰지 않는다.

## 기존 과학 수업 재개

과학 프로필은 자동 추정하지 않는다. 기존 계획과 승인 기록을 그대로 사용하되 모든 명령에 같은 규칙 파일을 지정한다. 코드 변경으로 기존 체크포인트가 무효화될 수 있으므로 먼저 재검사한다.

```powershell
python harness/gate.py --rules harness/rules-science.json --unit units/3-01_엔탈피와열화학반응식 check --report
python harness/validate.py --profile science
python harness/validate.py --profile ai_training
```

`docs/harness-*.md`의 기존 과학 수업 설계 이력과 새 연수 계약을 구분한다. 실제 레퍼런스 PPTX 복사본으로 과학 검사를 재실행하려면 `--source`와 `--renders`를 함께 제공할 수 있다.

## 판정의 범위

해시와 기록은 파일·참조·현재 버전의 일관성을 검사한다. 사람의 신원, 공식 문서 내용의 진위, 실제 실습 수행, 원격 서버의 현재 상태나 시각적 품질을 독립적으로 인증하지 않는다. 코드로 확인한 부분과 실제 사람·도구로 확인한 부분을 나누어 보고한다.

쓰기 제한은 `gate.py write`와 `finalize`를 통하는 관리 작업에 적용되며 OS 전체를 격리하지 않는다. 이미지 생성·Figma 도구는 해당 `tool-preflight` 성공 후 호출한다. 시험용 표시를 지워 모의 자료를 실제 승인·검토로 재사용하지 않는다.
