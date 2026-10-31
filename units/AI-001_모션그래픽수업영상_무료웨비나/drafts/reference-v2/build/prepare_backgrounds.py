"""Compose the selected original brand into course-specific document backgrounds.
The reusable library and original logo bytes remain unchanged.
"""
from pathlib import Path
import json
from PIL import Image, ImageOps

build=Path(__file__).resolve().parent
unit=build.parents[2]
repo=unit.parents[1]
library=repo/'assets/reference-templates'
out=build/'backgrounds'
out.mkdir(exist_ok=True)
spec=json.loads((library/'layouts.json').read_text(encoding='utf-8'))
catalog=json.loads((library/'catalog.json').read_text(encoding='utf-8'))
x,y,w,h=spec['common']['brand']
logo=Image.open(repo/'assets/branding/notiontalk-white.png').convert('RGBA')
placed=ImageOps.contain(logo,(w,h),Image.Resampling.LANCZOS)
for t in catalog['templates']:
    canvas=Image.open(library/t['background']).convert('RGBA')
    canvas.alpha_composite(placed,(x+(w-placed.width)//2,y+(h-placed.height)//2))
    canvas.convert('RGB').save(out/(t['id']+'.png'))
print('Prepared 5 branded document backgrounds from original assets.')
