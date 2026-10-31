from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image, ImageDraw
import json, hashlib, posixpath, subprocess
import numpy as np
import fitz, imageio_ffmpeg

B=Path(__file__).resolve().parent; U=B.parents[2]; R=U.parents[1]
O=R/'output/webinar-knowledge-only'
F=O/'NotionTalk_모션그래픽_흐름정리_캐릭터_16장_v10.pptx'
S=O/'NotionTalk_모션그래픽_19장_영상핵심5장확장_v8.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
spec=json.loads((B/'edits.json').read_text(encoding='utf-8'))
report={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ordered(z):
    rels=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
    paths={x.get('Id'):posixpath.normpath(posixpath.join('ppt',x.get('Target'))) if not x.get('Target').startswith('/') else x.get('Target').lstrip('/') for x in rels}
    return [paths[x.get('{'+N['r']+'}id')] for x in E.fromstring(z.read('ppt/presentation.xml')).findall('p:sldIdLst/p:sldId',N)]
with ZipFile(F) as z,ZipFile(S) as s:
    final=ordered(z);source=ordered(s);assert len(final)==16
    timing=[];mascots=[];tables=[]
    for p,part in enumerate(final,1):
        x=E.fromstring(z.read(part));old=E.fromstring(s.read(source[spec[p-1]['source_page']-1]))
        for name,expected in spec[p-1]['edits'].items():
            candidates=[a for a in x.findall('.//p:sp',N) if a.find('p:nvSpPr/p:cNvPr',N).get('name')==name]
            assert len(candidates)==1,(p,name)
            actual='\n'.join(''.join(a.xpath('.//a:t/text()',namespaces=N)) for a in candidates[0].findall('p:txBody/a:p',N))
            assert actual==expected,(p,name,actual,expected)
        a=x.find('p:timing',N);b=old.find('p:timing',N)
        assert (E.tostring(a) if a is not None else None)==(E.tostring(b) if b is not None else None),(p,'timing changed')
        if a is not None:timing.append(p)
        names=x.xpath('.//p:pic/p:nvPicPr/p:cNvPr/@name',namespaces=N)
        if any(n.startswith('mascot-') for n in names):mascots.append(p)
        if x.findall('.//a:tbl',N):tables.append(p)
        assert 'NotionTalk' in ''.join(x.xpath('.//a:t/text()',namespaces=N)),p
    gifs={n:s.read(n) for n in s.namelist() if n.lower().endswith('.gif')}
    assert all(z.read(n)==v for n,v in gifs.items())
    media=[z.read(n) for n in z.namelist() if n.startswith('ppt/media/')]
    for path in (U/'assets/mascots-20261028').glob('*-guide-v1.png'):assert path.read_bytes() in media
    report.update(slides=16,source_order=[x['source_page'] for x in spec],all_literal_edits_verified=True,native_timing_preserved_pages=timing,original_gif_media_preserved=len(gifs),mascot_pages=mascots,native_table_pages=tables,brand_text_verified=True)
pdf=fitz.open(F.with_suffix('.pdf'));assert len(pdf)==16
render=U/'renders/reflow-mascots-20261028';assert len(list(render.glob('slide-*.png')))==16
bounds=json.loads((render/'text-bounds.json').read_text(encoding='utf-8-sig'))
issues=[];inherited=[]
for t in bounds:
    dx=t['text_left']+t['text_width']-t['shape_left']-t['shape_width'];dy=t['text_top']+t['text_height']-t['shape_top']-t['shape_height']
    if dx>2 or dy>2:
        v={'page':t['slide'],'shape':t['name'],'overflow_right_pt':round(dx,2),'overflow_bottom_pt':round(dy,2)}
        (inherited if t['name']=='copyright_footer' else issues).append(v)
assert not issues,issues
assert sha(F)==json.loads((B/'validation-v10.json').read_text())['finalSha256']
lesson=R/'lesson.md'; assert sha(lesson)=='845e711e86e7017598b9f98ff43760d1cc485d9becbf29c0c27cc477feedc471'
report.update(pdf_pages=len(pdf),all_slides_native_rendered=True,body_text_overflow=issues,inherited_footer_box_overflow=inherited,lesson_sha256=sha(lesson),final_sha256=sha(F),finalizer_pass=True)

ffmpeg=imageio_ffmpeg.get_ffmpeg_exe();video=B/'playback-reflow.mp4'
def frame(t,name):
    dest=B/(name+'.png')
    subprocess.run([ffmpeg,'-y','-loglevel','error','-ss',str(t),'-i',str(video),'-frames:v','1',str(dest)],check=True)
    return np.asarray(Image.open(dest).convert('RGB')).astype(int)
vqa=[]
for page,start in [(3,0),(5,4),(12,8)]:
    ta,tb=(start+.5,start+2.5) if page==5 else (start+.2,start+1.2)
    a=frame(ta,f'qa-{page}-a');b=frame(tb,f'qa-{page}-b')
    # Native video is 1280x720, the same geometry as the authoring deck.
    rect=(790,380,1120,600) if page!=5 else (735,375,1120,640)
    x1,y1,x2,y2=rect;delta=np.max(np.abs(a[y1:y2,x1:x2]-b[y1:y2,x1:x2]),axis=2)
    changed=int((delta>12).sum());vqa.append({'page':page,'times_seconds':[ta,tb],'changed_pixels':changed,'roi':rect})
report['native_video_sampling']=vqa
report['native_video_all_samples_changed']=all(x['changed_pixels']>100 for x in vqa)
assert report['native_video_all_samples_changed'],vqa
check=U/'checks/reflow-mascots-20261028';check.mkdir(parents=True,exist_ok=True)
(check/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

# Review contact sheet, not a deliverable or a change to user image assets.
sheet=Image.new('RGB',(1280,800),'#333333');draw=ImageDraw.Draw(sheet)
for k in range(16):
    im=Image.open(render/f'slide-{k+1:02}.png').convert('RGB');im.thumbnail((320,180))
    x=(k%4)*320;y=(k//4)*200;sheet.paste(im,(x,y));draw.text((x+6,y+182),str(k+1),fill='white')
sheet.save(B/'contact-sheet-final.jpg',quality=93)
print(json.dumps({k:v for k,v in report.items() if k not in ['inherited_footer_box_overflow']},ensure_ascii=False,indent=2))
