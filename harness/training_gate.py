"""AI training contracts. Evidence checks do not authenticate people or judge pixels."""
import datetime as dt
import math
import re

from gate import NS, canonical, evidence, local, plan, read, require


def text(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, allow_empty=False):
    return (isinstance(value, list) and (allow_empty or bool(value)) and
            all(text(x) for x in value) and len(value) == len(set(value)))


def number(value, minimum=0):
    return type(value) in [int, float] and math.isfinite(value) and value >= minimum


def date(value):
    require(text(value), 'verification date missing')
    require(dt.date.fromisoformat(value).isoformat() == value, 'use ISO date YYYY-MM-DD')


def environment(engine, value):
    require(isinstance(value, dict) and all(text(value.get(k)) for k in
            engine.rules['training']['environment_fields']), 'product/version/OS/UI language/account missing')


def actual(engine, row, label):
    require(engine.test or not row.get('simulation', False), 'simulated ' + label + ' in production')


def copyright_text(engine, brand):
    cfg = engine.rules['design_review']['branding']
    require(brand.get('brand_id') in cfg['brands'], cfg['selection_question'])
    footer = brand.get('copyright', {})
    template = footer.get('template')
    require(text(template) and template.count('{holder}') == 1 and template.count('{year}') <= 1,
            'copyright template needs exactly one {holder}')
    require(type(footer.get('year')) is int and 1000 <= footer['year'] <= 9999, 'copyright year required')
    result = template.replace('{holder}', cfg['brands'][brand['brand_id']]['holder']).replace('{year}', str(footer['year']))
    require('{' not in result and '}' not in result, 'unknown copyright template placeholder')
    return result


def training_input(engine):
    data = read(engine.unit / 'input.json')
    require(data.get('profile') == 'ai_training', 'input.profile must be ai_training; legacy science needs --rules harness/rules-science.json')
    require(text(data.get('unit')) and text(data.get('audience')), 'training unit/audience missing')
    require(data.get('format') in engine.rules['training']['formats'], 'invalid training format')
    require(type(data.get('target_slides')) is int and data['target_slides'] > 0, 'invalid slide count')
    require(number(data.get('minutes')) and data['minutes'] > 0, 'invalid training minutes')
    environment(engine, data.get('environment'))
    objectives(data)
    delivery = data.get('deliverables')
    require(isinstance(delivery, dict) and set(delivery) == {'pdf', 'figma', 'exercises'} and
            all(type(v) is bool for v in delivery.values()), 'explicit boolean PDF/Figma/exercises delivery contract required')
    brand = data.get('branding', {})
    copyright_text(engine, brand)
    require(brand.get('mode') in ['text', 'logo'] and text(brand.get('label')) and
            isinstance(brand.get('logos'), list), 'explicit text/logo branding contract required')
    require((brand['mode'] == 'logo') == bool(brand['logos']), 'logo mode and supplied logos disagree')
    roles = []
    for logo in brand['logos']:
        role = logo.get('role')
        require(text(role) and role.endswith('_logo'), 'brand role must end in _logo')
        roles.append(role)
        slides = logo.get('slides')
        require(isinstance(slides, list) and slides and len(slides) == len(set(slides)) and
                all(type(n) is int and 1 <= n <= data['target_slides'] for n in slides), 'invalid brand slide coverage')
        evidence(engine.unit, logo['file'])
        require(role == engine.rules['design_review']['branding']['brands'][brand['brand_id']]['role'], 'logo does not match selected brand')
        require(sorted(slides) == list(range(1, data['target_slides'] + 1)), 'selected brand logo is required on every slide')
        for variant in logo.get('variants', {}).values():
            evidence(engine.unit, variant)
    require(len(roles) == len(set(roles)), 'duplicate brand role')
    require(len(roles) <= 1, 'use only the selected course brand')
    return data


def semantic_plan(root, data):
    """Bind approval to delivery choices, exercises and research, excluding routine layout edits."""
    result = {k: v for k, v in data.items() if k not in ['slides', 'design']}
    result['slides'] = [{k: v for k, v in row.items() if k not in ['layout', 'visual', 'character', 'title']}
                        for row in data['slides']]
    result['input'] = read(root / 'input.json')
    result['content'] = read(root / 'research/content-map.json')
    result['sources'] = read(root / 'research/sources.json')
    return result


