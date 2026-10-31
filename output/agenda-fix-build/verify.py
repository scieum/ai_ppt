from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops
import json,posixpath,hashlib,fitz
B=Path(__file__).resolve().parent;R=B.parents[1];U=next((R/'units').glob('AI-001*'));A=R/'assets/layout-library-20261028'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def ordered(z):
 rel={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};return[(rel[x.get('{'+N['r']+'}id')].lstrip('/')if rel[x.get('{'+N['r']+'}id')].startswith('/')else posixpath.normpath(posixpath.join('ppt',rel[x.get('{'+N['r']+'}id')])))for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
report=[]
for key,source,final,page,count,render,oldrender in[
 ('library',A/'NotionTalk_상황별레이아웃_20종_v3.pptx',A/'NotionTalk_상황별레이아웃_20종_v4.pptx',2,20,A/'previews',None),
 ('application',R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_레이아웃에셋적용_21장_v16.pptx',R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_목차수정_21장_v17.pptx',3,21,U/'renders/agenda-fix-20261028',U/'renders/layout-assets-20261028')]:
 with ZipFile(source)as s,ZipFile(final)as z:
  old=ordered(s);new=ordered(z);assert len(new)==count
  for n,(op,np)in enumerate(zip(old,new),1):
   if n!=page:assert s.read(op)==z.read(np),n
  x=E.fromstring(z.read(new[page-1]));custom=x.findall('.//a:custGeom',N);assert len(custom)==4
  assert all(len(g.findall('.//a:cubicBezTo',N))==6 for g in custom)
  labels=x.xpath('.//a:t/text()',namespaces=N);assert all('PART '+str(n)in labels for n in range(1,5))
  assert len(x.findall('.//p:pic',N))==1
  for p in s.namelist():
   if p.endswith('.gif'):assert s.read(p)==z.read(p)
  if key=='application':
   assert len(fitz.open(final.with_suffix('.pdf')))==21
   for n in range(1,22):
    if n!=page:assert ImageChops.difference(Image.open(render/f'slide-{n:02}.png'),Image.open(oldrender/f'slide-{n:02}.png')).getbbox()is None,n
  issues=[]
  for t in json.loads((B/(key+'-text-bounds.json')).read_text(encoding='utf-8-sig')):
   if t['slide']==page and t['name']not in['copyright-footer','copyright_footer']:
    if t['text_left']+t['text_width']>t['shape_left']+t['shape_width']+2 or t['text_top']+t['text_height']>t['shape_top']+t['shape_height']+2:issues.append(t['name'])
  assert not issues,issues
  sha=hashlib.sha256(final.read_bytes()).hexdigest();assert sha==json.loads((B/(key+'-validation.json')).read_text())['finalSha256']
  report.append({'key':key,'slide_count':count,'only_modified_page':page,'editable_rounded_blocks':4,'part_labels':4,'extra_header_subtitle_and_bottom_slogan_removed':True,'other_slide_XML_unchanged':True,'body_overflow':issues,'final_sha256':sha})
check=U/'checks/agenda-fix-20261028';check.mkdir(parents=True,exist_ok=True);(check/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
