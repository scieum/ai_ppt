from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import posixpath,json
B=Path(__file__).resolve().parent;R=B.parent.parent
src=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_헤더확대_글라스로고_43장_v27.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with ZipFile(src) as z:data={n:z.read(n) for n in z.namelist()}
with ZipFile(B/'colored-assets.pptx') as z:
 for i,name in enumerate(['claude','higgsfield'],1):
  part=f'ppt/slides/slide{i}.xml';root=E.fromstring(z.read(part));rid=root.find('.//a:blip',N).get('{'+N['r']+'}embed')
  rel=next(r for r in E.fromstring(z.read(f'ppt/slides/_rels/slide{i}.xml.rels')) if r.get('Id')==rid)
  target=posixpath.normpath(posixpath.join(posixpath.dirname(part),rel.get('Target')))
  data[f'ppt/media/header-glass-{name}.png']=z.read(target.lstrip('/'))
with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as z:
 for n,v in data.items():z.writestr(n,v)
s=(R/'output/header-glass-build/finalize.mjs').read_text(encoding='utf-8')
s=s.replace('NotionTalk_모션그래픽_사이클활동안내_43장_v26.pptx',src.name).replace("path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_헤더확대_글라스로고_43장_v27.pptx')","path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_로고색복원_43장_v28.pptx')")
# The output replacement above also matches source: reset the source declaration explicitly.
s=s.replace("const source=path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_로고색복원_43장_v28.pptx')",f"const source=path.join(R,'output/webinar-knowledge-only/{src.name}')")
(B/'finalize.mjs').write_text(s,encoding='utf-8')
s=(R/'output/header-glass-build/export.ps1').read_text(encoding='utf-8-sig').replace('output/header-glass-build','output/logo-color-build').replace('NotionTalk_모션그래픽_헤더확대_글라스로고_43장_v27','NotionTalk_모션그래픽_로고색복원_43장_v28').replace('renders/header-glass-20261030','renders/logo-color-20261030')
(B/'export.ps1').write_text(s,encoding='utf-8-sig')
print('Only two media payloads replaced; all slide XML preserved.')
