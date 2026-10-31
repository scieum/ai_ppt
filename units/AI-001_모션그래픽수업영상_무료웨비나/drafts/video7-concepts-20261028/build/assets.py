from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,math,json
B=Path(__file__).resolve().parent;A=B/'assets';A.mkdir(exist_ok=True)
W,H=720,240;BG=(32,32,32);O=(255,145,29)
def frame(kind,u):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 if kind=='morph':
  exponent=2+4*(.5-.5*math.cos(u*2*math.pi));pts=[]
  for i in range(180):
   a=i*math.pi/90;c=math.cos(a);s=math.sin(a)
   pts.append((360+74*math.copysign(abs(c)**(2/exponent),c),120+74*math.copysign(abs(s)**(2/exponent),s)))
  d.polygon(pts,fill=O)
 elif kind=='rotation':
  angle=u*2*math.pi;ax=-.35;verts=[]
  for x,y,z in [(-54,-54,-54),(54,-54,-54),(54,54,-54),(-54,54,-54),(-54,-54,54),(54,-54,54),(54,54,54),(-54,54,54)]:
   xx=x*math.cos(angle)+z*math.sin(angle);zz=-x*math.sin(angle)+z*math.cos(angle);yy=y*math.cos(ax)-zz*math.sin(ax);zz=y*math.sin(ax)+zz*math.cos(ax);verts.append((xx,yy,zz))
  faces=[([0,1,2,3],(255,146,30)),([4,5,6,7],(224,119,21)),([0,1,5,4],(255,213,145)),([3,2,6,7],(174,93,21)),([0,3,7,4],(235,132,29)),([1,2,6,5],(249,169,65))]
  for ids,col in sorted(faces,key=lambda f:sum(verts[i][2]for i in f[0])/4,reverse=True):
   pts=[(360+x*400/(400+z),120+y*400/(400+z))for x,y,z in [verts[i]for i in ids]];d.polygon(pts,fill=col)
 elif kind=='gradient':
  yy,xx=np.mgrid[:H,:W];phase=(xx/W+.30*np.sin(yy/H*math.pi)+u)%1
  v=.5+.5*np.sin(phase*2*math.pi);low=np.array([210,105,15]);high=np.array([255,225,160]);rgb=(low+(high-low)*v[...,None]).astype('uint8')
  layer=Image.fromarray(rgb);mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rounded_rectangle((140,40,580,200),radius=38,fill=255);im.paste(layer,(0,0),mask)
 return im
for kind in ['morph','rotation','gradient']:
 # Smooth periodic curves start and finish at adjacent phases.
 frames=[frame(kind,i/75)for i in range(75)]
 frames[0].save(A/(kind+'.gif'),save_all=True,append_images=frames[1:],duration=40,loop=0,optimize=False,disposal=2)
 frames[0].save(A/(kind+'-poster.png'))
 phases=[0,.125,.25]if kind=='rotation'else[0,.25,.5]if kind=='morph'else[0,.2,.4]
 for k,u in enumerate(phases):frame(kind,u).save(A/f'{kind}-state-{k}.png')
(A/'manifest.json').write_text(json.dumps({'origin':'original mathematical motion illustrations','fps':25,'loop':0,'source_media_reused':False,'kinds':['morph','rotation','gradient']},indent=2),encoding='utf8')
print('Generated original morph, 3D rotation and gradient flow examples with static snapshots.')
