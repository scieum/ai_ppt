from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import posixpath,hashlib,json
B=Path(__file__).resolve().parent; U=B.parents[2];R=U.parents[1]
F=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_흐름정리_캐릭터_16장_v10.pptx'
OLD=R/'output/webinar-part01-added/NotionTalk_대표5장유지_Part0_Part1추가_9장_v2.pptx'
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PK='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types'
N={'p':P,'a':A,'r':REL}
def xml(x):return E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
def rel(part):p=Path(part);return str(p.parent/'_rels'/(p.name+'.rels')).replace('\\','/')
def target(part,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part),t))
def ordered(z):
 rs=E.fromstring(z.read('ppt/_rels/presentation.xml.rels')); ps={r.get('Id'):target('ppt/presentation.xml',r.get('Target')) for r in rs}
 return [ps[x.get('{'+REL+'}id')] for x in E.fromstring(z.read('ppt/presentation.xml')).findall('p:sldIdLst/p:sldId',N)]
with ZipFile(F) as base,ZipFile(OLD) as old:
 files={n:base.read(n) for n in base.namelist()};oldpart=ordered(old)[2]
 existing=ordered(base);firstrels=E.fromstring(base.read(rel(existing[0])))
 layout=next(target(existing[0],r.get('Target')) for r in firstrels if r.get('Type').endswith('/slideLayout'))
 oldrels=E.fromstring(old.read(rel(oldpart)));newpart='ppt/slides/restored-preparation.xml';newnote='ppt/notesSlides/restored-preparation.xml'
 for r in oldrels:
  typ=r.get('Type'); op=target(oldpart,r.get('Target'))
  if typ.endswith('/slideLayout'):r.set('Target','/'+layout)
  elif typ.endswith('/notesSlide'):
   note=E.fromstring(old.read(op)); nr=E.fromstring(old.read(rel(op)))
   firstnote=next(target(existing[0],r.get('Target')) for r in firstrels if r.get('Type').endswith('/notesSlide'))
   fnr=E.fromstring(base.read(rel(firstnote)));nm=next(target(firstnote,r.get('Target')) for r in fnr if r.get('Type').endswith('/notesMaster'))
   for q in nr:q.set('Target','/'+(newpart if q.get('Type').endswith('/slide') else nm))
   for sh in note.findall('.//p:sp',N):
    ph=sh.find('.//p:ph',N)
    if ph is not None and ph.get('type')=='body':
     body=sh.find('p:txBody',N)
     for q in list(body.findall('a:p',N)):body.remove(q)
     para=E.SubElement(body,'{'+A+'}p');run=E.SubElement(para,'{'+A+'}r');E.SubElement(run,'{'+A+'}t').text=(B/'restored-notes.txt').read_text(encoding='utf-8')
    if ph is not None and ph.get('type')=='sldNum':
     for t in sh.findall('.//a:t',N):t.text='2'
   files[newnote]=xml(note);files[rel(newnote)]=xml(nr);r.set('Target','/'+newnote)
  elif typ.endswith('/image'):
   data=old.read(op);new='ppt/media/restored-prep-'+hashlib.sha256(data).hexdigest()[:16]+Path(op).suffix;files[new]=data;r.set('Target','/'+new)
  else:raise ValueError(typ)
 files[newpart]=old.read(oldpart);files[rel(newpart)]=xml(oldrels)
 pres=E.fromstring(files['ppt/presentation.xml']);ids=pres.find('p:sldIdLst',N)
 pr=E.fromstring(files['ppt/_rels/presentation.xml.rels']);rid='rIdRestoredPreparation';E.SubElement(pr,'{'+PK+'}Relationship',Id=rid,Type=REL+'/slide',Target='/'+newpart)
 sid=max(int(x.get('id')) for x in ids)+1;ids.insert(1,E.Element('{'+P+'}sldId',id=str(sid),attrib={'{'+REL+'}id':rid}))
 files['ppt/presentation.xml']=xml(pres);files['ppt/_rels/presentation.xml.rels']=xml(pr)
 ct=E.fromstring(files['[Content_Types].xml'])
 for part,typ in [(newpart,'slide'),(newnote,'notesSlide')]:E.SubElement(ct,'{'+CT+'}Override',PartName='/'+part,ContentType='application/vnd.openxmlformats-officedocument.presentationml.'+typ+'+xml')
 files['[Content_Types].xml']=xml(ct)
 app=E.fromstring(files['docProps/app.xml'])
 for x in app.iter():
  if E.QName(x).localname in ['Slides','Notes']:x.text='17'
 files['docProps/app.xml']=xml(app)
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as z:
  for name,data in files.items():z.writestr(name,data)
 assert all(files[n]==base.read(n) for n in existing)
 print('Inserted original preparation slide after cover; all 16 current slide XML parts unchanged.')
