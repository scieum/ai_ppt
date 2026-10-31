from zipfile import ZipFile
from lxml import etree as E
from pathlib import Path
import json
B=Path('output/reference-style-build');m=json.loads((B/'slide-map.json').read_text(encoding='utf8'))
with ZipFile(B/'candidate.pptx') as z:
 for d in m['slides'][:3]:
  x=E.fromstring(z.read(d['package_part']));out=B/f"debug-{d['page']}.xml";out.write_bytes(E.tostring(x,pretty_print=True));print(d['page'],x.nsmap)
