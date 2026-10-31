from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from collections import defaultdict
import json
B=Path(__file__).resolve().parent;R=B.parent.parent
spec=json.loads((B/'spec.json').read_text(encoding='utf-8'));log=json.loads((B/'artifact-edit-log.json').read_text(encoding='utf-8'));assert log['editedTextObjects']==len(spec['edits'])
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(spec['source']) as z:data={n:z.read(n) for n in z.namelist()}
grouped=defaultdict(list)
for e in spec['edits']:grouped[e['part']].append(e)
actual=[]
for part,edits in grouped.items():
 root=E.fromstring(data[part]);before=E.tostring(root)
 for e in edits:
  s=next(s for s in root.findall('.//p:sp',N) if s.find('p:nvSpPr/p:cNvPr',N).get('name')==e['name']);old=E.tostring(s)
  off=s.find('p:spPr/a:xfrm/a:off',N);ext=s.find('p:spPr/a:xfrm/a:ext',N);p=e['position']
  off.set('x',str(round(p['left']*9525)));off.set('y',str(round(p['top']*9525)));ext.set('cx',str(round(p['width']*9525)));ext.set('cy',str(round(p['height']*9525)))
  if e['font_pt'] is not None:
   for el in s.xpath('.//*[@sz]'):el.set('sz',str(round(e['font_pt']*100)))
  if e['anchor']:s.find('p:txBody/a:bodyPr',N).set('anchor',e['anchor'])
  if old!=E.tostring(s):actual.append(e)
 if before!=E.tostring(root):data[part]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as z:
 for n,v in data.items():z.writestr(n,v)
(B/'actual-edits.json').write_text(json.dumps(actual,ensure_ascii=False,indent=2),encoding='utf-8')
newname='NotionTalk_모션그래픽_폰트간격점검_43장_v29'
s=(R/'output/logo-color-build/finalize.mjs').read_text(encoding='utf-8')
s=s.replace('NotionTalk_모션그래픽_헤더확대_글라스로고_43장_v27.pptx','NotionTalk_모션그래픽_로고색복원_43장_v28.pptx')
start="finalPath:path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_로고색복원_43장_v28.pptx')"
s=s.replace(start,f"finalPath:path.join(R,'output/webinar-knowledge-only/{newname}.pptx')")
(B/'finalize.mjs').write_text(s,encoding='utf-8')
s=(R/'output/logo-color-build/export.ps1').read_text(encoding='utf-8-sig').replace('output/logo-color-build','output/typography-qa-build').replace('NotionTalk_모션그래픽_로고색복원_43장_v28',newname).replace('renders/logo-color-20261030','renders/typography-qa-20261030')
(B/'export.ps1').write_text(s,encoding='utf-8-sig')
print(f'Applied {len(actual)} minimal typography/frame adjustments; all images, timing, tables and content retained.')
