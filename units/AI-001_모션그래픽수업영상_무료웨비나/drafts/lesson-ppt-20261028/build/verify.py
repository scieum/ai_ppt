from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops
import json,hashlib,re,posixpath,datetime,fitz
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1];C=U/'checks/lesson-ppt-20261028';C.mkdir(exist_ok=True)
F=R/'output/webinar-lesson-applied/NotionTalk_웨비나_계획반영_Part1_15장_v1.pptx'
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';NS={'p':P,'a':A,'r':REL};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ordered(z):
 rels={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};ids=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',NS);out=[]
 for x in ids:
  t=rels[x.get('{'+REL+'}id')];out.append(t.lstrip('/') if t.startswith('/') else posixpath.normpath('ppt/'+t))
 return out
z=ZipFile(F);parts=ordered(z);assert len(parts)==15
texts=['\n'.join(E.fromstring(z.read(p)).xpath('.//a:t/text()',namespaces=NS)) for p in parts]
assert all('© 2026. NotionTalk. All rights reserved.' in x for x in texts)
prompts=[m[1] for m in re.finditer(r'```text\s*\n(.*?)\n```',(U/'part-1.md').read_text(encoding='utf-8'),re.S)]
norm=lambda x:re.sub(r'\s+','',x)
prompt_checks=[]
for page,idx in [(7,0),(9,2),(11,4)]:
 tree=E.fromstring(z.read(parts[page-1]));sp=next(x for x in tree.findall('.//p:sp',NS) if x.find('p:nvSpPr/p:cNvPr',NS).get('name')=='full-prompt-body');actual='\n'.join(sp.xpath('.//a:t/text()',namespaces=NS));assert norm(actual)==norm(prompts[idx]);prompt_checks.append({'page':page,'matches_part_1_prompt':True})
assert all('None' not in x for x in texts)
pdf=fitz.open(F.with_suffix('.pdf'));assert len(pdf)==15
for page in pdf:assert page.get_text().strip()
bounds=json.loads((U/'renders/lesson-ppt-20261028/text-bounds.json').read_text(encoding='utf-8-sig'));overflow=[x for x in bounds if x['text_height']>x['shape_height']+3 or x['text_width']>x['shape_width']+4];assert not overflow
pres=json.loads((B/'preservation.json').read_text(encoding='utf-8'))
source=R/'output/webinar-part01-added/NotionTalk_대표5장유지_Part0_Part1추가_9장_v2.pptx';base=ZipFile(source);bp=ordered(base)
for item in pres['source_slide_geometry']:
 before=E.fromstring(base.read(bp[item['source_display_page']-1]));after=E.fromstring(z.read(parts[item['target_page']-1]))
 for tree in [before,after]:
  for x in tree.findall('.//p:txBody',NS):x.getparent().remove(x)
 assert E.tostring(before,method='c14n')==E.tostring(after,method='c14n')
for n in base.namelist():
 if n.startswith(('ppt/media/','ppt/slideMasters/','ppt/slideLayouts/','ppt/theme/')):assert base.read(n)==z.read(n)
old=U/'renders/prep-tools-v2/powerpoint';new=U/'renders/lesson-ppt-20261028';comparisons=[]
for src,dst in [(1,1),(2,2),(3,3),(4,6),(5,8),(6,10),(7,13),(8,14),(9,15)]:
 a=Image.open(old/f'slide-{src:02}.png').convert('RGB');b=Image.open(new/f'slide-{dst:02}.png').convert('RGB');assert a.size==b.size
 same=ImageChops.difference(a,b).getbbox() is None
 if src in [1,3]:assert same
 pair=Image.new('RGB',(a.width*2,a.height));pair.paste(a,(0,0));pair.paste(b,(a.width,0));pair.save(C/f'comparison-{src:02}-to-{dst:02}.png')
 comparisons.append({'source_page':src,'target_page':dst,'pixel_identical':same})
checks=json.loads((U/'checks/lesson-plan-update/before.json').read_text(encoding='utf-8'))['before'];protected=[]
for name,expected in checks.items():
 actual=sha(R/name);assert actual==expected,name;protected.append({'path':name,'sha256':actual,'unchanged':True})
validation=json.loads((B/'validation.json').read_text(encoding='utf-8'));assert sha(F)==validation['finalSha256']
for doc in ['plan.md','part-1.md']:
 for link in re.findall(r'\]\(([^)]+)\)',(U/doc).read_text(encoding='utf-8')):
  if not link.startswith('http') and 'checks/lesson-ppt-20261028/verification.json' not in link:assert (U/link.split('#')[0]).exists(),link
report={'checked_on':'2026-10-28','timezone':'Asia/Seoul','scope':'Existing representative deck and Part 1 content applied; not the complete 42-slide curriculum','pptx':str(F.relative_to(R)),'pptx_sha256':sha(F),'pdf_sha256':sha(F.with_suffix('.pdf')),'slides':15,'pdf_pages':len(pdf),'opened_and_exported_by_powerpoint':True,'individual_slides_visually_inspected':list(range(1,16)),'native_text_boxes_checked':len(bounds),'text_overflow_flags':len(overflow),'start_prompts':prompt_checks,'original_geometry_preserved':pres['source_slide_geometry'],'original_media_masters_layouts_themes_preserved':True,'comparisons':comparisons,'source_files_unchanged':protected,'formal_G10_clearance_created':False,'new_app_execution_performed':False,'new_video_generation_performed':False}
(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['original_geometry_preserved','comparisons','source_files_unchanged']},ensure_ascii=False,indent=2))
