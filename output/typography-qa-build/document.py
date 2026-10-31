from pathlib import Path
import json,shutil
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
prefix='''## 최신 전체 글자·간격 점검 — 2026-10-30

현재 강의는 `output/webinar-knowledge-only/NotionTalk_모션그래픽_폰트간격점검_43장_v29.pptx`와 PDF다. 승인한 v28을 바탕으로 43장 전체를 검토하고 같은 역할의 글자 크기·시작 위치·간격만 정리했다. 내용·순서·색·이미지·로고·표·GIF·애니메이션·노트를 보존한다. 기존 디자인을 새로 구성하지 않는다.

- 공통 상단 Part 표기는 18pt, 섹션 번호·제목은 24pt로 통일한다. 이미 승인한 준비물 장표의 확대 크기를 기준으로 하며 이전 +2pt를 다시 누적하지 않는다.
- 일반 본문 장표의 큰 제목은 32pt, 부제는 17pt, 푸터는 10pt로 정리하고 같은 역할의 세로 위치·정렬을 맞춘다. 표지·파트 구분·목차의 별도 큰 제목과 캘린더 날짜 표기는 유지한다.
- 1280×720 기준 Part 표기는 x60/y59.333, 섹션 번호는 x60/y95, 섹션 제목은 x116/y95다. 일반 큰 제목 y199.333, 부제 y269.333, 푸터 y686.667이다. 글꼴은 Pretendard를 유지한다.
- 31쪽 폴더 아래 ‘노션톡 영상 기준’ 문구만 6px 아래로 내려 그림과 간격을 확보했다. 다른 본문·이미지 위치는 그대로다.
- 준비물 로고는 클로드 코랄·힉스필드 라임·코덱스 흰색과 중성 유리 재질을 유지한다. 43장 구성과 11월 2일 시작 사이클 일정도 유지한다.

원본 전체 장표와 수정본 렌더를 시각 검토했고 PowerPoint 글자 크기/영역·겹침 검사를 통과했다. 모든 텍스트·미디어·표·애니메이션을 보존했으며 PDF 픽셀 차이는 편집한 텍스트 영역 안에만 있다. 검증은 단원 `checks/typography-qa-20261030/verification.json`, 렌더는 `renders/typography-qa-20261030/`다. v28은 보존하며 아래는 이전 이력이다.

'''
for p in [R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md',U/'part-0.md']:
 backup=U/'history/typography-qa-20261030'/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(p,backup)
 s=p.read_text(encoding='utf-8-sig')
 if not s.startswith('## 최신 전체 글자·간격 점검'):p.write_text(prefix+s,encoding='utf-8')
p=U/'checks/typography-qa-20261030/verification.json';v=json.loads(p.read_text(encoding='utf-8'))
v['visual_review']={'source_all_43_full_size':True,'final_all_43_contact_sheets':True,'final_full_size_spot_checks':[3,6,24,31,41,43],'unresolved_typography_or_spacing_findings':[]}
p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
print('Saved v29 review record and current typography rules; prior documents backed up.')
