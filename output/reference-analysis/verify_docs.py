from pathlib import Path
import json, re, subprocess

root=Path(__file__).resolve().parents[2]
records=json.loads((root/'output/reference-analysis/inventory.json').read_text(encoding='utf-8'))
samples={
'R01':[1,2,3,10,20,55,76,87], 'R02':[4,8,23,37,52,70,91,103],
'R03':[2,6,9,14,27,31,35,37], 'R04':[1,6,10,11,15,25,39,46],
'R05':[4,8,15,24,31,37,44,52], 'R06':[1,2,12,25,38,52,67,80],
'R07':[1,2,15,25,37,49,65,79],
}
assert len(records)==7 and sum(r['page_count'] for r in records)==562
assert sum(map(len,samples.values()))==56
for r in records:
    assert all(1<=p<=r['page_count'] for p in samples[r['id']])
    assert Path(r['path']).is_file()
files=[root/'plan.md',root/'design.md',root/'docs/ai-training-reference-analysis.md',root/'AGENTS.md']
for file in files:
    content=file.read_text(encoding='utf-8')
    assert '\ufffd' not in content and '\x00' not in content, file
    if file.name!='AGENTS.md':
        assert content.count('```')%2==0, f'unbalanced code fence: {file}'
        for dest in re.findall(r'\]\(([^)]+)\)',content):
            if '://' not in dest and not dest.startswith('#'):
                assert (file.parent/dest.split('#')[0]).exists(), (file,dest)
        blocks=re.split(r'\n\s*\n',content)
        for block in blocks:
            lines=[line for line in block.splitlines() if line.startswith('|')]
            if lines:
                assert len({line.count('|') for line in lines})==1, ('table columns',file,lines)
    print(f'{file.relative_to(root)}: {len(content.splitlines())} lines; text/links/tables OK')
for row in [(60,5,5,10,10,15,10,5),(90,10,10,10,15,25,10,10),(120,10,10,15,20,35,15,15)]:
    assert row[0]==sum(row[1:])
old=subprocess.check_output(['git','show','HEAD:AGENTS.md'],cwd=root).decode('utf-8').replace('\r\n','\n')
new=(root/'AGENTS.md').read_text(encoding='utf-8')
assert new.endswith(old), 'existing AGENTS body changed'
changed=subprocess.check_output(['git','diff','--name-only'],cwd=root).decode().splitlines()
assert set(changed)=={'AGENTS.md','plan.md','design.md'}, changed
assert subprocess.check_output(['git','diff','--','harness','units'],cwd=root)==b''
print('Verified: 7 PDFs / 562 pages / 56 visual samples; time totals; original AGENTS body, harness code and science unit unchanged.')
