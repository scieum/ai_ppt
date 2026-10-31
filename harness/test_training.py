"""Self-contained, explicitly simulated parser/contract fixtures; no training deliverables."""
import base64
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import xml.etree.ElementTree as ET

from gate import Engine, NS, canonical, digest, plan, plan_hash, read, save
from validate_science import bind, write_plan, docx_fixture, with_notes

HERE = Path(__file__).resolve().parent
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jB1sAAAAASUVORK5CYII=')


def ppt_fixture(path, n=7, footer=None):
    """Minimal OOXML parser fixture; no claim of PowerPoint/visual validation."""
    relns = 'http://schemas.openxmlformats.org/package/2006/relationships'
    pres = ET.Element('{' + NS['p'] + '}presentation')
    slides = ET.SubElement(pres, '{' + NS['p'] + '}sldIdLst')
    rels = ET.Element('Relationships', xmlns=relns)
    with zipfile.ZipFile(path, 'w') as z:
        for i in range(1, n + 1):
            ET.SubElement(slides, '{' + NS['p'] + '}sldId', {'id': str(255+i), '{'+NS['r']+'}id': f'rId{i}'})
            ET.SubElement(rels, 'Relationship', {'Id': f'rId{i}', 'Type': NS['r']+'/slide', 'Target': f'slides/slide{i}.xml'})
            z.writestr(f'ppt/slides/slide{i}.xml', f'<p:sld xmlns:p="{NS["p"]}" xmlns:a="{NS["a"]}"><p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r><a:t>SIMULATION {i} {footer or ""}</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>')
        z.writestr('ppt/presentation.xml', ET.tostring(pres))
        z.writestr('ppt/_rels/presentation.xml.rels', ET.tostring(rels))
        z.writestr('[Content_Types].xml', '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="xml" ContentType="application/xml"/></Types>')


def training_script(path, n):
    docx_fixture(path, n)
    with zipfile.ZipFile(path) as z:
        entries = {k: z.read(k) for k in z.namelist()}
    xml = ET.fromstring(entries['word/document.xml'])
    for node in xml.findall('.//w:t', NS):
        if not node.text.startswith('Slide '):
            node.text = '발화: SIMULATION ONLY. 조작: simulated input. 대기: simulated wait. Source: parser fixture'
    entries['word/document.xml'] = ET.tostring(xml)
    with zipfile.ZipFile(path, 'w') as z:
        for k, value in entries.items():
            z.writestr(k, value)


