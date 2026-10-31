from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json,posixpath
B=Path(__file__).resolve().parent;R=B.parent.parent
old='NotionTalk_모션그래픽_준비물안내박스_43장_v30';new='NotionTalk_모션그래픽_논리구조에셋반영_43장_v31'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
spec=json.loads((B/'spec.json').read_text(encoding='utf8'));parts=json.loads((R/'output/typography-qa-build/spec.json').read_text(encoding='utf8'))['parts']
def xml(e):return E.tostring(e,encoding='UTF-8',xml_declaration=True,standalone=True)
def nv(e):return e.find('.//p:cNvPr',N)
def frame(el):return el.find('p:spPr/a:xfrm',N)
def shift(el,dx,dy):
 f=frame(el);off=f.find('a:off',N)
 for k,d in [('x',dx),('y',dy)]:off.set(k,str(int(off.get(k))+round(d*9525)))
def character(el,x,y,h,center=False):
 f=frame(el);off=f.find('a:off',N);ext=f.find('a:ext',N);w=h*int(ext.get('cx'))/int(ext.get('cy'))
 if center:x-=w/2
 off.set('x',str(round(x*9525)));off.set('y',str(round(y*9525)));ext.set('cx',str(round(w*9525)));ext.set('cy',str(round(h*9525)))
with ZipFile(R/f'output/webinar-knowledge-only/{old}.pptx') as z,ZipFile(B/'bodies.pptx') as a:
 data={n:z.read(n) for n in z.namelist()}
 for index,d in enumerate(spec,1):
  part=parts[d['page']-1];root=E.fromstring(data[part]);tree=root.find('p:cSld/p:spTree',N)
  body=E.fromstring(a.read(f'ppt/slides/slide{index}.xml')).find('p:cSld/p:spTree',N)
  keepnames={'part_label','part-label','section_number','group-number','section_heading','group-label','title','slide-title','subtitle','slide-subtitle','copyright_footer','copyright-footer','clear-content'}
  overlay=[]
  for el in list(tree):
   info=nv(el)
   if info is None or el.tag.endswith('nvGrpSpPr') or el.tag.endswith('grpSpPr'):continue
   name=info.get('name','')
   if name in keepnames:continue
   ispic=el.tag.endswith('pic')
   if ispic and name=='':
    if d['page']==36 and info.get('id')=='17':tree.remove(el);shift(el,27.5,18);overlay.append(el)
    else:continue # original main brand image
   elif ispic:
    tree.remove(el)
    if d['page']==20:character(el,640,315,120,True)
    elif d['page']==37:character(el,100,407,210)
    elif d['page']==40:character(el,135,374,230)
    overlay.append(el)
   elif d['page']==36 and name in {'still-sample-frame','still-sample-top','still-sample-title'}:
    tree.remove(el);shift(el,27.5,18);overlay.append(el)
   else:tree.remove(el)
  counter=100
  for el in body:
   if el.tag.endswith('nvGrpSpPr') or el.tag.endswith('grpSpPr'):continue
   el=deepcopy(el)
   for c in el.findall('.//p:cNvPr',N):
    c.set('id','21' if d['page']==20 and c.get('name')=='motion-branch-title' else str(counter));counter+=1
   tree.append(el)
  for el in overlay:tree.append(el)
  data[part]=xml(root);d['package_part']=part
  # Preserve notes, append actual design source attribution and revised review emphasis.
  relpart=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
  rels=E.fromstring(data[relpart]);note_rel=next(r for r in rels if r.get('Type').endswith('/notesSlide'));t=note_rel.get('Target');np=t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part),t))
  note=E.fromstring(data[np]);tb=next(s.find('p:txBody',N) for s in note.findall('.//p:sp',N) if s.find('p:nvSpPr/p:nvPr/p:ph',N)is not None and s.find('p:nvSpPr/p:nvPr/p:ph',N).get('type')=='body')
  para=E.SubElement(tb,'{'+N['a']+'}p');run=E.SubElement(para,'{'+N['a']+'}r');txt=E.SubElement(run,'{'+N['a']+'}t')
  txt.text='구성 참고: 사용자 제공 「기획부터 디자인까지 쭉! AI 디자인 하네스 만들기」 캡처, '+', '.join(d['refs'])+'. '+d['pattern']+' 구조를 노션톡 모션그래픽 웨비나 내용으로 재구성. 원본 문구·펭귄·로고·스크린샷은 장표에 사용하지 않음.'
  data[np]=xml(note);d['notes_part']=np
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as zz:
  for n,b in data.items():zz.writestr(n,b)
 assert all(data[n]==z.read(n) for n in z.namelist() if n.startswith('ppt/media/'))
(B/'spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf8')
f=(R/'output/prep-label-spacing-build/finalize.mjs').read_text(encoding='utf8').replace('NotionTalk_모션그래픽_폰트간격점검_43장_v29',old).replace(f'/{old}.pptx\'),pythonExecutable',f'/{new}.pptx\'),pythonExecutable').replace('[22,25,33,34]','[22,25,33,34,37]')
(B/'finalize.mjs').write_text(f,encoding='utf8')
ex=(R/'output/prep-label-spacing-build/export.ps1').read_text(encoding='utf-8-sig').replace('output/prep-label-spacing-build','output/reference-logic-build').replace(old,new).replace('renders/prep-label-spacing-20261030','renders/reference-logic-20261030')
(B/'export.ps1').write_text(ex,encoding='utf-8-sig')
print('Replaced five bodies; all headers, 38 other slides, original media and timing preserved.')
