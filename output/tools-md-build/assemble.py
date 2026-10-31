from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import posixpath,json,hashlib
B=Path(__file__).resolve().parent;R=B.parent.parent
SOURCE=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_표디자인정리_40장_v22.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'};PK='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types'
def target(p,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(e):return E.tostring(e,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};return[target('ppt/presentation.xml',rs[x.get('{'+N['r']+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
spec=json.loads((B/'additions.json').read_text(encoding='utf-8'))
with ZipFile(SOURCE)as z,ZipFile(B/'additions.pptx')as a:
 files={n:z.read(n)for n in z.namelist()};old=ordered(z);auth=ordered(a)
 prs=E.fromstring(files['ppt/presentation.xml']);lst=prs.find('p:sldIdLst',N);prsrels=E.fromstring(files['ppt/_rels/presentation.xml.rels']);types=E.fromstring(files['[Content_Types].xml'])
 for i,d in enumerate(spec):
  ref=old[(d['replace'] or 36)-1];rr=E.fromstring(files[rel(ref)])
  layout=next(target(ref,r.get('Target')) for r in rr if r.get('Type').endswith('/slideLayout'))
  note_src=next(target(ref,r.get('Target')) for r in rr if r.get('Type').endswith('/notesSlide'))
  dst=ref if d['replace'] else 'ppt/slides/tools-narration.xml'
  note_dst=note_src if d['replace'] else 'ppt/notesSlides/tools-narration.xml'
  src=auth[i];sr=E.fromstring(a.read(rel(src)));newrel=E.Element('{'+PK+'}Relationships',nsmap={None:PK})
  for r in sr:
   kind=r.get('Type').split('/')[-1];rd=deepcopy(r)
   if kind=='slideLayout':rd.set('Target','/'+layout)
   elif kind=='image':
    data=a.read(target(src,r.get('Target')));media='ppt/media/tools-md-'+hashlib.sha256(data).hexdigest()[:16]+'.png';files[media]=data;rd.set('Target','/'+media)
   elif kind=='notesSlide':continue
   else:raise ValueError(kind)
   newrel.append(rd)
  E.SubElement(newrel,'{'+PK+'}Relationship',Id='rIdToolNotes',Type=N['r']+'/notesSlide',Target='/'+note_dst)
  files[dst]=a.read(src);files[rel(dst)]=xml(newrel)
  note=E.fromstring(files[note_src]);body=next(sp.find('p:txBody',N)for sp in note.findall('.//p:sp',N)if sp.find('p:nvSpPr/p:nvPr/p:ph',N)is not None and sp.find('p:nvSpPr/p:nvPr/p:ph',N).get('type')=='body')
  for pp in body.findall('a:p',N):body.remove(pp)
  pp=E.SubElement(body,'{'+N['a']+'}p');run=E.SubElement(pp,'{'+N['a']+'}r');E.SubElement(run,'{'+N['a']+'}t').text=d['notes'];files[note_dst]=xml(note)
  if not d['replace']:
   nr=E.fromstring(files[rel(note_src)])
   for r in nr:
    if r.get('Type').endswith('/slide'):r.set('Target','/'+dst)
    else:r.set('Target','/'+target(note_src,r.get('Target')))
   files[rel(note_dst)]=xml(nr)
   rid='rIdToolsNarration';E.SubElement(prsrels,'{'+PK+'}Relationship',Id=rid,Type=N['r']+'/slide',Target='/'+dst)
   sid=E.Element('{'+N['p']+'}sldId',id=str(max(int(x.get('id')) for x in lst)+1));sid.set('{'+N['r']+'}id',rid);lst.insert(d['before']-1,sid)
   for part,kind in [(dst,'slide'),(note_dst,'notesSlide')]:E.SubElement(types,'{'+CT+'}Override',PartName='/'+part,ContentType=f'application/vnd.openxmlformats-officedocument.presentationml.{kind}+xml')
  d['package_part']=dst
 files['ppt/presentation.xml']=xml(prs);files['ppt/_rels/presentation.xml.rels']=xml(prsrels);files['[Content_Types].xml']=xml(types)
 app=E.fromstring(files['docProps/app.xml']);app.find('{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Slides').text='41';files['docProps/app.xml']=xml(app)
 assert all(files[n]==z.read(n) for n in z.namelist() if n.startswith('ppt/media/'))
 assert all(files[n]==z.read(n) for i,n in enumerate(old,1) if i not in (3,25))
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED)as out:
  for name,data in files.items():out.writestr(name,data)
 (B/'slide-map.json').write_text(json.dumps({'source':str(SOURCE),'source_parts':old,'changes':spec,'count':41},ensure_ascii=False,indent=2),encoding='utf-8')
print('41 slides: replaced 3 and 25, added narration at 37; preserved 38 original slides and all media.')
