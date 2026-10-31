from pathlib import Path
import json,fitz
from PIL import Image,ImageDraw
B=Path('output/reference-style-build');R=Path.cwd();U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';f=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_레퍼런스표현강화_40장_v20.pdf';d=fitz.open(f);out=U/'renders/reference-style-20261029/pdf';out.mkdir(exist_ok=True)
for i,p in enumerate(d,1):p.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(str(out/f'slide-{i:02}.png'))
for part,ns in [('changed',list(range(24,32))+list(range(34,40))),('unchanged',list(range(1,24))+[32,33,40])]:
 sheet=Image.new('RGB',(1600,250*((len(ns)+3)//4)),'#eeeeee');dr=ImageDraw.Draw(sheet)
 for i,n in enumerate(ns):
  im=Image.open(out/f'slide-{n:02}.png');im.thumbnail((400,225));x=i%4*400;y=i//4*250;sheet.paste(im,(x,y+25));dr.text((x+10,y+5),str(n),fill='black')
 sheet.save(B/f'{part}-final.jpg')
rows=json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig'));changed=list(range(24,32))+list(range(34,40));issues=[]
for t in rows:
 if t['slide']in changed and t['name']!='copyright-footer' and (t['text_left']+t['text_width']>t['shape_left']+t['shape_width']+2 or t['text_top']+t['text_height']>t['shape_top']+t['shape_height']+2):issues.append(t)
print(json.dumps(issues,ensure_ascii=False))
