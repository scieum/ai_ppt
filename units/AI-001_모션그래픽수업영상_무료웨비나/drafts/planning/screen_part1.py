"""Preliminary text screening only; does not clear rights or satisfy G10."""
from pathlib import Path
import hashlib
import json
import sys

UNIT = Path(__file__).resolve().parents[2]
ROOT = UNIT.parents[1]
sys.path.insert(0, str(ROOT / 'harness'))
from copyright_gate import normalized

width = json.loads((ROOT / 'harness/rules.json').read_text(encoding='utf-8'))['copyright_review']['normalized_match_characters']
target = UNIT / 'part-1.md'
paragraphs = [(n, normalized(value)) for n, value in enumerate(target.read_text(encoding='utf-8').split('\n\n'), 1)]
inventory = json.loads((ROOT / 'output/reference-analysis/inventory.json').read_text(encoding='utf-8'))
findings = []
sources = []
for source in inventory:
    digest = hashlib.sha256(Path(source['path']).read_bytes()).hexdigest()
    if digest != source['sha256']:
        raise ValueError('Reference extraction no longer matches original: ' + source['id'])
    sources.append({'id': source['id'], 'sha256': digest, 'pages': len(source['pages'])})
    for page in source['pages']:
        original = normalized(page['text'])
        for number, text in paragraphs:
            for offset in range(max(0, len(text) - width + 1)):
                sample = text[offset:offset + width]
                if sample in original:
                    findings.append({'source_id': source['id'], 'page': page['page'], 'paragraph': number, 'sample': sample})
                    break
report = {'status': 'preliminary_screen_only', 'target': 'part-1.md',
          'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
          'match_characters': width, 'sources': sources, 'findings': findings,
          'human_review': 'not_completed', 'G10': 'not_cleared',
          'limit': 'Cached PDF extracted text only, original hashes verified. No semantic, visual, license or legal clearance.'}
output = UNIT / 'checks/part-1-originality-screen.json'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'sources': len(sources), 'pages': sum(r['pages'] for r in sources), 'literal_findings': len(findings), 'G10': 'not_cleared'}))
