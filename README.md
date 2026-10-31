# PPT Harness

작업 저장소: [scieum/ai_ppt](https://github.com/scieum/ai_ppt). 원본 하네스의 Git 이력을 유지하며 AI 연수용 개정과 노션톡 웨비나 작업을 보관합니다.

## 최신 웨비나 자료

- [48장 PPTX v34](output/webinar-knowledge-only/NotionTalk_모션그래픽_텍스트바정리_48장_v34.pptx)
- [정지 화면 PDF v34](output/webinar-knowledge-only/NotionTalk_모션그래픽_텍스트바정리_48장_v34.pdf)
- [단원 계획](units/AI-001_모션그래픽수업영상_무료웨비나/plan.md) · [디자인 기준](units/AI-001_모션그래픽수업영상_무료웨비나/design.md)
- [영상 분석](lesson.md) · [모션 효과·효과음·AE 추가 조사](docs/motion-effects-audio-ae-20261030.md)

PPTX의 모션 예시는 슬라이드 쇼에서 움직입니다. 19쪽 효과음 비교 영상은 클릭해서 재생합니다. PDF는 정지 화면만 제공합니다.

완성본과 이전 납품 버전, 직접 만든 에셋, 제작 스크립트, 계획·분석·검수 기록을 포함합니다. 설치 패키지, 다운로드한 실행 파일, 원본 자료 캐시, 임시 프레임·렌더·중간 PPT는 제외합니다. 기존 검수 기록의 로컬 절대 경로는 당시 실행 증거이며 다른 컴퓨터에서는 경로 조정이 필요합니다. 일부 제작 스크립트는 Codex의 번들 라이브러리와 Windows PowerPoint를 사용합니다.

AI 강의·사용법 연수 자료의 근거 분석, 페이지 계획, 승인, 실습·디자인·배포본 검수를 관리하는 하네스입니다. 기존 G01~G09 구조에 저작권·권리·독자성 검토 G10을 추가했으며 과학 수업용 프로필은 별도로 보존합니다.

## 구성

- `AGENTS.md`: 작업 절차와 사용자 지침
- `design.md`: 디자인 기준
- `docs/`: 하네스 목적·설계·파이프라인·역할·게이트·검증 및 관련 참고 문서
- `plan.md`, `units/*/plan.md`: 공통 제작 기준과 강의별 실행 계획
- `harness/gate.py`: 제작 단계 및 승인 검사
- `harness/design_gate.py`: 레퍼런스 재현 검사
- `harness/training_gate.py`: AI 연수 데이터·실습·납품·리허설·디자인 검사
- `harness/copyright_gate.py`: 저작권 검토 기록·이용 근거·문구 일치 선별 검사
- `harness/rules.json`: AI 연수용 G01~G10 검사 규칙
- `harness/rules-science.json`: 기존 과학 수업용 규칙
- `harness/validate.py`: 격리된 회귀 검증
- `harness/README.md`: 사용법과 데이터 계약
- `harness/validation-report.md`: 기존 검증 결과 기록

## 실행

Python 3.10 이상을 사용합니다. 연수용 PDF 검증과 회귀 시험에는 pypdf가 필요합니다.

```sh
python -m pip install -r harness/requirements.txt
python harness/gate.py --help
python harness/validate.py
```

실제 제작·검증에는 해당 명령의 입력 자료와 승인·검토 증빙이 필요합니다. 기존 검토 상태를 보존하며 코드 시험이나 저장소 업로드를 배포 승인으로 간주하지 않습니다. 원본 교재 PDF와 로컬 도구 설치본은 이 저장소에 포함하지 않습니다.

사용법과 새 강의 양식은 [harness/README.md](harness/README.md), 실행 필드는 [AI 연수 계약](docs/ai-training-contract.md), 시험 결과는 [검증 보고서](harness/validation-report.md)를 참고합니다. 코드 시험은 실제 강의의 디자인 승인이나 전체 제작 완료를 의미하지 않습니다.
