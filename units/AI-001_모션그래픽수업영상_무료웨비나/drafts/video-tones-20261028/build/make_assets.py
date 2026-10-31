from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np,math,random,json,hashlib
B=Path(__file__).resolve().parent;U=B.parents[2];A=U/'assets/video-tones-20261028';A.mkdir(parents=True,exist_ok=True)
W,H=520,292;BG='#202020';OR='#FF9228';BLUE='#7DD3FC'
font=ImageFont.truetype('C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf',43)
small=ImageFont.truetype('C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf',20)
def center(d,xy,text,f=font,fill='white'):d.text(xy,text,font=f,fill=fill,anchor='mm')
def render(kind,k):
 t=k/40;phase=2*math.pi*t;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im);cx=260;cy=152
 if kind in ['hand','blueprint','neon']:
  cx=260+int(42*math.sin(phase));cy=125
  if kind=='hand':
   d.rounded_rectangle((20,14,500,278),radius=12,fill='#EEE7D9');rng=random.Random(10)
   for j in range(3):
    pts=[(cx+int((59+rng.random()*3)*math.cos(i*2*math.pi/64)),cy+int((59+rng.random()*3)*math.sin(i*2*math.pi/64)))for i in range(65)];d.line(pts,fill='#D77232',width=3)
   d.line((145,221,375,221),fill='#63564B',width=3);center(d,(260,238),'NotionTalk',small,'#51423A')
  elif kind=='blueprint':
   d.rounded_rectangle((20,14,500,278),radius=12,fill='#0B2D49')
   for x in range(20,501,24):d.line((x,14,x,278),fill='#173B56')
   for y in range(14,279,24):d.line((20,y,500,y),fill='#173B56')
   d.ellipse((cx-60,cy-60,cx+60,cy+60),outline=BLUE,width=3);d.line((cx-80,cy,cx+80,cy),fill=BLUE,width=1);d.line((cx,cy-80,cx,cy+80),fill=BLUE,width=1);d.line((cx-60,217,cx+60,217),fill='white',width=2);center(d,(260,246),'NotionTalk',small,BLUE)
  else:
   glow=Image.new('RGB',(W,H),BG);g=ImageDraw.Draw(glow);g.ellipse((cx-61,cy-61,cx+61,cy+61),outline=OR,width=14);glow=glow.filter(ImageFilter.GaussianBlur(12));im=Image.blend(im,glow,.9);d=ImageDraw.Draw(im);d.ellipse((cx-60,cy-60,cx+60,cy+60),outline='#FFBD70',width=3);d.line((145,221,375,221),fill=OR,width=2);center(d,(260,246),'NotionTalk',small)
 elif kind=='chrome':
  yy,xx=np.mgrid[0:H,0:W];sx=(xx-260)/86;sy=(yy-143)/86;inside=sx*sx+sy*sy<=1;z=np.sqrt(np.maximum(0,1-sx*sx-sy*sy));v=np.clip(110+110*np.sin(2.7*sy+.5*math.sin(phase))+60*z,25,250);arr=np.array(im);arr[inside]=np.stack([v,v*.99,v*.97],axis=-1)[inside];im=Image.fromarray(arr.astype('uint8'));d=ImageDraw.Draw(im);d.ellipse((172,55,348,231),outline='#D8E0E5',width=2);d.rounded_rectangle((111,101,204,199),radius=15,fill='#293A44',outline='#B2E6EF',width=2);d.line((121,112,193,112),fill='#D9FBFF',width=2)
 elif kind=='pixel':
  q=int(t*12)%6;d.line((65,246,460,246),fill='#616161',width=2)
  for j in range(6):
   h=40+((j+q)%6)*22;x=80+j*61
   for y in range(246-h,246,20):d.rectangle((x,y,x+38,y+17),fill=OR if j%2 else '#7BB8D0')
 elif kind=='clay':
  bounce=max(0,math.sin(phase));cy=190-int(90*bounce);rx=68+int(15*(1-bounce)**5);ry=65-int(16*(1-bounce)**5)
  d.ellipse((165,239,355,260),fill='#151515')
  for j in range(ry,0,-1):
   frac=j/ry;c=(int(245-50*frac),int(162-48*frac),int(80-35*frac));d.ellipse((260-rx*j/ry,cy-j,260+rx*j/ry,cy+j),fill=c)
  d.ellipse((222,cy-35,251,cy-17),fill='#FFD59B')
 elif kind=='morph':
  a=t*3;stage=int(a)%3;u=(a%1);u=u*u*(3-2*u);pts=[]
  for j in range(120):
   angle=j*2*math.pi/120;r=82;circle=(r*math.cos(angle),r*math.sin(angle));square=(r*math.cos(angle)/max(abs(math.cos(angle)),abs(math.sin(angle))),r*math.sin(angle)/max(abs(math.cos(angle)),abs(math.sin(angle))))
   triangle=[(0,-98),(90,62),(-90,62)];f=j/40;i=int(f)%3;v=f%1;tri=tuple(triangle[i][ax]*(1-v)+triangle[(i+1)%3][ax]*v for ax in (0,1));shapes=[circle,square,tri];pts.append(tuple([260+shapes[stage][0]*(1-u)+shapes[(stage+1)%3][0]*u,148+shapes[stage][1]*(1-u)+shapes[(stage+1)%3][1]*u]))
  d.polygon(pts,fill=OR)
 elif kind=='parallax':
  for i in range(-1,10):
   x=(i*82-int(t*100))%820-100;h=60+(i%3)*20;d.rectangle((x,215-h,x+46,215),fill='#3E6477')
  for i in range(-1,8):
   x=(i*124-int(t*290))%992-130;h=90+(i%2)*30;d.rectangle((x,264-h,x+66,264),fill='#C47938')
  d.line((0,265,W,265),fill='#FFBA78',width=3)
 elif kind=='camera':
  zoom=1+.4*(.5-.5*math.cos(phase));rng=random.Random(4)
  for _ in range(45):
   x=(rng.uniform(-270,270))*zoom+260;y=(rng.uniform(-140,140))*zoom+146;d.ellipse((x-1,y-1,x+1,y+1),fill='#AAAAAA')
  r=61*zoom;d.ellipse((260-r,146-r,260+r,146+r),fill=OR);d.arc((260-1.6*r,146-.5*r,260+1.6*r,146+.5*r),0,360,fill=BLUE,width=3)
 else:
  beat=int(t*4);pulse=(t*4)%1;energy=math.exp(-6*pulse)
  for j in range(4):d.ellipse((186+j*40,19,200+j*40,33),fill=OR if beat==j else '#555555')
  if kind=='pulse':
   r=45+int(38*energy);d.ellipse((260-r,160-r,260+r,160+r),fill=OR)
  elif kind=='wave':
   pts=[(x,160+math.sin(x*.07+phase*8)*(15+40*energy))for x in range(55,466,2)];d.line(pts,fill=BLUE,width=5);d.line((55,225,465,225),fill='#555555',width=1)
  elif kind=='words':
   for j,word in enumerate(['함께','배우는','노션톡']):
    x=109+j*151;y=162-int(14*energy) if beat%3==j else 162;center(d,(x,y),word,ImageFont.truetype('C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf',35),OR if beat%3==j else '#777777')
 return im
kinds=['hand','blueprint','neon','chrome','pixel','clay','morph','parallax','camera','pulse','wave','words'];records=[]
for kind in kinds:
 frames=[render(kind,k)for k in range(40)];p=A/(kind+'.gif');frames[0].save(p,save_all=True,append_images=frames[1:],duration=75,loop=0,disposal=2,optimize=False);frames[6].save(A/(kind+'-poster.png'));records.append({'kind':kind,'file':str(p),'frames':40,'duration_ms':75,'loop':0,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'origin':'original programmatic motion illustration; no source video pixels or audio'})
(A/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8');print('Created 12 original animated examples.')
