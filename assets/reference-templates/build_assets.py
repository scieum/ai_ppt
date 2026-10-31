"""Extract source geometry as reusable backgrounds. Never edit source PDFs.

Run from the repo root. Requires PyMuPDF; --deps accepts a private install.
"""
from pathlib import Path
import argparse, hashlib, json, sys

parser = argparse.ArgumentParser()
parser.add_argument('--deps')
args = parser.parse_args()
if args.deps:
    sys.path.insert(0, args.deps)
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
inventory = json.loads((ROOT/'output/reference-analysis/inventory.json').read_text(encoding='utf-8'))
sources = {row['id']: row for row in inventory}
specs = [
    ('cover', 'R02', 1), ('agenda', 'R02', 4),
    ('five-elements', 'R02', 23), ('brief', 'R02', 91),
    ('prompt', 'R05', 31),
]
catalog = {'schema_version': '1.0', 'canvas': [1920,1080],
    'mode': 'source_geometry_locked',
    'font': {'replacement':'Pretendard', 'reason':'PDF text uses anonymous Type3 glyphs; family cannot be reliably identified.', 'size':'Source measured size retained.'},
    'exceptions': ['Selected brand replaces source logo.', 'Copyright footer follows user brand rule.', 'Topic text and figure slot contents are replaced.'],
    'templates': []}
for key, source_id, number in specs:
    source = sources[source_id]
    doc = fitz.open(source['path'])
    page = doc[number-1]
    folder = OUT/key
    folder.mkdir(parents=True, exist_ok=True)
    page.get_pixmap().save(folder/'source.png')
    blocks = [b for b in page.get_text('dict')['blocks'] if b['type']==0]
    measured=[]
    for b in blocks:
        for line in b['lines']:
            for span in line['spans']:
                measured.append({k:span[k] for k in ['text','bbox','font','size']})
    (folder/'source-text-metrics.json').write_text(json.dumps(measured,ensure_ascii=False,indent=2),encoding='utf-8')
    copy = fitz.open()
    copy.insert_pdf(doc, from_page=number-1, to_page=number-1)
    clean = copy[0]
    # Type3 text has both an invisible text layer and visible outlined paths.
    # Fully-contained-path redaction removes glyph paths but preserves larger
    # original boxes, chevrons, border radii, gradient and spacing.
    regions = [list(b['bbox']) for b in blocks]
    if key == 'agenda':
        regions += [[460,280,1460,380],[320,550,550,730],[690,550,860,730],
                    [1010,530,1220,710],[1400,550,1560,700]]
    if key == 'cover':
        regions += [[180,175,1250,475]]
        for xref in {im['xref'] for im in clean.get_image_info(xrefs=True) if im['xref']}:
            clean.delete_image(xref)
    if key == 'prompt':
        # Left figure is a replaceable content slot, not a structural component.
        regions += [[390,560,830,880],[400,280,1520,460]]
    regions += [[1470,60,1860,165]]  # source brand artwork
    for region in regions:
        clean.add_redact_annot(fitz.Rect(region), fill=False)
    clean.apply_redactions(images=0, graphics=1, text=0)
    if key == 'cover':
        # A Type3 glyph with an inaccurate text bounding box survives redaction.
        # This region is wholly within the source's flat solid-color left band.
        clean.draw_rect(fitz.Rect(180,335,285,465),color=None,
                        fill=(200/255,44/255,114/255),overlay=True)
    if key == 'prompt':
        clean.draw_rect(fitz.Rect(390,560,830,880), color=None, fill=(0,0,0), overlay=True)
    clean.get_pixmap().save(folder/'background.png')
    (folder/'background.svg').write_text(clean.get_svg_image(),encoding='utf-8')
    catalog['templates'].append({'id': key, 'source_id':source_id, 'source_name':source['name'],
        'source_page':number, 'source_sha256':source['sha256'],
        'source_preview':f'{key}/source.png', 'background':f'{key}/background.png',
        'vector_background':f'{key}/background.svg',
        'background_sha256':hashlib.sha256((folder/'background.png').read_bytes()).hexdigest(),
        'metrics':f'{key}/source-text-metrics.json'})
(OUT/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
print('Extracted',len(specs),'source templates without changing source PDFs.')
