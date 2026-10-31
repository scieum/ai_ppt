from pathlib import Path
import fitz
p=Path('output/webinar-knowledge-only/NotionTalk_모션그래픽_레퍼런스표현강화_40장_v20.pdf');d=fitz.open(p);d[24].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save('output/reference-style-build/pdf-25.png')
