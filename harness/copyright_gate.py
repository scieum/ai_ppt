"""G10: fail-closed rights/originality review records, not a legal verdict.

The text scan is a screening aid. It neither detects all paraphrases nor decides
whether a quotation, design, generated image or trademark use is lawful.
"""
import datetime as dt
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET

from gate import canonical, digest, evidence, local, plan, ppt_info, read, require, NS


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def snapshot(engine):
    """Bind the whole plan, current standard outputs, references and used assets."""
    root = engine.unit
    paths = {'plan.md', 'input.json', 'research/sources.json',
             'research/content-map.json', 'assets/manifest.json'}
    for rel in ['drafts/deck.pptx', 'drafts/script.docx', 'drafts/deck.pdf']:
        if (root / rel).is_file():
            paths.add(rel)
    for rel in ['design-review/reference-lock.json', 'design-review/review.json']:
        if (root / rel).is_file():
            paths.add(rel)
    sources = read(root / 'research/sources.json')
    assets = read(root / 'assets/manifest.json')
    for row in sources:
        evidence(root, row['evidence'])
        paths.add(row['evidence']['path'])
    for row in assets:
        evidence(root, row['file'])
        paths.add(row['file']['path'])
    review_path = root / 'design-review/review.json'
    if review_path.is_file():
        for row in read(review_path).get('slides', []):
            for key in ['artifact', 'render', 'layout', 'comparison']:
                if key in row:
                    evidence(root, row[key])
                    paths.add(row[key]['path'])
    files = {rel: digest(local(root, rel)) for rel in sorted(paths)}
    return {'unit': plan(root)['unit'], 'files': files,
            'scope_hash': canonical(files),
            'source_ids': sorted(row['id'] for row in sources),
            'asset_ids': sorted(row['id'] for row in assets)}


def text_file(path):
    ext = path.suffix.lower()
    if ext in ['.txt', '.md', '.json', '.csv', '.html', '.svg']:
        return path.read_text(encoding='utf-8-sig')
    if ext == '.pdf':
        from pypdf import PdfReader
        from pypdf.errors import PyPdfError
        try:
            return '\n'.join(p.extract_text() or '' for p in PdfReader(path).pages)
        except PyPdfError as err:
            raise ValueError('copyright scan cannot read PDF: ' + path.name) from err
    if ext == '.pptx':
        return '\n'.join('\n'.join(s['texts']) for s in ppt_info(path))
    if ext == '.docx':
        with zipfile.ZipFile(path) as z:
            return '\n'.join(t.text for t in ET.fromstring(z.read('word/document.xml')).findall('.//w:t', NS) if t.text)
    return None


def normalized(value):
    return ''.join(re.findall(r'[가-힣A-Za-z0-9]', value)).casefold()


def scan(engine):
    scope = snapshot(engine)
    p = plan(engine.unit)
    cfg = engine.rules['copyright_review']
    width = cfg['normalized_match_characters']
    targets = [('plan.md', (engine.unit / 'plan.md').read_text(encoding='utf-8-sig'))]
    for row in p['slides']:
        for field in ['title', 'message', 'instructor_action', 'learner_action']:
            targets.append((f"plan:slide{row['number']}:{field}", row.get(field, '')))
    for row in p.get('exercises', []):
        for field in ['instructions', 'expected_result', 'success_criteria']:
            value = row.get(field, '')
            targets.append((f"plan:exercise:{row['id']}:{field}", '\n'.join(value) if isinstance(value, list) else value))
    for rel in ['drafts/deck.pptx', 'drafts/script.docx']:
        if (engine.unit / rel).is_file():
            targets.append((rel, text_file(engine.unit / rel)))
    for row in read(engine.unit / 'assets/manifest.json'):
        if row.get('kind') in ['exercise_file', 'prompt', 'starter', 'checkpoint']:
            value = text_file(evidence(engine.unit, row['file']))
            if value is not None:
                targets.append((row['file']['path'], value))
    findings, unavailable = [], []
    for source in read(engine.unit / 'research/sources.json'):
        value = text_file(evidence(engine.unit, source['evidence']))
        if value is None or not normalized(value):
            unavailable.append(source['id'])
            continue
        original = normalized(value)
        # Report at most one literal-match sample per target/reference pair.
        for location, target in targets:
            target = normalized(target or '')
            for offset in range(max(0, len(target) - width + 1)):
                sample = target[offset:offset + width]
                if sample in original:
                    key = {'target': location, 'source_id': source['id'], 'sample': sample}
                    findings.append(dict(key, id=canonical(key)[:20]))
                    break
    return {'schema_version': 1, 'scope_hash': scope['scope_hash'],
            'match_characters': width, 'findings': findings,
            'text_unavailable_sources': sorted(unavailable),
            'limit': 'Literal normalized matches only. No semantic, image, music, license or legal clearance is inferred.'}


def actual(engine, row):
    require(engine.test or not row.get('simulation', False), 'simulated copyright review in production')


