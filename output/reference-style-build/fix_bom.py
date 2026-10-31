from pathlib import Path
p=Path('output/reference-style-build/export.ps1');p.write_text(p.read_text(encoding='utf-8-sig').lstrip('\ufeff'),encoding='utf-8-sig')
