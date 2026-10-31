from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json, hashlib, posixpath
import fitz

B=Path(__file__).resolve().parent; U=B.parents[2]; R=U.parents[1]
D=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_10장_v2.pptx'
S=R/'output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
rid='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
def ordered(z):
    rel={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
    return [posixpath.normpath('ppt/'+rel[x.get(rid)]) if not rel[x.get(rid)].startswith('/') else rel[x.get(rid)].lstrip('/') for x in E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N)]
spec=json.loads((B/'content.json').read_text(encoding='utf8'))
out={}
with ZipFile(D) as z, ZipFile(S) as src:
    parts=ordered(z); old=ordered(src)
    assert len(parts)==10
    trees=[E.fromstring(z.read(p)) for p in parts]
    text=['\n'.join(t.itertext()) for tree in trees for t in tree.findall('.//a:t',N)]
    visible='\n'.join(text)
    forbidden=['프롬프트','고려해야','장면표','커넥터','원자모형','레퍼런스 분석','완료 기준','제작 실습','실습하기']
    assert not any(t in visible for t in forbidden)
    anim=[]
    for i,tree in enumerate(trees):
        timing=tree.find('p:timing',N)
        if timing is not None:
            orig=E.fromstring(src.read(old[spec[i]['source_page']-1])).find('p:timing',N)
            assert E.tostring(timing)==E.tostring(orig)
            anim.append(i+1)
    assert anim==[3,6,7,8,9]
    assert trees[9].find('.//a:tbl',N) is not None
    for i in [6,7]:
        names=[x.get('name','') for x in trees[i].findall('.//p:cNvPr',N)]
        assert not any(n.startswith(('dev-effect-use-','dev-reveal-use-')) for n in names)
    media=[p for p in z.namelist() if p.startswith('ppt/media/')]
    assert all(p in src.namelist() and z.read(p)==src.read(p) for p in media)
    notes=[p for p in z.namelist() if p.startswith('ppt/notesSlides/') and p.endswith('.xml')]
    assert len(notes)==10
    note_text='\n'.join(''.join(E.fromstring(z.read(p)).itertext()) for p in notes)
    assert not any(t in note_text for t in forbidden)
    out.update(slides=10,notes=10,native_animation_pages=anim,native_animation_xml_preserved=True,native_table_pages=[10],source_media_bytes_preserved=True,media_count=len(media),removed_production_and_advice_content=True)
with fitz.open(D.with_suffix('.pdf')) as pdf:
    assert len(pdf)==10
    out['pdf_pages']=len(pdf)
bounds=json.loads((U/'renders/knowledge-only-20261028/text-bounds.json').read_text(encoding='utf-8-sig'))
overflow=[]
for b in bounds:
    if b['name'] in ['copyright_footer','section_number']:continue
    if b['text_width']>b['shape_width']+1 or b['text_height']>b['shape_height']+1:
        overflow.append(b)
assert not overflow, overflow
out['body_text_overflow_count']=0
assert len(list((U/'renders/knowledge-only-20261028').glob('slide-*.png')))==10
out['all_slides_native_rendered']=True
h=hashlib.sha256(D.read_bytes()).hexdigest()
assert h==json.loads((B/'validation-v2.json').read_text(encoding='utf8'))['finalSha256']
out['pptx_sha256']=h
oldreport=json.loads((U/'checks/lesson-only-20261028/verification.json').read_text(encoding='utf8'))
lessonhash=hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest()
assert lessonhash==oldreport['source_lesson_sha256']
out['lesson_unchanged']=True
out['g10_status']='unchanged; existing asset rights inventory remains pending'
P=U/'checks/knowledge-only-20261028/verification.json';P.parent.mkdir(parents=True,exist_ok=True)
P.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
