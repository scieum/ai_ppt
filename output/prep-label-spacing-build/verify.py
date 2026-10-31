from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import fitz,numpy as np,json,hashlib,shutil
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
src=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_폰트간격점검_43장_v29.pptx';out=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_준비물안내박스_43장_v30.pptx'
part='ppt/slides/restored-preparation.xml';N={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
with ZipFile(src) as a,ZipFile(out) as b:
 assert set(a.namelist())==set(b.namelist())
 changed=[n for n in a.namelist() if a.read(n)!=b.read(n)];assert changed==[part],changed
 x=E.fromstring(a.read(part));y=E.fromstring(b.read(part));assert x.xpath('//a:t/text()',namespaces=N)==y.xpath('//a:t/text()',namespaces=N)
 sx={s.find('p:nvSpPr/p:cNvPr',N).get('name'):E.tostring(s) for s in x.findall('.//p:sp',N)}
 sy={s.find('p:nvSpPr/p:cNvPr',N).get('name'):E.tostring(s) for s in y.findall('.//p:sp',N)}
 assert {n for n in sx if sx[n]!=sy[n]}=={'optional','choose-one','watch-demo'}
old=fitz.open(src.with_suffix('.pdf'));new=fitz.open(out.with_suffix('.pdf'));assert len(old)==len(new)==43
for i in range(43):
 a=old[i].get_pixmap();b=new[i].get_pixmap();av=np.frombuffer(a.samples,np.uint8).reshape(a.height,a.width,a.n);bv=np.frombuffer(b.samples,np.uint8).reshape(b.height,b.width,b.n);diff=np.any(av!=bv,axis=2)
 if i==2:diff[421:492,147:859]=False
 assert not diff.any(),i+1
bounds=json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig'));s={x['name']:x for x in bounds if x['slide']==3}
gaps={}
for label,caption in [('required','choose-one'),('optional','watch-demo')]:
 gaps[label]=s[caption]['text_top']-(s[label]['shape_top']+s[label]['shape_height'])
 assert gaps[label]>=10,gaps
 assert s[caption]['text_top']+s[caption]['text_height']<510
record={'slides':43,'changed_slide':3,'changed_shapes':['optional','choose-one','watch-demo'],'all_other_42_slides_byte_and_pixel_identical':True,'all_text_media_tables_animations_unchanged':True,'caption_gap_below_label_box_pt':gaps,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
dest=U/'checks/prep-label-spacing-20261030';dest.mkdir(parents=True,exist_ok=True);(dest/'verification.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=True))