def review(engine):
    root = engine.unit
    require((root / 'rights/inventory.json').is_file(), 'G10 rights inventory missing; reused templates/assets require rights review')
    require((root / 'rights/review.json').is_file(), 'G10 human copyright review missing')
    scope = snapshot(engine)
    inventory = read(root / 'rights/inventory.json')
    report = read(root / 'rights/review.json')
    actual(engine, inventory)
    actual(engine, report)
    require(inventory.get('unit') == report.get('unit') == scope['unit'], 'copyright unit mismatch')
    require(report.get('scope_hash') == scope['scope_hash'], 'stale copyright scope; plan/assets/references/output changed')
    require(report.get('inventory_hash') == canonical(inventory), 'stale copyright inventory review')
    stored_scan = read(root / 'rights/scan.json')
    current_scan = scan(engine)
    require(stored_scan == current_scan, 'missing/stale copyright similarity scan')
    require(report.get('scan_hash') == canonical(current_scan), 'stale copyright scan review')
    require(read(root / 'rights/open-issues.json') == [], 'unresolved copyright issues')
    require(report.get('status') == 'reviewed' and report.get('actor') == 'human' and
            nonempty(report.get('reviewer')) and nonempty(report.get('message_ref')), 'human copyright reviewer/evidence required')
    dt.date.fromisoformat(report['checked_on'])
    evidence(root, report['evidence'])
    uses = inventory.get('intended_uses')
    allowed = set(engine.rules['copyright_review']['uses'])
    require(isinstance(uses, list) and uses and len(uses) == len(set(uses)) and set(uses) <= allowed, 'explicit copyright distribution scope required')
    inp = read(root / 'input.json')
    require('live_presentation' in uses, 'live-presentation rights scope missing')
    for key, use in [('pdf', 'pdf_distribution'), ('exercises', 'exercise_distribution'), ('figma', 'figma_publication')]:
        require(not inp['deliverables'][key] or use in uses, 'delivery rights scope missing: ' + use)
    refs = inventory.get('references', [])
    ids = [row['source_id'] for row in refs]
    require(len(ids) == len(set(ids)) and sorted(ids) == scope['source_ids'], 'copyright reference coverage mismatch')
    for row in refs:
        actual(engine, row)
        require(nonempty(row.get('review_note')), 'reference rights/use note missing')
        require(row.get('use') in ['analysis_only', 'quoted', 'adapted', 'reproduced'], 'reference use classification missing')
        if row['use'] != 'analysis_only':
            require(row.get('basis') in ['permission', 'license', 'public_domain', 'exception_review'],
                    'reused reference needs a rights basis, not merely attribution')
            require(set(uses) <= set(row.get('allowed_uses', [])), 'reference permission does not cover distribution scope')
            evidence(root, row['evidence'])
            if row['basis'] == 'exception_review':
                require(nonempty(row.get('legal_reasoning')), 'reference exception needs case-specific reasoning')
    materials = inventory.get('materials', [])
    ids = [row['asset_id'] for row in materials]
    require(len(ids) == len(set(ids)) and sorted(ids) == scope['asset_ids'], 'copyright material coverage mismatch')
    registered = {row['id']: row for row in read(root / 'assets/manifest.json')}
    for row in materials:
        actual(engine, row)
        require(row.get('file') == registered[row['asset_id']]['file'], 'copyright material binding mismatch')
        evidence(root, row['file'])
        require(row.get('basis') in engine.rules['copyright_review']['rights_bases'], 'unresolved/unknown asset rights basis')
        require(row.get('use') in ['original', 'generated', 'reproduced', 'adapted'], 'asset reuse classification missing')
        require(not (row['use'] in ['reproduced', 'adapted'] and row['basis'] in ['original', 'generated']),
                'copied/adapted source cannot be cleared as original/generated')
        require(nonempty(row.get('rights_holder')) and nonempty(row.get('reason')), 'asset rights holder/reason missing')
        require(set(uses) <= set(row.get('allowed_uses', [])), 'asset permission does not cover distribution scope')
        require(isinstance(row.get('source_ids'), list) and set(row['source_ids']) <= set(scope['source_ids']), 'unknown asset rights source')
        evidence(root, row['evidence'])
        if row['basis'] == 'exception_review':
            require(nonempty(row.get('legal_reasoning')), 'case-specific exception reasoning required; education/free is not automatic clearance')
    criteria = report.get('criteria', {})
    require(set(criteria) == set(engine.rules['copyright_review']['criteria']), 'copyright review criteria coverage mismatch')
    for key, row in criteria.items():
        actual(engine, row)
        require(row.get('status') == 'reviewed' and nonempty(row.get('reason')), 'unreviewed copyright criterion: ' + key)
        evidence(root, row['evidence'])
    resolutions = report.get('resolutions', [])
    ids = [r['finding_id'] for r in resolutions]
    require(len(ids) == len(set(ids)) and sorted(ids) == sorted(r['id'] for r in current_scan['findings']), 'unresolved/extra copyright text findings')
    for row in resolutions:
        actual(engine, row)
        require(row.get('decision') in ['common_term', 'permitted_quote', 'independent_expression'] and nonempty(row.get('reason')),
                'copyright finding needs a reasoned disposition')
        evidence(root, row['evidence'])
