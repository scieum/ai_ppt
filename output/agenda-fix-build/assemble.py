from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import posixpath
B=Path(__file__).resolve().parent;R=B.parents[1]
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
PK='http://schemas.openxmlformats.org/package/2006/relationships'
def target(p,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};return[target('ppt/presentation.xml',rs[x.get('{'+N['r']+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
def xml(x):return E.tostring(x,encoding='UTF-8',xml_declaration=True,standalone=True)
jobs=[('library',R/'assets/layout-library-20261028/NotionTalk_상황별레이아웃_20종_v3.pptx',2),('application',R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_레이아웃에셋적용_21장_v16.pptx',3)]
for key,source,page in jobs:
 with ZipFile(source)as z,ZipFile(B/(key+'-agenda.pptx'))as a:
  files={n:z.read(n)for n in z.namelist()};part=ordered(z)[page-1];base=E.fromstring(files[part]);authpart=ordered(a)[0];new=E.fromstring(a.read(authpart));oldtree=base.find('p:cSld/p:spTree',N);tree=deepcopy(new.find('p:cSld/p:spTree',N))
  footer=next(x for x in oldtree.findall('p:sp',N)if x.find('p:nvSpPr/p:cNvPr',N).get('name')in['copyright-footer','copyright_footer']);tree.append(deepcopy(footer))
  for i,cn in enumerate(tree.findall('.//p:cNvPr',N),1):cn.set('id',str(i))
  assert base.find('p:timing',N)is None
  base.find('p:cSld',N).replace(oldtree,tree)
  # Bind the logo to the unchanged original branding file; no reference-page bitmap is used.
  sr=E.fromstring(files[rel(part)]);pic=tree.find('p:pic',N);rid='rIdAgendaOriginalLogo';pic.find('p:blipFill/a:blip',N).set('{'+N['r']+'}embed',rid);media='ppt/media/agenda-notiontalk-original.png';files[media]=(R/'assets/branding/notiontalk-white.png').read_bytes();E.SubElement(sr,'{'+PK+'}Relationship',Id=rid,Type=N['r']+'/image',Target='/'+media)
  files[part]=xml(base);files[rel(part)]=xml(sr)
  with ZipFile(B/(key+'-candidate.pptx'),'w',ZIP_DEFLATED)as out:
   for name,data in files.items():out.writestr(name,data)
 print(key,'updated only page',page)
