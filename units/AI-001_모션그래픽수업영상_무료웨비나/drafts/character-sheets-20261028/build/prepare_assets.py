from pathlib import Path
from PIL import Image
from scipy.ndimage import label,find_objects
import numpy as np,json,hashlib
B=Path(__file__).resolve().parent;U=B.parents[2];A=U/'assets/character-sheets-20261028'
names={'bear':['thinking','stopwatch','greeting'],'woman':['compare','explain','celebrate'],'man':['review','approve','present']};poses=[]
records=json.loads((A/'manifest.json').read_text(encoding='utf-8'))
for rec in records:
 p=Path(rec['workspace_path']);im=Image.open(p);w,h=im.size;mask=np.array(im.getchannel('A'))>32;lab,num=label(mask);objects=[]
 for i,sl in enumerate(find_objects(lab),1):
  if sl is not None:
   count=int((lab[sl]==i).sum())
   if count>10000:objects.append((count,sl))
 figures=sorted(sorted(objects,reverse=True,key=lambda x:x[0])[:3],key=lambda x:x[1][1].start);assert len(figures)==3
 for pose,(_,sl) in zip(names[rec['kind']],figures):
  x0=max(0,sl[1].start-12);x1=min(w,sl[1].stop+12);y0=max(0,sl[0].start-12);y1=min(h,sl[0].stop+12)
  poses.append({'id':rec['kind']+'-'+pose,'character':rec['kind'],'pose':pose,'file':str(p.resolve()),'pixel_rect':[x0,y0,x1,y1],'crop':{'left':x0/w,'top':y0/h,'right':1-x1/w,'bottom':1-y1/h},'aspect_ratio':(x1-x0)/(y1-y0)})
 rec.update(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),dimensions=[w,h],mode=im.mode,alpha_extrema=list(im.getchannel('A').getextrema()),pose_ids=[x['id']for x in poses if x['character']==rec['kind']],visual_review='three distinct full-body poses, consistent face/hair/clothes/glasses, transparent; no user image pixels edited')
(A/'poses.json').write_text(json.dumps(poses,ensure_ascii=False,indent=2),encoding='utf-8');(A/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8');print([(x['id'],x['pixel_rect'])for x in poses])