def objectives(data):
    rows = data.get('objectives')
    require(isinstance(rows, list) and rows, 'performance objectives missing')
    ids = [r['id'] for r in rows]
    require(strings(ids) and all(text(r.get('action')) and text(r.get('result')) for r in rows),
            'objectives need unique ID, observable action and result')
    return set(ids)


def research(engine):
    inp = training_input(engine)
    goals = objectives(inp)
    sources = read(engine.unit / 'research/sources.json')
    rows = read(engine.unit / 'research/content-map.json')
    require(isinstance(sources, list) and sources and isinstance(rows, list) and rows, 'empty training research')
    ids = [s['id'] for s in sources]
    require(strings(ids), 'duplicate/empty source ID')
    roles = {s.get('role') for s in sources}
    require(roles <= set(engine.rules['source_roles']), 'unknown source role')
    for group in engine.rules['required_source_role_groups']:
        require(roles & set(group), 'content/official and design references required')
    official = set()
    for source in sources:
        require(text(source.get('citation')) and text(source.get('locator')), 'source citation/location missing')
        evidence(engine.unit, source['evidence'])
        actual(engine, source, 'source verification')
        if source['role'] == 'official':
            require(re.fullmatch(r'https://[^\s]+', source.get('url', '')), 'official HTTPS documentation URL required')
            date(source.get('checked_on'))
            official.add(source['id'])
    require(strings([r['id'] for r in rows]), 'duplicate/empty content ID')
    for row in rows:
        require(row.get('scope') in engine.rules['allowed_scope'], 'unclassified training content')
        require(row.get('kind') in engine.rules['training']['content_kinds'], 'unknown training content kind')
        require(text(row.get('claim')) and text(row.get('rationale')), 'content reasoning missing')
        require(strings(row.get('source_ids')) and set(row['source_ids']) <= set(ids), 'unknown/empty content source IDs')
        require(strings(row.get('objective_ids'), row['scope'] == '제외') and
                set(row['objective_ids']) <= goals, 'content objective missing/unknown')
        if row['scope'] == '선택·심화':
            require(text(row.get('inclusion_reason')) and text(row.get('separation')), 'supplementary justification missing')
        if row['kind'] == 'technical' and row['scope'] != '제외':
            require(set(row['source_ids']) & official, 'technical content requires official documentation')
            verification = row.get('verification', {})
            require(verification.get('status') == 'verified', 'technical procedure is unverified')
            date(verification.get('checked_on'))
            require(verification.get('environment') == inp['environment'], 'technical verification environment mismatch')
            evidence(engine.unit, verification['evidence'])
            actual(engine, verification, 'technical verification')


