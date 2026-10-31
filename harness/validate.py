"""Run both profiles in isolated fixtures without external reference materials."""
import argparse
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
import uuid

from gate import Engine, digest, save, read
from test_training import TrainingTests, PNG, ppt_fixture, fixture
from test_copyright import CopyrightTests
import validate_science


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=['all', 'ai_training', 'science'], default='all')
    parser.add_argument('--source', help='optional legacy science PPTX, read only')
    parser.add_argument('--renders', help='legacy source render directory')
    parser.add_argument('--out', default=str(Path(__file__).with_name('validation')))
    args = parser.parse_args()
    if bool(args.source) != bool(args.renders):
        parser.error('--source and --renders must be supplied together')
    session = Path(args.out).resolve() / (dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8])
    session.mkdir(parents=True)
    source = Path(args.source).resolve() if args.source else session / 'science-parser-fixture.pptx'
    renders = Path(args.renders).resolve() if args.renders else session / 'science-renders'
    if not args.source:
        ppt_fixture(source)
        renders.mkdir()
        for i in range(1, 8):
            (renders / f'slide{i}.png').write_bytes(PNG)
    before = digest(source)
    suite = unittest.TestSuite()
    if args.profile in ['all', 'ai_training']:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(CopyrightTests))
    if args.profile in ['all', 'ai_training']:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TrainingTests))
    if args.profile in ['all', 'science']:
        validate_science.build_fixture(session, source, renders, Path(__file__).with_name('rules-science.json'))
        validate_science.GatesTest.template = session
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(validate_science.GatesTest))
    with (session / 'tests.log').open('w', encoding='utf-8') as log:
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    # Retain a complete, clearly marked training contract example for inspection.
    with tempfile.TemporaryDirectory(prefix='training-positive-') as temp:
        engine = fixture(Path(temp))
        positive = engine.check(list(engine.rules['gates']))
        production = Engine(engine.unit, control=Path(temp) / 'control').check(list(engine.rules['gates']))
    after = digest(source)
    summary = {'profile': args.profile, 'rules_version': read(Path(__file__).with_name('rules.json'))['version'], 'tests_run': result.testsRun,
               'failures': len(result.failures), 'errors': len(result.errors), 'skipped': len(result.skipped),
               'expected_results_match': result.wasSuccessful() and not result.skipped,
               'source_unchanged': before == after, 'training_simulation_all_gates_passed': positive['passed'],
               'production_rejects_simulation': not production['passed'],
               'failure_details': [{'test': str(t), 'trace': trace} for t, trace in result.failures + result.errors],
               'limits': ['Fixtures test records and parser behavior, not real user approval, UI fidelity, or tool execution.',
                          'No reference PDF, installed tool, external service, or Figma file is modified.',
                          'The local guard applies to harness-managed writes, not OS-wide access control.']}
    save(session / 'summary.json', summary)
    save(session / 'simulation-report.json', positive)
    save(session / 'production-rejection-report.json', production)
    save(Path(args.out).resolve() / 'latest.json', {'session': str(session), 'summary': str(session / 'summary.json')})
    print(json.dumps({k: v for k, v in summary.items() if k != 'failure_details'}, ensure_ascii=True, indent=2))
    print('Validation details: ' + str(session / 'tests.log'))
    return 0 if (summary['expected_results_match'] and summary['source_unchanged'] and positive['passed'] and not production['passed']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
