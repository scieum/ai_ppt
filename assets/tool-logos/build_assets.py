"""Reuse logo vector outlines from the user's reference PDFs, with SVG badges.

Run from the repository root with --deps <private PyMuPDF install>, if needed.
"""
from pathlib import Path
import argparse,hashlib,json,math,sys,zipfile,subprocess,os
from PIL import Image,ImageDraw,ImageFont

parser=argparse.ArgumentParser()
parser.add_argument('--deps')
args=parser.parse_args()
if args.deps:sys.path.insert(0,args.deps)
import pymupdf as fitz

DEST=Path(__file__).resolve().parent
ROOT=DEST.parents[1]
OUT=ROOT/'output/tool-logos'
OUT.mkdir(parents=True,exist_ok=True)
refs={r['id']:r for r in json.loads((ROOT/'output/reference-analysis/inventory.json').read_text(encoding='utf-8'))}
for sub in ['svg','png','marks']:(DEST/sub).mkdir(exist_ok=True)

def point(v):return float(v.x),float(v.y)
def path_data(drawing):
    data=[];current=None
    for item in drawing['items']:
        kind=item[0]
        if kind in ('l','c'):
            start=point(item[1])
            if current is None or any(abs(a-b)>.001 for a,b in zip(start,current)):
                data.append('M %.6f %.6f'%start)
            if kind=='l':
                current=point(item[2]);data.append('L %.6f %.6f'%current)
            else:
                coords=tuple(v for q in item[2:5] for v in point(q))
                data.append('C '+' '.join('%.6f'%v for v in coords));current=point(item[4])
        elif kind=='re':
            x0,y0,x1,y1=item[1]
            data.append(f'M {x0} {y0} H {x1} V {y1} H {x0} Z');current=None
        elif kind=='qu':
            q=item[1];a,b,c,d=map(point,[q.ul,q.ur,q.lr,q.ll])
            data.append('M %.6f %.6f L %.6f %.6f L %.6f %.6f L %.6f %.6f Z'%(*a,*b,*c,*d));current=None
        else:raise ValueError('Unhandled path item '+kind)
    if drawing.get('closePath'):data.append('Z')
    return ' '.join(data)

def svg_render(svg,destination,scale=1):
    doc=fitz.open(stream=svg.encode(),filetype='svg')
    page_doc=fitz.open('pdf',doc.convert_to_pdf())
    pix=page_doc[0].get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=True)
    pix.save(destination)

definitions='''
<defs>
 <linearGradient id="tile" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#17181B"/><stop offset=".58" stop-color="#242528"/><stop offset="1" stop-color="#353638"/></linearGradient>
 <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#FFFFFF" stop-opacity=".52"/><stop offset=".4" stop-color="#A9AAAE" stop-opacity=".1"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".25"/></linearGradient>
 <radialGradient id="reflection" cx="1" cy="1" r="1"><stop stop-color="#B2B3B7" stop-opacity=".23"/><stop offset=".38" stop-color="#B2B3B7" stop-opacity=".07"/><stop offset="1" stop-color="#B2B3B7" stop-opacity="0"/></radialGradient>
 <radialGradient id="shadow"><stop stop-color="#000000" stop-opacity=".3"/><stop offset="1" stop-color="#000000" stop-opacity="0"/></radialGradient>
 <clipPath id="tileClip"><rect x="160" y="160" width="704" height="704" rx="126"/></clipPath>
</defs>'''

items=[]
settings=[('claude','Claude','R01',5,(240,560,282,601),'#D97757',0,362),
          ('codex','Codex','R01',5,(279,603,320,643),'#FEFEFE',0,362),
          ('higgsfield','Higgsfield','R06',7,(485,582,633,693),'#C5FF00',20.82,455)]
