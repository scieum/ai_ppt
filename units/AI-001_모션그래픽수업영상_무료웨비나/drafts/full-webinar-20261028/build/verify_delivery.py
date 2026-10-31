from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from PIL import Image, ImageChops
import hashlib,json,re,posixpath,fitz
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1];O=R/'output/webinar-complete';C=U/'checks/full-webinar-20261028';C.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=R/'output/webinar-part1-developed/NotionTalk_Part1_내용디자인고도화_21장_v5.pptx'
dst=O/'NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx'
pres=json.loads((B/'preservation.json').read_text(encoding='utf8'))
assert sha(src)==pres['source_sha256']
allowed={'ppt/presentation.xml','ppt/_rels/presentation.xml.rels','[Content_Types].xml','docProps/app.xml'}
with ZipFile(src) as a,ZipFile(dst) as b:
 diffs=[p for p in a.namelist() if p not in b.namelist() or a.read(p)!=b.read(p)]
 assert set(diffs)<=allowed,diffs
 N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
 ids=E.fromstring(b.read('ppt/presentation.xml')).find('p:sldIdLst',N);assert len(ids)==48
 rs={x.get('Id'):x.get('Target') for x in E.fromstring(b.read('ppt/_rels/presentation.xml.rels'))}
 slides=[]
 for sid in ids:
  t=rs[sid.get('{'+N['r']+'}id')];p=t.lstrip('/') if t.startswith('/') else posixpath.normpath('ppt/'+t);slides.append(E.fromstring(b.read(p)))
 tables=[i for i,x in enumerate(slides,1) if x.find('.//a:tbl',N) is not None]
 assert all(x in tables for x in [21,25,28,33,37,39,40,45])
 for i in [29,30,31]:
  x=slides[i-1];assert x.find('p:timing',N) is not None
  shape_ids={n.get('id') for n in x.findall('.//p:cNvPr',N)}
  assert all(n.get('spid') in shape_ids for n in x.findall('.//p:spTgt',N))
 alltext='\n'.join(''.join(x.xpath('.//a:t/text()',namespaces=N)) for x in slides)
 assert '학생이 따라올 수 있는 영상인가요?' not in alltext
 assert all('NotionTalk' in ''.join(x.xpath('.//a:t/text()',namespaces=N)) for x in slides)
pixels=[]
for old,new in pres['original_page_mapping'].items():
 a=Image.open(U/f'renders/class-support-example-20261028/slide-{int(old):02}.png').convert('RGB');b=Image.open(U/f'renders/full-webinar-20261028/slide-{new:02}.png').convert('RGB')
 equal=a.size==b.size and ImageChops.difference(a,b).getbbox() is None;pixels.append({'old':int(old),'new':new,'pixel_identical':equal})
assert all(x['pixel_identical'] for x in pixels)
bounds=json.loads((U/'renders/full-webinar-20261028/text-bounds.json').read_text(encoding='utf-8-sig'))
new_pages=set(range(20,49))-{34,41};issues=[];inherited=[]
for x in bounds:
 if x['slide'] not in new_pages:continue
 l,t,w,h=[x[k] for k in ['shape_left','shape_top','shape_width','shape_height']];tl,tt,tw,th=[x[k] for k in ['text_left','text_top','text_width','text_height']]
 if tl<l-1 or tt<t-1 or tl+tw>l+w+1 or tt+th>t+h+1:
  (inherited if x['name'] in ['footer','copyright_footer','section_number'] else issues).append(x)
