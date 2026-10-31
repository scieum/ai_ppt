from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json,posixpath,hashlib
B=Path(__file__).resolve().parent;R=B.parent.parent
A=R/'units/AI-001_모션그래픽수업영상_무료웨비나/assets/motion-audio-20261030'
SOURCE=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_결론텍스트바_43장_v32.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
PK='http://schemas.openxmlformats.org/package/2006/relationships';CT='http://schemas.openxmlformats.org/package/2006/content-types'
def xml(e):return E.tostring(e,encoding='utf-8',xml_declaration=True,standalone=True)
def target(p,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def ordered(z):
 rs={x.get('Id'):x.get('Target')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 return [target('ppt/presentation.xml',rs[x.get('{'+N['r']+'}id')])for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
def name(el):
 c=el.find('.//p:cNvPr',N);return c.get('name','')if c is not None else ''
def settext(root,key,value):
 sh=next(s for s in root.findall('p:cSld/p:spTree/p:sp',N)if name(s)==key)
 ts=sh.findall('.//a:t',N);ts[0].text=value
 for t in ts[1:]:t.text=''
def appendnote(data,part,value):
 rs=E.fromstring(data[rel(part)]);nr=next(x for x in rs if x.get('Type').endswith('/notesSlide'));np=target(part,nr.get('Target'));note=E.fromstring(data[np])
 body=next(s.find('p:txBody',N)for s in note.findall('.//p:sp',N)if s.find('p:nvSpPr/p:nvPr/p:ph',N)is not None and s.find('p:nvSpPr/p:nvPr/p:ph',N).get('type')=='body')
 para=E.SubElement(body,'{'+N['a']+'}p');run=E.SubElement(para,'{'+N['a']+'}r');E.SubElement(run,'{'+N['a']+'}t').text=value;data[np]=xml(note)

spec=json.loads((B/'spec.json').read_text(encoding='utf8'))
with ZipFile(SOURCE)as z,ZipFile(B/'additions.pptx')as authored,ZipFile(B/'video-objects.pptx')as vz:
 data={n:z.read(n)for n in z.namelist()};old=ordered(z);auth=ordered(authored)
 prs=E.fromstring(data['ppt/presentation.xml']);lst=prs.find('p:sldIdLst',N);oldids=[deepcopy(x)for x in lst]
 prsrels=E.fromstring(data['ppt/_rels/presentation.xml.rels']);types=E.fromstring(data['[Content_Types].xml'])
 def content_type(ext,ctype):
  if not any(x.get('Extension')==ext for x in types):E.SubElement(types,'{'+CT+'}Default',Extension=ext,ContentType=ctype)
 for e,c in [('gif','image/gif'),('png','image/png'),('mp4','video/mp4')]:content_type(e,c)
 def override(part,ctype):E.SubElement(types,'{'+CT+'}Override',PartName='/'+part,ContentType=ctype)
 def mediafile(file):
  dst='ppt/media/ma33-'+file.name;data[dst]=file.read_bytes();return dst
 # Consolidate repeated concepts in the original effect slides, retaining their layouts.
 root=E.fromstring(data[old[12]])
 settext(root,'reveal-name-0','마스크 리빌');settext(root,'reveal-en-0','Mask reveal');settext(root,'reveal-name-2','순차 등장 / 스태거')
 data[old[12]]=xml(root)
 appendnote(data,old[12],'추가 설명: 마스크 리빌은 가림 영역이 열리는 표현이고, 스태거는 여러 요소가 시간차를 두고 시작하는 방식입니다. 같은 효과의 별도 장표는 추가하지 않았습니다. 출처: 사용자 제공 @mynameisjaemin 캡처, 2026-10-30.')
 root=E.fromstring(data[old[13]]);rs=E.fromstring(data[rel(old[13])])
 settext(root,'effect-name-1','입체 회전 / 카드 플립');settext(root,'effect-en-1','3D rotation / Card flip');settext(root,'effect-desc-1','180° 회전하며 앞뒷면이 바뀜')
 for nm,filename in [('video7-rotation','flip.gif'),('video7-rotation-state-0','flip-start.png'),('video7-rotation-state-1','flip-middle.png'),('video7-rotation-state-2','flip-end.png')]:
  pic=next(s for s in root.findall('.//p:pic',N)if name(s)==nm);blip=pic.find('p:blipFill/a:blip',N);rid=blip.get('{'+N['r']+'}embed');relation=next(r for r in rs if r.get('Id')==rid);relation.set('Target','/'+mediafile(A/filename))
 data[old[13]]=xml(root);data[rel(old[13])]=xml(rs)
 appendnote(data,old[13],'입체 회전의 구체적인 예시로 질문 카드가 180도 회전해 답으로 바뀌는 자체 제작 GIF를 넣었습니다. 360도는 처음 면으로 돌아옵니다. 모핑은 기존 예시와 묶었습니다. 출처: 사용자 제공 @mynameisjaemin 캡처, 2026-10-30.')
 additions={};mapping=[];sidmax=max(int(x.get('id'))for x in oldids)
 for idx,d in enumerate(spec):
  base=old[d['base']-1];dst=f'ppt/slides/ma33-{d["id"]}.xml';root=E.fromstring(z.read(base));tree=root.find('p:cSld/p:spTree',N)
  keep={'part_label','section_number','section_heading','title','subtitle','copyright_footer','clear-content'}
  for el in list(tree):
   if el.tag.endswith('nvGrpSpPr')or el.tag.endswith('grpSpPr'):continue
   if name(el)in keep:continue
   if el.tag.endswith('pic')and name(el)=='':continue # Existing brand logo.
   tree.remove(el)
  for t in root.findall('p:timing',N)+root.findall('p:transition',N):root.remove(t)
  settext(root,'title',d['title']);settext(root,'subtitle',d['subtitle'])
  rs=E.fromstring(z.read(rel(base)));counter=max(int(x)for x in root.xpath('//p:cNvPr/@id',namespaces=N))+1
  # Duplicate speaker notes without sharing mutable notes with the original slide.
  anote=next(r for r in E.fromstring(authored.read(rel(auth[idx])))if r.get('Type').endswith('/notesSlide'))
  np=f'ppt/notesSlides/ma33-{d["id"]}.xml';data[np]=authored.read(target(auth[idx],anote.get('Target')))
  oldnr=next(r for r in rs if r.get('Type').endswith('/notesSlide'));oldnp=target(base,oldnr.get('Target'));oldnr.set('Target','/'+np)
  nrs=E.fromstring(z.read(rel(oldnp)))
  for nr in nrs:
   if nr.get('Type').endswith('/slide'):nr.set('Target','/'+dst)
   else:nr.set('Target','/'+target(oldnp,nr.get('Target')))
  data[rel(np)]=xml(nrs);override(np,'application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml')
  def import_shapes(package,part,elements,prefix):
   nonlocal_dummy=None
   global_r={r.get('Id'):r for r in E.fromstring(package.read(rel(part)))};copied={}
   result=[]
   for el in elements:
    el=deepcopy(el)
    for node in el.iter():
     for attr,val in list(node.attrib.items()):
      if attr.startswith('{'+N['r']+'}')and not val:
       del node.attrib[attr] # Optional empty r:id on PowerPoint's media action.
       continue
      if attr.startswith('{'+N['r']+'}')and val:
       if val not in copied:
        rr=deepcopy(global_r[val]);newrid=prefix+val;rr.set('Id',newrid)
        if rr.get('TargetMode')!='External':
         src=target(part,rr.get('Target'));ext=Path(src).suffix;mdst='ppt/media/'+prefix+Path(src).name;data[mdst]=package.read(src);rr.set('Target','/'+mdst)
         if ext.lower()=='.emf':content_type('emf','image/x-emf')
         if ext.lower()=='.wdp':content_type('wdp','image/vnd.ms-photo')
        rs.append(rr);copied[val]=newrid
       node.set(attr,copied[val])
    result.append(el)
   return result
  body=E.fromstring(authored.read(auth[idx])).find('p:cSld/p:spTree',N)
  image_names={0:['motion-snap','motion-blur'],1:['motion-counter','motion-squash'],2:['video-placeholder-silent','video-placeholder-with-sound'],4:['original-bear-character']}
  for image_el,image_name in zip(body.findall('p:pic',N),image_names.get(idx,[])):
   image_el.find('p:nvPicPr/p:cNvPr',N).set('name',image_name)
  els=[el for el in body if not el.tag.endswith('nvGrpSpPr')and not el.tag.endswith('grpSpPr')and not name(el).startswith('video-placeholder-')]
  for el in import_shapes(authored,auth[idx],els,'rMA'+str(idx)):
   for nv in el.findall('.//p:cNvPr',N):nv.set('id',str(counter));counter+=1
   if name(el).startswith('motion-'):
    kind=name(el).removeprefix('motion-');blip=el.find('p:blipFill/a:blip',N);rid=blip.get('{'+N['r']+'}embed');next(r for r in rs if r.get('Id')==rid).set('Target','/'+mediafile(A/(kind+'.gif')))
   tree.append(el)
  if d['id']=='sound-compare':
   vp=ordered(vz)[0];vr=E.fromstring(vz.read(vp));vids=vr.findall('p:cSld/p:spTree/p:pic',N)
   idmap={}
   for el in import_shapes(vz,vp,vids,'rMAVideo'):
    for nv in el.findall('.//p:cNvPr',N):idmap[nv.get('id')]=str(counter);nv.set('id',str(counter));counter+=1
    tree.append(el)
   timing=vr.find('p:timing',N)
   if timing is not None:
    timing=deepcopy(timing)
    for el in timing.iter():
     if el.get('spid')in idmap:el.set('spid',idmap[el.get('spid')])
    root.append(timing)
  data[dst]=xml(root);data[rel(dst)]=xml(rs);override(dst,'application/vnd.openxmlformats-officedocument.presentationml.slide+xml')
  prid='rMA33Slide'+str(idx);E.SubElement(prsrels,'{'+PK+'}Relationship',Id=prid,Type=N['r']+'/slide',Target='/'+dst)
  si=E.Element('{'+N['p']+'}sldId',id=str(sidmax+idx+1));si.set('{'+N['r']+'}id',prid);additions.setdefault(d['after'],[]).append((si,dst,d))
 for el in list(lst):lst.remove(el)
 for i,oldid in enumerate(oldids,1):
  lst.append(oldid);mapping.append({'page':len(mapping)+1,'kind':'modified'if i in[13,14]else'preserved','original_page':i,'part':old[i-1]})
  for si,dst,d in additions.get(i,[]):lst.append(si);mapping.append({'page':len(mapping)+1,'kind':'new','id':d['id'],'title':d['title'],'part':dst})
 assert len(mapping)==48
 data['ppt/presentation.xml']=xml(prs);data['ppt/_rels/presentation.xml.rels']=xml(prsrels);data['[Content_Types].xml']=xml(types)
 app=E.fromstring(data['docProps/app.xml']);app.find('{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Slides').text='48';data['docProps/app.xml']=xml(app)
 assert all(data[old[i-1]]==z.read(old[i-1])for i in range(1,44)if i not in[13,14])
 assert all(data[n]==z.read(n)for n in z.namelist()if n.startswith('ppt/media/'))
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED)as out:
  for n,v in data.items():out.writestr(n,v)
 (B/'slide-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf8')
print('48 slides assembled: 41 preserved, 2 consolidated, 5 new. Original media retained.')
