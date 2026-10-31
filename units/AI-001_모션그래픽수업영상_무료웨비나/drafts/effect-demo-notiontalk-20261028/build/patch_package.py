from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import posixpath,json,sys,hashlib
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
S=R/'output/webinar-part1-developed/NotionTalk_Part1_내용디자인고도화_21장_v2.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def relpart(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def target(p,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def at(z,n):
 ids=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N);rs=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'));rid=ids[n-1].get('{'+N['r']+'}id');return target('ppt/presentation.xml',next(r.get('Target') for r in rs if r.get('Id')==rid))
def name(n):return n.find('.//p:cNvPr',N).get('name','')
def raw(n):return E.tostring(n,encoding='UTF-8',xml_declaration=True,standalone=True)
timing=len(sys.argv)>1 and sys.argv[1]=='timing'
with ZipFile(B/'candidate.pptx' if timing else S) as base,ZipFile(B/('native-animation.pptx' if timing else 'edited-roundtrip.pptx')) as extra:
 files={n:base.read(n) for n in base.namelist()}
 if timing:
  part=at(base,9);s=E.fromstring(files[part]);e=E.fromstring(extra.read(at(extra,9)));old=s.find('p:timing',N);s.replace(old,deepcopy(e.find('p:timing',N)));files[part]=raw(s)
 else:
  for page in [8,9]:
   part=at(base,page);ep=at(extra,page);s=E.fromstring(files[part]);e=E.fromstring(extra.read(ep));st=s.find('p:cSld/p:spTree',N);et=e.find('p:cSld/p:spTree',N)
   prefix=('demo-fade','demo-slide','demo-zoom') if page==8 else ('demo-wipe','demo-type-','demo-stagger-')
   chosen=lambda n:any(name(n)==p or name(n).startswith(p) for p in prefix)
   old={name(n):n for n in st.findall('p:sp',N) if chosen(n)};new={name(n):n for n in et.findall('p:sp',N) if chosen(n)};nid=max(int(x.get('id')) for x in st.findall('.//p:cNvPr',N))+1
   for key,o in old.items():
    n=deepcopy(new[key]);n.find('.//p:cNvPr',N).set('id',o.find('.//p:cNvPr',N).get('id'));st.replace(o,n)
   for key,n in new.items():
    if key not in old:
     n=deepcopy(n);n.find('.//p:cNvPr',N).set('id',str(nid));nid+=1;st.append(n)
   files[part]=raw(s)
   if page==9:
    rs=E.fromstring(files[relpart(part)]);ers=E.fromstring(extra.read(relpart(ep)));np=target(part,next(r.get('Target') for r in rs if r.get('Type').endswith('/notesSlide')));enp=target(ep,next(r.get('Target') for r in ers if r.get('Type').endswith('/notesSlide')))
    no=E.fromstring(files[np]);ne=E.fromstring(extra.read(enp))
    def body(nt):
     return next(x.find('p:txBody',N) for x in nt.findall('.//p:sp',N) if x.find('.//p:ph',N) is not None and x.find('.//p:ph',N).get('type')=='body')
    ob=body(no);ob.getparent().replace(ob,deepcopy(body(ne)));files[np]=raw(no)
with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as out:
 for n,v in files.items():out.writestr(n,v)
with ZipFile(S) as src:
 changed=[n for n in src.namelist() if src.read(n)!=files[n]]
 assert set(changed)<={'ppt/slides/fundamentals-entrances.xml','ppt/slides/fundamentals-reveals.xml','ppt/notesSlides/fundamentals-reveals.xml'},changed
 (B/'preservation.json').write_text(json.dumps({'source_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'changed_parts':changed,'timing_updated':timing,'edited_pages':[8,9]},indent=2),encoding='utf8')
print('Surgical package update completed. Timing:',timing)
