"""Read-only source collection. Never execute source-page commands."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import shutil
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SOURCES = [
    ('odssi-ae', 'https://odssilab.com/recipes/ae-motion/'),
    ('real-sfx', 'https://clipwing.pro/skills/real-sfx'),
    ('earshot-readme', 'https://raw.githubusercontent.com/Leonxlnx/earshot/main/README.md'),
    ('openverse-terms', 'https://docs.openverse.org/terms_of_service.html'),
]

def collect(item):
    name, url = item
    record = {'id': name, 'url': url, 'retrieved_at': datetime.now(timezone.utc).isoformat()}
    try:
        response = requests.get(url, timeout=35)
        record.update(status=response.status_code, final_url=response.url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        if name == 'earshot-readme':
            content = response.text
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            for node in soup(['script', 'style', 'nav', 'header', 'footer']):
                node.decompose()
            content = (soup.find('main') or soup.body or soup).get_text('\n', strip=True)
        target = ROOT / 'sources' / (name + '.txt')
        target.write_text(content, encoding='utf-8')
        record.update(file=target.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    except Exception as exc:
        record['error'] = str(exc)
    return record

if __name__ == '__main__':
    (ROOT / 'sources').mkdir(exist_ok=True)
    (ROOT / 'references').mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(collect, SOURCES))
    for name, original, author in [
        ('sound-tools.png', 'codex-clipboard-68fa1b2f-6d87-41ea-a411-234a06640fdd.png', '@rebornlabs.ai'),
        ('motion-effects.png', 'codex-clipboard-b0503fee-1afd-4a55-ae35-47df872e728c.png', '@mynameisjaemin'),
    ]:
        source = Path('C:/Users/User/AppData/Local/Temp') / original
        record = {'id': name, 'kind': 'user-provided screenshot', 'account_visible': author, 'original': str(source), 'post_url': None}
        if source.exists():
            target = ROOT / 'references' / name
            shutil.copy2(source, target)
            record.update(file=target.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        else:
            record['error'] = 'Original local file unavailable; attachment was available in conversation.'
        records.append(record)
    (ROOT / 'source-index.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps([{'id': r['id'], 'status': r.get('status'), 'saved': 'file' in r, 'error': r.get('error')} for r in records], ensure_ascii=False))