def planning(engine):
    p, inp = plan(engine.unit), training_input(engine)
    require(all(k in p and p[k] is not None for k in engine.rules['plan_fields']), 'training plan fields missing')
    for key in ['profile', 'unit', 'audience', 'format', 'environment', 'objectives', 'target_slides', 'minutes', 'deliverables', 'branding']:
        require(p.get(key) == inp.get(key), 'input-plan mismatch: ' + key)
    require(text(p['design']), 'design guide missing')
    n = p['target_slides']
    require(isinstance(p['slides'], list) and len(p['slides']) == n and
            [s['number'] for s in p['slides']] == list(range(1, n + 1)), 'slide count/numbering mismatch')
    goals = objectives(p)
    rows = read(engine.unit / 'research/content-map.json')
    included = {r['id'] for r in rows if r['scope'] != '제외'}
    source_ids = {s['id'] for s in read(engine.unit / 'research/sources.json')}
    exercises = p['exercises']
    require(isinstance(exercises, list) and exercises, 'at least one hands-on or observation exercise required')
    exids = [e['id'] for e in exercises]
    require(strings(exids), 'duplicate/empty exercise ID')
    covered, used, seen_ex, duration = set(), set(), set(), {}
    for s in p['slides']:
        require(all(k in s and s[k] is not None for k in engine.rules['slide_fields']), 'training slide fields missing')
        require(all(text(s[k]) for k in ['title', 'message', 'layout', 'character', 'instructor_action', 'learner_action']), 'empty training slide description')
        require(s['activity'] in engine.rules['training']['activities'], 'unknown slide activity')
        require(s['design_type'] in engine.rules['design_review']['types'], 'unknown slide design type')
        require(number(s['minutes']) and s['minutes'] > 0, 'invalid slide minutes')
        require(strings(s['visual'], True), 'visual must be unique asset IDs')
        require(strings(s['content_ids']) and set(s['content_ids']) <= included, 'excluded/unknown content in plan')
        require(strings(s['source_ids']) and set(s['source_ids']) <= source_ids, 'slide source missing')
        require(strings(s['objective_ids'], True) and set(s['objective_ids']) <= goals, 'unknown slide objective')
        require(strings(s['exercise_ids'], True) and len(s['exercise_ids']) <= 1 and
                set(s['exercise_ids']) <= set(exids), 'unknown/overlapping exercise on slide')
        if s['activity'] in ['guided_practice', 'practice', 'check', 'troubleshooting']:
            require(s['exercise_ids'], 'practice/check/error slide needs exercise ID')
        used.update(s['content_ids'])
        seen_ex.update(s['exercise_ids'])
        for eid in s['exercise_ids']:
            duration[eid] = duration.get(eid, 0) + s['minutes']
    require(used == included, 'included content missing from plan')
    require(seen_ex == set(exids), 'exercise not connected to slides')
    tolerance = engine.rules['training']['minutes_tolerance']
    rest = p.get('break_minutes', 0)
    require(number(rest), 'invalid break minutes')
    require(abs(sum(s['minutes'] for s in p['slides']) + rest - p['minutes']) <= tolerance,
            'slide/break time does not equal total minutes')
    for ex in exercises:
        require(all(k in ex and ex[k] is not None for k in engine.rules['training']['exercise_fields']), 'exercise card fields missing')
        require(ex['mode'] in engine.rules['training']['exercise_modes'], 'unknown exercise mode')
        require(strings(ex['objective_ids']) and set(ex['objective_ids']) <= goals, 'unknown exercise objective')
        covered.update(ex['objective_ids'])
        require(all(text(ex[k]) for k in ['title', 'start_conditions', 'input_location', 'expected_result', 'fallback', 'customization']), 'exercise instructions/result/fallback missing')
        require(strings(ex['instructions']) and strings(ex['success_criteria']), 'exercise needs steps and observable success criteria')
        require(strings(ex['file_ids'], True) and strings(ex['source_ids']) and set(ex['source_ids']) <= source_ids,
                'exercise file/source references invalid')
        require(isinstance(ex['errors'], list) and ex['errors'] and all(all(text(e.get(k)) for k in
                ['symptom', 'check', 'action', 'expected_state']) for e in ex['errors']), 'error recovery path missing')
        require(number(ex['minutes']) and ex['minutes'] > 0 and abs(duration[ex['id']] - ex['minutes']) <= tolerance,
                'exercise time does not match connected slides')
        linked = [s for s in p['slides'] if ex['id'] in s['exercise_ids']]
        require(all(set(ex['objective_ids']) <= set(s['objective_ids']) for s in linked), 'exercise/slide objective mismatch')
        if ex['mode'] == 'hands_on':
            require(any(s['activity'] in ['guided_practice', 'practice'] for s in linked), 'hands-on exercise has no learner practice')
        require(any(s['activity'] == 'check' for s in linked), 'exercise has no result-check slide')
    require(covered == goals, 'performance objective lacks exercise/observation and success check')
    supplementary = {r['id']: {k: r[k] for k in ['inclusion_reason', 'separation', 'source_ids']}
                     for r in rows if r['scope'] == '선택·심화'}
    require(p.get('supplementary', {}) == supplementary, 'supplementary content not embedded in plan')


def exercise_files(engine):
    return [a for a in read(engine.unit / 'assets/manifest.json')
            if a.get('kind') in engine.rules['training']['file_kinds']]


