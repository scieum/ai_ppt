from pathlib import Path,PurePosixPath
import zipfile,xml.etree.ElementTree as ET,posixpath,json,hashlib
B=Path(__file__).resolve().parent;U=B.parents[2];ROOT=U.parents[1]
SOURCE=ROOT/'output/webinar-part01-added/NotionTalk_대표5장유지_Part0_Part1추가_9장_v1.pptx'
base=zipfile.ZipFile(SOURCE);extra=zipfile.ZipFile(B/'edited-roundtrip.pptx')
files={n:base.read(n) for n in base.namelist()};before=files.copy()
P='http://schemas.openxmlformats.org/presentationml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PR='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types'
def relpart(part):return posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
def target(part,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part),t))
def xml(e,ns):
 ET.register_namespace('',ns);return ET.tostring(e,encoding='utf-8',xml_declaration=True)
def slide_at(z,n):
 ids=ET.fromstring(z.read('ppt/presentation.xml')).find('{'+P+'}sldIdLst')
 rid=ids[n-1].get('{'+R+'}id');rels=ET.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
 return target('ppt/presentation.xml',next(x.get('Target') for x in rels if x.get('Id')==rid))
newpart=slide_at(base,3);oldpart=slide_at(extra,3)
oldbase=ET.fromstring(base.read(relpart(newpart)))
layout=next(target(newpart,r.get('Target')) for r in oldbase if r.get('Type').endswith('/slideLayout'))
note=next(target(newpart,r.get('Target')) for r in oldbase if r.get('Type').endswith('/notesSlide'))
note_rels=ET.fromstring(base.read(relpart(note)))
note_master=next(target(note,r.get('Target')) for r in note_rels if r.get('Type').endswith('/notesMaster'))
types=ET.fromstring(files['[Content_Types].xml']);exttypes=ET.fromstring(extra.read('[Content_Types].xml'))
defaults={x.get('Extension') for x in types if x.tag.endswith('Default')}
sha=lambda b:hashlib.sha256(b).hexdigest()
def media(part):
 data=extra.read(part)
 for name,v in files.items():
  if name.startswith('ppt/media/') and sha(v)==sha(data):return name
 name='ppt/media/prep-tools-'+PurePosixPath(part).name;files[name]=data
 ext=PurePosixPath(name).suffix[1:]
 if ext not in defaults:
  ct=next(x.get('ContentType') for x in exttypes if x.tag.endswith('Default') and x.get('Extension')==ext)
  ET.SubElement(types,'{'+CT+'}Default',Extension=ext,ContentType=ct);defaults.add(ext)
 return name
rels=ET.fromstring(extra.read(relpart(oldpart)));files[newpart]=extra.read(oldpart)
for rel in rels:
 if rel.get('TargetMode')=='External':continue
 t=target(oldpart,rel.get('Target'));kind=rel.get('Type').rsplit('/',1)[-1]
 if kind=='slideLayout':dest=layout
 elif kind=='image':dest=media(t)
 elif kind=='notesSlide':
  dest=note;files[note]=extra.read(t)
  nr=ET.fromstring(extra.read(relpart(t)))
  for r in nr:
   nk=r.get('Type').rsplit('/',1)[-1]
   if nk=='slide':r.set('Target','/'+newpart)
   elif nk=='notesMaster':r.set('Target','/'+note_master)
   else:raise ValueError(nk)
  files[relpart(note)]=xml(nr,PR)
 else:raise ValueError(kind)
 rel.set('Target','/'+dest)
files[relpart(newpart)]=xml(rels,PR)
if len(defaults)!=len([x for x in ET.fromstring(before['[Content_Types].xml']) if x.tag.endswith('Default')]):files['[Content_Types].xml']=xml(types,CT)
allowed={newpart,relpart(newpart),note,relpart(note),'[Content_Types].xml'}
for n,v in before.items():
 if n not in allowed:assert files[n]==v,n
with zipfile.ZipFile(B/'candidate.pptx','w',zipfile.ZIP_DEFLATED) as z:
 for n,v in files.items():z.writestr(n,v)
(B/'preservation.json').write_text(json.dumps({'edited_display_slide':3,'edited_part':newpart,'original_sha256':sha(SOURCE.read_bytes()),'unchanged_other_slides':8,'allowed_changed_parts':sorted(allowed)},indent=2),encoding='utf-8')
print('Patched only preparation slide and its notes; all other 8 slides preserved.')
