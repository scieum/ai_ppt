from pathlib import Path
import sys,json,re,hashlib,zipfile
from PIL import Image,ImageDraw,ImageFont
from pypdf import PdfReader
build=Path(__file__).resolve().parent
unit=build.parents[2];repo=unit.parents[1]
sys.path.insert(0,str(repo/'harness'))
from gate import Engine,ppt_info
out=repo/'output/webinar-samples'
pptx=out/'NotionTalk_모션그래픽_주황포인트_자체사례_v5.pptx'
pdf=pptx.with_suffix('.pdf')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((build/'validation-orange-original-v5.json').read_text(encoding='utf-8'))
assert receipt['finalSha256']==sha(pptx)
slides=ppt_info(pptx);assert len(slides)==5
assert len(PdfReader(pdf).pages)==5
footer='© 2026. NotionTalk. All rights reserved.'
assert all(footer in ''.join(s['texts']) for s in slides)
assert all('출처:' in s['notes'] for s in slides)
guard=Engine(unit).check(['G07']);assert guard['passed']
text=(unit/'plan.md').read_text(encoding='utf-8')
blocks=re.findall(r'```harness-plan\n(.*?)\n```',text,re.S);assert len(blocks)==1
plan=json.loads(blocks[0]);assert len(plan['slides'])==42 and sum(s['minutes'] for s in plan['slides'])==90
for ex in plan['exercises']:
 assert sum(s['minutes'] for s in plan['slides'] if ex['id'] in s['exercise_ids'])==ex['minutes']
assert all(name in text for name in ['LESSON_BRIEF.md','VISUAL_RULES.md','SCENE_PLAN.md'])
assert '4+6+8+6=24초' in text

font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',22)
sheet=Image.new('RGB',(1960,1740),'#0C1118');draw=ImageDraw.Draw(sheet)
orange=[];final=unit/'renders/orange-original-v4/final-v5';final.mkdir(exist_ok=True)
for n in range(1,6):
 im=Image.open(unit/f'renders/orange-original-v4/powerpoint/slide-{n:02}.png').convert('RGB')
 assert im.size==(1920,1080)
 logo=sum(1 for r,g,b in im.crop((1480,68,1826,168)).getdata() if min(r,g,b)>220)
 assert logo>2000
 pixels=list(im.getdata())
 count=sum(1 for r,g,b in pixels if r>230 and 100<g<185 and b<90)
 pink=sum(1 for r,g,b in pixels if r>200 and g<100 and b>100)
 if n>1:assert count>500 and pink==0,(n,count,pink)
 orange.append({'slide':n,'orange_pixels':count,'pink_pixels':pink,'visible_logo_pixels':logo})
 im.save(final/f'final-{n:02}.png')
 thumb=im.resize((960,540),Image.Resampling.LANCZOS)
 x=500 if n==5 else 10+((n-1)%2)*980;y=30+((n-1)//2)*570
 sheet.paste(thumb,(x,y));draw.text((x+8,y+543),f'{n:02}',font=font,fill='#FF9228')
sheet.save(out/'주황포인트_자체사례_v5_미리보기.jpg',quality=95)

refs=json.loads((repo/'output/reference-analysis/inventory.json').read_text(encoding='utf-8'))
norm=lambda s:re.sub(r'\s+','',s)
source_pages=[(d['id'],p['page'],norm(p['text'])) for d in refs for p in d['pages']]
matches=[]
for n,sl in enumerate(slides,1):
 for t in sl['texts']:
  if len(re.findall('[가-힣]',t))<8:continue
  value=norm(t)
  for rid,page,src in source_pages:
   if value in src:matches.append({'slide':n,'text':t,'reference':rid,'page':page})
report={'scope':'Five representative slides; not full 42-slide production or approval',
 'pptx_sha256':sha(pptx),'pdf_sha256':sha(pdf),'source_protection':guard,
 'visible_color_checks':orange,'plan':{'slides':42,'minutes':90,'scene_seconds':[4,6,8,6]},
 'content_changes':['Classroom opening question','Pair-discussion activity instructions','Student-facing review criteria','New document roles and prompts'],
 'exact_text_matches_over_8_hangul_chars':matches,
 'text_check_limit':'Exact normalized string search only; not a semantic originality score.',
 'native_powerpoint_exported':True,'design_approval':'not asserted'}
(unit/'checks/orange-original-v5-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: native five-slide/PDF output, orange accents, no pink accents on content slides, brand/footer, protected originals, 42-slide/90-minute plan.')
print('Exact source sentence matches:',len(matches))
