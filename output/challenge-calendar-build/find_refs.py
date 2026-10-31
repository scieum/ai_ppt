from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import subprocess,json,fitz
R=Path(__file__).resolve().parents[2];B=Path(__file__).resolve().parent
files=subprocess.check_output(['rg','--files','-g','*.pptx','-g','*.pdf'],cwd=R,text=True,encoding='utf-8').splitlines()
seen=set();matches=[]
for f in files:
 if any(s in f for s in ['node_modules','deps','history','candidate','additions','restyled','publish-final']):continue
 p=R/f
 if p.suffix=='.pptx':
  with ZipFile(p)as z:
   for n in z.namelist():
    if n.startswith('ppt/slides/')and n.endswith('.xml'):
     text=' '.join(E.fromstring(z.read(n)).xpath('//*[local-name()="t"]/text()'))
     if any(k in text for k in ['캘린더','달력','1차 사이클','2차 사이클','일 월 화','SUN','Sun','요일','챌린지 일정']) and text not in seen:
      seen.add(text);matches.append({'file':str(p),'part':n,'text':text[:1800]})
for p in Path('C:/Users/User/Downloads').glob('*.pdf'):
 if not any(k in p.name for k in ['사이클','허들링','챌린지']):continue
 try:
  doc=fitz.open(p)
  for i,page in enumerate(doc):
   t=page.get_text()
   if any(k in t for k in ['캘린더','달력','1차 사이클','2차 사이클','월 화 수','SUN','Sun','챌린지 일정']):
    matches.append({'file':str(p),'page':i+1,'text':t[:1400]})
 except Exception:pass
(B/'reference-matches.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(matches,ensure_ascii=False,indent=2)[:22000])