def assets(engine):
    p, inp = plan(engine.unit), training_input(engine)
    require(inp['branding']['mode'] == 'logo' and len(inp['branding']['logos']) == 1,
            'selected brand logo asset missing; resolve original asset before production')
    rows = read(engine.unit / 'assets/manifest.json')
    require(isinstance(rows, list), 'asset manifest must be an array (empty allowed for text-only lesson)')
    expected = {x for s in p['slides'] for x in s['visual']} | {x for e in p['exercises'] for x in e['file_ids']}
    require(len({a['id'] for a in rows}) == len(rows) and {a['id'] for a in rows} == expected, 'planned asset IDs mismatch')
    paths = [a['file']['path'] for a in rows]
    require(len(paths) == len(set(paths)), 'asset file paths must be unique')
    sources = {s['id'] for s in read(engine.unit / 'research/sources.json')}
    for a in rows:
        evidence(engine.unit, a['file'])
        require(text(a.get('purpose')) and a.get('kind') in engine.rules['training']['asset_kinds'], 'asset kind/purpose missing')
        require(a.get('review') == 'passed' and text(a.get('reviewer')), 'asset review incomplete')
        actual(engine, a, 'asset review')
        if a['kind'] in ['screenshot', 'crop']:
            require(a.get('source_id') in sources and text(a.get('locator')), 'capture/crop source location missing')
        else:
            require(text(a.get('provenance')), 'asset provenance missing')
        if a['kind'] == 'screenshot' or a.get('purpose_type') == 'tool_ui':
            require(a['kind'] in ['screenshot', 'crop'], 'tool UI evidence must be an actual screenshot/crop')
            date(a.get('checked_on'))
            require(a.get('environment') == inp['environment'], 'capture environment mismatch')
        if a['kind'] in engine.rules['training']['file_kinds']:
            require(a['file']['path'].startswith('exercises/'), 'exercise files must live under exercises/')
        else:
            require(a['file']['path'].startswith('assets/'), 'visual assets must live under assets/')
    fileids = {a['id'] for a in exercise_files(engine)}
    require({x for e in p['exercises'] for x in e['file_ids']} <= fileids, 'exercise file ID points to a visual asset')
    require(inp['deliverables']['exercises'] == bool(fileids), 'exercise file delivery contract mismatch')


def deliverables(engine, script_texts, ppt_slides):
    inp, p = training_input(engine), plan(engine.unit)
    footer = copyright_text(engine, inp['branding'])
    require(all(footer in ''.join(s['texts']) for s in ppt_slides), 'PPT copyright footer is missing or uses the wrong brand')
    if inp['deliverables']['pdf']:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ValueError('PDF validation requires pypdf: python -m pip install -r harness/requirements.txt') from exc
        try:
            reader = PdfReader(engine.unit / 'drafts/deck.pdf', strict=True)
            require(not reader.is_encrypted, 'delivery PDF must not be encrypted')
            require(len(reader.pages) == p['target_slides'], 'PDF page count mismatch')
            require(all(float(pg.mediabox.width) > 0 and float(pg.mediabox.height) > 0 for pg in reader.pages), 'invalid PDF page bounds')
        except Exception as exc:
            raise ValueError('PDF validation failed: ' + str(exc)) from exc
    cfg = engine.rules['training']
    for i, slide in enumerate(p['slides'], 1):
        start = script_texts.index('Slide ' + str(i)) + 1
        end = script_texts.index('Slide ' + str(i + 1)) if i < len(p['slides']) else len(script_texts)
        body = '\n'.join(script_texts[start:end])
        require(cfg['script_speech_label'] in body, 'speaker speech label missing: slide ' + str(i))
        if slide['activity'] in ['demo', 'guided_practice', 'practice', 'troubleshooting']:
            require(cfg['script_action_label'] in body, 'demonstration action label missing: slide ' + str(i))
        if slide['activity'] in ['guided_practice', 'practice']:
            require(cfg['script_wait_label'] in body, 'learner wait instruction missing: slide ' + str(i))


def rehearsal(engine):
    inp, p = training_input(engine), plan(engine.unit)
    data = read(engine.unit / 'checks/rehearsal.json')
    from gate import plan_hash
    require(data.get('plan_hash') == plan_hash(engine.unit) and data.get('artifacts') == engine.artifact_binding(), 'stale rehearsal plan/artifacts')
    require(data.get('status') == 'passed' and text(data.get('reviewer')), 'rehearsal incomplete')
    require(number(data.get('elapsed_minutes')) and 0 < data['elapsed_minutes'] <= p['minutes'], 'rehearsal exceeds available time')
    require(data.get('environment') == inp['environment'], 'rehearsal environment mismatch')
    date(data.get('checked_on'))
    evidence(engine.unit, data['evidence'])
    actual(engine, data, 'rehearsal')
    rows = data.get('exercises', [])
    require(len(rows) == len(p['exercises']) and {r['id'] for r in rows} == {e['id'] for e in p['exercises']}, 'rehearsal exercise coverage mismatch')
    byid = {r['id']: r for r in rows}
    for ex in p['exercises']:
        row = byid[ex['id']]
        require(row.get('status') == 'passed' and text(row.get('reviewer')), 'exercise rehearsal not passed')
        require(row.get('environment') == inp['environment'], 'exercise rehearsal environment mismatch')
        date(row.get('checked_on'))
        actual(engine, row, 'exercise rehearsal')
        results = row.get('criteria_results', [])
        require([r.get('criterion') for r in results] == ex['success_criteria'] and
                all(r.get('status') == 'passed' for r in results), 'exercise success criteria not demonstrated')
        for key in ['evidence', 'recovery_evidence', 'fallback_evidence']:
            evidence(engine.unit, row[key])
    links = p.get('links', [])
    require(strings(links, True) and all(re.fullmatch(r'https?://[^\s]+', u) for u in links), 'plan links must be unique HTTP(S) URLs')
    checks = data.get('links', [])
    require(len(checks) == len(links) and {r['url'] for r in checks} == set(links), 'distribution link check coverage mismatch')
    for row in checks:
        require(row.get('status') == 'passed', 'distribution link not verified')
        evidence(engine.unit, row['evidence'])
        actual(engine, row, 'link check')