def fixture(root):
    from pypdf import PdfWriter
    u = root / 'unit'
    for rel in ['research', 'assets', 'exercises', 'drafts/representatives', 'design-review', 'renders', 'checks']:
        (u / rel).mkdir(parents=True, exist_ok=True)
    (u / '.harness-test').write_text('SIMULATION ONLY')
    (root / 'protected').mkdir()
    (root / 'protected/original.txt').write_text('Do not change this fixture source.')
    env = {'product': 'SIMULATION', 'version': 'fixture', 'os': 'Windows', 'ui_language': 'ko', 'account': 'test'}
    (u / 'assets/logo.png').write_bytes(PNG)
    inp = {'profile': 'ai_training', 'unit': 'training-simulation', 'audience': 'parser test only', 'format': 'workshop',
           'environment': env, 'objectives': [{'id': 'O1', 'action': 'inspect the simulated result', 'result': 'fixture text'}],
           'target_slides': 7, 'minutes': 7, 'deliverables': {'pdf': True, 'figma': False, 'exercises': True},
           'branding': {'brand_id': 'notiontalk', 'mode': 'logo', 'label': 'SIMULATION',
                        'copyright': {'template': '© {year}. {holder}. All rights reserved.', 'year': 2026},
                        'logos': [{'role': 'notiontalk_logo', 'file': bind(u, 'assets/logo.png'), 'slides': list(range(1, 8))}]}}
    footer = '© 2026. NotionTalk. All rights reserved.'
    save(u / 'input.json', inp)
    for rel in ['research/evidence.txt', 'approval-evidence.txt', 'exercises/prompt.txt']:
        (u / rel).write_text('SIMULATION ONLY. Not actual user consent, documentation, rehearsal, or a training asset.', encoding='utf-8')
    save(u / 'research/sources.json', [
        {'id': 'S1', 'role': 'official', 'citation': 'Simulated official source', 'url': 'https://example.invalid/fixture',
         'checked_on': '2026-10-27', 'locator': 'test fixture', 'simulation': True, 'evidence': bind(u, 'research/evidence.txt')},
        {'id': 'D1', 'role': 'design', 'citation': 'Simulated design reference', 'locator': 'page 1', 'simulation': True,
         'evidence': bind(u, 'research/evidence.txt')}])
    save(u / 'research/content-map.json', [{'id': 'C1', 'kind': 'technical', 'claim': 'simulated procedure',
         'rationale': 'parser fixture only', 'scope': '기본', 'source_ids': ['S1'], 'objective_ids': ['O1'],
         'verification': {'status': 'verified', 'checked_on': '2026-10-27', 'environment': env,
                          'simulation': True, 'evidence': bind(u, 'research/evidence.txt')}}])
    p = copy.deepcopy(inp)
    types = read(HERE / 'rules.json')['design_review']['types']
    p.update(design='design.md', supplementary={}, links=[], exercises=[{
        'id': 'EX1', 'title': 'Simulated exercise', 'objective_ids': ['O1'], 'mode': 'hands_on',
        'start_conditions': 'simulated session', 'input_location': 'simulated chat', 'instructions': ['enter fixture text'],
        'expected_result': 'fixture result', 'success_criteria': ['result contains fixture text'],
        'errors': [{'symptom': 'missing text', 'check': 'inspect input', 'action': 'retry fixture', 'expected_state': 'fixture result'}],
        'fallback': 'use fixture result', 'customization': 'replace the fixture label', 'minutes': 7,
        'file_ids': ['PROMPT'], 'source_ids': ['S1']}],
        slides=[{'number': i, 'title': f'SIMULATION {i}', 'message': f'fixture message {i}', 'content_ids': ['C1'],
                 'source_ids': ['S1'], 'visual': ['LOGO'], 'layout': kind, 'design_type': kind, 'character': 'none', 'minutes': 1,
                 'activity': 'practice' if i == 6 else 'check' if i == 7 else 'explanation', 'objective_ids': ['O1'],
                 'exercise_ids': ['EX1'], 'instructor_action': 'explain fixture', 'learner_action': 'inspect fixture'}
                for i, kind in enumerate(types, 1)])
    write_plan(u, p)
    save(u / 'assets/manifest.json', [{'id': 'PROMPT', 'kind': 'prompt', 'file': bind(u, 'exercises/prompt.txt'),
         'purpose': 'simulated input', 'provenance': 'parser fixture', 'review': 'passed', 'reviewer': 'simulation', 'simulation': True},
        {'id': 'LOGO', 'kind': 'existing', 'file': bind(u, 'assets/logo.png'), 'purpose': 'simulated brand logo',
         'provenance': 'parser fixture', 'review': 'passed', 'reviewer': 'simulation', 'simulation': True}])
    ppt_fixture(root / 'source.pptx', footer=footer)
    with_notes(root / 'source.pptx', u / 'drafts/deck.pptx', 7)
    training_script(u / 'drafts/script.docx', 7)
    writer = PdfWriter()
    for _ in range(7):
        writer.add_blank_page(width=960, height=540)
    writer.write(u / 'drafts/deck.pdf')
    for i in range(1, 8):
        (u / f'renders/slide{i:02}.png').write_bytes(PNG)
    cfg = read(HERE / 'rules.json')['design_review']
    refs, candidates = [], []
    for i, kind in enumerate(types, 1):
        rel = f'drafts/representatives/{kind}.txt'
        (u / rel).write_text('SIMULATION ' + kind)
        objects = [{'role': role, 'kind': 'text', 'bbox': [0.1, 0.1, 0.2, 0.2], 'fill': '#FFFFFF',
                    'font_family': 'Pretendard', 'font_size': 40, 'font_weight': 700, 'alignment': 'left', 'character_asset_id': 'none'}
                   for role in cfg['required_roles'][kind]]
        objects += [dict(objects[0], role='notiontalk_logo', bbox=[0.8, 0.04, 0.15, 0.08],
                         visible_bbox=[0.8, 0.04, 0.15, 0.08], asset_sha256=digest(u / 'assets/logo.png')),
                    dict(objects[0], role='copyright_footer', bbox=[0.55, 0.94, 0.4, 0.04], text=footer)]
        layout = {'artifact_sha256': digest(u / rel), 'render_sha256': digest(u / f'renders/slide{i:02}.png'),
                  'exporter': 'SIMULATION ONLY', 'canvas': [1920, 1080], 'objects': objects}
        for tag in ['source', 'candidate', 'target']:
            save(u / f'design-review/{kind}-{tag}.json', layout)
        ref = {'id': 'ref-'+kind, 'type': kind, 'slide': i, 'mode': 'adopt', 'source': bind(u, rel),
               'render': bind(u, f'renders/slide{i:02}.png'), 'layout': bind(u, f'design-review/{kind}-source.json'),
               'recipe': {'adopted': ['layout hierarchy'], 'replaced': [], 'adjustments': []},
               'target': {'artifact': bind(u, rel), 'render': bind(u, f'renders/slide{i:02}.png'), 'layout': bind(u, f'design-review/{kind}-target.json')}}
        refs.append(ref)
        candidates.append({'id': 'candidate-'+kind, 'type': kind, 'slide': i, 'reference_id': ref['id'],
                           'artifact': bind(u, rel), 'render': ref['render'], 'layout': bind(u, f'design-review/{kind}-candidate.json'),
                           'comparison': ref['render'], 'reviewer': 'simulation', 'reason': 'parser fixture', 'simulation': True,
                           'criteria': {k: {'status': 'passed', 'reason': 'parser fixture', 'reviewer': 'simulation',
                                            'simulation': True, 'evidence': ref['render']} for k in cfg['criteria']}})
    lock = {'unit': inp['unit'], 'templates': refs}
    save(u / 'design-review/reference-lock.json', lock)
    save(u / 'design-review/review.json', {'unit': inp['unit'], 'version': 'simulation-1', 'plan_hash': plan_hash(u),
         'reference_hash': canonical(lock), 'simulation': True, 'slides': candidates})
    save(u / 'design-review/feedback.json', [])
    e = Engine(u, control=root / 'control', test=True)
    e.baseline([root / 'protected'])
    reviews = []
    for i, kind in enumerate(types, 1):
        layout = read(u / f'design-review/{kind}-candidate.json')
        layout['artifact_sha256'] = digest(u / 'drafts/deck.pptx')
        save(u / f'checks/layout{i:02}.json', layout)
        rev = {'status': 'passed', 'reviewer': 'simulation', 'comment': 'parser fixture only', 'simulation': True,
               'evidence': bind(u, 'research/evidence.txt')}
        reviews.append(dict(number=i, render=bind(u, f'renders/slide{i:02}.png'), layout=bind(u, f'checks/layout{i:02}.json'),
                            pdf_review={'pdf_sha256': digest(u / 'drafts/deck.pdf'), 'page': i,
                                        'status': 'passed', 'reviewer': 'simulation', 'comment': 'parser fixture', 'simulation': True,
                                        'render': bind(u, f'renders/slide{i:02}.png'), 'evidence': bind(u, 'research/evidence.txt')},
                            **{k: copy.deepcopy(rev) for k in e.rules['review_categories']}))
    save(u / 'checks/reviews.json', {'plan_hash': plan_hash(u), 'artifacts': e.artifact_binding(), 'open_issues': [], 'slides': reviews})
    save(u / 'checks/rehearsal.json', {'plan_hash': plan_hash(u), 'artifacts': e.artifact_binding(), 'environment': env,
         'status': 'passed', 'reviewer': 'simulation', 'checked_on': '2026-10-27', 'elapsed_minutes': 7, 'simulation': True,
         'evidence': bind(u, 'research/evidence.txt'), 'links': [], 'exercises': [{
            'id': 'EX1', 'status': 'passed', 'reviewer': 'simulation', 'checked_on': '2026-10-27', 'environment': env,
            'simulation': True, 'criteria_results': [{'criterion': 'result contains fixture text', 'status': 'passed'}],
            **{k: bind(u, 'research/evidence.txt') for k in ['evidence', 'recovery_evidence', 'fallback_evidence']}}]})
    approve_fixture(e)
    copyright_fixture(e)
    return e


