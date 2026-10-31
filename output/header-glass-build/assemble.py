from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import json, shutil, hashlib
B=Path(__file__).resolve().parent; R=B.parent.parent
audit=json.loads((B/'source-audit.json').read_text(encoding='utf-8'))
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
ASSET=R/'assets/tool-logos/glass-v3';ASSET.mkdir(parents=True,exist_ok=True)
generated=Path('C:/Users/User/.codex/generated_images/01a17c20-5bae-7d62-b099-b665b7e19a91')
names={'claude':'exec-0ada6fa8-0d85-4eba-9aa1-47af661ebfd3.png','codex':'exec-f246c392-7c1b-4e1d-a911-9cc68cebf714.png','higgsfield':'exec-b64a2798-10c4-4437-a8cf-6a85b2997eec.png'}
prompt='Edit the supplied {name} app-icon tile as a production slide asset. Preserve the exact recognizable logo silhouette, proportions, center position, front-facing orientation, rounded square tile footprint and generous transparent margin of the reference. Replace its matte dark tile and orange corner lines with restrained smoked-clear glass: neutral graphite transparency, subtle silver rim, gentle soft white reflection at top-left and a thin refractive glass edge. The tile must look like thin premium glass, not chrome or chunky ice. Recolor the central logo to crisp ivory white, clean and flat enough to remain readable at small sizes. Remove ALL orange, warm tint, neon colors, corner decorations, underlines and accent marks. No letters or captions, no extra symbols, no backdrop or cast shadow outside tile. True transparent background around the rounded square. Square composition, tile occupies exactly about 70 percent of canvas width and height, centered, matching source placement. Keep logo topology accurate. This is an edit of the existing logo tile, not a new logo design.'
manifest=[]
for name,file in names.items():
 dest=ASSET/f'{name}-front.png';shutil.copy2(generated/file,dest)
 manifest.append({'name':name,'tool':'built-in image_gen.imagegen','reference':f'assets/tool-logos/orange-v2/png/{name}-front.png','generated_path':str(generated/file),'asset':str(dest.relative_to(R)),'transparent_background':True,'prompt':prompt.format(name=name),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
(ASSET/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(ASSET/'README.md').write_text('# 준비물용 유리 질감 로고\n\n2026-10-30 사용자 요청에 따라 기존 주황 로고 타일을 built-in ImageGen으로 편집했습니다. 흰색 로고와 중성 회색 유리 질감, 투명 배경을 사용합니다. 준비물 3쪽에만 적용하며 기존 자산은 보존합니다.\n\n세 PNG와 원본 경로·생성 프롬프트·해시는 manifest.json에 기록했습니다. 브랜드 원본 벡터가 아닌 기존 타일의 생성형 편집 자산입니다.\n',encoding='utf-8')
with ZipFile(audit['source']) as z: data={n:z.read(n) for n in z.namelist()}
with ZipFile(B/'container.pptx') as z:
 native=E.fromstring(z.read('ppt/slides/slide1.xml')).find('.//p:sp/p:spPr',N)
selected={'part_label','section_number','section_heading','part-label','group-number','group-label','part','group'}
changes=[];modified=[]
for index,part in enumerate(audit['parts'],1):
 root=E.fromstring(data[part]);dirty=False
 for sp in root.findall('.//p:sp',N):
  name=sp.find('p:nvSpPr/p:cNvPr',N).get('name')
  if name in selected:
   before=sp.xpath('.//@sz')
   assert before,(index,name)
   for el in sp.xpath('.//*[@sz]'):el.set('sz',str(int(el.get('sz'))+200))
   changes.append({'slide':index,'name':name,'before_pt':sorted(set(int(v)/100 for v in before)),'after_pt':sorted(set(int(v)/100+2 for v in before))})
   if name=='section_number':
    ext=sp.find('p:spPr/a:xfrm/a:ext',N);ext.set('cx',str(int(ext.get('cx'))+76200))
   if name=='section_heading':
    off=sp.find('p:spPr/a:xfrm/a:off',N);ext=sp.find('p:spPr/a:xfrm/a:ext',N)
    off.set('x',str(int(off.get('x'))+76200));ext.set('cx',str(int(ext.get('cx'))-76200))
   dirty=True
  if index==3 and name=='required':
   prior=sp.find('p:spPr',N);replacement=deepcopy(native)
   replacement.replace(replacement.find('a:xfrm',N),deepcopy(prior.find('a:xfrm',N)))
   sp.replace(prior,replacement);dirty=True
 if dirty:
  data[part]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True);modified.append(part)
prep=audit['parts'][2];rp='ppt/slides/_rels/'+Path(prep).name+'.rels'
rels=E.fromstring(data[rp])
for pic,name in zip([31,33,35],names):
 item=next(p for p in audit['prep'] if p.get('pic_id')==str(pic))
 rel=next(x for x in rels if x.get('Id')==item['rid']); rel.set('Target',f'../media/header-glass-{name}.png')
 data[f'ppt/media/header-glass-{name}.png']=(ASSET/f'{name}-front.png').read_bytes()
data[rp]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as z:
 for n,v in data.items():z.writestr(n,v)
(B/'changes.json').write_text(json.dumps({'headers':changes,'modified_slide_parts':modified,'prep_relationships':rp},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Changed {len(changes)} mini headers on {len(modified)} slides; three logos; one editable text container')
