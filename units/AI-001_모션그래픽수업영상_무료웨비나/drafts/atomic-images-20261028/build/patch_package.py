from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
import posixpath, json, hashlib

B=Path(__file__).resolve().parent
U=B.parents[2]
ROOT=U.parents[1]
A=ROOT/'assets/atomic-models/20261028'
SOURCE=ROOT/'output/webinar-cleanup/NotionTalk_검토장표삭제_21장_v1.pptx'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
PR='http://schemas.openxmlformats.org/package/2006/relationships'
def relpart(p): return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
def target(p,t): return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def at(z,n):
    ids=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',NS)
    rid=ids[n-1].get('{'+NS['r']+'}id')
    rs=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
    return target('ppt/presentation.xml',next(x.get('Target') for x in rs if x.get('Id')==rid))
def raw(e): return E.tostring(e,encoding='UTF-8',xml_declaration=True,standalone=True)
def name(n):
    p=n.find('.//p:cNvPr',NS)
    return p.get('name','') if p is not None else ''
def digest(b): return hashlib.sha256(b).hexdigest()
with ZipFile(SOURCE) as base, ZipFile(B/'edited-roundtrip.pptx') as extra:
    files={n:base.read(n) for n in base.namelist()}
    before=files.copy()
    part=at(base,17); ep=at(extra,17)
    slide=E.fromstring(files[part]); st=slide.find('p:cSld/p:spTree',NS)
    es=E.fromstring(extra.read(ep)).find('p:cSld/p:spTree',NS)
    old={'thomson-positive','thomson-electron','orbit','nucleus','electron'}
    labels={'model-label-'+str(i) for i in range(3)}
    removed=[]
    for n in list(st):
        if name(n) in old|labels:
            removed.append(name(n)); st.remove(n)
    assert len(removed)==14,removed
    pics=[n for n in es.findall('p:pic',NS) if int(n.find('p:spPr/a:xfrm/a:ext',NS).get('cx'))<10000000]
    pics.sort(key=lambda n:int(n.find('p:spPr/a:xfrm/a:off',NS).get('x')))
    assert len(pics)==3,len(pics)
    newlabels=[n for n in es.findall('p:sp',NS) if name(n) in labels|{'atomic-model-caption'}]
    assert len(newlabels)==4
    rs=E.fromstring(files[relpart(part)])
    nxt=max(int(n.get('id')) for n in st.findall('.//p:cNvPr',NS))+1
    for i,(key,pic) in enumerate(zip(['thomson','rutherford','bohr'],pics),1):
        pic=deepcopy(pic);rid='rIdAtomic'+str(i)
        assert not any(r.get('Id')==rid for r in rs)
        cp=pic.find('.//p:cNvPr',NS);cp.set('name','generated-atomic-'+key);cp.set('descr',key+' historical atomic model, generated conceptual illustration. Electron count and scale simplified.')
        cp.set('id',str(nxt));nxt+=1
        pic.find('.//a:blip',NS).set('{'+NS['r']+'}embed',rid)
        media='ppt/media/atomic-'+key+'.png'
        assert media not in files
        files[media]=(A/(key+'.png')).read_bytes()
        E.SubElement(rs,'{'+PR+'}Relationship',Id=rid,Type=NS['r']+'/image',Target='/'+media)
        st.append(pic)
    for n in newlabels:
        n=deepcopy(n);n.find('.//p:cNvPr',NS).set('id',str(nxt));nxt+=1;st.append(n)
    files[part]=raw(slide);files[relpart(part)]=raw(rs)
    note=target(part,next(r.get('Target') for r in rs if r.get('Type').endswith('/notesSlide')))
    nt=E.fromstring(files[note]);body=None
    for sp in nt.findall('.//p:sp',NS):
        ph=sp.find('.//p:ph',NS)
        if ph is not None and ph.get('type')=='body': body=sp.find('p:txBody',NS);break
    assert body is not None
    para=E.SubElement(body,'{'+NS['a']+'}p');run=E.SubElement(para,'{'+NS['a']+'}r');E.SubElement(run,'{'+NS['a']+'}t').text='2026-10-28 이미지 개정: 톰슨·러더퍼드·보어 세 삽화는 image_gen으로 새로 생성했다. 실제 원자의 사진이 아닌 역사적 모형의 개념 모식도이며 전자 수와 크기 비율은 단순화했다. 러더퍼드의 경로선은 설명용이고 보어의 두 반지름은 허용 궤도의 구분을 나타낸다. 과학 설명 확인: AIP https://history.aip.org/exhibits/electron/jjelectr.htm 및 https://history.aip.org/exhibits/rutherford/sections/alpha-particles-atom.html, Nobel https://educationalgames.nobelprize.org/educational/physics/quantised_world/structure-2.html. 외부 자료의 그림을 복제하지 않았다. 이번 변경은 G10 승인이나 실제 영상 제작 완료를 뜻하지 않는다.'
    files[note]=raw(nt)
    changed=[n for n in before if files[n]!=before[n]]
    assert set(changed)=={part,relpart(part),note},changed
    for n,v in before.items():
        if n not in changed: assert files[n]==v,n
    with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as out:
        for n,v in files.items():out.writestr(n,v)
    (B/'preservation.json').write_text(json.dumps({'source_sha256':digest(SOURCE.read_bytes()),'display_slide':17,'changed_original_parts':changed,'added_media':[n for n in files if n not in before],'other_slide_parts_byte_identical':True,'slide_count':21},ensure_ascii=False,indent=2),encoding='utf8')
print('Updated only slide 17 atomic model illustrations, labels and note. All other source package parts preserved.')
