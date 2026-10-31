from zipfile import ZipFile
from lxml import etree as E
from pathlib import Path
import json
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'};B=Path('output/reference-style-build');ds=json.loads((B/'slide-map.json').read_text(encoding='utf8'))['slides']
with ZipFile(B/'candidate.pptx')as z:
 for d in ds[:3]:
  x=E.fromstring(z.read(d['package_part']));print(d['page']);print(E.tostring(x.find(".//p:sp[p:nvSpPr/p:cNvPr[@name='part-label']]",N)) if False else x.xpath(".//p:cNvPr[@name='part-label']/..",namespaces=N)[0].getparent().find('p:spPr',N)[0].attrib)
  for sp in x.findall('.//p:sp',N)[:3]:print(E.tostring(sp.find('p:spPr/a:xfrm',N)).decode(),sp.find('p:nvSpPr/p:cNvPr',N).attrib)
  print('pics',[(q.find('p:nvPicPr/p:cNvPr',N).attrib, q.find('p:blipFill/a:blip',N).attrib) for q in x.findall('.//p:pic',N)])
