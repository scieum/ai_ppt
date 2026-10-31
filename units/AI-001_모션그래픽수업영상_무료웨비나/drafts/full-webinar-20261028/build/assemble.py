from pathlib import Path,PurePosixPath
from zipfile import ZipFile,ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
import posixpath,json,hashlib,sys
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
SRC=R/'output/webinar-part1-developed/NotionTalk_Part1_내용디자인고도화_21장_v5.pptx'
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PKG='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types'
NS={'p':P,'a':A,'r':REL};sha=lambda b:hashlib.sha256(b).hexdigest()
def target(part,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part),t))
def relpart(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(e):return E.tostring(e,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 ids=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',NS);rs={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 return [target('ppt/presentation.xml',rs[x.get('{'+REL+'}id')]) for x in ids]
rows=json.loads((B/'additions.json').read_text(encoding='utf8'))
if len(sys.argv)>1 and sys.argv[1]=='timing':
 with ZipFile(B/'candidate.pptx') as base,ZipFile(B/'native-animation.pptx') as anim:
  files={n:base.read(n) for n in base.namelist()};bp=ordered(base);ap=ordered(anim)
  for page in [29,30]:
   tree=E.fromstring(files[bp[page-1]]);extra=E.fromstring(anim.read(ap[page-1]));timing=extra.find('p:timing',NS);assert timing is not None
   old=tree.find('p:timing',NS)
   if old is not None:tree.remove(old)
   tree.append(deepcopy(timing));files[bp[page-1]]=xml(tree)
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as out:
  for n,v in files.items():out.writestr(n,v)
 print('Transplanted native effects on pages 29 and 30 only.');sys.exit(0)
with ZipFile(SRC) as base,ZipFile(B/'edited-roundtrip.pptx') as extra:
 files={n:base.read(n) for n in base.namelist()};original=files.copy();bp=ordered(base);ep=ordered(extra)
 types=E.fromstring(files['[Content_Types].xml']);et=E.fromstring(extra.read('[Content_Types].xml'));ov={x.get('PartName'):x.get('ContentType') for x in et if x.tag.endswith('Override')};defaults={x.get('Extension') for x in types if x.tag.endswith('Default')}
 def override(new,old):E.SubElement(types,'{'+CT+'}Override',PartName='/'+new,ContentType=ov['/'+old])
 media_hash={sha(v):n for n,v in files.items() if n.startswith('ppt/media/')}
 def media(old):
  data=extra.read(old);digest=sha(data)
  if digest in media_hash:return media_hash[digest]
  ext=PurePosixPath(old).suffix[1:];new='ppt/media/complete-'+digest[:20]+'.'+ext;files[new]=data;media_hash[digest]=new
  if ext not in defaults:
   typ=next(x.get('ContentType') for x in et if x.tag.endswith('Default') and x.get('Extension')==ext);E.SubElement(types,'{'+CT+'}Default',Extension=ext,ContentType=typ);defaults.add(ext)
  return new
 pres=E.fromstring(files['ppt/presentation.xml']);ids=pres.find('p:sldIdLst',NS);old_ids=list(ids);pr=E.fromstring(files['ppt/_rels/presentation.xml.rels']);maxid=max(int(x.get('id')) for x in ids);newids={};newparts={}
 for i,row in enumerate(rows,1):
  old=ep[row['export_slide']-1];new='ppt/slides/complete-'+row['key']+'.xml';tree=E.fromstring(extra.read(old))
  if row.get('copyAnimation'):
   src=E.fromstring(base.read(bp[row['template']-1]));timing=deepcopy(src.find('p:timing',NS));oldnames={x.get('id'):x.get('name') for x in src.findall('.//p:cNvPr',NS)};newnames={x.get('name'):x.get('id') for x in tree.findall('.//p:cNvPr',NS)}
   for x in timing.findall('.//p:spTgt',NS):x.set('spid',newnames[oldnames[x.get('spid')]])
   tree.append(timing)
  files[new]=xml(tree);override(new,old)
  template=bp[row['template']-1];br=E.fromstring(base.read(relpart(template)));layout=next(target(template,x.get('Target')) for x in br if x.get('Type').endswith('/slideLayout'));bn=next(target(template,x.get('Target')) for x in br if x.get('Type').endswith('/notesSlide'));nr=E.fromstring(base.read(relpart(bn)));master=next(target(bn,x.get('Target')) for x in nr if x.get('Type').endswith('/notesMaster'))
  rs=E.fromstring(extra.read(relpart(old)))
  for rel in rs:
   if rel.get('TargetMode')=='External':continue
   t=target(old,rel.get('Target'));kind=rel.get('Type').rsplit('/',1)[-1]
   if kind=='slideLayout':dest=layout
   elif kind=='image':dest=media(t)
   elif kind=='notesSlide':
    dest='ppt/notesSlides/complete-'+row['key']+'.xml';files[dest]=extra.read(t);override(dest,t);nrs=E.fromstring(extra.read(relpart(t)))
    for nrel in nrs:
     nk=nrel.get('Type').rsplit('/',1)[-1]
     if nk=='slide':nd=new
     elif nk=='notesMaster':nd=master
     elif nk=='image':nd=media(target(t,nrel.get('Target')))
     else:raise ValueError(nk)
     nrel.set('Target','/'+nd)
    files[relpart(dest)]=xml(nrs)
   else:raise ValueError(kind)
   rel.set('Target','/'+dest)
  files[relpart(new)]=xml(rs);rid='rIdComplete'+str(i);assert not any(x.get('Id')==rid for x in pr);E.SubElement(pr,'{'+PKG+'}Relationship',Id=rid,Type=REL+'/slide',Target='/'+new);newids[row['key']]=E.Element('{'+P+'}sldId',{'id':str(maxid+i),'{'+REL+'}id':rid});newparts[row['key']]=new
 sequence=[None]*48
 for i in range(19):sequence[i]=i+1
 sequence[33]=20;sequence[40]=21
 for row in rows:assert sequence[row['page']-1] is None;sequence[row['page']-1]=row['key']
 assert None not in sequence
 for x in list(ids):ids.remove(x)
 for key in sequence:ids.append(old_ids[key-1] if isinstance(key,int) else newids[key])
 files['ppt/presentation.xml']=xml(pres);files['ppt/_rels/presentation.xml.rels']=xml(pr);files['[Content_Types].xml']=xml(types)
 if 'docProps/app.xml' in files:
  app=E.fromstring(files['docProps/app.xml'])
  for el in app.iter():
   if E.QName(el).localname=='Slides':el.text='48'
  files['docProps/app.xml']=xml(app)
 allowed={'ppt/presentation.xml','ppt/_rels/presentation.xml.rels','[Content_Types].xml','docProps/app.xml'}
 for name,data in original.items():
  if name not in allowed:assert files[name]==data,name
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as z:
  for n,v in files.items():z.writestr(n,v)
 (B/'preservation.json').write_text(json.dumps({'source_sha256':sha(SRC.read_bytes()),'sequence':sequence,'all_21_original_slides_and_media_preserved':True,'new_slide_parts':newparts,'original_page_mapping':{str(i):sequence.index(i)+1 for i in range(1,22)}},ensure_ascii=False,indent=2),encoding='utf8')
print('Assembled 48 slides; all 21 original slide parts, media, notes and animations preserved.')