for key,label,rid,num,region,color,undo_rotation,target_size in settings:
    source=refs[rid]
    pdf=fitz.open(source['path']);page=pdf[num-1]
    candidates=[d for d in page.get_drawings() if d['fill'] is not None and len(d['items'])>20 and fitz.Rect(region).contains(d['rect'])]
    if key=='claude':candidates=[d for d in candidates if d['fill'][0]>.8 and .3<d['fill'][1]<.6]
    if key=='codex':candidates=[d for d in candidates if min(d['fill'])>.9]
    if key=='higgsfield':candidates=[d for d in candidates if d['fill'][1]>.95 and d['fill'][2]<.05]
    assert len(candidates)==1,(key,len(candidates))
    drawing=candidates[0];data=path_data(drawing)
    cx=(drawing['rect'].x0+drawing['rect'].x1)/2
    cy=(drawing['rect'].y0+drawing['rect'].y1)/2
    # Raster measurement only computes an SVG viewBox; it does not alter logo pixels.
    test=f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="{cx-200} {cy-200} 400 400"><g transform="rotate({undo_rotation} {cx} {cy})"><path d="{data}" fill="{color}"/></g></svg>'
    probe=OUT/(key+'-bounds.png');svg_render(test,probe,2)
    alpha=Image.open(probe).getchannel('A');bbox=alpha.getbbox();assert bbox
    x0=cx-200+bbox[0]/2;y0=cy-200+bbox[1]/2
    width=(bbox[2]-bbox[0])/2;height=(bbox[3]-bbox[1])/2
    factor=target_size/max(width,height)
    # Keep every outline and its original aspect ratio. R06 was already tilted.
    symbol=f'<g transform="translate({512-width*factor/2:.6f} {512-height*factor/2:.6f}) scale({factor:.8f}) translate({-x0:.6f} {-y0:.6f}) rotate({undo_rotation} {cx:.6f} {cy:.6f})"><path d="{data}" fill="{color}" fill-rule="'+('evenodd' if drawing.get('even_odd') else 'nonzero')+'"/></g>'
    for variant,angle in [('front',0),('tilted',-18)]:
        frame=f'''<g transform="rotate({angle} 512 512)">
 <rect x="160" y="169" width="704" height="704" rx="126" fill="#090A0C"/>
 <rect x="160" y="160" width="704" height="704" rx="126" fill="url(#tile)"/>
 <g clip-path="url(#tileClip)"><rect x="340" y="370" width="620" height="620" fill="url(#reflection)"/></g>
 <rect x="160" y="160" width="704" height="704" rx="126" fill="none" stroke="url(#edge)" stroke-width="2"/>
 {symbol}
</g>'''
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024" role="img" aria-label="{label}, reference-style dark glass badge">{definitions}{frame}</svg>'
        svg_path=DEST/'svg'/f'{key}-{variant}.svg';svg_path.write_text(svg,encoding='utf-8')
        png_path=DEST/'png'/f'{key}-{variant}.png';svg_render(svg,png_path)
        im=Image.open(png_path);assert im.mode=='RGBA' and im.size==(1024,1024) and im.getpixel((0,0))[3]==0
        items.append({'id':key+'-'+variant,'brand':label,'variant':variant,'angle':angle,'svg':str(svg_path.relative_to(DEST)).replace('\\','/'),'png':str(png_path.relative_to(DEST)).replace('\\','/'),
            'sha256':hashlib.sha256(png_path.read_bytes()).hexdigest(),'source_id':rid,'source_name':source['name'],'source_page':num,'source_sha256':source['sha256'],
            'original_logo_bounds':list(drawing['rect']),'source_path_segments':len(drawing['items']),
            'method':'Original vector outline extracted from the provided PDF; normalized without aspect distortion; common SVG badge frame recreated.'})
    mark=f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">{symbol}</svg>'
    (DEST/'marks'/f'{key}.svg').write_text(mark,encoding='utf-8')
    svg_render(mark,DEST/'marks'/f'{key}.png')

runtime_root=Path('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies')
env=dict(os.environ,RUNTIME_NODE_MODULES=str(runtime_root/'node/node_modules'))
subprocess.run([str(runtime_root/'node/bin/node.exe'),str(DEST/'render_svgs.mjs')],env=env,check=True)
for item in items:
    item['sha256']=hashlib.sha256((DEST/item['png']).read_bytes()).hexdigest()
catalog={'schema_version':'1.0','canvas':[1024,1024],'style':'Reference-derived dark glass rounded app badge','transparent':True,
 'source_role':'Marks are extracted from user-provided PDFs, not claimed as official brand downloads.',
 'codex_note':'The reference labels the OpenAI knot mark as Codex. These assets follow that reference. No claim is made that this is a distinct current Codex app icon.',
 'variants':['front','tilted'],'files':items,'checked_on':'2026-10-27'}
(DEST/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')

sheet=Image.new('RGB',(1600,1110),'#0B0C0F');d=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf',30)
small=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',21)
d.text((56,32),'REFERENCE STYLE / TOOL LOGOS',font=font,fill='#FFFFFF')
d.text((56,78),'위: 정면 · 어두운 배경 / 아래: 기울임 · 밝은 배경',font=small,fill='#A8A9AE')
d.rectangle((0,600,1600,1110),fill='#F3F2EF')
for i,(key,label,*_) in enumerate(settings):
    for variant,y in [('front',110),('tilted',600)]:
        im=Image.open(DEST/'png'/f'{key}-{variant}.png').resize((420,420),Image.Resampling.LANCZOS)
        x=56+i*520;sheet.paste(im,(x,y),im)
        text_color='#FFFFFF' if variant=='front' else '#212226'
        d.text((x+210,y+418),label,font=font,fill=text_color,anchor='mt')
sheet.save(OUT/'tool-logos-preview-final.png')
with zipfile.ZipFile(OUT/'Claude_Codex_Higgsfield_reference_icons.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in DEST.rglob('*'):
        if f.is_file() and f.suffix not in ['.py','.mjs'] and '__pycache__' not in str(f):z.write(f,Path('tool-logos')/f.relative_to(DEST))
print('Prepared 3 brands x 2 badge styles, standalone marks, transparent PNG + scalable SVG, catalog and preview.')