def approve_fixture(engine):
    u = engine.unit
    save(u / 'approvals.json', [{'unit': read(u / 'input.json')['unit'], 'actor': 'human', 'decision': 'approve',
         'simulation': True, 'message_ref': 'test://plan', 'plan_hash': plan_hash(u), 'evidence': bind(u, 'approval-evidence.txt')}])
    rev = read(u / 'design-review/review.json')
    save(u / 'design-review/approvals.json', [{'unit': rev['unit'], 'version': rev['version'], 'review_hash': canonical(rev),
         'reference_hash': rev['reference_hash'], 'actor': 'human', 'decision': 'approve_design', 'simulation': True,
         'message_ref': 'test://design', 'evidence': bind(u, 'approval-evidence.txt')}])


def copyright_fixture(engine):
    """SIMULATION ONLY. Never use parser-fixture review records for real work."""
    assert engine.test and (engine.unit / '.harness-test').is_file()
    from copyright_gate import snapshot, scan
    u = engine.unit
    scope = snapshot(engine)
    uses = ['live_presentation', 'pdf_distribution', 'exercise_distribution']
    if read(u / 'input.json')['deliverables']['figma']:
        uses.append('figma_publication')
    proof = bind(u, 'research/evidence.txt')
    inventory = {'unit': scope['unit'], 'simulation': True, 'intended_uses': uses,
        'references': [{'source_id': sid, 'use': 'analysis_only', 'review_note': 'Simulated parser reference only', 'simulation': True}
                       for sid in scope['source_ids']],
        'materials': [dict(asset_id=a['id'], file=a['file'], use='original', basis='original',
             rights_holder='SIMULATION fixture author', reason='Test bytes only', allowed_uses=uses,
             source_ids=[], evidence=proof, simulation=True) for a in read(u / 'assets/manifest.json')]}
    save(u / 'rights/inventory.json', inventory)
    screening = scan(engine)
    save(u / 'rights/scan.json', screening)
    save(u / 'rights/open-issues.json', [])
    save(u / 'rights/review.json', {'unit': scope['unit'], 'simulation': True,
        'scope_hash': scope['scope_hash'], 'inventory_hash': canonical(inventory), 'scan_hash': canonical(screening),
        'status': 'reviewed', 'actor': 'human', 'reviewer': 'SIMULATION ONLY', 'message_ref': 'test://copyright',
        'checked_on': '2026-10-27', 'evidence': proof,
        'criteria': {key: {'status': 'reviewed', 'reason': 'Parser fixture, not legal clearance', 'evidence': proof, 'simulation': True}
                     for key in engine.rules['copyright_review']['criteria']},
        'resolutions': [{'finding_id': row['id'], 'decision': 'common_term', 'reason': 'SIMULATION parser text',
                         'evidence': proof, 'simulation': True} for row in screening['findings']]})


class TrainingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ai-training-gates-')
        self.root = Path(self.temp.name)
        self.e = fixture(self.root)
        self.u = self.e.unit

    def tearDown(self):
        self.temp.cleanup()

    def mutate(self, rel, fn):
        obj = read(self.u / rel); fn(obj); save(self.u / rel, obj)

    def change_plan(self, fn):
        p = plan(self.u); fn(p); write_plan(self.u, p)

    def fails(self, gate, detail=None):
        result = self.e.check([gate])
        self.assertFalse(result['passed'], result)
        if detail:
            self.assertIn(detail, result['results'][0]['detail'])

    def checkpoint_all(self):
        for stage in self.e.rules['stages']:
            report = self.e.checkpoint(stage)
            self.assertTrue(report['passed'], report)

    def refresh_bindings(self):
        lock = read(self.u / 'design-review/reference-lock.json')
        self.mutate('design-review/review.json', lambda d: d.update(plan_hash=plan_hash(self.u), reference_hash=canonical(lock)))
        for rel in ['checks/reviews.json', 'checks/rehearsal.json']:
            self.mutate(rel, lambda d: d.update(plan_hash=plan_hash(self.u), artifacts=self.e.artifact_binding()))
        approve_fixture(self.e)
        copyright_fixture(self.e)

    def test_all_nine_gates_without_science_or_figma_or_characters(self):
        report = self.e.check(list(self.e.rules['gates']))
        self.assertTrue(report['passed'], report)

    def test_research_before_plan_exists(self):
        (self.u / 'plan.md').unlink()
        self.assertTrue(self.e.checkpoint('research')['passed'])

    def test_legacy_input_rejected_by_training(self):
        self.mutate('input.json', lambda d: d.pop('profile')); self.fails('G01', 'profile')

    def test_science_rules_cannot_validate_training(self):
        e = Engine(self.u, HERE / 'rules-science.json', control=self.root / 'other-control', test=True)
        self.assertFalse(e.check(['G01'])['passed'])

    def test_official_source_required_for_technical_claim(self):
        self.mutate('research/sources.json', lambda d: d[0].update(role='content')); self.fails('G01', 'official')

    def test_reference_cannot_be_unknown_role(self):
        self.mutate('research/sources.json', lambda d: d[1].update(role='standard')); self.fails('G01')

    def test_unverified_procedure(self):
        self.mutate('research/content-map.json', lambda d: d[0]['verification'].update(status='unverified')); self.fails('G01')

    def test_wrong_technical_environment(self):
        self.mutate('research/content-map.json', lambda d: d[0]['verification']['environment'].update(os='macOS')); self.fails('G01')

    def test_invalid_verification_date(self):
        self.mutate('research/content-map.json', lambda d: d[0]['verification'].update(checked_on='yesterday')); self.fails('G01')

    def test_stale_source_evidence(self):
        (self.u / 'research/evidence.txt').write_text('changed'); self.fails('G01')

    def test_pending_scope(self):
        self.mutate('research/content-map.json', lambda d: d[0].update(scope='确认 필요')); self.fails('G01')

    def test_supplement_requires_rationale(self):
        self.mutate('research/content-map.json', lambda d: d[0].update(scope='선택·심화')); self.fails('G01')

    def test_duplicate_objective(self):
        self.mutate('input.json', lambda d: d['objectives'].append(d['objectives'][0])); self.fails('G01')

    def test_slide_count(self):
        self.change_plan(lambda p: p['slides'].pop()); self.fails('G02')

    def test_time_sum(self):
        self.change_plan(lambda p: p['slides'][0].update(minutes=2)); self.fails('G02', 'total minutes')

    def test_nan_time(self):
        self.change_plan(lambda p: p['slides'][0].update(minutes=float('nan'))); self.fails('G02')

    def test_unknown_slide_design_type(self):
        self.change_plan(lambda p: p['slides'][0].update(design_type='dashboard')); self.fails('G02')

    def test_no_result_check(self):
        self.change_plan(lambda p: p['slides'][-1].update(activity='explanation')); self.fails('G02', 'result-check')

    def test_no_learner_practice(self):
        self.change_plan(lambda p: p['slides'][-2].update(activity='demo')); self.fails('G02', 'learner practice')

    def test_no_success_criteria(self):
        self.change_plan(lambda p: p['exercises'][0].update(success_criteria=[])); self.fails('G02')

    def test_no_fallback(self):
        self.change_plan(lambda p: p['exercises'][0].update(fallback='')); self.fails('G02')

    def test_no_error_recovery(self):
        self.change_plan(lambda p: p['exercises'][0].update(errors=[])); self.fails('G02')

    def test_unknown_objective_on_exercise(self):
        self.change_plan(lambda p: p['exercises'][0].update(objective_ids=['unknown'])); self.fails('G02')

    def test_exercise_duration(self):
        self.change_plan(lambda p: p['exercises'][0].update(minutes=6)); self.fails('G02', 'exercise time')

    def test_input_delivery_change_invalidates_approval(self):
        self.mutate('input.json', lambda d: d['deliverables'].update(figma=True))
        self.change_plan(lambda p: p['deliverables'].update(figma=True))
        self.fails('G03', 'approval')

    def test_exercise_meaning_change_invalidates_approval(self):
        self.change_plan(lambda p: p['exercises'][0].update(expected_result='different result')); self.fails('G03', 'approval')

    def test_routine_layout_change_keeps_plan_approval(self):
        self.change_plan(lambda p: p['slides'][0].update(layout='different layout'))
        self.assertTrue(self.e.check(['G03'])['passed'])

    def test_simulation_blocked_in_production(self):
        e = Engine(self.u, control=self.root / 'control')
        self.assertFalse(e.check(['G01', 'G03', 'G06', 'G09'])['passed'])

    def test_missing_approval_blocks_asset_write(self):
        save(self.u / 'approvals.json', [])
        with self.assertRaises(ValueError): self.e.write('image', 'exercises/new.txt', b'denied')
        self.assertFalse((self.u / 'exercises/new.txt').exists())

    def test_stale_prompt_file(self):
        (self.u / 'exercises/prompt.txt').write_text('changed'); self.fails('G04')

    def test_prompt_cannot_escape_exercises_folder(self):
        self.mutate('assets/manifest.json', lambda d: d[0].update(file=bind(self.u, 'research/evidence.txt'))); self.fails('G04')

    def test_screenshot_environment_required(self):
        p = plan(self.u); p['slides'][0]['visual'] = ['LOGO', 'UI']; write_plan(self.u, p); approve_fixture(self.e)
        (self.u / 'assets/ui.png').write_bytes(PNG)
        self.mutate('assets/manifest.json', lambda d: d.append({'id': 'UI', 'kind': 'screenshot', 'file': bind(self.u, 'assets/ui.png'),
            'purpose': 'tool UI', 'review': 'passed', 'reviewer': 'simulation', 'source_id': 'S1', 'locator': 'fixture screen'}))
        self.fails('G04', 'date')

    def test_generated_ui_evidence_rejected(self):
        self.mutate('assets/manifest.json', lambda d: d[0].update(kind='generated', purpose_type='tool_ui')); self.fails('G04', 'actual screenshot')

    def test_pdf_page_count(self):
        from pypdf import PdfWriter
        w = PdfWriter(); w.add_blank_page(width=960, height=540); w.write(self.u / 'drafts/deck.pdf')
        self.fails('G05', 'PDF page count')

    def test_corrupt_pdf(self):
        (self.u / 'drafts/deck.pdf').write_text('not a PDF'); self.fails('G05', 'PDF validation')

    def test_missing_pdf(self):
        (self.u / 'drafts/deck.pdf').unlink(); self.fails('G05')

    def test_missing_manuscript_operating_instructions(self):
        docx_fixture(self.u / 'drafts/script.docx', 7); self.fails('G05', 'speech label')

    def test_missing_rehearsal(self):
        (self.u / 'checks/rehearsal.json').unlink(); self.fails('G06')

    def test_pdf_page_correspondence_review_required(self):
        self.mutate('checks/reviews.json', lambda d: d['slides'][0].pop('pdf_review')); self.fails('G06', 'PDF page review')

    def test_rehearsal_too_long(self):
        self.mutate('checks/rehearsal.json', lambda d: d.update(elapsed_minutes=8)); self.fails('G06', 'available time')

    def test_rehearsal_success_not_demonstrated(self):
        self.mutate('checks/rehearsal.json', lambda d: d['exercises'][0]['criteria_results'][0].update(status='unverified')); self.fails('G06')

    def test_rehearsal_current_files_required(self):
        self.mutate('checks/rehearsal.json', lambda d: d['artifacts'].update({'exercises/prompt.txt': 'stale'})); self.fails('G06', 'stale rehearsal')

    def test_selected_figma_cannot_be_skipped(self):
        for rel in ['input.json']:
            self.mutate(rel, lambda d: d['deliverables'].update(figma=True))
        self.change_plan(lambda p: p['deliverables'].update(figma=True))
        self.mutate('design-review/review.json', lambda d: d.update(plan_hash=plan_hash(self.u)))
        for rel in ['checks/reviews.json', 'checks/rehearsal.json']:
            self.mutate(rel, lambda d: d.update(plan_hash=plan_hash(self.u)))
        approve_fixture(self.e); self.fails('G06', 'mapping.json')

    def test_unselected_figma_tool_denied(self):
        with self.assertRaises(ValueError): self.e.tool_preflight('figma-preview')

    def test_source_protection(self):
        (self.root / 'protected/original.txt').write_text('changed'); self.fails('G07')

    def test_seven_representatives_required(self):
        self.mutate('design-review/review.json', lambda d: d['slides'].pop()); self.fails('G08')

    def test_candidate_geometry_must_match_adopted_target(self):
        self.mutate('design-review/cover-candidate.json', lambda d: d['objects'][0].update(bbox=[0.2, 0.1, 0.2, 0.2]))
        self.mutate('design-review/review.json', lambda d: d['slides'][0].update(layout=bind(self.u, 'design-review/cover-candidate.json')))
        self.fails('G08', 'position/scale')

    def test_undeclared_adoption_changes(self):
        self.mutate('design-review/cover-target.json', lambda d: d['objects'][0].update(fill='#000000'))
        self.mutate('design-review/reference-lock.json', lambda d: d['templates'][0]['target'].update(layout=bind(self.u, 'design-review/cover-target.json')))
        lock = read(self.u / 'design-review/reference-lock.json')
        self.mutate('design-review/review.json', lambda d: d.update(reference_hash=canonical(lock)))
        self.fails('G08', 'adoption changes')

    def test_selected_brand_requires_no_other_institution_logo(self):
        self.assertTrue(self.e.check(['G08', 'G09'])['passed'])

    def test_copied_institution_logo_rejected(self):
        self.mutate('checks/layout02.json', lambda d: d['objects'].append(dict(d['objects'][0], role='tsherpa_logo')))
        self.mutate('checks/reviews.json', lambda d: d['slides'][1].update(layout=bind(self.u, 'checks/layout02.json')))
        self.fails('G06', 'brand logo')

    def test_full_deck_layout_binding(self):
        self.mutate('checks/layout02.json', lambda d: d.update(artifact_sha256='bad'))
        self.mutate('checks/reviews.json', lambda d: d['slides'][1].update(layout=bind(self.u, 'checks/layout02.json')))
        self.fails('G06', 'bound')

    def test_nan_layout_bounds(self):
        self.mutate('checks/layout02.json', lambda d: d['objects'][0].update(bbox=[float('nan'), 0.1, 0.2, 0.2]))
        self.mutate('checks/reviews.json', lambda d: d['slides'][1].update(layout=bind(self.u, 'checks/layout02.json')))
        self.fails('G06', 'bbox')

    def test_missing_design_confirmation(self):
        save(self.u / 'design-review/approvals.json', []); self.fails('G09')

    def test_global_feedback_not_closed_by_local_fix(self):
        save(self.u / 'design-review/feedback.json', [{'id': 'F1', 'scope': 'global', 'text': 'rejected', 'message_ref': 'test://reject',
            'evidence': bind(self.u, 'approval-evidence.txt'), 'status': 'resolved', 'resolution_version': 'simulation-1',
            'resolution_reason': 'local fix', 'resolution_evidence': bind(self.u, 'approval-evidence.txt'), 'confirmation_ref': 'old'}])
        self.fails('G09')

    def test_unchanged_resume(self):
        self.checkpoint_all(); self.assertTrue(self.e.resume()['complete'])

    def test_exercise_change_invalidates_checkpoint(self):
        self.checkpoint_all(); (self.u / 'exercises/prompt.txt').write_text('changed')
        self.assertEqual(self.e.resume()['resume_from'], 'image')

    def test_rehearsal_change_invalidates_checkpoint(self):
        self.checkpoint_all(); self.mutate('checks/rehearsal.json', lambda d: d.update(status='pending'))
        self.assertEqual(self.e.resume()['resume_from'], 'review')

    def test_no_figma_directory_required_by_checkpoints(self):
        self.assertFalse((self.u / 'figma').exists()); self.checkpoint_all()

    def test_role_boundary_and_history(self):
        self.e.write('image', 'exercises/prompt.txt', b'new prompt')
        self.assertTrue(list((self.u / 'history').rglob('prompt.txt')))
        with self.assertRaises(ValueError): self.e.write('sample', 'drafts/deck.pptx', b'denied')
        with self.assertRaises(ValueError): self.e.write('analysis', '../escape', b'denied')

    def test_simulation_cannot_finalize(self):
        with self.assertRaises(ValueError): self.e.finalize()
        self.assertFalse((self.u / 'final').exists())

    def test_retry_limit(self):
        self.assertEqual(self.e.retry('production', 'overlap'), 1)
        self.assertEqual(self.e.retry('production', 'overlap'), 2)
        with self.assertRaises(ValueError): self.e.retry('production', 'overlap')

    def test_exact_reference_mode(self):
        self.mutate('design-review/reference-lock.json', lambda d: [r.update(mode='exact') for r in d['templates']])
        self.refresh_bindings()
        self.assertTrue(self.e.check(['G08', 'G09'])['passed'])

    def test_declared_adoption_adjustment_passes(self):
        for tag in ['target', 'candidate']:
            self.mutate('design-review/cover-'+tag+'.json', lambda d: d['objects'][0].update(fill='#000000'))
        def update_lock(d):
            ref = d['templates'][0]
            ref['target']['layout'] = bind(self.u, 'design-review/cover-target.json')
            ref['recipe']['adjustments'] = [{'role': 'title', 'property': 'fill', 'reason': 'training theme'}]
        self.mutate('design-review/reference-lock.json', update_lock)
        self.mutate('design-review/review.json', lambda d: d['slides'][0].update(layout=bind(self.u, 'design-review/cover-candidate.json')))
        self.refresh_bindings()
        report = self.e.check(['G08', 'G09']); self.assertTrue(report['passed'], report)

    def test_selected_figma_positive_and_duplicate_nodes_rejected(self):
        self.mutate('input.json', lambda d: d['deliverables'].update(figma=True))
        self.change_plan(lambda p: p['deliverables'].update(figma=True))
        save(self.u / 'figma/mapping.json', {'url': 'https://www.figma.com/design/SIMULATION/test',
             'deck_sha256': digest(self.u / 'drafts/deck.pptx'), 'status': 'verified', 'reviewer': 'simulation', 'simulation': True,
             'evidence': bind(self.u, 'research/evidence.txt'), 'frames': [{'slide': i, 'node_id': f'0:{i}'} for i in range(1, 8)]})
        self.refresh_bindings()
        report = self.e.check(['G06']); self.assertTrue(report['passed'], report)
        self.mutate('figma/mapping.json', lambda d: d['frames'][1].update(node_id='0:1'))
        self.fails('G06', 'duplicate')

    def test_pdf_can_be_explicitly_omitted(self):
        self.mutate('input.json', lambda d: d['deliverables'].update(pdf=False))
        self.change_plan(lambda p: p['deliverables'].update(pdf=False))
        (self.u / 'drafts/deck.pdf').unlink()
        self.refresh_bindings()
        self.assertTrue(self.e.check(list(self.e.rules['gates']))['passed'])

    def test_text_only_observation_without_exercise_files(self):
        self.mutate('input.json', lambda d: (d.update(format='lecture'), d['deliverables'].update(exercises=False)))
        def change(p):
            p['format'] = 'lecture'; p['deliverables']['exercises'] = False
            p['exercises'][0].update(mode='observation', file_ids=[])
            p['slides'][-2]['activity'] = 'explanation'
        self.change_plan(change)
        save(self.u / 'assets/manifest.json', [a for a in read(self.u / 'assets/manifest.json') if a['id'] == 'LOGO'])
        self.refresh_bindings()
        report = self.e.check(list(self.e.rules['gates'])); self.assertTrue(report['passed'], report)

    def test_provided_logo_and_geometry_contract(self):
        report = self.e.check(list(self.e.rules['gates'])); self.assertTrue(report['passed'], report)
        self.mutate('checks/layout01.json', lambda d: next(o for o in d['objects'] if o['role'] == 'notiontalk_logo').update(visible_bbox=[0.8, 0.04, 0.16, 0.08]))
        self.mutate('checks/reviews.json', lambda d: d['slides'][0].update(layout=bind(self.u, 'checks/layout01.json')))
        self.fails('G06', 'brand reference mismatch')

    def test_final_delivery_copy_contract_in_isolation(self):
        # Only test the file-copy branch. Validation and resume are mocked explicitly;
        # this does not certify the fixture as a human-approved production course.
        self.e.test = False
        with patch.object(self.e, 'check', return_value={'passed': True, 'run_id': 'copy-only-test'}), \
             patch.object(self.e, 'resume', return_value={'complete': True}):
            self.e.finalize()
            self.e.finalize()
        for rel in ['deck.pptx', 'deck.pdf', 'script.docx', 'exercises/prompt.txt']:
            self.assertTrue((self.u / 'final' / rel).is_file())
        self.assertTrue((self.u / 'history/copy-only-test/final/deck.pdf').is_file())

    def test_final_protected_destination_denied_before_any_copy(self):
        (self.u / 'final').mkdir()
        (self.u / 'final/deck.pdf').write_text('protected')
        self.e = Engine(self.u, control=self.root / 'protected-final-control')
        self.e.baseline([self.u / 'final/deck.pdf'])
        with patch.object(self.e, 'check', return_value={'passed': True, 'run_id': 'copy-only-test'}), \
             patch.object(self.e, 'resume', return_value={'complete': True}):
            with self.assertRaises(ValueError): self.e.finalize()
        self.assertEqual((self.u / 'final/deck.pdf').read_text(), 'protected')
        self.assertFalse((self.u / 'final/deck.pptx').exists())

    def test_cli_exit_codes_and_machine_readable_report(self):
        command = [sys.executable, str(HERE / 'gate.py'), '--unit', str(self.u), '--control', str(self.root / 'control'), '--test-mode']
        result = subprocess.run(command + ['check', '--gate', 'G02'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)['passed'])
        save(self.u / 'approvals.json', [])
        result = subprocess.run(command + ['check', '--gate', 'G03'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)['passed'])
        result = subprocess.run(command + ['tool-preflight', 'figma-preview'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)['status'], 'blocked')

    def test_missing_brand_selection_requires_question(self):
        self.mutate('input.json', lambda d: d['branding'].pop('brand_id'))
        self.fails('G01', '이번에는 사이음/노션톡 중 무엇인가요?')

    def test_unknown_brand_requires_question(self):
        self.mutate('input.json', lambda d: d['branding'].update(brand_id='previous-course'))
        self.fails('G01', '이번에는 사이음/노션톡 중 무엇인가요?')

    def test_copyright_switch_changes_only_holder(self):
        from training_gate import copyright_text
        brand = copy.deepcopy(read(self.u / 'input.json')['branding'])
        brand['copyright'] = {'year': 2027, 'template': '© {year}. @{holder}. All rights reserved. / course footer'}
        brand['brand_id'] = 'scieum'
        before = copyright_text(self.e, brand)
        brand['brand_id'] = 'notiontalk'
        after = copyright_text(self.e, brand)
        self.assertEqual(before, '© 2027. @Sci_eum. All rights reserved. / course footer')
        self.assertEqual(after, before.replace('Sci_eum', 'NotionTalk'))

    def test_brand_logo_cannot_be_only_on_cover(self):
        self.mutate('input.json', lambda d: d['branding']['logos'][0].update(slides=[1]))
        self.fails('G01', 'every slide')

    def test_selected_brand_asset_cannot_be_replaced_by_text(self):
        self.mutate('input.json', lambda d: d['branding'].update(mode='text', logos=[]))
        self.change_plan(lambda p: p['branding'].update(mode='text', logos=[]))
        self.refresh_bindings()
        self.fails('G04', 'logo asset missing')

    def test_wrong_brand_logo_role_rejected(self):
        self.mutate('input.json', lambda d: d['branding']['logos'][0].update(role='sci_eum_logo'))
        self.fails('G01', 'selected brand')

    def test_logo_upper_right_required(self):
        self.mutate('checks/layout01.json', lambda d: next(o for o in d['objects'] if o['role']=='notiontalk_logo').update(visible_bbox=[0.1,0.04,0.15,0.08]))
        self.mutate('checks/reviews.json', lambda d: d['slides'][0].update(layout=bind(self.u,'checks/layout01.json')))
        self.fails('G06', 'upper right')

    def test_wrong_layout_copyright_holder_rejected(self):
        self.mutate('checks/layout01.json', lambda d: next(o for o in d['objects'] if o['role']=='copyright_footer').update(text='© 2026. Sci_eum. All rights reserved.'))
        self.mutate('checks/reviews.json', lambda d: d['slides'][0].update(layout=bind(self.u,'checks/layout01.json')))
        self.fails('G06', 'footer brand/text')

    def test_missing_ppt_copyright_footer_rejected(self):
        ppt_fixture(self.root / 'no-footer.pptx')
        with_notes(self.root / 'no-footer.pptx', self.u / 'drafts/deck.pptx', 7)
        self.fails('G05', 'copyright footer')

    def test_missing_layout_footer_rejected(self):
        self.mutate('checks/layout01.json', lambda d: d.update(objects=[o for o in d['objects'] if o['role']!='copyright_footer']))
        self.mutate('checks/reviews.json', lambda d: d['slides'][0].update(layout=bind(self.u,'checks/layout01.json')))
        self.fails('G06', 'copyright footer')

    def test_missing_selected_logo_on_body_slide_rejected(self):
        self.mutate('checks/layout02.json', lambda d: d.update(objects=[o for o in d['objects'] if o['role']!='notiontalk_logo']))
        self.mutate('checks/reviews.json', lambda d: d['slides'][1].update(layout=bind(self.u,'checks/layout02.json')))
        self.fails('G06', 'missing brand logo')

    def test_registered_black_white_variant_is_allowed(self):
        from training_gate import branding
        (self.u / 'assets/white.png').write_bytes(PNG + b'SIMULATION VARIANT')
        self.mutate('input.json', lambda d: d['branding']['logos'][0].update(variants={'white':bind(self.u,'assets/white.png')}))
        objects = {o['role']:o for o in read(self.u / 'checks/layout01.json')['objects']}
        objects['notiontalk_logo']['asset_sha256'] = digest(self.u / 'assets/white.png')
        branding(self.e, objects, 1)
        objects['notiontalk_logo']['asset_sha256'] = 'unregistered'
        with self.assertRaises(ValueError): branding(self.e, objects, 1)
