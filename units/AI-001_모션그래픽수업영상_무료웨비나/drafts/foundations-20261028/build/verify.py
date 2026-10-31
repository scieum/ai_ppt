from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageChops
import json,re,hashlib,posixpath,fitz
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1];C=U/'checks/foundations-20261028';C.mkdir(exist_ok=True)
F=R/'output/webinar-fundamentals/NotionTalk_모션그래픽_개념부터실습까지_21장_v1.pptx';S=R/'output/webinar-lesson-applied/NotionTalk_웨비나_계획반영_Part1_15장_v1.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ordered(z):
 rels={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};out=[]
 for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N):
  t=rels[x.get('{'+N['r']+'}id')];out.append(t.lstrip('/') if t.startswith('/') else posixpath.normpath('ppt/'+t))
 return out
z=ZipFile(F);parts=ordered(z);assert len(parts)==21;pdf=fitz.open(F.with_suffix('.pdf'));assert len(pdf)==21
timing=[];alltext=[]
for page,part in enumerate(parts,1):
 x=E.fromstring(z.read(part));t='\n'.join(x.xpath('.//a:t/text()',namespaces=N));alltext.append(t);assert '© 2026. NotionTalk. All rights reserved.' in t
 if x.find('p:timing',N) is not None:timing.append(page)
 assert pdf[page-1].get_text().strip()
assert timing==[4,6,7,8,9]
native=json.loads((B/'native-animation-report.json').read_text(encoding='utf-8-sig'));assert len(native)==18
prompts=[m[1] for m in re.finditer(r'```text\s*\n(.*?)\n```',(U/'part-1.md').read_text(encoding='utf-8'),re.S)];norm=lambda t:re.sub(r'\s+','',t)
for page,idx in [(13,0),(15,2),(17,4)]:assert norm(prompts[idx]) in norm(alltext[page-1])
plantext=(U/'plan.md').read_text(encoding='utf-8');blocks=re.findall(r'```harness-plan\s*\n(.*?)\n```',plantext,re.S);assert len(blocks)==1;plan=json.loads(blocks[0]);assert len(plan['slides'])==48;assert plan['target_slides']==48
assert [s['number'] for s in plan['slides']]==list(range(1,49));assert sum(s['minutes'] for s in plan['slides'])==90;assert sum(s['minutes'] for s in plan['slides'][4:16])==26
rows=[l for l in plantext.split('```harness-plan')[0].splitlines() if re.match(r'^\| \d+ \|',l)];assert len(rows)==48
for row,s in zip(rows,plan['slides']):
 t=[x.strip() for x in row.strip('|').split('|')];assert [int(t[0]),float(t[1]),t[2],t[3],t[4]]==[s['number'],s['minutes'],s['title'],s['instructor_action'],s['learner_action']]
for e in plan['exercises']:assert e['minutes']==sum(s['minutes'] for s in plan['slides'] if e['id'] in s['exercise_ids'])
bounds=json.loads((U/'renders/foundations-20261028/text-bounds.json').read_text(encoding='utf-8-sig'));overflow=[x for x in bounds if x['text_height']>x['shape_height']+3 or x['text_width']>x['shape_width']+4];assert not overflow
base=ZipFile(S);bp=ordered(base);source_old=U/'renders/lesson-ppt-20261028';render=U/'renders/foundations-20261028';same=[]
mapping=[(1,1),(2,2),(3,3)]+[(i,i+6) for i in range(5,16)]
for old,new in mapping:
 a=E.fromstring(base.read(bp[old-1]));b=E.fromstring(z.read(parts[new-1]))
 for x in [a,b]:
  for tx in x.findall('.//p:txBody',N):tx.getparent().remove(tx)
 assert E.tostring(a,method='c14n')==E.tostring(b,method='c14n')
 ia=Image.open(source_old/f'slide-{old:02}.png').convert('RGB');ib=Image.open(render/f'slide-{new:02}.png').convert('RGB');identical=ImageChops.difference(ia,ib).getbbox() is None
 if old!=2:assert identical,(old,new)
 same.append({'old_page':old,'new_page':new,'pixel_identical':identical,'non_text_xml_identical':True})
for name in base.namelist():
 if name.startswith(('ppt/media/','ppt/slideMasters/','ppt/slideLayouts/','ppt/theme/')):assert base.read(name)==z.read(name)
for name,h in json.loads((B/'source-hashes.json').read_text(encoding='utf-8')).items():assert sha(R/name)==h
for file in ['plan.md','part-1.md']:
 for target in re.findall(r'\]\(([^)]+)\)',(U/file).read_text(encoding='utf-8')):
  if not target.startswith('http'):assert (U/target.split('#')[0]).exists(),target
playback=json.loads((render/'animation-playback-check.json').read_text(encoding='utf-8'));assert playback['all_video_frames_decode'];assert playback['first_slide_mean_frame_difference']>0
validation=json.loads((B/'validation.json').read_text(encoding='utf-8'));assert sha(F)==validation['finalSha256']
report={'checked_on':'2026-10-28','slides':21,'pdf_pages':21,'foundation_pages':list(range(4,11)),'animation_pages':timing,'native_effects':18,'powerpoint_open_render_export':True,'native_animation_video_playback_check':playback,'text_boxes_checked':len(bounds),'overflow_flags':len(overflow),'unchanged_previous_slides':same,'original_media_masters_themes_preserved':True,'original_decks_preserved':True,'plan_slides':48,'plan_minutes':90,'part_1_minutes':26,'human_plan_matches_json':True,'start_prompts_match_part_1':True,'pptx_sha256':sha(F),'pdf_sha256':sha(F.with_suffix('.pdf')),'G10_clearance_created':False,'new_AI_app_execution':False}
(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('Verified 21 slides, 18 effects, 48-slide / 90-minute plan, Part 1 26 minutes, source geometry and 13 existing slides pixel-identical.')
