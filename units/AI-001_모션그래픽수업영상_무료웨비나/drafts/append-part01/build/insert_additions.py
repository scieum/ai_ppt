"""Insert four Artifact Tool template duplicates into the untouched base package.

Existing slide XML, relationships, masters, media and notes stay byte-identical.
The four new slides reuse their corresponding existing layout and notes master.
"""
from pathlib import Path,PurePosixPath
import zipfile,posixpath,json,hashlib,re
import xml.etree.ElementTree as ET

B=Path(__file__).resolve().parent;U=B.parents[2];ROOT=U.parents[1]
SOURCE=ROOT/'output/webinar-samples/NotionTalk_모션그래픽_주황포인트_자체사례_v5.pptx'
PR='http://schemas.openxmlformats.org/package/2006/relationships'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
CT='http://schemas.openxmlformats.org/package/2006/content-types'
sha=lambda b:hashlib.sha256(b).hexdigest()
source_hash=sha(SOURCE.read_bytes())
base=zipfile.ZipFile(SOURCE);extra=zipfile.ZipFile(B/'roundtrip-with-additions.pptx')
files={n:base.read(n) for n in base.namelist()}
added={};mapping=json.loads((B/'additions.json').read_text())
types=ET.fromstring(files['[Content_Types].xml'])
extra_types=ET.fromstring(extra.read('[Content_Types].xml'))
defaults={e.get('Extension'):e.get('ContentType') for e in types if e.tag.endswith('Default')}
overrides={e.get('PartName'):e.get('ContentType') for e in extra_types if e.tag.endswith('Override')}
def target(part,value):return value.lstrip('/') if value.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part),value))
def relpart(part):return posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
def xml(root,default):
    ET.register_namespace('',default);ET.register_namespace('p',P);ET.register_namespace('r',R)
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)
def override(new,old):
    typ=overrides.get('/'+old)
    if typ:ET.SubElement(types,'{'+CT+'}Override',PartName='/'+new,ContentType=typ)
def image(old):
    data=extra.read(old)
    for name in files:
        if name.startswith('ppt/media/') and sha(files[name])==sha(data):return name
    new='ppt/media/part01-'+PurePosixPath(old).name
    if new in added and added[new]!=data:raise ValueError('Media collision')
    added[new]=data
    ext=PurePosixPath(new).suffix.lstrip('.')
    if ext not in defaults:
        typ=next(e.get('ContentType') for e in extra_types if e.tag.endswith('Default') and e.get('Extension')==ext)
        ET.SubElement(types,'{'+CT+'}Default',Extension=ext,ContentType=typ);defaults[ext]=typ
    return new

notes_master=next(n for n in files if re.fullmatch(r'ppt/notesMasters/notesMaster\d+\.xml',n))
new_ids=[];new_slide_names=[]
presentation=ET.fromstring(files['ppt/presentation.xml'])
slide_ids=presentation.find('{'+P+'}sldIdLst')
max_id=max(int(e.get('id')) for e in slide_ids)
presrels=ET.fromstring(files['ppt/_rels/presentation.xml.rels'])
for i,row in enumerate(mapping,1):
    old=f"ppt/slides/slide{row['export_slide']}.xml"
    new=f'ppt/slides/part01-slide{i}.xml'
    added[new]=extra.read(old);override(new,old)
    original=f"ppt/slides/slide{row['template_slide']}.xml"
    oldrels=ET.fromstring(base.read(relpart(original)))
    layout=next(target(original,e.get('Target')) for e in oldrels if e.get('Type').endswith('/slideLayout'))
    rels=ET.fromstring(extra.read(relpart(old)))
    for rel in rels:
        if rel.get('TargetMode')=='External':continue
        kind=rel.get('Type').rsplit('/',1)[-1];t=target(old,rel.get('Target'))
        if kind=='slideLayout':dest=layout
        elif kind=='image':dest=image(t)
        elif kind=='notesSlide':
            dest=f'ppt/notesSlides/part01-notes{i}.xml'
            added[dest]=extra.read(t);override(dest,t)
            notesrels=ET.fromstring(extra.read(relpart(t)))
            for nr in notesrels:
                nk=nr.get('Type').rsplit('/',1)[-1]
                if nk=='slide':nd=new
                elif nk=='notesMaster':nd=notes_master
                elif nk=='image':nd=image(target(t,nr.get('Target')))
                else:raise ValueError('Unexpected notes relationship '+nk)
                nr.set('Target','/'+nd)
            added[relpart(dest)]=xml(notesrels,PR)
        else:raise ValueError('Unexpected slide relationship '+kind)
        rel.set('Target','/'+dest)
    added[relpart(new)]=xml(rels,PR)
    rid=f'rIdPart01Add{i}'
    ET.SubElement(presrels,'{'+PR+'}Relationship',Id=rid,Type=R+'/slide',Target='/'+new)
    sid=ET.Element('{'+P+'}sldId',{'id':str(max_id+i),'{'+R+'}id':rid})
    slide_ids.insert(1+i,sid) # Existing cover + overview, then the four additions.
    new_slide_names.append(new)
files['ppt/presentation.xml']=xml(presentation,P)
files['ppt/_rels/presentation.xml.rels']=xml(presrels,PR)
files['[Content_Types].xml']=xml(types,CT)
if 'docProps/app.xml' in files:
    files['docProps/app.xml']=re.sub(rb'(<Slides>)5(</Slides>)',rb'\g<1>9\2',files['docProps/app.xml'])
for k,v in added.items():
    if k in files:raise ValueError('New part conflicts with original '+k)
    files[k]=v
candidate=B/'candidate.pptx'
with zipfile.ZipFile(candidate,'w',zipfile.ZIP_DEFLATED) as z:
    for n,data in files.items():z.writestr(n,data)
changed_allowed={'ppt/presentation.xml','ppt/_rels/presentation.xml.rels','[Content_Types].xml','docProps/app.xml'}
unchanged=[]
for name in base.namelist():
    if name not in changed_allowed:
        assert base.read(name)==files[name],name
        unchanged.append(name)
assert source_hash==sha(SOURCE.read_bytes())
report={'source':str(SOURCE),'source_sha256':source_hash,'original_parts_preserved_count':len(unchanged),'original_slides_unchanged':5,'new_slides':4,'total_slides':9,'existing_slide_final_positions':[1,2,7,8,9],'additions_final_positions':[3,4,5,6],'allowed_existing_part_updates':sorted(changed_allowed),'new_parts':list(added)}
(B/'preservation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Inserted 4 slides; preserved',len(unchanged),'original package parts byte-for-byte. Total 9 slides.')
