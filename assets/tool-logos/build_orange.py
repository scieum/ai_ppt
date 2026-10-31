"""Create a new orange-accent badge family from the existing vector marks."""
from pathlib import Path
import json,hashlib,subprocess,os,xml.etree.ElementTree as E,zipfile,shutil
from PIL import Image,ImageDraw,ImageFont

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
DEST=BASE/'orange-v2'
OUT=ROOT/'output/tool-logos'
for sub in ['svg','png','marks']:(DEST/sub).mkdir(parents=True,exist_ok=True)
ns='http://www.w3.org/2000/svg';E.register_namespace('',ns)
prior=json.loads((BASE/'catalog.json').read_text(encoding='utf-8'))
definitions='''<defs>
<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#11171E"/><stop offset="1" stop-color="#252C34"/></linearGradient>
<linearGradient id="outline" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#FF982F" stop-opacity=".62"/><stop offset=".4" stop-color="#5F6875" stop-opacity=".28"/><stop offset="1" stop-color="#FE8A21" stop-opacity=".5"/></linearGradient>
<radialGradient id="warm" cx="0" cy="0" r="1"><stop stop-color="#F88A24" stop-opacity=".14"/><stop offset="1" stop-color="#F88A24" stop-opacity="0"/></radialGradient>
<clipPath id="panelClip"><rect x="160" y="160" width="704" height="704" rx="92"/></clipPath>
</defs>'''
items=[]
for key,label in [('claude','Claude'),('codex','Codex'),('higgsfield','Higgsfield')]:
    doc=E.parse(BASE/'marks'/f'{key}.svg')
    symbol=E.tostring(list(doc.getroot())[0],encoding='unicode')
    for variant,angle in [('front',0),('tilted',-12)]:
        body=f'''<g transform="rotate({angle} 512 512)">
<rect x="160" y="166" width="704" height="704" rx="92" fill="#090D12"/>
<rect x="160" y="160" width="704" height="704" rx="92" fill="url(#panel)"/>
<g clip-path="url(#panelClip)"><rect x="160" y="160" width="704" height="704" fill="url(#warm)"/></g>
<rect x="160" y="160" width="704" height="704" rx="92" fill="none" stroke="url(#outline)" stroke-width="2.5"/>
<path d="M 194 286 V 237 Q 194 194 237 194 H 286" fill="none" stroke="#FF9228" stroke-width="6" stroke-linecap="round"/>
{symbol}
<path d="M 464 816 H 560" fill="none" stroke="#FF9228" stroke-width="5" stroke-linecap="round"/>
</g>'''
        svg=f'<svg xmlns="{ns}" width="1024" height="1024" viewBox="0 0 1024 1024" role="img" aria-label="{label}, original orange-accent teaching badge">{definitions}{body}</svg>'
        (DEST/'svg'/f'{key}-{variant}.svg').write_text(svg,encoding='utf-8')
        source=next(x for x in prior['files'] if x['id']==key+'-front')
        items.append({'id':key+'-'+variant,'brand':label,'svg':f'svg/{key}-{variant}.svg','png':f'png/{key}-{variant}.png',
            'angle':angle,'accent':'#FF9228','mark_source':source['source_name'],'mark_source_page':source['source_page'],
            'source_sha256':source['source_sha256'],'mark_color_preserved':True})
    for ext in ['svg','png']:shutil.copyfile(BASE/'marks'/f'{key}.{ext}',DEST/'marks'/f'{key}.{ext}')

# Keep the renderer local to this new family; no changes to the prior assets.
shutil.copyfile(BASE/'render_svgs.mjs',DEST/'render_svgs.mjs')
runtime=Path('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies')
env=dict(os.environ,RUNTIME_NODE_MODULES=str(runtime/'node/node_modules'))
subprocess.run([str(runtime/'node/bin/node.exe'),str(DEST/'render_svgs.mjs')],env=env,check=True)
for item in items:
    p=DEST/item['png'];im=Image.open(p)
    assert im.mode=='RGBA' and im.size==(1024,1024) and im.getpixel((0,0))[3]==0
    item['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
(DEST/'catalog.json').write_text(json.dumps({'version':'orange-v2','accent':'#FF9228','files':items,
    'changes':['Matte graphite surface instead of reference glass reflections','Sharper corner radius','Orange corner accent and lower marker','New tilt angle -12 degrees'],
    'codex':'Reference OpenAI knot mark, not claimed as a separate current app icon'},ensure_ascii=False,indent=2),encoding='utf-8')
sheet=Image.new('RGB',(1600,1080),'#0C1118');d=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf',31)
small=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',21)
d.rounded_rectangle((56,35,64,111),radius=4,fill='#FF9228')
d.text((85,34),'NOTIONTALK / TOOL ASSETS',font=font,fill='#FFFFFF')
d.text((85,80),'주황 포인트 · 매트 패널 · 원본 브랜드 심볼 유지',font=small,fill='#A8B2BF')
d.rectangle((0,580,1600,1080),fill='#F4F1EC')
for i,(key,label) in enumerate([('claude','Claude'),('codex','Codex'),('higgsfield','Higgsfield')]):
    for variant,y in [('front',100),('tilted',580)]:
        im=Image.open(DEST/'png'/f'{key}-{variant}.png').resize((410,410),Image.Resampling.LANCZOS)
        x=60+i*520;sheet.paste(im,(x,y),im)
        d.text((x+205,y+407),label,font=font,fill='#FFFFFF' if variant=='front' else '#1A2530',anchor='mt')
sheet.save(OUT/'tool-logos-orange-v2-preview.png')
with zipfile.ZipFile(OUT/'Claude_Codex_Higgsfield_orange_v2.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in DEST.rglob('*'):
        if f.is_file() and f.suffix!='.mjs':z.write(f,Path('tool-logos-orange-v2')/f.relative_to(DEST))
print('Prepared orange-v2: six badges, transparent PNG/SVG, original mark colors and prior versions preserved.')
