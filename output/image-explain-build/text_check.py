from pathlib import Path
import json
B=Path('output/image-explain-build');rows=json.loads((B/'application-text-bounds.json').read_text(encoding='utf-8-sig'));issues=[]
for t in rows:
 if t['slide']in[24,30,38]and t['name']!='copyright-footer'and(t['text_left']+t['text_width']>t['shape_left']+t['shape_width']+2 or t['text_top']+t['text_height']>t['shape_top']+t['shape_height']+2):issues.append(t)
print(json.dumps(issues,ensure_ascii=False))
