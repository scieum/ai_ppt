from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import posixpath,json,hashlib
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1];SRC=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_준비물복원_17장_v11.pptx'
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PK='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types';N={'p':P,'a':A}
def target(p,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(x):return E.tostring(x,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 return [target('ppt/presentation.xml',rs[x.get('{'+REL+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
with ZipFile(SRC)as src,ZipFile(B/'roundtrip.pptx')as authored:
 files={p:src.read(p)for p in src.namelist()};sp=ordered(src);ep=ordered(authored);ct=E.fromstring(files['[Content_Types].xml']);pres=E.fromstring(files['ppt/presentation.xml']);ids=pres.find('p:sldIdLst',N);oldids=[deepcopy(x)for x in ids];pr=E.fromstring(files['ppt/_rels/presentation.xml.rels']);added={}
 for spec in json.loads((B/'edits.json').read_text(encoding='utf-8')):
  page=spec['page'];old=sp[7];part=f'ppt/slides/video-tones-{page}.xml';note=f'ppt/notesSlides/video-tones-{page}.xml';base=E.fromstring(src.read(old));edit=E.fromstring(authored.read(ep[spec['export_page']-1]));tree=base.find('p:cSld/p:spTree',N)
  cur={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in base.findall('.//p:sp',N)};changed={x.find('p:nvSpPr/p:cNvPr',N).get('name'):x for x in edit.findall('.//p:sp',N)}
  for name in spec['remove']:
   sh=cur[name];sh.getparent().remove(sh)
  for pic in list(tree.findall('p:pic',N)):
   if pic.find('p:nvPicPr/p:cNvPr',N).get('name','').startswith('motion-example-'):tree.remove(pic)
  for name,value in spec['edits'].items():
   body=cur[name].find('p:txBody',N);para=body.find('a:p',N);run=deepcopy(para.find('a:r',N));run.find('a:t',N).text=value
   for p in list(body.findall('a:p',N)):body.remove(p)
   p=E.SubElement(body,'{'+A+'}p');prop=para.find('a:pPr',N)
   if prop is not None:p.append(deepcopy(prop))
   p.append(run)
   if name.startswith('effect-desc-'):
    props=cur[name].find('p:spPr',N);props.replace(props.find('a:xfrm',N),deepcopy(changed[name].find('p:spPr/a:xfrm',N)))
  nextid=max(int(x.get('id'))for x in base.findall('.//p:cNvPr',N))+1
  bottom=deepcopy(changed['tone-takeaway']);bottom.find('p:nvSpPr/p:cNvPr',N).set('id',str(nextid));nextid+=1;tree.append(bottom)
  sr=E.fromstring(src.read(rel(old)));oldnote=target(old,next(x.get('Target')for x in sr if x.get('Type').endswith('/notesSlide')))
  for x in sr:
   if x.get('TargetMode')!='External':x.set('Target','/'+(note if x.get('Type').endswith('/notesSlide')else target(old,x.get('Target'))))
  for j,(im,pic) in enumerate(zip(spec['images'],edit.findall('.//p:pic',N)[-3:])):
   pic=deepcopy(pic);cn=pic.find('p:nvPicPr/p:cNvPr',N);cn.set('id',str(nextid));cn.set('name',im['name']);nextid+=1
   rid='rIdTone'+str(j);pic.find('p:blipFill/a:blip',N).set('{'+REL+'}embed',rid);data=Path(im['file']).read_bytes();media='ppt/media/tone-'+hashlib.sha256(data).hexdigest()[:16]+'.gif';files[media]=data;E.SubElement(sr,'{'+PK+'}Relationship',Id=rid,Type=REL+'/image',Target='/'+media);tree.append(pic)
  timing=base.find('p:timing',N)
  if timing is not None:base.remove(timing)
  nt=E.fromstring(src.read(oldnote));body=next(x.find('p:txBody',N)for x in nt.findall('.//p:sp',N)if x.find('.//p:ph',N)is not None and x.find('.//p:ph',N).get('type')=='body')
  for p in list(body.findall('a:p',N)):body.remove(p)
  for line in spec['notes'].split('\n'):
   para=E.SubElement(body,'{'+A+'}p');run=E.SubElement(para,'{'+A+'}r');E.SubElement(run,'{'+A+'}t').text=line
  for sh in nt.findall('.//p:sp',N):
   ph=sh.find('.//p:ph',N)
   if ph is not None and ph.get('type')=='sldNum':
    for t in sh.findall('.//a:t',N):t.text=str(page)
  nr=E.fromstring(src.read(rel(oldnote)))
  for x in nr:
   if x.get('TargetMode')!='External':x.set('Target','/'+(part if x.get('Type').endswith('/slide')else target(oldnote,x.get('Target'))))
  files[part]=xml(base);files[rel(part)]=xml(sr);files[note]=xml(nt);files[rel(note)]=xml(nr)
  for pp,typ in [(part,'slide'),(note,'notesSlide')]:E.SubElement(ct,'{'+CT+'}Override',PartName='/'+pp,ContentType='application/vnd.openxmlformats-officedocument.presentationml.'+typ+'+xml')
  rid='rIdTones'+str(page);E.SubElement(pr,'{'+PK+'}Relationship',Id=rid,Type=REL+'/slide',Target='/'+part);added[page]=E.Element('{'+P+'}sldId',{'id':str(1000+page),'{'+REL+'}id':rid})
 order=[1,2,3,4,5,6,'tone','material',7,8,9,10,'transition','rhythm',11,12,13,14,15,16,17]
 for x in list(ids):ids.remove(x)
 for page,old in enumerate(order,1):ids.append(oldids[old-1] if isinstance(old,int)else added[page])
 files['ppt/presentation.xml']=xml(pres);files['ppt/_rels/presentation.xml.rels']=xml(pr);app=E.fromstring(files['docProps/app.xml'])
 for x in app.iter():
  if E.QName(x).localname in ['Slides','Notes']:x.text='21'
 files['docProps/app.xml']=xml(app);files['[Content_Types].xml']=xml(ct)
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED)as out:
  for name,data in files.items():out.writestr(name,data)
 assert all(files[p]==src.read(p)for p in sp)
print('Preserved 17 slides and inserted four original animated comparison slides.')
