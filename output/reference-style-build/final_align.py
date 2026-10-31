from pathlib import Path
B=Path('output/reference-style-build');p=B/'author.mjs';s=p.read_text(encoding='utf8').replace("963,548,140,19,C.muted,false,'right'","1010,548,130,19,C.muted,false,'left'").replace("428,557,210","535,557,210").replace("370,599,610","335,599,610");p.write_text(s,encoding='utf8')
s=(B/'finalize-repair.mjs').read_text(encoding='utf-8-sig').replace('publish-final/','publish-final-2/').replace('final-validation-repair.json','final-validation-complete.json');(B/'publish-final-2').mkdir(exist_ok=True);(B/'finalize-complete.mjs').write_text(s,encoding='utf8')
