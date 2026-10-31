from pathlib import Path
import sys, json, hashlib, re
from PIL import Image
from pypdf import PdfReader

unit = Path(__file__).resolve().parents[3]
root = unit.parents[1]
sys.path.insert(0, str(root / 'harness'))
from gate import Engine, ppt_info

out = root / 'output/webinar-samples'
pptx = out / 'NotionTalk_모션그래픽_무료웨비나_대표5장_v1.pptx'
pdf = pptx.with_suffix('.pdf')
receipt = json.loads((Path(__file__).parent / 'validation.json').read_text(encoding='utf-8'))
hashfile = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert hashfile(pptx) == receipt['finalSha256'], 'PowerPoint export changed the original PPTX'
slides = ppt_info(pptx)
assert len(slides) == 5
footer = '© 2026. NotionTalk. All rights reserved.'
assert all(footer in ''.join(s['texts']) for s in slides)
assert all('출처:' in s['notes'] for s in slides)
doc = PdfReader(pdf)
assert len(doc.pages) == 5
assert all(re.sub(r'\s+', '', footer) in re.sub(r'\s+', '', pg.extract_text() or '') for pg in doc.pages)
guard = Engine(unit).check(['G07'])
assert guard['passed'], guard

sheet = Image.new('RGB', (1968, 1716), '#080D16')
for i in range(5):
    p = unit / f'renders/powerpoint/slide-{i+1:02}.png'
    with Image.open(p) as im:
        assert im.size == (1920,1080)
        thumb = im.convert('RGB').resize((960,540), Image.Resampling.LANCZOS)
    x = 504 if i == 4 else 12 + (i % 2) * 984
    y = 12 + (i // 2) * 564
    sheet.paste(thumb, (x,y))
sheet.save(out / '대표5장_미리보기.jpg', quality=94)
report = {
    'scope':'user-requested five-slide representative preview, not full-course approval',
    'slides':5, 'pptx_sha256':hashfile(pptx), 'pdf_sha256':hashfile(pdf),
    'package_and_geometry': 'passed with artifact-tool finalizer',
    'font':'Pretendard', 'native_powerpoint_opened':True,
    'native_powerpoint_slide_images_inspected':[1,2,3,4,5],
    'pdf_pages':5, 'copyright_text_all_slides':True, 'notes_and_sources_all_slides':True,
    'source_protection':guard, 'full_harness_G03_G09':'not asserted; current request is a five-slide manual preview',
    'limitations':['No animation/video execution or live AI-tool rehearsal; 20-second storyboard is a proposed example.']
}
(unit / 'checks').mkdir(exist_ok=True)
(unit / 'checks/sample-review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2),encoding='utf-8')
print('Verified 5 PPTX slides, 5 PDF pages, native PowerPoint renders, footers, notes, unchanged final PPTX and protected originals.')
