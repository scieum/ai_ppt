import json
from pathlib import Path
rows=json.loads(Path('output/reference-style-build/application-text-bounds.json').read_text(encoding='utf-8-sig'))
for r in rows:
 if r['slide']in[24,25,26,34]and r['name']in['part-label','group-label','copyright-footer']:print(r)
