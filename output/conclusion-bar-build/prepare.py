from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json
B=Path(__file__).resolve().parent;R=B.parent.parent
src=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_논리구조에셋반영_43장_v31.pptx';parts=json.loads((R/'output/typography-qa-build/spec.json').read_text(encoding='utf8'))['parts']
targets={6:'dev-definition-takeaway',20:'conclusion-text',22:'lesson7-storyline-note',23:'dev-definition-takeaway',25:'takeaway',26:'takeaway',36:'conclusion-text',37:'conclusion-text',38:'visual-takeaway',39:'conclusion-text',40:'conclusion-text'}
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'};spec=[]
with ZipFile(src) as z:
 for page,name in targets.items():
  root=E.fromstring(z.read(parts[page-1]));shape=next(s for s in root.findall('.//p:sp',N) if s.find('p:nvSpPr/p:cNvPr',N).get('name')==name)
  remove=['conclusion-band','conclusion-tag','conclusion-tag-text','conclusion-text'] if name=='conclusion-text' else [name]
  spec.append({'page':page,'part':parts[page-1],'remove':remove,'message':' '.join(shape.xpath('.//a:t/text()',namespaces=N))})
(B/'spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf8')
print('Selected 11 existing key-message positions; wording preserved.')
