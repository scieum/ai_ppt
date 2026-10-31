import sys,json
from pathlib import Path
sys.path.insert(0,'output/reference-analysis/deps')
import pymupdf as f
r=json.loads(Path('output/reference-analysis/inventory.json').read_text(encoding='utf-8'))[1]
d=f.open(r['path']);p=d[0]
for x in [22,14,18]:
 a=d.extract_image(x);Path('output/reference-analysis/image-%s.%s'%(x,a['ext'])).write_bytes(a['image'])
q=f.open();q.insert_pdf(d,from_page=3,to_page=3);p=q[0]
regions=[(460,280,1460,380),(1480,70,1850,150),(320,550,550,730),(690,550,860,730),(1010,530,1220,710),(1400,550,1560,700)]
for re in regions:p.add_redact_annot(f.Rect(re),fill=False)
p.apply_redactions(images=0,graphics=1,text=0)
p.get_pixmap(matrix=f.Matrix(.5,.5)).save('output/reference-analysis/testclean.png')
q.save('output/reference-analysis/testclean.pdf')
