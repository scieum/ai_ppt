from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json
B=Path(__file__).resolve().parent;R=B.parent.parent
old='NotionTalk_모션그래픽_논리구조에셋반영_43장_v31';new='NotionTalk_모션그래픽_결론텍스트바_43장_v32'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
spec=json.loads((B/'spec.json').read_text(encoding='utf8'))
with ZipFile(R/f'output/webinar-knowledge-only/{old}.pptx') as a,ZipFile(B/'bars.pptx') as b:
 data={n:a.read(n) for n in a.namelist()}
 for idx,item in enumerate(spec,1):
  root=E.fromstring(data[item['part']]);tree=root.find('p:cSld/p:spTree',N);maxid=max(map(int,root.xpath('//p:cNvPr/@id',namespaces=N)))
  for s in list(tree):
   nv=s.find('p:nvSpPr/p:cNvPr',N)
   if nv is not None and nv.get('name') in item['remove']:tree.remove(s)
  bars=E.fromstring(b.read(f'ppt/slides/slide{idx}.xml'))
  for s in bars.findall('p:cSld/p:spTree/p:sp',N):
   s=deepcopy(s);maxid+=1;s.find('p:nvSpPr/p:cNvPr',N).set('id',str(maxid));tree.append(s)
  data[item['part']]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as z:
  for n,d in data.items():z.writestr(n,d)
f=(R/'output/reference-logic-build/finalize.mjs').read_text(encoding='utf8').replace('NotionTalk_모션그래픽_준비물안내박스_43장_v30',old).replace(f'/{old}.pptx\'),pythonExecutable',f'/{new}.pptx\'),pythonExecutable')
(B/'finalize.mjs').write_text(f,encoding='utf8')
ex=(R/'output/reference-logic-build/export.ps1').read_text(encoding='utf-8-sig').replace('output/reference-logic-build','output/conclusion-bar-build').replace(old,new).replace('renders/reference-logic-20261030','renders/conclusion-bar-20261030')
(B/'export.ps1').write_text(ex,encoding='utf-8-sig')
print('Updated conclusion bars only; all other shapes and package parts preserved.')
