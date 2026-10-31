from pathlib import Path
import zipfile,lxml.etree as E
p=Path('output/webinar-samples/NotionTalk_모션그래픽_무료웨비나_대표5장_v2.pptx')
with zipfile.ZipFile(p) as z:
 for i in range(1,6):
  r=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'));ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
  print(i,[(x.find('.//p:cNvPr',ns).get('name'),x.find('.//a:blip',ns).attrib) for x in r.findall('.//p:pic',ns)])
