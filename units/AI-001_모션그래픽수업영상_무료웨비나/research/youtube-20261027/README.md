# 유튜브 6편 — yt-dlp 수집 기록

분석 문서의 정본은 루트의 [lesson.md](../../../../lesson.md)다. 조사일은 2026-10-27이다.

## 최종 상태

6편 모두 전체 한국어 자막을 끝부분까지 확보하고 읽었다. 수집한 것은 메타데이터·설명란·자막이며 영상 본체와 시각 프레임은 수집·분석하지 않았다. 자동 인식 또는 번역 자막에는 고유명사·용어 오류가 있을 수 있다. 화면에만 보이는 프롬프트 전문이나 시각 구성을 확인했다고 주장하지 않는다.

- `source-index.json`: 영상별 제목·채널·길이·자막 종료 시각·구간 수·문자 수·원본 자막 SHA256.
- `collection-report.json`: 최종 6편의 자막·메타데이터·정규화 파일 존재와 파싱 확인.
- `yt-dlp/*.ko.json3`: 수집한 자막 원본. 로컬 조사 자료로 보존한다.
- `yt-dlp/*.transcript.txt`, `*.segments.json`: 시간표시를 정규화한 분석용 파일.
- `yt-dlp/*.info.json`, `*.description`: yt-dlp의 메타데이터와 설명란.

자막의 시간 구간은 영상 끝을 약간 넘거나 마지막 음악 구간 전에 끝날 수 있다. `fetch-results.json`·`remaining-results.json`은 당시 시도의 성공·오류 이력이다. 재시도 후 상태를 나타내는 정본은 `collection-report.json`이다. 초기에 생성된 크기 0의 `*-captions-*.json`은 실패 응답이며 분석에 사용하지 않았다.

## 도구 검증

사용자 요청의 [공식 yt-dlp 서명 검증 절차](https://github.com/yt-dlp/yt-dlp#release-files)를 적용했다. [2026.10.26 릴리스](https://github.com/yt-dlp/yt-dlp/releases/tag/2026.10.26)의 `yt-dlp.exe`와 두 체크섬 목록·서명을 내려받았다.

```powershell
gpg --verify SHA2-256SUMS.sig SHA2-256SUMS
gpg --verify SHA2-512SUMS.sig SHA2-512SUMS
```

두 서명 검증에 더해 실행 파일의 실제 SHA256·SHA512와 목록의 값을 각각 대조해 일치를 확인했다. GPG는 기존 Git 설치본을 사용했고, 키는 작업 폴더의 별도 키링에 가져왔다. 전역 신뢰도를 변경하지 않았다. 공식 저장소 키 지문은 `AC0C BBE6 848D 6A87 3464 AF4E 57CF 6593 3B5A 7581`이다. GPG의 서명 유효성과 키 소유자에 대한 개인 신뢰 인증은 별개다.

원본 raw 공개키 URL에서 Windows 인증서 폐기 상태 확인 오류가 발생해, 동일 공식 저장소의 GitHub Contents API로 공개키 파일을 받았다. TLS 검증은 비활성화하지 않았다. 상세 결과는 로컬 `toolchain/yt-dlp-2026.10.26/verification.json`, `verify-256.log`, `verify-512.log`에 있다.

## 수집 경로와 재현

1. `setup-ytdlp.ps1`: 공식 배포 파일 취득·GPG 서명 검증·두 해시 대조·버전 확인.
2. `fetch_ytdlp.py`: 검증한 실행 파일에 `--skip-download --write-subs --write-auto-subs --sub-langs ko --sub-format json3 --write-info-json --write-description`을 적용. 기존 정상 수집 파일은 건너뛴다.
3. 일부 자막 다운로드에서 실행 파일 내부 curl_cffi의 인증서 체인 오류가 발생했다. `no-certifi,prefer-legacy-http-handler` 호환 옵션 후에도 일부 요청에 같은 오류가 남았다.
4. `fetch_remaining.py`: 동일한 검증 배포본으로 메타데이터와 자막 URL을 추출하고 Python urllib의 기본 TLS 검증으로 자막을 받았다. `wOF1EDpWxQw` 수집에 성공했다.
5. `x08U8HJKV0E`의 자동 번역 경로는 HTTP 429를 반환했다. `retry_last.py`에서 메타데이터에 명시된 한국어 원본 자동 자막 트랙 `ko-orig`로 요청해 성공했다. 로그인 쿠키·프록시 변경·TLS 검증 해제는 사용하지 않았다.
6. `normalize_transcripts.py`: 6개 JSON3를 파싱해 시간표시 텍스트와 구간 JSON·해시 목록을 생성했다.

실행 환경의 Node.js 경로가 스크립트에 기록되어 있다. 다른 PC에서 재현하려면 해당 환경 경로를 조정해야 한다. 스트리밍 자막 URL은 만료되므로 오래된 URL을 재사용하지 말고 yt-dlp로 다시 추출한다. 공개키 파일과 실제 서명 키도 재취득 시 다시 확인한다.

## 보존·배포

전체 자막·원본 메타데이터의 만료 URL·다운로드 실행 파일·로컬 키링은 `.gitignore`로 저장소 추가 대상에서 제외했다. 분석 원문과 수집 증거는 로컬에 남아 있다. 배포용 강의에는 자체 요약·새로 작성한 예제·원본 링크를 사용하고, 원본 영상·음원·캡처의 삽입은 기존 G10에서 별도로 검토한다.

이전 힉스필드 분석은 이번 `lesson.md`의 근거에 포함하지 않았다. 기존 PPT·PDF·plan.md·design.md·검사 코드·G10 상태는 이번 자막 분석 작업에서 변경하지 않았다.
