from pathlib import Path
import hashlib, json, re, shutil, sys, zipfile
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageStat
from pypdf import PdfReader

build=Path(__file__).resolve().parent
unit=build.parents[2]
repo=unit.parents[1]
sys.path.insert(0,str(repo/'harness'))
from gate import Engine, ppt_info
out=repo/'output/webinar-samples'
pptx=out/'NotionTalk_모션그래픽_원본에셋_대표5장.pptx'
pdf=pptx.with_suffix('.pdf')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((build/'validation-original-assets.json').read_text(encoding='utf-8'))
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
library=repo/'assets/reference-templates'
catalog=json.loads((library/'catalog.json').read_text(encoding='utf-8'))
inventory=json.loads((repo/'output/reference-analysis/inventory.json').read_text(encoding='utf-8'))
for source in inventory:
    assert sha(Path(source['path']))==source['sha256']

font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',22)
sheet=Image.new('RGB',(1960,5*590+50),'#EEEEEE')
draw=ImageDraw.Draw(sheet)
draw.text((20,10),'왼쪽: 실제 원본 PDF / 오른쪽: 원본 에셋을 사용한 수정본',font=font,fill='black')
patches=[(0,0,100,850),(240,510,320,770),(234,550,265,780),(505,600,522,665),(945,590,980,620)]
patch_results=[]
final_renders=unit/'renders/reference-v2/final'
final_renders.mkdir(exist_ok=True)
for i,t in enumerate(catalog['templates']):
    src=Image.open(library/t['source_preview']).convert('RGB')
    actual=Image.open(unit/f'renders/reference-v2/powerpoint/slide-{i+1:02}.png').convert('RGB')
    assert actual.size==(1920,1080)
    actual.save(final_renders/f'final-slide-{i+1:02}.png')
    # White logo pixels must actually be visible in the native render.
    logo=actual.crop((1480,68,1826,168))
    white_pixels=sum(1 for r,g,b in logo.getdata() if min(r,g,b)>220)
    assert white_pixels>2000,(i,white_pixels)
    diff=ImageChops.difference(src.crop(patches[i]),actual.crop(patches[i]))
    mean=max(ImageStat.Stat(diff).mean)
    assert mean<3,(i,mean)
    patch_results.append({'slide':i+1,'source_patch':patches[i],'mean_channel_difference_max':mean,'white_logo_pixels':white_pixels})
    y=50+i*590
    label=f'{i+1:02}  {t["source_id"]} PDF p.{t["source_page"]} / {t["id"]}'
    draw.text((20,y),label,font=font,fill='black')
    src.thumbnail((960,540),Image.Resampling.LANCZOS)
    actual.thumbnail((960,540),Image.Resampling.LANCZOS)
    sheet.paste(src,(10,y+35));sheet.paste(actual,(990,y+35))
    pair=Image.new('RGB',(1960,590),'#EEEEEE')
    d=ImageDraw.Draw(pair);d.text((15,5),'원본 PDF',font=font,fill='black');d.text((995,5),'수정본',font=font,fill='black')
    pair.paste(src,(10,40));pair.paste(actual,(990,40))
    pair.save(out/f'원본비교_{i+1:02}.jpg',quality=95)
sheet.save(out/'원본대조_대표5장.jpg',quality=95)
with zipfile.ZipFile(out/'원본구조_템플릿에셋.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in library.rglob('*'):
        if f.is_file() and '__pycache__' not in str(f):z.write(f,Path('reference-templates')/f.relative_to(library))
report={'scope':'Five representative slides corrected using source-extracted geometry. User approval not asserted.',
    'pptx_sha256':sha(pptx),'pdf_sha256':sha(pdf),'slide_count':5,'pdf_pages':5,
    'native_powerpoint_exported':True,'finalizer_receipt':'validation-original-assets.json',
    'reference_patches':patch_results,'source_protection':guard,
    'all_seven_source_pdf_hashes_unchanged':True,
    'editability':'New text editable; source backgrounds, shapes and selected logo are fixed assets.',
    'differences':['Topic text, supplied scene and selected brand replaced.',
        'Anonymous source Type3 font replaced with Pretendard.',
        'Footer added per user rule; Part capitalization follows existing user instruction.',
        'Prompt page section accent uses the R02 pink instead of the R05 green.'],
    'full_harness_approvals':'Not asserted; manual representative preview.'}
(unit/'checks/reference-assets-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 5 slides/PDF pages, native visible logos, footers, notes, preserved source patches and all original PDF hashes.')
print(json.dumps(patch_results))
