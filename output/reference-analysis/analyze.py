from pathlib import Path
from pypdf import PdfReader
import json, hashlib

base = Path(r'C:\Users\User\Downloads')
out = Path(__file__).parent
names = [
    '[4차 사이클 라이브] 기획부터 디자인까지 쭉! AI 디자인 하네스 만들기 (1).pdf',
    '[사이클 라이브] 클로드 코드로 만드는 일관된 모션 시스템.pdf',
    '[사이클 라이브]MCP 적용부터 제작까지 100% 활용하기 (1).pdf',
    '[초보자 3주 챌린지 - 1주차] CLI 설치하고 에이전트 스킬 만들어보기 (1).pdf',
    '[초보자 3주 챌린지 - 2주차] Figma 디자인 기반으로 프론트 엔드 화면 만들어보기.pdf',
    '[허들링 클럽] 0802 AI 생성형 이미지 만들기 (1).pdf',
    '[허들링 클럽] 내 클로드 코드는 왜 쓸수록 멍청해질까_.pdf',
]
records = []
for i, name in enumerate(names, 1):
    path = base / name
    doc = PdfReader(path)
    pages = []
    for j, page in enumerate(doc.pages, 1):
        content = page.extract_text() or ''
        pages.append({'page': j, 'text': content})
    rec = {'id': f'R{i:02}', 'name': name, 'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'page_count': len(pages), 'pages': pages}
    records.append(rec)
    (out / f'R{i:02}-full.txt').write_text('\n\n'.join(f'===== PDF p.{p["page"]} =====\n{p["text"]}' for p in pages), encoding='utf-8')
    (out / f'R{i:02}-outline.txt').write_text('\n'.join(f'{p["page"]:03}: '+ ' / '.join(p['text'].splitlines())[:300] for p in pages), encoding='utf-8')
    print(f'R{i:02}: {len(pages)} pages; {sum(len(p["text"]) for p in pages)} chars; size={doc.pages[0].mediabox}; {name}')
(out / 'inventory.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
