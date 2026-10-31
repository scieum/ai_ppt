"""Create original frame diagrams, independently of the generated illustration."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math
R=Path(__file__).resolve().parent
S=3;W=240;H=165;orange=(255,146,40)
poses=[(70+14*i,112-20*math.sin(math.pi*i/5)) for i in range(6)]
def svg(x,y):return f'<svg xmlns="http://www.w3.org/2000/svg" width="240" height="165" viewBox="0 0 240 165"><rect x="2" y="2" width="236" height="161" rx="13" fill="white" stroke="#DDDDDD" stroke-width="2"/><path d="M24 137 H216" stroke="#CCCCCC" stroke-width="2"/><circle cx="{x:.3f}" cy="{y:.3f}" r="14" fill="#FF9228"/></svg>'
def draw(x,y):
 im=Image.new('RGB',(W*S,H*S),'#000000');d=ImageDraw.Draw(im);d.rounded_rectangle((2*S,2*S,238*S,163*S),radius=13*S,fill='white',outline='#DDDDDD',width=2*S);d.line((24*S,137*S,216*S,137*S),fill='#CCCCCC',width=2*S);d.ellipse(((x-14)*S,(y-14)*S,(x+14)*S,(y+14)*S),fill=orange);return im
for i,(x,y) in enumerate(poses,1):
 (R/f'frame-{i:02}.svg').write_text(svg(x,y),encoding='utf-8');draw(x,y).save(R/f'frame-{i:02}.png')
board='<svg xmlns="http://www.w3.org/2000/svg" width="1520" height="215" viewBox="0 0 1520 215"><rect width="1520" height="215" fill="black"/>'
for i,(x,y) in enumerate(poses):board+=f'<g transform="translate({i*252+4} 4)">'+svg(x,y).split('>',1)[1].rsplit('</svg>',1)[0]+f'<text x="120" y="196" fill="#AAAAAA" text-anchor="middle" font-family="sans-serif" font-size="20">{i+1}</text></g>'
(R/'six-frame-strip.svg').write_text(board+'</svg>',encoding='utf-8')
forward=[(70+70*i/23,112-20*math.sin(math.pi*i/23)) for i in range(24)];loop=forward+forward[-2:0:-1];frames=[draw(x,y) for x,y in loop];durations=[80]*len(frames);durations[0]=240;durations[23]=240
frames[0].save(R/'flipbook-motion.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2,optimize=False)
frames[0].save(R/'loop-preview.png')
(R/'frames.json').write_text(json.dumps({'logical_size':[240,165],'poses':poses,'gif_frame_count':len(loop),'frame_durations_ms':durations,'purpose':'Original instructional diagrams; ball position changes slightly; playback uses forward and reverse loop'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Created six SVG/PNG frames and a 46-frame original animated GIF.')