assert not issues,[(x['slide'],x['name']) for x in issues]
planfile=U/'plan.md';s=planfile.read_text(encoding='utf8');m=re.search(r'```harness-plan\s*(.*?)```',s,re.S);plan=json.loads(m.group(1));title='모션 그래픽을 이용한 수업 영상 제작하기'
plan['slides'][0]['title']=title;plan['slides'][0]['message']='AI로 수업 영상을 제작하는 다섯 단계와 세 사례를 소개한다'
s=s[:m.start(1)]+json.dumps(plan,ensure_ascii=False,indent=2)+'\n'+s[m.end(1):];s=s.replace('| 1 | 0.5 |  |',f'| 1 | 0.5 | {title} |');planfile.write_text(s,encoding='utf8')
index=json.loads((B/'page-index.json').read_text(encoding='utf8'));index[0]['title']=title;(B/'page-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf8')
assert len(plan['slides'])==48 and sum(x['minutes'] for x in plan['slides'])==90
assert all(x['title']==y['title'] for x,y in zip(plan['slides'],index))
pdf=fitz.open(dst.with_suffix('.pdf'));assert len(pdf)==48
doc=O/'NotionTalk_전체웨비나_강사용진행원고.docx'
with ZipFile(doc) as z:
 x=E.fromstring(z.read('word/document.xml'));W={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
 headings=x.xpath('//w:p[w:pPr/w:pStyle[@w:val="Heading1"]]',namespaces=W)
 numbered=[''.join(x.xpath('.//w:t/text()',namespaces=W)) for x in headings if re.match(r'^\d{2} ',''.join(x.xpath('.//w:t/text()',namespaces=W)))]
 assert len(numbered)==48
docpdf=fitz.open(B/'docx-render/script.pdf');assert len(docpdf)==25
assert len(list((B/'docx-render').glob('page-*.png')))==25
v=json.loads((B/'validation-v2.json').read_text(encoding='utf8'));assert v['finalSha256']==sha(dst)
for path,lead in [
 (R/'AGENTS.md','## 최신 전체 웨비나 완성 범위 — 2026-10-28\n\n최신 작업 기준은 `output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx`와 PDF다. 전체 48장·90분 진행안이며 기존 21장의 XML·이미지·노트·효과와 출력 픽셀을 보존했다. 기존 1~19쪽은 동일 위치, 20쪽은 34쪽, 21쪽은 41쪽이다. Part 2~5와 마무리 27장을 추가했다. 기존 대표 디자인과 모든 최신 사용자 문구 정정을 유지한다. 아래 이전 버전 경로는 개정 이력이다. 강사용 원고와 일곱 실습 Markdown 파일은 같은 출력 폴더에 있다. 실제 인앱 실행·외부 생성 영상·MP4 출력·리허설·G10 승인을 완료한 것으로 표시하지 않는다. G05는 input.json 부재, G10은 기존 자산 권리 목록 부재로 미통과이며 G07은 통과다. 검증은 단원 `checks/full-webinar-20261028/verification.json`이다.\n\n'),
 (U/'design.md','## 전체 웨비나 확장 — 2026-10-28\n\n최신 결과물은 `output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx`와 PDF다. 기존 21장 전체를 그대로 보존하고 동일한 검정·흰색·주황·Pretendard·NotionTalk 로고와 푸터로 27장을 추가했다. 기존 1~19쪽은 동일, 20쪽→34쪽, 21쪽→41쪽이다. Part 2는 20~26쪽, Part 3은 27~33쪽, Part 4는 34~40쪽, Part 5는 41~45쪽, 마무리는 46~48쪽이다.\n\n새 장표에는 넓은 요청문·평평한 비교 행·시간표·문서 예시·효과 시연을 내용에 맞게 사용했다. 상단 번호는 관련 주제별로 묶고 모든 페이지마다 늘리지 않는다. 29·30쪽에는 확대·순차 등장, 31쪽에는 기존과 같은 이동 비교를 넣었다. 시간표와 대응표 8개는 편집 가능한 PowerPoint 표다. 42·44쪽의 추상 배경은 생성 정지 구상 예시이며 실제 영상이나 과학 관측 자료로 표시하지 않는다. 신규 배경 프롬프트와 원본은 `assets/webinar-full/20261028/`에 보관했다. 기존 21장과 대표 디자인의 변경을 이 확장으로 허가한 것으로 해석하지 않는다.\n\n아래 21장·9장 등 이전 결과물 설명은 해당 단계의 이력이다. G10 권리 검토는 별도 미통과 상태다.\n\n')]:
 text=path.read_text(encoding='utf8')
 if lead.split('\n')[0] not in text:path.write_text(lead+text,encoding='utf8')
zipout=O/'NotionTalk_웨비나_실습자료와대본.zip'
with ZipFile(zipout,'w',ZIP_DEFLATED) as z:
 for p in sorted((O/'실습자료').glob('*.md')):z.write(p,'실습자료/'+p.name)
 for p in [doc,O/'강사용_진행원고.md']:z.write(p,p.name)
 for p in [R/'assets/webinar-full/20261028/concept-background.png',R/'assets/webinar-full/20261028/provenance.json']:z.write(p,'구상배경/'+p.name)
report={'date':'2026-10-28','slide_count':48,'minutes':90,'final_sha256':sha(dst),'source_sha256':sha(src),'source_original_parts_preserved':True,'allowed_changed_package_parts':diffs,'source_slide_pixel_comparison':pixels,'native_table_pages':tables,'animation_shape_targets_valid':[29,30,31],'new_slide_text_bound_issues':issues,'inherited_template_bound_exceptions':inherited,'powerpoint_native_open_pdf_and_48_png_export':True,'visual_inspection_new_slide_pages':sorted(new_pages),'docx_pages':25,'docx_slide_sections':48,'docx_all_25_pngs_visually_inspected':True,'docx_render_method':'Skill render_docx.py attempted; soffice.exe unavailable. Native Word PDF export plus bundled pdf2image/Poppler PNG fallback used.','plan_pages_and_minutes_match':True,'workshop_markdown_files':7,'gates':{'G05':'failed: missing input.json','G07':'passed','G10':'failed: missing rights inventory for reused assets'},'actual_new_app_runs':False,'external_generated_video':False,'mp4_output':False,'rehearsal':False,'publication':False,'g10_approval_created':False,'deliverables':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in [dst,dst.with_suffix('.pdf'),doc,zipout]}}
(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
(R/'assets/webinar-full/README.md').write_text('# 전체 웨비나 추가 배경\n\n20261028/concept-background.png는 Part 5의 외부 소재 구상과 글자 합성 설명에 쓴 생성 정지 이미지다. 검정 배경과 주황빛 유리 소재의 추상 연출이며 실제 영상·원자 관측·과학적 모형이 아니다. 원본 파일과 생성 프롬프트는 같은 폴더의 provenance.json에 보관한다.\n',encoding='utf8')
print('Verified 48 slides, 90 minutes, all 21 original slides pixel-identical, 25 DOCX pages, seven workshop files. Packaged deliverables.')
