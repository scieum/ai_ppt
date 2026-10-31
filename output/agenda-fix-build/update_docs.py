from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from PIL import Image,ImageDraw
import json,hashlib,re,shutil
B=Path(__file__).resolve().parent;R=B.parents[1];A=R/'assets/layout-library-20261028';U=next((R/'units').glob('AI-001*'));lib=A/'NotionTalk_상황별레이아웃_20종_v4.pptx'
for p,imp in[(R/'output/layout-library-build/author-library.mjs',"import{roundedAgendaContent}from'../../assets/layout-library-20261028/recipes/rounded-agenda.mjs';"),(A/'recipes/author-library.mjs',"import{roundedAgendaContent}from'./rounded-agenda.mjs';")]:
 s=p.read_text(encoding='utf-8');s=imp+'\n'+s if 'import{roundedAgendaContent}'not in s else s
 s=re.sub(r"case'agenda':.*?break;\n case'divider':","case'agenda':\n  for(const sh of [...s.shapes.items])if(sh.name!=='copyright-footer')sh.delete();\n  roundedAgendaContent(s);break;\n case'divider':",s,flags=re.S);p.write_text(s,encoding='utf-8')
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
catalog=json.loads((A/'catalog.json').read_text(encoding='utf-8'))
with ZipFile(lib)as z:
 rs={x.get('Id'):x.get('Target').lstrip('/')for x in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))};ids=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N);root=E.fromstring(z.read(rs[ids[1].get('{'+N['r']+'}id')]))
 objects=[]
 for sh in root.findall('.//p:sp',N):
  name=sh.find('p:nvSpPr/p:cNvPr',N).get('name');xf=sh.find('p:spPr/a:xfrm',N);txt='\n'.join(''.join(p.xpath('.//a:t/text()',namespaces=N))for p in sh.findall('p:txBody/a:p',N));obj={'name':name,'type':'text'if txt else 'shape','editable':True,'default_text':txt,'geometry':'custom-rounded-chevron'if sh.find('p:spPr/a:custGeom',N)is not None else 'textbox'}
  if xf is not None:obj['box']={k:round(int(xf.find(el,N).get(v))/9525,3)for k,el,v in[('left','a:off','x'),('top','a:off','y'),('width','a:ext','cx'),('height','a:ext','cy')]}
  objects.append(obj)
L=catalog['layouts'][1];L['objects']=objects;L['design_rules']=['four uniform gray rounded chevron blocks','PART labels in orange, left-aligned with topic text','single centered heading; no extra section header, subtitle or bottom slogan','brand logo and copyright retained'];L['recipe']='recipes/rounded-agenda.mjs'
catalog['presentation']=lib.name;catalog['presentation_sha256']=hashlib.sha256(lib.read_bytes()).hexdigest();catalog['version']='1.1';(A/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
p=A/'README.md';s=p.read_text(encoding='utf-8').replace('20종_v3','20종_v4').replace('NotionTalk_모션그래픽_레이아웃에셋적용_21장_v16','NotionTalk_모션그래픽_목차수정_21장_v17');s+='\n## 목차 디자인 수정\n\nL02는 원본처럼 둥근 모서리의 꺾인 블록 네 개, PART 라벨, 왼쪽 정렬 문구와 중앙 제목으로 구성한다. 기본 프리셋 화살표로 대체하지 않는다. 기존 노션톡 로고·저작권은 유지한다. `recipes/rounded-agenda.mjs`에 네이티브 자유형 곡선과 텍스트 위치를 고정했다. 실제 웨비나의 3쪽에도 같은 구성을 적용했다.\n';p.write_text(s,encoding='utf-8')
p=A/'current-deck-application.json';j=json.loads(p.read_text(encoding='utf-8'));j['result']='NotionTalk_모션그래픽_목차수정_21장_v17.pptx';j['agenda_fix']={'page':3,'layout_id':'L02','library_version':'v4'};p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
archive=U/'history/before-agenda-fix-20261028';archive.mkdir(exist_ok=True)
for name in ['plan.md','design.md','part-0.md']:
 p=U/name
 if not(archive/name).exists():shutil.copy2(p,archive/name)
 s=p.read_text(encoding='utf-8').replace('NotionTalk_모션그래픽_레이아웃에셋적용_21장_v16','NotionTalk_모션그래픽_목차수정_21장_v17').replace('21장 v16','21장 v17');s+='\n목차 정정: 3쪽은 원본의 둥근 꺾인 블록 네 개와 PART 라벨·왼쪽 정렬을 따른다. 제목과 네 블록으로 구성하며 상단 소제목·부제·하단 요약 문구는 넣지 않는다. 노션톡 로고·저작권은 유지한다. 기본 프리셋 화살표를 목차로 사용하지 않는다.\n';p.write_text(s,encoding='utf-8')
p=R/'AGENTS.md';p.write_text('## 최신 목차 디자인 정정 — 2026-10-28\n\n현재 강의는 `output/webinar-knowledge-only/NotionTalk_모션그래픽_목차수정_21장_v17.pptx`와 PDF, 에셋은 `assets/layout-library-20261028/NotionTalk_상황별레이아웃_20종_v4.pptx`다. 사용자 지적에 따라 라이브러리 L02의 기본 화살표를 폐기하고 원본의 둥근 꺾인 블록 네 개·PART 라벨·왼쪽 정렬을 적용했다. 실제 강의 3쪽도 같은 기준으로 수정했다. 목차는 중앙 제목과 네 블록, 기존 브랜드·저작권만 사용하고 불필요한 상단 소제목·부제·하단 문구는 넣지 않는다. 재사용 코드는 assets/layout-library-20261028/recipes/rounded-agenda.mjs다. 다른 20장·라이브러리 19장·준비물·네 캐릭터 포즈·움직임·lesson.md·하네스·상속 G10 상태는 보존한다. 아래 버전은 이력이다.\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
sheet=Image.new('RGB',(1280,1020),'#333333');draw=ImageDraw.Draw(sheet)
for k in range(20):
 im=Image.open(A/'previews'/f'slide-{k+1:02}.png').convert('RGB');im.thumbnail((320,180));x=k%4*320;y=k//4*204;sheet.paste(im,(x,y));draw.text((x+6,y+184),f'L{k+1:02}',fill='white')
sheet.save(A/'overview.jpg',quality=94)
print('Updated agenda recipe, catalog, previews and current deck documentation.')
