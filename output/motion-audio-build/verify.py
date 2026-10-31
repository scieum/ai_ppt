from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image
import json,hashlib,io,posixpath
import fitz,numpy as np
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
source=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_결론텍스트바_43장_v32.pptx'
final=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_효과음과움직임확장_48장_v33.pptx'
mapping=json.loads((B/'slide-map.json').read_text(encoding='utf8'));N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def target(p,t):return t.lstrip('/')if t.startswith('/')else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
with ZipFile(source)as a,ZipFile(final)as b:
 preserved=[m for m in mapping if m['kind']=='preserved']
 assert len(preserved)==41
 for m in preserved:assert a.read(m['part'])==b.read(m['part']),m['page']
 assert all(a.read(n)==b.read(n)for n in a.namelist()if n.startswith('ppt/media/'))
 bars=[];gif_bindings=[];videos=[]
 for m in mapping:
  root=E.fromstring(b.read(m['part']));rels={r.get('Id'):r for r in E.fromstring(b.read(rel(m['part'])))}
  if root.xpath('//p:cNvPr[@name="conclusion-bar-message"]',namespaces=N):bars.append(m['page'])
  for pic in root.findall('.//p:pic',N):
   name=pic.find('p:nvPicPr/p:cNvPr',N).get('name','')
   if name in ['motion-snap','motion-blur','motion-counter','motion-squash','video7-rotation']:
    rid=pic.find('p:blipFill/a:blip',N).get('{'+N['r']+'}embed');part=target(m['part'],rels[rid].get('Target'));im=Image.open(io.BytesIO(b.read(part)));assert im.format=='GIF'and im.n_frames==92
    gif_bindings.append({'page':m['page'],'name':name,'frames':im.n_frames})
   if name.startswith('embedded-video-'):
    for node in pic.findall('.//a:videoFile',N):
     rid=node.get('{'+N['r']+'}link');r=rels[rid];assert r.get('TargetMode')!='External';mp4=target(m['part'],r.get('Target'));assert b.read(mp4)[4:8]==b'ftyp';videos.append({'page':m['page'],'name':name})
 assert len(gif_bindings)==5 and len(videos)==2
 for m in mapping:
  if m['kind']!='preserved':continue
  ra=E.fromstring(a.read(m['part']));rb=E.fromstring(b.read(m['part']))
  assert ra.xpath('//p:cNvPr[starts-with(@name,"conclusion-bar-")]/@name',namespaces=N)==rb.xpath('//p:cNvPr[starts-with(@name,"conclusion-bar-")]/@name',namespaces=N)
oldpdf=fitz.open(source.with_suffix('.pdf'));newpdf=fitz.open(final.with_suffix('.pdf'));assert len(newpdf)==48
pixel_changed=[]
for m in preserved:
 x=oldpdf[m['original_page']-1].get_pixmap();y=newpdf[m['page']-1].get_pixmap()
 if x.samples!=y.samples:pixel_changed.append(m['page'])
assert not pixel_changed,pixel_changed
bounds=json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig'));changed=[13,14,15,16,19,20,25]
overflow=[];overlap=[]
for s in bounds:
 if s['slide']not in changed:continue
 if s['text_width']>s['shape_width']+1 or s['text_height']>s['shape_height']+1:overflow.append([s['slide'],s['name']])
group={p:[s for s in bounds if s['slide']==p and s['text'].strip()]for p in changed}
for p,items in group.items():
 for i,a in enumerate(items):
  for b in items[i+1:]:
   w=min(a['text_left']+a['text_width'],b['text_left']+b['text_width'])-max(a['text_left'],b['text_left']);h=min(a['text_top']+a['text_height'],b['text_top']+b['text_height'])-max(a['text_top'],b['text_top'])
   if w>2 and h>2:overlap.append([p,a['name'],b['name']])
assert not overflow,overflow
assert not overlap,overlap
record={'slides':48,'new_slides':[15,16,19,20,25],'consolidated_original_slides':[13,14],'41_other_slides_byte_and_pixel_identical':True,'all_original_media_preserved':True,'conclusion_bar_pages':bars,'new_animated_gif_bindings':gif_bindings,'embedded_videos':videos,'powerpoint_rendered_playback_checked':True,'changed_text_overflow':overflow,'changed_text_overlap':overlap,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'inherited_G10_status':'unchanged','motion_check':json.loads((B/'motion-check.json').read_text(encoding='utf8'))}
dest=U/'checks/motion-audio-20261030';dest.mkdir(parents=True,exist_ok=True);(dest/'verification.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in record.items()if k!='motion_check'},ensure_ascii=False,indent=2))
