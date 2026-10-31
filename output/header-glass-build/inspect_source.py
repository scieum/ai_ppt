from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import posixpath,json,collections
B=Path(__file__).resolve().parent;R=B.parent.parent
SOURCE=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_사이클활동안내_43장_v26.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def target(p,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
with ZipFile(SOURCE)as z:
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};parts=[target('ppt/presentation.xml',rs[x.get('{'+N['r']+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
 matches=[];prep=[]
 for i,part in enumerate(parts,1):
  root=E.fromstring(z.read(part))
  for sp in root.findall('.//p:sp',N):
   name=sp.find('p:nvSpPr/p:cNvPr',N).get('name');sid=sp.find('p:nvSpPr/p:cNvPr',N).get('id');off=sp.find('p:spPr/a:xfrm/a:off',N);ext=sp.find('p:spPr/a:xfrm/a:ext',N)
   if off is None:continue
   x,y=float(off.get('x'))/9525,float(off.get('y'))/9525
   t=''.join(sp.xpath('.//a:t/text()',namespaces=N));sizes=sp.xpath('.//@sz')
   item={'slide':i,'part':part,'id':sid,'name':name,'x':x,'y':y,'width':float(ext.get('cx'))/9525,'height':float(ext.get('cy'))/9525,'text':t,'sizes':sizes}
   if y<140 and x<1000 and t:matches.append(item)
   if i==3:prep.append(item)
  if i==3:
   rp=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels');rels={r.get('Id'):target(part,r.get('Target')) for r in E.fromstring(z.read(rp))}
   for pic in root.findall('.//p:pic',N):
    nv=pic.find('p:nvPicPr/p:cNvPr',N);rid=pic.find('.//a:blip',N).get('{'+N['r']+'}embed');prep.append({'pic_id':nv.get('id'),'name':nv.get('name'),'media':rels[rid],'rid':rid})
 (B/'source-audit.json').write_text(json.dumps({'source':str(SOURCE),'parts':parts,'headers':matches,'prep':prep},ensure_ascii=False,indent=2),encoding='utf-8')
 grouped=collections.defaultdict(list)
 for a in matches:grouped[(a['name'],tuple(a['sizes']))].append(a['slide'])
 for k,v in grouped.items():print(k,v)
 print(json.dumps(prep,ensure_ascii=False,indent=2))
