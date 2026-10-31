"""Preserve existing template parts; transplant six authored additions."""
from pathlib import Path,PurePosixPath
from zipfile import ZipFile,ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
import posixpath,json,hashlib,re
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
SRC=R/'output/webinar-lesson-applied/NotionTalk_웨비나_계획반영_Part1_15장_v1.pptx'
P='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PKG='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types'
NS={'p':P,'a':A,'r':REL};sha=lambda b:hashlib.sha256(b).hexdigest()
base=ZipFile(SRC);extra=ZipFile(B/'edited-roundtrip.pptx');files={n:base.read(n) for n in base.namelist()};original=dict(files)
def target(part,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part),t))
def relpart(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def xml(e):return E.tostring(e,encoding='UTF-8',xml_declaration=True,standalone=True)
def ordered(z):
 ids=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',NS);rs={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 return [target('ppt/presentation.xml',rs[x.get('{'+REL+'}id')]) for x in ids]
bp=ordered(base);ep=ordered(extra)
def set_text(body,value):
 old=body.findall('a:p',NS);template=deepcopy(old[0]) if old else E.Element('{'+A+'}p')
 sample=template.find('a:r',NS);sample=deepcopy(sample) if sample is not None else E.Element('{'+A+'}r')
 for x in old:body.remove(x)
 for line in value.split('\n'):
  para=deepcopy(template)
  for child in list(para):
   if child.tag!='{'+A+'}pPr':para.remove(child)
  run=deepcopy(sample)
  for child in list(run):
   if child.tag!='{'+A+'}rPr':run.remove(child)
  E.SubElement(run,'{'+A+'}t').text=line;para.append(run);body.append(para)
edits=json.loads((B/'edits.json').read_text(encoding='utf-8'))
for n,row in edits.items():
 part=bp[int(n)-1];tree=E.fromstring(files[part])
 for name,value in row['values'].items():
  matches=[x for x in tree.findall('.//p:sp',NS) if x.find('p:nvSpPr/p:cNvPr',NS).get('name')==name];assert len(matches)==1,name
  set_text(matches[0].find('p:txBody',NS),value)
 files[part]=xml(tree)
 rels=E.fromstring(files[relpart(part)]);note=next(target(part,x.get('Target')) for x in rels if x.get('Type').endswith('/notesSlide'));nt=E.fromstring(files[note])
 body=next(x.find('p:txBody',NS) for x in nt.findall('.//p:sp',NS) if x.find('p:nvSpPr/p:nvPr/p:ph',NS) is not None and x.find('p:nvSpPr/p:nvPr/p:ph',NS).get('type')=='body')
 set_text(body,row['notes']);files[note]=xml(nt)

types=E.fromstring(files['[Content_Types].xml']);et=E.fromstring(extra.read('[Content_Types].xml'));ov={x.get('PartName'):x.get('ContentType') for x in et if x.tag.endswith('Override')};defaults={x.get('Extension') for x in types if x.tag.endswith('Default')}
def override(new,old):E.SubElement(types,'{'+CT+'}Override',PartName='/'+new,ContentType=ov['/'+old])
def media(old):
 raw=extra.read(old)
 for name,data in files.items():
  if name.startswith('ppt/media/') and sha(data)==sha(raw):return name
 new='ppt/media/lesson-'+PurePosixPath(old).name;assert new not in files or files[new]==raw
 files[new]=raw;ext=PurePosixPath(new).suffix[1:]
 if ext not in defaults:
  typ=next(x.get('ContentType') for x in et if x.tag.endswith('Default') and x.get('Extension')==ext);E.SubElement(types,'{'+CT+'}Default',Extension=ext,ContentType=typ);defaults.add(ext)
 return new
pres=E.fromstring(files['ppt/presentation.xml']);ids=pres.find('p:sldIdLst',NS);old_ids=list(ids);pr=E.fromstring(files['ppt/_rels/presentation.xml.rels']);maxid=max(int(x.get('id')) for x in ids);newids={};newparts={}
for i,row in enumerate(json.loads((B/'additions.json').read_text()),1):
 old=ep[row['export_slide']-1];new=f'ppt/slides/fundamentals-{row["key"]}.xml';files[new]=extra.read(old);override(new,old)
 template=bp[row['template']-1];br=E.fromstring(base.read(relpart(template)));layout=next(target(template,x.get('Target')) for x in br if x.get('Type').endswith('/slideLayout'))
 bn=next(target(template,x.get('Target')) for x in br if x.get('Type').endswith('/notesSlide'));nr=E.fromstring(base.read(relpart(bn)));master=next(target(bn,x.get('Target')) for x in nr if x.get('Type').endswith('/notesMaster'))
 rs=E.fromstring(extra.read(relpart(old)))
 for rel in rs:
  if rel.get('TargetMode')=='External':continue
  t=target(old,rel.get('Target'));kind=rel.get('Type').rsplit('/',1)[-1]
  if kind=='slideLayout':dest=layout
  elif kind=='image':dest=media(t)
  elif kind=='notesSlide':
   dest=f'ppt/notesSlides/fundamentals-{row["key"]}.xml';files[dest]=extra.read(t);override(dest,t);nrs=E.fromstring(extra.read(relpart(t)))
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
 files[relpart(new)]=xml(rs);rid='rIdFundamentals'+str(i);E.SubElement(pr,'{'+PKG+'}Relationship',Id=rid,Type=REL+'/slide',Target='/'+new);newids[row['key']]=E.Element('{'+P+'}sldId',{'id':str(maxid+i),'{'+REL+'}id':rid});newparts[row['key']]=new
sequence=[1,2,3,'definition','formats','properties','entrances','reveals','timing','vocabulary-prompt',5,6,7,8,9,10,11,12,13,14,15]
for x in list(ids):ids.remove(x)
for key in sequence:ids.append(old_ids[key-1] if isinstance(key,int) else newids[key])
files['ppt/presentation.xml']=xml(pres);files['ppt/_rels/presentation.xml.rels']=xml(pr);files['[Content_Types].xml']=xml(types)
if 'docProps/app.xml' in files:files['docProps/app.xml']=re.sub(rb'(<Slides>)15(</Slides>)',rb'\g<1>21\2',files['docProps/app.xml'])
geometry=[]
for index in [1,2,3,5,6,7,8,9,10,11,12,13,14,15]:
 part=bp[index-1];a=E.fromstring(original[part]);b=E.fromstring(files[part])
 for tree in [a,b]:
  for x in tree.findall('.//p:txBody',NS):x.getparent().remove(x)
 same=E.tostring(a,method='c14n')==E.tostring(b,method='c14n');assert same,part
 geometry.append({'source_display_page':index,'target_page':sequence.index(index)+1,'non_text_xml_identical':same,'whole_slide_identical':files[part]==original[part]})
for name,data in original.items():
 if name.startswith(('ppt/media/','ppt/slideMasters/','ppt/slideLayouts/','ppt/theme/')):assert files[name]==data
with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as z:
 for name,data in files.items():z.writestr(name,data)
(B/'preservation.json').write_text(json.dumps({'source_sha256':sha(SRC.read_bytes()),'sequence':sequence,'source_slide_geometry':geometry,'all_original_media_masters_layouts_themes_identical':True,'new_slide_parts':newparts},ensure_ascii=False,indent=2),encoding='utf-8')
print('Assembled 21 slides. Retained slide geometries and all source media/masters/themes preserved.')
