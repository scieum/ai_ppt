from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json
B=Path(__file__).resolve().parent;R=B.parent.parent
src=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_로고색복원_43장_v28.pptx'
parts=json.loads((R/'output/header-glass-build/source-audit.json').read_text(encoding='utf-8'))['parts']
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
spec=[]
def properties(s):
 off=s.find('p:spPr/a:xfrm/a:off',N);ext=s.find('p:spPr/a:xfrm/a:ext',N)
 return {'left':int(off.get('x'))/9525,'top':int(off.get('y'))/9525,'width':int(ext.get('cx'))/9525,'height':int(ext.get('cy'))/9525}
with ZipFile(src) as z:
 for i,part in enumerate(parts,1):
  for s in E.fromstring(z.read(part)).findall('.//p:sp',N):
   name=s.find('p:nvSpPr/p:cNvPr',N).get('name');txt=''.join(s.xpath('.//a:t/text()',namespaces=N))
   if not txt:continue
   old=properties(s);new=dict(old);size=None;anchor=None;reason=None
   if name in ['part_label','part-label','part']:
    new.update(left=60,top=59+1/3,width=800,height=30);size=18;anchor='t';reason='Part label consistency'
   elif name in ['section_number','group-number']:
    new.update(left=60,top=95,width=51+1/3,height=40);size=24;anchor='t';reason='Section number consistency'
   elif name in ['section_heading','group-label','group']:
    new.update(left=116,top=95,width=825+1/3,height=40);size=24;anchor='t';reason='Section heading consistency'
   elif name in ['title','slide-title']:
    new.update(top=199+1/3,height=60);size=32;anchor='t';reason='Content title size and baseline consistency'
   elif name in ['subtitle','slide-subtitle']:
    new.update(top=269+1/3,height=36+2/3);size=17;anchor='t';reason='Subtitle size and baseline consistency'
   elif name in ['copyright','copyright_footer','copyright-footer']:
    new.update(left=720,top=686+2/3,width=506+2/3,height=20);size=10;anchor='t';reason='Footer size and right-edge consistency'
   elif i==31 and name=='bundle':
    new.update(top=609);reason='Add breathing room below folder image'
   if reason:
    font=sorted(set(int(v)/100 for v in s.xpath('.//@sz')))
    spec.append({'slide':i,'part':part,'name':name,'text':txt,'old_position':old,'position':new,'old_pt':font,'font_pt':size,'anchor':anchor,'reason':reason})
(B/'spec.json').write_text(json.dumps({'source':str(src),'parts':parts,'edits':spec},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(spec)} text objects reviewed for common typography; body and evidence left unchanged.')
