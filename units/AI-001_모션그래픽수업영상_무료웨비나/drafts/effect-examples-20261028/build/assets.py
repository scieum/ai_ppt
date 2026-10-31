from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math,json
B=Path(__file__).resolve().parent; A=B/'assets';A.mkdir(exist_ok=True)
W,H=720,240
BG=(32,32,32);ORANGE=(255,145,29);BLUE=(117,211,247)
FONT='C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf'
def canvas():return Image.new('RGB',(W,H),BG)
def word(im,text,x,y,size,color):
 d=ImageDraw.Draw(im);d.text((x,y),text,font=ImageFont.truetype(FONT,max(1,round(size))),fill=color,anchor='mm')
def blend(c,t):return tuple(round(BG[i]+(c[i]-BG[i])*t) for i in range(3))
def ease(t):return 1-(1-t)**3
def frame(kind,t):
 im=canvas();p=min(1,max(0,(t-.3)/1.4))
 if kind=='fade':
  a=min(1,max(0,(t-.25)/.8))*(1-min(1,max(0,(t-1.8)/.8)))
  word(im,'노션톡',360,120,112,blend(ORANGE,a))
 elif kind=='slide':word(im,'노션톡',-210+570*ease(p),120,112,ORANGE)
 elif kind=='zoom':
  q=min(1,max(0,(t-.25)/.85)) if t<1.8 else 1-min(1,max(0,(t-1.8)/.85))
  word(im,'노션톡',360,120,30+82*q,ORANGE)
 elif kind=='reveal':
  lay=canvas();word(lay,'노션톡',360,80,86,BLUE);word(lay,'웨비나 챌린지',360,173,76,BLUE)
  left=35;right=left+round(650*p)
  if right>left:im.paste(lay.crop((left,0,right,H)),(left,0))
 elif kind=='typewriter':
  chars='노션톡웨비나챌린지';n=min(9,int(p*10));xs=[130,220,310,440,530,620,270,360,450]
  for i in range(n):word(im,chars[i],xs[i],74 if i<6 else 172,85,BLUE)
 elif kind=='stagger':
  for i,txt in enumerate(['노션톡','웨비나','챌린지']):
   q=min(1,max(0,(t-.3-i*.4)/.5));word(im,txt,126+i*234,120+55*(1-ease(q)),68,blend(BLUE,q))
 return im
for kind in ['fade','slide','zoom','reveal','typewriter','stagger']:
 # The stored first frame shows the finished example in static viewers.
 # Subsequent frames demonstrate the motion and repeat in slideshow playback.
 # Start in the finished state, then continue the cycle from that same phase.
 # Matching first/last states prevents a one-frame flash at each repeat.
 frames=[frame(kind,1.7)]+[frame(kind,i/25) for i in list(range(43,76))+list(range(43))]
 frames[0].save(A/(kind+'.gif'),save_all=True,append_images=frames[1:],duration=[40]+[40]*76,loop=0,optimize=False,disposal=2)
 frame(kind,1.7).save(A/(kind+'-poster.png'))
(A/'manifest.json').write_text(json.dumps({'origin':'programmatically authored typography demonstrations','font':'Pretendard','loop':0,'fps':25,'effects':['fade','slide','zoom','reveal','typewriter','stagger']},ensure_ascii=False,indent=2),encoding='utf8')
print('Generated six looping motion examples.')
