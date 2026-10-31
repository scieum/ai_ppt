from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import fitz,json,hashlib
B=Path(__file__).resolve().parent;R=B.parent.parent
U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
O=R/'output/webinar-knowledge-only'
old=O/'NotionTalk_모션그래픽_이미지설명강화_40장_v21.pptx'
new=O/'NotionTalk_모션그래픽_표디자인정리_40장_v22.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
changed=[]
slide_map=json.loads((B/'slide-map.json').read_text(encoding='utf-8'))
with ZipFile(old) as a,ZipFile(new) as b:
 assert set(a.namelist())==set(b.namelist())
 for name in a.namelist():
  if a.read(name)!=b.read(name):changed.append(name)
 assert set(changed)==set(slide_map['changed']),changed
 for n in (25,34):
  name=slide_map['ordered_parts'][n-1]
  x,y=E.fromstring(a.read(name)),E.fromstring(b.read(name))
  tx,ty=x.find('.//a:tbl',ns),y.find('.//a:tbl',ns)
  assert tx.xpath('.//a:t/text()',namespaces=ns)==ty.xpath('.//a:t/text()',namespaces=ns)
  fills=ty.xpath('.//a:tcPr/a:solidFill/a:srgbClr/@val',namespaces=ns)
  assert set(fills)=={'2D2D2D','303030','1E1E1E'},fills
  tx.getparent().remove(tx);ty.getparent().remove(ty)
  assert E.tostring(x)==E.tostring(y)
 gifs=sum(n.startswith('ppt/media/') and n.lower().endswith('.gif') for n in b.namelist())
pdf0,pdf1=fitz.open(old.with_suffix('.pdf')),fitz.open(new.with_suffix('.pdf'))
assert len(pdf0)==len(pdf1)==40
same=[]
for i in range(40):
 p0,p1=pdf0[i],pdf1[i]
 if i+1 not in (25,34):
  assert p0.get_pixmap().samples==p1.get_pixmap().samples,f'Unexpected PDF change {i+1}'
  same.append(i+1)
 else:
  p1.get_pixmap(matrix=fitz.Matrix(2,2)).save(B/f'after-{i+1}.png')
  assert p0.get_text().split()==p1.get_text().split()
out={'slides':40,'changed_slides':[25,34],'other_slides_pixel_identical':same,'changed_package_parts':changed,'all_text_preserved':True,'all_media_notes_and_timing_preserved':True,'gif_count':gifs,'reference':'R01 page 20 dark comparison table','table_fills':['#2D2D2D','#303030','#1E1E1E'],'pptx_sha256':hashlib.sha256(new.read_bytes()).hexdigest()}
check=U/'checks/dark-tables-20261029';check.mkdir(parents=True,exist_ok=True)
(check/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
