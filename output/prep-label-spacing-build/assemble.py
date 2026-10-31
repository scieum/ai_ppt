from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
B=Path(__file__).resolve().parent;R=B.parent.parent
old='NotionTalk_모션그래픽_폰트간격점검_43장_v29';new='NotionTalk_모션그래픽_준비물안내박스_43장_v30'
src=R/f'output/webinar-knowledge-only/{old}.pptx';part='ppt/slides/restored-preparation.xml'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(src) as z:data={n:z.read(n) for n in z.namelist()}
root=E.fromstring(data[part]);shapes={s.find('p:nvSpPr/p:cNvPr',N).get('name'):s for s in root.findall('.//p:sp',N)}
with ZipFile(B/'container.pptx') as z:ct=E.fromstring(z.read('ppt/slides/slide1.xml'))
newprop=deepcopy(ct.find('.//p:sp/p:spPr',N));opt=shapes['optional'];prop=opt.find('p:spPr',N);opt.replace(prop,newprop)
# Use precisely the same text inset and vertical centering as the approved left label.
bp=opt.find('p:txBody/a:bodyPr',N);bp.getparent().replace(bp,deepcopy(shapes['required'].find('p:txBody/a:bodyPr',N)))
for name in ['choose-one','watch-demo']:shapes[name].find('p:spPr/a:xfrm/a:off',N).set('y',str(616*9525))
data[part]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as z:
 for n,b in data.items():z.writestr(n,b)
f=(R/'output/typography-qa-build/finalize.mjs').read_text(encoding='utf-8').replace('NotionTalk_모션그래픽_로고색복원_43장_v28',old).replace(f'/{old}.pptx\'),pythonExecutable',f'/{new}.pptx\'),pythonExecutable')
(B/'finalize.mjs').write_text(f,encoding='utf-8')
e=(R/'output/typography-qa-build/export.ps1').read_text(encoding='utf-8-sig').replace('output/typography-qa-build','output/prep-label-spacing-build').replace(old,new).replace('renders/typography-qa-20261030','renders/prep-label-spacing-20261030')
(B/'export.ps1').write_text(e,encoding='utf-8-sig')
print('Assembled narrow three-shape edit on slide 3 only.')
