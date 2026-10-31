from pathlib import Path
import json,re,sys
from pypdf import PdfReader
rows=json.loads(Path('output/reference-analysis/inventory.json').read_text(encoding='utf-8'))
for d in rows:
    if d['id'] not in sys.argv[1:]: continue
    print(d['id'], d['page_count'], flush=True)
    for p in d['pages']:
        print('{} p.{}: {}'.format(d['id'],p['page'],re.sub(r'\s+','',p['text'])[:110]))
    reader=PdfReader(d['path'])
    fonts=set()
    for p in reader.pages:
        for f in p.get('/Resources',{}).get('/Font',{}).values():
            fonts.add(str(f.get_object().get('/BaseFont')))
    print('FONTS:', ', '.join(sorted(fonts)))
