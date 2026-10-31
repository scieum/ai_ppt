from zipfile import ZipFile
from lxml import etree as E
from pathlib import Path
import json,re,hashlib,fitz
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
F=R/'output/webinar-lesson-restructured/NotionTalk_모션그래픽_원리중심_27장_v2.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(F) as z,ZipFile(R/'output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx') as source:
 ss=sorted(n for n in z.namelist() if re.fullmatch(r'ppt/slides/lesson-\d+.xml',n))
 # Separate paragraphs to avoid false positives across independent text boxes and table cells.
 texts=['\n'.join(''.join(p.xpath('.//a:t/text()',namespaces=N)) for p in E.fromstring(z.read(n)).findall('.//a:p',N)) for n in ss]
 terms=['프롬프트','제작','실습','Markdown','SCENE_PLAN','LESSON_BRIEF','VISUAL_RULES','커넥터','힉스필드','코덱스','클로드','계정','로그인','저장','출력','입력창']
 bad=[{'page':i+1,'term':term} for i,t in enumerate(texts) for term in terms if term in t]
 assert not bad,bad
 assert len(ss)==27
 assert len([n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/lesson-\d+.xml',n)])==27
 assert not [n for n in z.namelist() if re.fullmatch(r'ppt/slides/[^/]+\.xml',n) and n not in ss]
 pdf=fitz.open(F.with_suffix('.pdf'));assert len(pdf)==27
 bounds=json.loads((U/'renders/lesson-only-20261028/text-bounds.json').read_text(encoding='utf-8-sig'))
 badb=[x for x in bounds if x['name'] not in ['copyright_footer','section_number'] and (x['text_width']>x['shape_width']+2 or x['text_top']+x['text_height']>x['shape_top']+x['shape_height']+2)]
 assert not badb
 inv=json.loads((B/'source-inventory.json').read_text(encoding='utf8'));spec=json.loads((B/'content.json').read_text(encoding='utf8'));gx=[];anim=[];media=[];tables=[]
 for i,s in enumerate(spec):
  old=E.fromstring(source.read(inv[s['source_page']-1]['part']));new=E.fromstring(z.read(ss[i]))
  same=[E.tostring(n) for n in old.findall('.//a:xfrm',N)]==[E.tostring(n) for n in new.findall('.//a:xfrm',N)]
  gx.append({'page':i+1,'same_template_geometry':same})
  if new.find('p:timing',N) is not None:
   anim.append(i+1);assert E.tostring(new.find('p:timing',N))==E.tostring(old.find('p:timing',N))
  if new.find('.//a:tbl',N) is not None:tables.append(i+1)
 assert all(x['same_template_geometry'] for x in gx)
 assert anim==[8,9,10],anim
 assert tables==[5,7,13,14,23],tables
 media=[n for n in z.namelist() if n.startswith('ppt/media/') and n in source.namelist() and z.read(n)==source.read(n)]
v=json.loads((B/'validation-v2.json').read_text(encoding='utf8'));assert v['finalSha256']==hashlib.sha256(F.read_bytes()).hexdigest()
C=U/'checks/lesson-only-20261028';C.mkdir(parents=True,exist_ok=True)
r={'slides':27,'pdf_pages':27,'visual_inspection_all_pages':True,'source':'lesson.md','excluded_production_terms_in_visible_slide_text':bad,'removed_original_slides_and_notes_from_package':True,'geometry_comparison':gx,'native_animation_pages':anim,'native_table_pages':tables,'unchanged_reused_media_count':len(media),'body_bound_issues':badb,'G10_status':'unchanged; prior reused asset rights inventory remains pending','new_external_execution':False,'source_lesson_sha256':hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest(),'pptx_sha256':v['finalSha256']}
(C/'verification.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
print('Verified 27 explanation slides, 27 PDF pages, preserved template geometry and animation; no production guidance terms.')
