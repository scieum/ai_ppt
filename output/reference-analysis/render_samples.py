from pathlib import Path
from PIL import Image, ImageDraw
import json, subprocess, shutil
from concurrent.futures import ThreadPoolExecutor

out = Path(__file__).parent
records = json.loads((out / 'inventory.json').read_text(encoding='utf-8'))
samples = {
 'R01': [1,2,3,10,20,55,76,87],
 'R02': [4,8,23,37,52,70,91,103],
 'R03': [2,6,9,14,27,31,35,37],
 'R04': [1,6,10,11,15,25,39,46],
 'R05': [4,8,15,24,31,37,44,52],
 'R06': [1,2,12,25,38,52,67,80],
 'R07': [1,2,15,25,37,49,65,79],
}
poppler = shutil.which('pdftoppm')
def render(rec):
    rid = rec['id']
    imgs = []
    for p in samples[rid]:
        prefix = out / f'{rid}-p{p:03}'
        subprocess.run([poppler, '-f', str(p), '-l', str(p), '-scale-to-x', '960', '-scale-to-y', '-1', '-singlefile', '-png', rec['path'], str(prefix)], capture_output=True, check=True)
        imgs.append((p, prefix.with_suffix('.png')))
    sheet = Image.new('RGB', (1920, 4 * 572), '#d5d5d5')
    d = ImageDraw.Draw(sheet)
    for n, (p, file) in enumerate(imgs):
        x,y = (n % 2) * 960, (n // 2) * 572
        d.text((x+10, y+8), f'{rid} / PDF p.{p}', fill='black')
        with Image.open(file) as im:
            sheet.paste(im.convert('RGB'), (x, y+30))
    sheet.save(out / f'{rid}-samples.jpg', quality=90)
    print(f'{rid}: rendered {samples[rid]}', flush=True)
with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(render, records))
