from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,fitz,hashlib
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';O=R/'output/webinar-knowledge-only'
old=O/'NotionTalk_모션그래픽_표디자인정리_40장_v22.pptx';new=O/'NotionTalk_모션그래픽_준비물_문서_내레이션_41장_v23.pptx'
spec=json.loads((B/'slide-map.json').read_text(encoding='utf-8'));preserved=[]
with ZipFile(old)as a,ZipFile(new)as b:
 for i,p in enumerate(spec['source_parts'],1):
  if i not in (3,25):assert a.read(p)==b.read(p);preserved.append(i)
 for n in a.namelist():
  if n.startswith('ppt/media/'):assert a.read(n)==b.read(n)
 gif_count=sum(n.startswith('ppt/media/')and n.endswith('.gif')for n in b.namelist())
pdf0,pdf1=fitz.open(old.with_suffix('.pdf')),fitz.open(new.with_suffix('.pdf'));assert len(pdf0)==40 and len(pdf1)==41
for n in preserved:
 idx=n-1 if n<37 else n
 assert pdf0[n-1].get_pixmap().samples==pdf1[idx].get_pixmap().samples,f'Unexpected change {n}'
for n in (3,25,37):pdf1[n-1].get_pixmap(matrix=fitz.Matrix(2,2)).save(B/f'after-{n}.png')
assert 'Higgsfield' not in pdf1[2].get_text() and '힉스필드' not in pdf1[2].get_text()
assert all(x in pdf1[24].get_text()for x in ['storyline.md','design.md','motion.md'])
assert 'ElevenLabs' in pdf1[36].get_text()
result={'count':41,'replaced':[3,25],'added':[37],'preserved_original_slide_count':len(preserved),'preserved_original_slide_xml_and_pdf_pixels':True,'all_original_media_preserved':True,'gif_count':gif_count,'pptx_sha256':hashlib.sha256(new.read_bytes()).hexdigest()}
check=U/'checks/tools-md-20261029';check.mkdir(parents=True,exist_ok=True);(check/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result))
