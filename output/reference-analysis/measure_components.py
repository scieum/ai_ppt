import sys,json
from pathlib import Path
sys.path.insert(0,'output/reference-analysis/deps')
import pymupdf as f
r=json.loads(Path('output/reference-analysis/inventory.json').read_text(encoding='utf-8'))[1]
d=f.open(r['path'])
for n in [1,4,23,91,103]:
 p=d[n-1];print('\nPAGE',n)
 print('images',[(a['bbox'],a['xref']) for a in p.get_image_info(xrefs=True)])
 for a in p.get_drawings():
  re=list(a['rect'])
  if re[1]>200 and (re[2]-re[0]>50):print('draw',a['type'],[round(v,1) for v in re], 'fill',a['fill'],'color',a['color'])