def snapshot(engine, binding, artifact_key):
    value = read(evidence(engine.unit, binding['layout']))
    require(value.get('artifact_sha256') == binding[artifact_key]['sha256'] and
            value.get('render_sha256') == binding['render']['sha256'], 'layout export is not bound to artifact/render')
    require(text(value.get('exporter')) and value.get('canvas') == engine.rules['design_review']['canvas'], 'normalised layout export missing')
    rows = value.get('objects')
    require(isinstance(rows, list) and rows and strings([o['role'] for o in rows]), 'empty/duplicate layout roles')
    for obj in rows:
        require(all(k in obj for k in engine.rules['design_review']['locked_properties']), 'layout property missing')
        box = obj['bbox']
        require(isinstance(box, list) and len(box) == 4 and all(number(v) for v in box) and
                box[2] > 0 and box[3] > 0 and box[0] + box[2] <= 1 and box[1] + box[3] <= 1, 'invalid normalised bbox')
    return {o['role']: o for o in rows}


def compare(engine, left, right):
    require(set(left) == set(right), 'reference object role omitted or invented')
    for role in left:
        for key in engine.rules['design_review']['locked_properties']:
            if key == 'bbox':
                require(all(abs(a-b) <= engine.rules['design_review']['bbox_tolerance'] for a, b in
                            zip(left[role][key], right[role][key])), 'reference position/scale mismatch: ' + role)
            else:
                require(left[role][key] == right[role][key], 'reference ' + key + ' mismatch: ' + role)


def in_region(box, region):
    x, y, w, h = region
    return (isinstance(box, list) and len(box) == 4 and all(number(v) for v in box) and
            box[2] > 0 and box[3] > 0 and box[0] >= x and box[1] >= y and
            box[0] + box[2] <= x + w and box[1] + box[3] <= y + h)


def branding(engine, objects, slide):
    logos = training_input(engine)['branding']['logos']
    expected = {r['role']: r for r in logos}
    found = {k: o for k, o in objects.items() if k.endswith('_logo')}
    require(set(found) == set(expected), 'undeclared/missing brand logo on slide ' + str(slide))
    for role, spec in expected.items():
        obj = found[role]
        allowed = {spec['file']['sha256']} | {v['sha256'] for v in spec.get('variants', {}).values()}
        require(obj.get('asset_sha256') in allowed, 'brand logo does not use provided asset')
        box = obj.get('visible_bbox')
        require(isinstance(box, list) and len(box) == 4 and all(number(v) for v in box) and
                box[2] > 0 and box[3] > 0, 'brand visible bounds missing')
        require(in_region(box, engine.rules['design_review']['branding']['logo_region']), 'brand logo must be in the upper right')
    footer = objects.get('copyright_footer', {})
    require(footer.get('text') == copyright_text(engine, training_input(engine)['branding']), 'copyright footer brand/text mismatch')
    require(in_region(footer.get('bbox'), engine.rules['design_review']['branding']['footer_region']), 'copyright footer must be at the bottom')


