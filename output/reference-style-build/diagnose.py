from zipfile import ZipFile
from lxml import etree as E
from pathlib import Path
import json
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
B=Path('output/reference-style-build');m=json.loads((B/'slide-map.json').read_text(encoding='utf8'))
with ZipFile(B/'candidate.pptx') as z:
 for d in m['slides']:
  x=E.fromstring(z.read(d['package_part']));print(d['page'],x.xpath('.//a:t/text()',namespaces=N)[:5]);print(x.xpath('.//p:cNvPr/@descr',namespaces=N))
