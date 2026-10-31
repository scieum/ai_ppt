from pathlib import Path
import fitz,json
R=Path.cwd();B=R/'output/dark-tables-build';c=json.loads((R/'assets/layout-library-20261028/catalog.json').read_text(encoding='utf8'))
d=fitz.open(c['source_documents'][0]['path'])
for n in [10,20,47,70]:d[n-1].get_pixmap(matrix=fitz.Matrix(1,1)).save(str(B/f'reference-{n}.png'))
d=fitz.open(R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_이미지설명강화_40장_v21.pdf')
for n in [22,25,33,34]:d[n-1].get_pixmap(matrix=fitz.Matrix(1,1)).save(str(B/f'before-{n}.png'))