def design_review(engine, current_plan_hash):
    cfg, root = engine.rules['design_review'], engine.unit
    lock = read(root / 'design-review/reference-lock.json')
    data = read(root / 'design-review/review.json')
    inp = training_input(engine)
    require(lock.get('unit') == inp['unit'] == data.get('unit'), 'wrong design-review unit')
    require(data.get('plan_hash') == current_plan_hash and data.get('reference_hash') == canonical(lock), 'stale design plan/reference lock')
    require(text(data.get('version')), 'design version missing')
    actual(engine, data, 'design review')
    refs, rows = lock.get('templates', []), data.get('slides', [])
    for items in [refs, rows]:
        require(len(items) == len(cfg['types']) and sorted(r['type'] for r in items) == sorted(cfg['types']), 'all seven design types required exactly once')
        require(strings([r['id'] for r in items]), 'duplicate/empty design ID')
    bytype = {r['type']: r for r in refs}
    for row in rows:
        ref = bytype[row['type']]
        require(row.get('reference_id') == ref['id'], 'candidate substituted reference')
        require(type(ref.get('slide')) is int and ref['slide'] > 0, 'reference PDF page/PPTX slide missing')
        require(type(row.get('slide')) is int and row['slide'] > 0, 'candidate representative page missing')
        if row['type'] == 'cover':
            require(row['slide'] == 1, 'cover must be first slide')
        for binding, keys in [(ref, ['source', 'render', 'layout']), (row, ['artifact', 'render', 'layout', 'comparison'])]:
            for key in keys:
                evidence(root, binding[key])
        source = snapshot(engine, ref, 'source')
        candidate = snapshot(engine, row, 'artifact')
        require(ref.get('mode') in cfg['reference_modes'], 'explicit exact/adopt reference mode required')
        expected = source
        if ref['mode'] == 'adopt':
            recipe = ref.get('recipe', {})
            require(strings(recipe.get('adopted')) and strings(recipe.get('replaced'), True) and
                    isinstance(recipe.get('adjustments'), list), 'adoption recipe missing')
            for key in ['artifact', 'render', 'layout']:
                evidence(root, ref['target'][key])
            expected = snapshot(engine, ref['target'], 'artifact')
            changes = set()
            for role in set(source) | set(expected):
                if role not in source or role not in expected:
                    changes.add((role, '__role__'))
                else:
                    properties = cfg['locked_properties'] + (cfg['branding']['locked_properties'] if role.endswith('_logo') else [])
                    changes.update((role, k) for k in properties if source[role].get(k) != expected[role].get(k))
            adjustments = recipe['adjustments']
            require(all(text(a.get('role')) and text(a.get('property')) and text(a.get('reason')) for a in adjustments), 'adoption adjustment reason missing')
            declared = {(a['role'], a['property']) for a in adjustments}
            require(declared == changes and len(declared) == len(adjustments), 'adoption changes must be declared exactly; no silent reference relaxation')
        require(set(cfg['required_roles'][row['type']]) <= set(expected), 'mandatory training layout role missing')
        compare(engine, expected, candidate)
        branding(engine, candidate, row['slide'])
        for role in candidate:
            if role.endswith('_logo'):
                for key in cfg['branding']['locked_properties']:
                    require(key in expected[role] and candidate[role].get(key) == expected[role][key], 'brand reference geometry/asset mismatch')
        require(text(row.get('reviewer')) and text(row.get('reason')), 'design judgement missing')
        actual(engine, row, 'design row')
        criteria = row.get('criteria', {})
        require(set(criteria) == set(cfg['criteria']), 'design criteria missing/unknown')
        for category, result in criteria.items():
            require(result.get('status') in ['passed', 'not_applicable'] and text(result.get('reason')) and
                    text(result.get('reviewer')), 'failed/unverified design item: ' + category)
            if result['status'] == 'not_applicable':
                require(category in cfg['optional_criteria'], 'mandatory design item cannot be not_applicable')
                if category == 'character_identity':
                    require(all(o.get('character_asset_id') in [None, '', 'none'] for o in candidate.values()), 'character present but identity review skipped')
            evidence(root, result['evidence'])
            actual(engine, result, 'design judgement')
    return data


def full_deck_layouts(engine, rows, deck_hash):
    lock = read(engine.unit / 'design-review/reference-lock.json')
    templates = {r['type']: r for r in lock['templates']}
    p = plan(engine.unit)
    for row in rows:
        objects = snapshot(engine, dict(row, artifact={'sha256': deck_hash}), 'artifact')
        branding(engine, objects, row['number'])
        for logo in training_input(engine)['branding']['logos']:
            if row['number'] not in logo['slides']:
                continue
            # The approved representative of the page's type locks visible logo geometry.
            kind = p['slides'][row['number'] - 1]['design_type']
            template = templates[kind]
            binding, key = (template['target'], 'artifact') if template['mode'] == 'adopt' else (template, 'source')
            expected = snapshot(engine, binding, key)
            require(logo['role'] in expected, 'logo has no reference geometry for this slide type')
            for prop in engine.rules['design_review']['branding']['locked_properties']:
                require(objects[logo['role']].get(prop) == expected[logo['role']].get(prop), 'full-deck brand reference mismatch')
