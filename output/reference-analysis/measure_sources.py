import sys,json
from pathlib import Path
sys.path.insert(0,'output/reference-analysis/deps')
import pymupdf as f
rows=json.loads(Path('output/reference-analysis/inventory.json').read_text(encoding='utf-8'))
d=f.open(rows[1]['path'])
print('page size',d[0].rect)
for n in [1,4,23,91,103]:
 p=d[n-1]
 print('\nPAGE',n,'draws',len(p.get_drawings()),'images',len(p.get_image_info()))
 for b in p.get_text('dict')['blocks']:
  if b['type']==0:
   for l in b['lines']:
    for s in l['spans']:print(json.dumps({k:s[k] for k in ['text','bbox','font','size','color']},ensure_ascii=False))
 p.get_pixmap(matrix=f.Matrix(.5,.5)).save('output/reference-analysis/R02-p%03d-actual.png'%n)
