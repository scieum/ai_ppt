# 강의별 계획 양식

이 파일은 편집용 예시이며 실제 제작 승인·검증 기록이 아니다.

시간과 페이지를 실제 강의에 맞게 수정하고 출처·실습 파일·대표 시안을 준비한다. 승인 증빙은 실제 사용자 응답 이후에만 만든다.

```harness-plan
{
  "profile": "ai_training",
  "unit": "AI-001_안내문 초안 만들기",
  "audience": "AI 채팅 도구를 처음 사용하는 성인",
  "format": "workshop",
  "environment": {
    "product": "선택한 AI 도구명",
    "version": "제작일 확인 필요",
    "os": "Windows",
    "ui_language": "한국어",
    "account": "사용 계정과 요금제 확인 필요"
  },
  "objectives": [
    {
      "id": "O1",
      "action": "일정 메모로 안내문 초안을 만들고 원문과 대조한다",
      "result": "검토한 안내문 텍스트"
    }
  ],
  "target_slides": 7,
  "minutes": 7,
  "deliverables": {
    "pdf": true,
    "figma": false,
    "exercises": true
  },
  "branding": {
    "mode": "text",
    "label": "강사명 입력",
    "logos": [],
    "brand_id": null,
    "copyright": {
      "template": "© {year}. {holder}. All rights reserved.",
      "year": 2026
    }
  },
  "design": "design.md",
  "supplementary": {},
  "links": [],
  "exercises": [
    {
      "id": "EX1",
      "title": "안내문 초안 작성과 대조",
      "objective_ids": [
        "O1"
      ],
      "mode": "hands_on",
      "start_conditions": "선택한 도구에 로그인하고 일정 메모 열기",
      "input_location": "AI 도구의 새 대화 입력창",
      "instructions": [
        "일정 메모와 프롬프트를 입력한다",
        "출력의 날짜·대상·장소를 원문과 비교한다"
      ],
      "expected_result": "일정 메모에 근거한 안내문 초안",
      "success_criteria": [
        "날짜·대상·장소가 원문과 일치한다"
      ],
      "errors": [
        {
          "symptom": "필수 정보 누락",
          "check": "원문과 출력 비교",
          "action": "누락한 항목을 지정해 다시 요청",
          "expected_state": "필수 정보가 모두 포함된 초안"
        }
      ],
      "fallback": "강사가 제공한 중간 완성본으로 결과 비교 활동에 합류",
      "customization": "자신의 행사 일정으로 메모 교체",
      "minutes": 7,
      "file_ids": [
        "PROMPT"
      ],
      "source_ids": [
        "S1"
      ]
    }
  ],
  "slides": [
    {
      "number": 1,
      "title": "오늘의 결과물",
      "message": "오늘의 결과물의 핵심 메시지 작성",
      "content_ids": [
        "C1"
      ],
      "source_ids": [
        "S1"
      ],
      "visual": [],
      "layout": "cover",
      "design_type": "cover",
      "character": "none",
      "minutes": 1,
      "activity": "explanation",
      "objective_ids": [
        "O1"
      ],
      "exercise_ids": [
        "EX1"
      ],
      "instructor_action": "이 페이지의 설명·조작 작성",
      "learner_action": "이 페이지에서 수행할 행동 작성"
    },
    {
      "number": 2,
      "title": "실습 흐름",
      "message": "실습 흐름의 핵심 메시지 작성",
      "content_ids": [
        "C1"
      ],
      "source_ids": [
        "S1"
      ],
      "visual": [],
      "layout": "part",
      "design_type": "part",
      "character": "none",
      "minutes": 1,
      "activity": "explanation",
      "objective_ids": [
        "O1"
      ],
      "exercise_ids": [
        "EX1"
      ],
      "instructor_action": "이 페이지의 설명·조작 작성",
      "learner_action": "이 페이지에서 수행할 행동 작성"
    },
    {
      "number": 3,
      "title": "수행 목표",
      "message": "수행 목표의 핵심 메시지 작성",
      "content_ids": [
        "C1"
      ],
      "source_ids": [
        "S1"
      ],
      "visual": [],
      "layout": "objectives",
      "design_type": "objectives",
      "character": "none",
      "minutes": 1,
      "activity": "explanation",
      "objective_ids": [
        "O1"
      ],
      "exercise_ids": [
        "EX1"
      ],
      "instructor_action": "이 페이지의 설명·조작 작성",
      "learner_action": "이 페이지에서 수행할 행동 작성"
    },
    {
      "number": 4,
      "title": "진행 순서",
      "message": "진행 순서의 핵심 메시지 작성",
      "content_ids": [
        "C1"
      ],
      "source_ids": [
        "S1"
      ],
      "visual": [],
      "layout": "contents",
      "design_type": "contents",
      "character": "none",
      "minutes": 1,
      "activity": "explanation",
      "objective_ids": [
        "O1"
      ],
      "exercise_ids": [
        "EX1"
      ],
      "instructor_action": "이 페이지의 설명·조작 작성",
      "learner_action": "이 페이지에서 수행할 행동 작성"
    },
    {
      "number": 5,
      "title": "입력 자료와 화면",
      "message": "입력 자료와 화면의 핵심 메시지 작성",
      "content_ids": [
        "C1"
      ],
      "source_ids": [
        "S1"
      ],
      "visual": [],
      "layout": "figure",
      "design_type": "figure",
      "character": "none",
      "minutes": 1,
      "activity": "explanation",
      "objective_ids": [
        "O1"
      ],
      "exercise_ids": [
        "EX1"
      ],
      "instructor_action": "이 페이지의 설명·조작 작성",
      "learner_action": "이 페이지에서 수행할 행동 작성"
    },
    {
      "number": 6,
      "title": "안내문 초안 작성",
      "message": "안내문 초안 작성의 핵심 메시지 작성",
      "content_ids": [
        "C1"
      ],
      "source_ids": [
        "S1"
      ],
      "visual": [],
      "layout": "table_formula",
      "design_type": "table_formula",
      "character": "none",
      "minutes": 1,
      "activity": "practice",
      "objective_ids": [
        "O1"
      ],
      "exercise_ids": [
        "EX1"
      ],
      "instructor_action": "이 페이지의 설명·조작 작성",
      "learner_action": "이 페이지에서 수행할 행동 작성"
    },
    {
      "number": 7,
      "title": "초안 대조와 수정",
      "message": "초안 대조와 수정의 핵심 메시지 작성",
      "content_ids": [
        "C1"
      ],
      "source_ids": [
        "S1"
      ],
      "visual": [],
      "layout": "comparison",
      "design_type": "comparison",
      "character": "none",
      "minutes": 1,
      "activity": "check",
      "objective_ids": [
        "O1"
      ],
      "exercise_ids": [
        "EX1"
      ],
      "instructor_action": "이 페이지의 설명·조작 작성",
      "learner_action": "이 페이지에서 수행할 행동 작성"
    }
  ]
}
```
