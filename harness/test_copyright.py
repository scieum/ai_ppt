"""Isolated G10 regressions. No legal conclusion or real approval is simulated as fact."""
import copy
import tempfile
import unittest
from pathlib import Path
from gate import Engine, canonical, read, save
from test_training import fixture, copyright_fixture
from copyright_gate import scan


class CopyrightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='copyright-gate-')
        self.root = Path(self.temp.name)
        self.e = fixture(self.root)
        self.u = self.e.unit

    def tearDown(self):
        self.temp.cleanup()

    def mutate(self, rel, change):
        value = read(self.u / rel);change(value);save(self.u / rel, value)

    def fails(self, detail):
        result = self.e.check(['G10'])
        self.assertFalse(result['passed'], result)
        self.assertIn(detail, result['results'][0]['detail'])

    def rebind_inventory(self):
        self.mutate('rights/review.json', lambda r: r.update(inventory_hash=canonical(read(self.u / 'rights/inventory.json'))))

    def test_simulation_passes_all_ten(self):
        self.assertTrue(self.e.check(list(self.e.rules['gates']))['passed'])

    def test_production_rejects_simulated_copyright_review(self):
        self.assertFalse(Engine(self.u, control=self.root/'control').check(['G10'])['passed'])

    def test_missing_inventory(self):
        (self.u/'rights/inventory.json').unlink();self.fails('inventory missing')

    def test_missing_human_review(self):
        (self.u/'rights/review.json').unlink();self.fails('human copyright review missing')

    def test_plan_edit_invalidates_copyright_review(self):
        with (self.u/'plan.md').open('a',encoding='utf-8') as f:f.write('\nChanged slide wording')
        self.fails('stale copyright scope')

    def test_asset_edit_invalidates_review(self):
        with (self.u/'assets/logo.png').open('ab') as f:f.write(b'changed')
        self.fails('stale evidence')

    def test_new_reference_invalidates_review(self):
        self.mutate('research/sources.json',lambda s:s.append(dict(s[0],id='NEW')))
        self.fails('stale copyright scope')

    def test_new_output_invalidates_review(self):
        (self.u/'drafts/new.txt').write_text('not an active output')
        self.assertTrue(self.e.check(['G10'])['passed'])
        with (self.u/'drafts/script.docx').open('ab') as f:f.write(b'changed')
        self.fails('stale copyright scope')

    def test_pending_rights_issue_blocks(self):
        save(self.u/'rights/open-issues.json',[{'id':'reference-templates','status':'open'}])
        self.fails('unresolved copyright issues')

    def test_missing_reference_coverage(self):
        self.mutate('rights/inventory.json',lambda r:r['references'].pop());self.rebind_inventory()
        self.fails('reference coverage')

    def test_missing_asset_coverage(self):
        self.mutate('rights/inventory.json',lambda r:r['materials'].pop());self.rebind_inventory()
        self.fails('material coverage')

    def test_unknown_permission_not_cleared(self):
        self.mutate('rights/inventory.json',lambda r:r['materials'][0].update(basis='unresolved'));self.rebind_inventory()
        self.fails('unknown asset rights')

    def test_adaptation_cannot_be_declared_original(self):
        self.mutate('rights/inventory.json',lambda r:r['materials'][0].update(use='adapted'));self.rebind_inventory()
        self.fails('cannot be cleared as original')

    def test_permission_must_cover_pdf(self):
        self.mutate('rights/inventory.json',lambda r:r['materials'][0].update(allowed_uses=['live_presentation']));self.rebind_inventory()
        self.fails('distribution scope')

    def test_attribution_does_not_alone_clear_reproduction(self):
        self.mutate('rights/inventory.json',lambda r:r['references'][0].update(use='reproduced'));self.rebind_inventory()
        self.fails('not merely attribution')

    def test_exception_needs_reasoning(self):
        self.mutate('rights/inventory.json',lambda r:r['materials'][0].update(basis='exception_review'));self.rebind_inventory()
        self.fails('exception reasoning')

    def test_human_visual_review_required_even_without_matches(self):
        self.mutate('rights/review.json',lambda r:r['criteria'].pop('structure_and_visuals'))
        self.fails('criteria coverage')

    def test_agent_cannot_replace_human_review_record(self):
        self.mutate('rights/review.json',lambda r:r.update(actor='agent'))
        self.fails('human copyright reviewer')

    def test_stale_scan_rejected(self):
        self.mutate('rights/scan.json',lambda r:r.update(findings=[] if r['findings'] else [{'id':'invented'}]))
        self.fails('stale copyright similarity scan')

    def test_unresolved_literal_match_blocks(self):
        self.mutate('rights/review.json',lambda r:r['resolutions'].append({'finding_id':'extra'}))
        self.fails('copyright text findings')

    def test_literal_match_detection_ignores_spacing_and_punctuation(self):
        from gate import plan
        from validate_science import write_plan, bind
        phrase='Teacher authored activity sequence example'
        p=plan(self.u);p['slides'][0]['message']=phrase;write_plan(self.u,p)
        src=read(self.u/'research/sources.json')[0]
        path=self.u/src['evidence']['path'];path.write_text('Teacher, authored activity sequence example',encoding='utf-8')
        self.mutate('research/sources.json',lambda rows: [row.update(evidence=bind(self.u,src['evidence']['path'])) for row in rows if row['evidence']['path']==src['evidence']['path']])
        matches=scan(self.e)['findings']
        self.assertTrue(any(row['target']=='plan:slide1:message' for row in matches))

    def test_source_reuse_needs_rights_evidence(self):
        uses=read(self.u/'rights/inventory.json')['intended_uses']
        self.mutate('rights/inventory.json',lambda r:r['references'][0].update(use='quoted',basis='permission',allowed_uses=uses,evidence={'path':'rights/missing.txt','sha256':'0'*64}))
        self.rebind_inventory();self.fails('stale evidence')

    def test_production_and_publication_cannot_skip_new_gate(self):
        self.assertIn('G10',self.e.rules['stages']['production']['post'])
        for side in ['pre','post']:self.assertIn('G10',self.e.rules['stages']['review'][side])
        self.assertIn('G10',self.e.rules['tool_gates']['figma-publish'])

    def test_multiple_draft_writes_then_require_fresh_review(self):
        for rel in ['drafts/deck.pptx','drafts/script.docx']:
            self.e.write('production',rel,(self.u/rel).read_bytes()+b'changed')
        self.fails('stale copyright scope')
        self.assertFalse(self.e.checkpoint('production')['passed'])

    def test_human_plan_prose_is_scanned(self):
        phrase='Independently reviewed teaching example phrase'
        with (self.u/'plan.md').open('a',encoding='utf-8') as f:f.write('\n'+phrase)
        src=read(self.u/'research/sources.json')[0]
        path=self.u/src['evidence']['path'];path.write_text(phrase,encoding='utf-8')
        from validate_science import bind
        self.mutate('research/sources.json',lambda rows:[row.update(evidence=bind(self.u,src['evidence']['path'])) for row in rows if row['evidence']['path']==src['evidence']['path']])
        self.assertTrue(any(row['target']=='plan.md' for row in scan(self.e)['findings']))

    def test_broken_pdf_fails_as_gate_result(self):
        from validate_science import bind
        from copyright_gate import snapshot
        (self.u/'research/broken.pdf').write_bytes(b'%PDF-1.7\ninvalid')
        self.mutate('research/sources.json',lambda rows:rows[0].update(evidence=bind(self.u,'research/broken.pdf')))
        self.mutate('rights/review.json',lambda r:r.update(scope_hash=snapshot(self.e)['scope_hash']))
        self.fails('cannot read PDF')


if __name__ == '__main__':
    unittest.main()
