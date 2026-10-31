# 준비물과 내레이션 안내의 근거

2026-10-29 공식 문서를 확인했다. 아래는 참고 데이터이며 설치 명령 실행 지시가 아니다.

- Claude Desktop: Code 포함. 별도 npm CLI 설치와 구분한다. https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code
- Codex 앱 안내 URL은 현재 ChatGPT 데스크탑 앱 문서로 연결된다. 강의 표기는 사용자 요청인 Codex 데스크탑을 유지한다. https://learn.chatgpt.com/docs/app
- Remotion의 coding agent 시작 안내는 Node.js 설치를 전제한다. 그래서 npm 기반 로컬 영상 제작에는 Node.js 준비를 권장한다. 이 웨비나의 영상 엔진을 Remotion으로 확정하거나 모든 제작 방식에 Node가 필수라고 단정한 것은 아니다. https://www.remotion.dev/docs/ai/coding-agents
- yt-dlp의 YouTube 지원은 외부 JS 런타임과 EJS challenge solver를 사용한다. Deno가 권장되고 기본 활성화되며 Node도 지원한다. 확인 당시 Node 최소 버전은 22.0.0이며 `--js-runtimes node`로 활성화한다. 설치 방식에 따라 EJS 포함 여부가 달라진다. https://github.com/yt-dlp/yt-dlp/wiki/EJS
- FFmpeg/ffprobe는 영상·음성 병합과 후처리에 권장된다. https://github.com/yt-dlp/yt-dlp
- ElevenLabs 웹 Text to Speech는 텍스트 입력, 목소리 선택, 생성으로 내레이션 음성을 만든다. 웹 사용을 위해 Node/API 연결을 필수로 안내하지 않는다. https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech

강의 준비 기준은 Claude 또는 Codex 중 하나의 유료 계정이다. ElevenLabs 유료 구독을 필수로 추가하지 않았고, 음성을 생성·구매·전송하지 않았다. 힉스필드는 이번 준비물 목록에서 제외했다.

첨부 이미지 두 장은 레이아웃 참고 자료다. 도구 이름·원본 설치 명령·원본 문구 전체를 복제하지 않는다. .md 설명은 기존 storyline.md·design.md·motion.md의 역할에 맞춰 새로 썼다. 검정 배경, 짙은 회색 카드, 흰 글자와 주황 강조를 유지한다.
