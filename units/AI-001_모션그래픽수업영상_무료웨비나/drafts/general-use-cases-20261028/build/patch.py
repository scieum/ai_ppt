from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
import posixpath,json,hashlib
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1];S=R/'output/webinar-part1-developed/NotionTalk_Part1_내용디자인고도화_21장_v3.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def target(p,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def at(z):
 rid=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)[5].get('{'+N['r']+'}id');rs=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'));return target('ppt/presentation.xml',next(r.get('Target') for r in rs if r.get('Id')==rid))
def raw(n):return E.tostring(n,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(S) as base,ZipFile(B/'edited-roundtrip.pptx') as extra:
 files={n:base.read(n) for n in base.namelist()};p=at(base);ep=at(extra);s=E.fromstring(files[p]);e=E.fromstring(extra.read(ep));names=['dev-format-head-2']+['dev-format-'+str(i)+'-2' for i in range(5)]
 for name in names:
  xpath='.//p:sp[p:nvSpPr/p:cNvPr[@name="'+name+'"]]';old=s.xpath(xpath,namespaces=N)[0];new=deepcopy(e.xpath(xpath,namespaces=N)[0]);new.find('.//p:cNvPr',N).set('id',old.find('.//p:cNvPr',N).get('id'));old.getparent().replace(old,new)
 files[p]=raw(s)
 rs=E.fromstring(files[rel(p)]);ers=E.fromstring(extra.read(rel(ep)));np=target(p,next(r.get('Target') for r in rs if r.get('Type').endswith('/notesSlide')));enp=target(ep,next(r.get('Target') for r in ers if r.get('Type').endswith('/notesSlide')))
 no=E.fromstring(files[np]);ne=E.fromstring(extra.read(enp))
 def body(nt):return next(x.find('p:txBody',N) for x in nt.findall('.//p:sp',N) if x.find('.//p:ph',N) is not None and x.find('.//p:ph',N).get('type')=='body')
 ob=body(no);ob.getparent().replace(ob,deepcopy(body(ne)));files[np]=raw(no)
 changed=[n for n in base.namelist() if base.read(n)!=files[n]];assert set(changed)=={p,np}
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as z:
  for n,v in files.items():z.writestr(n,v)
 (B/'preservation.json').write_text(json.dumps({'source_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'changed_parts':changed,'edited_page':6},indent=2),encoding='utf8')
print('Updated only slide 6 text objects and its speaker note.')
