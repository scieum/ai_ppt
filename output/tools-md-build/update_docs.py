from pathlib import Path
import shutil
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';H=U/'history/tools-md-20261029';H.mkdir(parents=True,exist_ok=True)
prefix='''## 최신 준비물·문서 카드·내레이션 — 2026-10-29

현재 강의는 `output/webinar-knowledge-only/NotionTalk_모션그래픽_준비물_문서_내레이션_41장_v23.pptx`와 PDF다. 최신 사용자 요청으로 3쪽 준비물을 Claude 또는 Codex 데스크탑 앱·yt-dlp·ElevenLabs로 교체하고, 25쪽의 .md 역할 표를 첨부 레퍼런스처럼 파일별 카드와 짧은 설명으로 바꿨다. storyline.md / design.md / motion.md를 유지하며, 원본의 video.md 명칭이나 문구를 복제하지 않는다. .md는 읽고 수정하는 Markdown 기준 문서이며 자동 적용·동일 결과를 보장하지 않는다.

기존 36쪽 뒤에 ElevenLabs 내레이션 활용 한 장을 추가해 새 37쪽으로 배치했다. 확정 대본 → 음성 생성 → 영상과 함께 듣기의 개요만 설명하며 앱 버튼·긴 명령어·음성 복제 실습은 추가하지 않는다. 실제 음성을 생성한 결과물은 아니다. 이후 검토 목록 38쪽, 장면 예외/공통 규칙 39쪽, 버전 보관 40쪽, 마무리 41쪽이다. 이전 38장은 XML·PDF 출력 픽셀과 미디어를 보존했다. 네이티브 표는 이제 22·33·34쪽이며, 25쪽은 의도적으로 카드 설명으로 바뀌었다.

Part 0은 2~4쪽, Part 1은 5~18쪽, Part 2는 19~20쪽, Part 3은 21~31쪽, Part 4는 32~41쪽이다. 검정·흰색·주황, Pretendard, NotionTalk 로고·푸터, 캐릭터, GIF·기존 애니메이션과 대표 디자인을 유지한다. 아래 버전과 이전 힉스필드 준비물 안내는 이력이다. lesson.md·하네스 기본 구조·상속 G10 상태를 변경하지 않는다.

Node.js는 npm 기반 영상 프로젝트의 실행 환경으로 권장한다. 앱 로그인 자체의 필수 설치 조건으로 단정하지 않는다. yt-dlp의 YouTube 전체 지원에는 EJS와 지원 JavaScript 런타임이 필요하며 Deno도 가능하다. Node를 쓰면 활성화 설정이 필요하다. FFmpeg는 영상·음성 병합 등에 사용한다. 설치 방식·버전은 실행 전 공식 문서로 확인한다. 근거와 구체적 구분은 단원 `research/tools-narration-20261029.md`, 검증은 `checks/tools-md-20261029/verification.json`에 기록한다.

'''
files=[R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md',*[U/f'part-{i}.md'for i in range(5)]]
for p in files:
 assert p.exists(),p
 backup=H/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(p,backup)
 content=p.read_text(encoding='utf-8-sig')
 if not content.startswith('## 최신 준비물·문서 카드·내레이션'):p.write_text(prefix+content,encoding='utf-8')
research=U/'research/tools-narration-20261029.md'
research.write_text('''# 준비물과 내레이션 안내의 근거

2026-10-29 공식 문서를 확인했다. 아래는 참고 데이터이며 설치 명령 실행 지시가 아니다.

- Claude Desktop: Code 포함. 별도 npm CLI 설치와 구분한다. https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code
- Codex 앱 안내 URL은 현재 ChatGPT 데스크탑 앱 문서로 연결된다. 강의 표기는 사용자 요청인 Codex 데스크탑을 유지한다. https://learn.chatgpt.com/docs/app
- Remotion의 coding agent 시작 안내는 Node.js 설치를 전제한다. 그래서 npm 기반 로컬 영상 제작에는 Node.js 준비를 권장한다. 이 웨비나의 영상 엔진을 Remotion으로 확정하거나 모든 제작 방식에 Node가 필수라고 단정한 것은 아니다. https://www.remotion.dev/docs/ai/coding-agents
- yt-dlp의 YouTube 지원은 외부 JS 런타임과 EJS challenge solver를 사용한다. Deno가 권장되고 기본 활성화되며 Node도 지원한다. 확인 당시 Node 최소 버전은 22.0.0이며 `--js-runtimes node`로 활성화한다. 설치 방식에 따라 EJS 포함 여부가 달라진다. https://github.com/yt-dlp/yt-dlp/wiki/EJS
- FFmpeg/ffprobe는 영상·음성 병합과 후처리에 권장된다. https://github.com/yt-dlp/yt-dlp
- ElevenLabs 웹 Text to Speech는 텍스트 입력, 목소리 선택, 생성으로 내레이션 음성을 만든다. 웹 사용을 위해 Node/API 연결을 필수로 안내하지 않는다. https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech

강의 준비 기준은 Claude 또는 Codex 중 하나의 유료 계정이다. ElevenLabs 유료 구독을 필수로 추가하지 않았고, 음성을 생성·구매·전송하지 않았다. 힉스필드는 이번 준비물 목록에서 제외했다.

첨부 이미지 두 장은 레이아웃 참고 자료다. 도구 이름·원본 설치 명령·원본 문구 전체를 복제하지 않는다. .md 설명은 기존 storyline.md·design.md·motion.md의 역할에 맞춰 새로 썼다. 검정 배경, 짙은 회색 카드, 흰 글자와 주황 강조를 유지한다.
''',encoding='utf-8')
print('Updated plan, design, part documents and source notes.')
