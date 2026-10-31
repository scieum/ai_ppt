from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,json
B=Path(__file__).resolve().parent;R=B.parents[4];A=B/'assets';A.mkdir(exist_ok=True)
FONT='C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf'
O=(255,145,29);C=(117,211,247);WHITE=(245,245,245)
def txt(im,t,x,y,size,col=WHITE,anchor='mm'):
 ImageDraw.Draw(im).text((x,y),t,font=ImageFont.truetype(FONT,max(1,round(size))),fill=col,anchor=anchor)
def ease(t):return 1-(1-t)**3
def clamp(t):return max(0,min(1,t))
logo=Image.open(R/'assets/branding/notiontalk-white.png').convert('RGBA');logo=logo.crop(logo.getbbox());logo.thumbnail((520,86),Image.Resampling.LANCZOS)
def types(kind,t):
 im=Image.new('RGB',(1120,108));d=ImageDraw.Draw(im);p=clamp((t-.25)/1.6)
 if kind=='typography':
  for j,(s,x)in enumerate([('함께',200),('배우는',480),('AI',750)]):
   q=ease(clamp((t-.15-j*.3)/.65));col=O if j==2 else WHITE
   col=tuple(round(v*q) for v in col);txt(im,s,x,55+40*(1-q),64 if j<2 else 76,col)
 elif kind=='infographic':
  n=round(100*ease(p));d.rounded_rectangle((50,39,830,70),radius=15,fill=(45,45,45))
  if n>0:d.rounded_rectangle((50,39,50+780*n/100,70),radius=15,fill=O)
  txt(im,f'{n}%',980,55,68,O)
 elif kind=='interface':
  d.rounded_rectangle((60,20,340,90),radius=12,fill=(32,32,32),outline=(105,105,105),width=2)
  txt(im,'검색',185,55,46,C)
  hit=clamp((t-.4)/.3)*(1-clamp((t-.9)/.3))
  d.ellipse((300-16*hit,55-16*hit,300+16*hit,55+16*hit),outline=O,width=3)
  for j in range(3):
   q=ease(clamp((t-.6-j*.25)/.45));x=420+j*200;v=round(70+120*q)
   d.rounded_rectangle((x,25+25*(1-q),x+160,85+25*(1-q)),radius=9,fill=(round(18+25*q),)*3)
   d.rounded_rectangle((x+18,43+25*(1-q),x+34,59+25*(1-q)),radius=3,fill=tuple(round(v*q)for v in C))
   d.line((x+49,52+25*(1-q),x+132,52+25*(1-q)),fill=(v,v,v),width=5)
 elif kind=='logo':
  q=ease(p);lay=logo.copy();lay.putalpha(lay.getchannel('A').point(lambda v:round(v*q)));im.paste(lay,((1120-lay.width)//2,round((108-lay.height)/2+30*(1-q))),lay)
  d.line((320,101,320+round(480*q),101),fill=O,width=4)
 elif kind=='illustration':
  # An original paper-plane illustration follows a curved path.
  x=150+800*p;y=55-16*math.sin(math.pi*p)
  for j in range(13):
   u=max(0,p-.02*j);xx=150+800*u;yy=55-16*math.sin(math.pi*u)
   if j>2:d.ellipse((xx-3,yy+12,xx+3,yy+18),fill=(round(80*(1-j/15)),round(145*(1-j/15)),round(170*(1-j/15))))
  d.polygon([(x-52,y-28),(x+58,y),(x-52,y+28),(x-19,y)],fill=O)
  d.polygon([(x-19,y),(x+58,y),(x-42,y+11)],fill=(255,205,127))
 return im
def timing(kind,t):
 im=Image.new('RGB',(720,240),(32,32,32));d=ImageDraw.Draw(im)
 delay=.9 if kind=='delay' else .2;duration=2.0 if kind=='long' else 1.0
 u=clamp((t-delay)/duration)
 if kind in ['ease-in','ease-out','ease-in-out']:
  u=clamp((t-.2)/1.8);u=u*u if kind=='ease-in' else 1-(1-u)**2 if kind=='ease-out' else u*u*(3-2*u)
 d.line((65,126,655,126),fill=(95,95,95),width=3)
 x=65+590*u;d.ellipse((x-23,103,x+23,149),fill=O)
 return im
allk=['typography','infographic','interface','logo','illustration','normal','delay','long','ease-in','ease-out','ease-in-out']
for kind in allk:
 fn=types if kind in allk[:5] else timing
 # Finish state is the static poster; phases join smoothly at loop boundary.
 times=[1.7]+[i/25 for i in list(range(43,88))+list(range(43))]
 frames=[fn(kind,t)for t in times]
 frames[0].save(A/(kind+'.gif'),save_all=True,append_images=frames[1:],duration=40,loop=0,optimize=False,disposal=2)
 frames[0].save(A/(kind+'-poster.png'))
(A/'manifest.json').write_text(json.dumps({'origin':'original code-authored concept examples','font':'Pretendard','logo':'assets/branding/notiontalk-white.png','no_reference_pdf_images_reused':True,'fictitious_infographic_values':True,'types':allk},ensure_ascii=False,indent=2),encoding='utf8')
print('Generated 5 type examples and 6 timing/easing examples.')
