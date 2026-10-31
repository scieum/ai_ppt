from pathlib import Path
import hashlib,json,re,sys
from PIL import Image,ImageChops
from pypdf import PdfReader

build=Path(__file__).resolve().parent
unit=build.parents[2]
repo=unit.parents[1]
sys.path.insert(0,str(repo/'harness'))
from gate import Engine,ppt_info
out=repo/'output/webinar-samples'
pptx=out/'NotionTalk_모션그래픽_주황표지_대표5장_v3.pptx'
pdf=pptx.with_suffix('.pdf')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((build/'validation-orange-cover.json').read_text(encoding='utf-8'))
assert sha(pptx)==receipt['finalSha256']
slides=ppt_info(pptx)
assert len(slides)==5
footer='© 2026. NotionTalk. All rights reserved.'
assert all(footer in ''.join(s['texts']) for s in slides)
assert all('레이아웃 출처:' in s['notes'] for s in slides)
pages=PdfReader(pdf).pages
assert len(pages)==5
assert all(re.sub(r'\s+','',footer) in re.sub(r'\s+','',p.extract_text() or '') for p in pages)
guard=Engine(unit).check(['G07'])
assert guard['passed'],guard
unchanged=[]
for i in range(1,6):
    current=Image.open(unit/f'renders/orange-cover-v3/powerpoint/slide-{i:02}.png').convert('RGB')
    assert current.size==(1920,1080)
    assert current.crop((1480,68,1826,168)).getextrema()[0][1]>240
    if i>1:
        old=Image.open(unit/f'renders/reference-v2/powerpoint/slide-{i:02}.png').convert('RGB')
        assert ImageChops.difference(old,current).getbbox() is None,i
        unchanged.append(i)
    else:
        current.save(out/'주황표지_v3_미리보기.png')
        r,g,b=current.getpixel((100,100))
        assert r>g>b and g>b*2,(r,g,b)
asset=unit/'assets/cover-characters-orange-v3.png'
im=Image.open(asset)
assert im.mode=='RGBA' and im.getextrema()[3][0]==0
manifest={'kind':'generated illustration','tool':'built-in image_gen','file':asset.name,
    'sha256':sha(asset),'reference':'webinar-poster.png','reference_sha256':sha(unit/'assets/webinar-poster.png'),
    'prompt_file':'cover-characters-orange-v3.prompt.txt','alpha_preserved':True,
    'visual_review':'Three characters retain hairstyle, glasses, clothing colors and proportions; new collaboration poses and motion-video props.',
    'use':'Cover figure slot, preserve full aspect ratio. Orange gradient is editable native PowerPoint geometry.'}
(unit/'assets/cover-characters-orange-v3.manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
report={'scope':'User-requested first-slide image regeneration and orange gradient',
    'pptx_sha256':sha(pptx),'pdf_sha256':sha(pdf),'slides':5,'pdf_pages':5,
    'unchanged_native_render_slides':unchanged,'source_protection':guard,
    'native_powerpoint_opened':True,'transparency_preserved':True,
    'slide_1_gradient':'orange to black','full_course_approval':'not asserted'}
(unit/'checks/orange-cover-v3-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 5 slides/PDF pages; slides 2-5 pixel-identical to prior native renders; orange cover, logos, footers, alpha and protected originals verified.')
