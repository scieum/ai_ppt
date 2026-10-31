from pathlib import Path
import fitz,json
from PIL import Image,ImageDraw
R=Path.cwd(); B=R/'output/reference-style-build'; c=json.loads((R/'assets/layout-library-20261028/catalog.json').read_text(encoding='utf8'))
for src,pages in [(c['source_documents'][0],[12,16,18,28,39,40,50,54,62,64,74,79]),(c['source_documents'][1],[5,17,29,31,33,34])]:
 d=fitz.open(src['path']); thumbs=[]
 for n in pages:
  pix=d[n-1].get_pixmap(matrix=fitz.Matrix(1,1)); f=B/f"{src['id']}-{n}.png";pix.save(str(f));im=Image.open(f).convert('RGB');im.thumbnail((640,360));thumbs.append((n,im))
 sheet=Image.new('RGB',(1280,390*((len(thumbs)+1)//2)),'#dddddd');dr=ImageDraw.Draw(sheet)
 for i,(n,im) in enumerate(thumbs):x=i%2*640;y=i//2*390;sheet.paste(im,(x,y+25));dr.text((x+10,y+5),f"{src['id']} p{n}",fill='black')
 sheet.save(B/f"{src['id']}-contact.jpg")
D=R/'units/AI-001_모션그래픽수업영상_무료웨비나/renders/style-docs-20261029';nums=list(range(24,32))+list(range(34,40));out=Image.new('RGB',(1280,390*7),'#dddddd');dr=ImageDraw.Draw(out)
for i,n in enumerate(nums):
 im=Image.open(D/f'slide-{n:02}.png');im.thumbnail((640,360));x=i%2*640;y=i//2*390;out.paste(im,(x,y+25));dr.text((x+10,y+5),str(n),fill='black')
out.save(B/'before.jpg')
