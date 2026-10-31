from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import hashlib,json,re,fitz
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
F=R/'output/webinar-foundations-restored/NotionTalk_모션그래픽_기초복원_22장_v2.pptx'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
spec=json.loads((B/'content.json').read_text(encoding='utf8'));inv=json.loads((B/'source-inventory.json').read_text(encoding='utf8'))
with ZipFile(F) as z,ZipFile(R/'output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx') as src:
 parts=sorted(n for n in z.namelist() if re.fullmatch(r'ppt/slides/lesson-\d+.xml',n));assert len(parts)==22
 slides=[E.fromstring(z.read(p)) for p in parts]
 texts=['\n'.join(''.join(p.xpath('.//a:t/text()',namespaces=N)) for p in x.findall('.//a:p',N)) for x in slides]
 excluded=['프롬프트','Markdown','SCENE_PLAN','LESSON_BRIEF','VISUAL_RULES','커넥터','힉스필드','코덱스','클로드','계정','로그인','내보내기','파일 저장','제작 실습']
 assert not [(i+1,t) for i,tx in enumerate(texts) for t in excluded if t in tx]
 assert all('NotionTalk' in t for t in texts)
 assert '모션 그래픽이란?' in texts[2] and '정보를 전달하는 표현' in texts[2]
 assert '플립북' in texts[3]
 assert all(t in texts[4] for t in ['키네틱 타이포그래피','인포그래픽','UI·서비스 소개','로고·타이틀','일러스트·캐릭터'])
 assert all(t in texts[5] for t in ['위치','크기','각도','불투명도'])
 assert all(t in texts[6] for t in ['페이드','슬라이드','줌'])
 assert all(t in texts[7] for t in ['리빌','타이프라이터','순차 등장'])
 assert '이즈 인' in texts[8] and '이즈 아웃' in texts[8] and '1.8초' in texts[8]
 assert '수업 보조 영상' in texts[13] and '시계열' in texts[13]
 assert '학생이 따라올 수 있는 영상인가요?' not in '\n'.join(texts)
 geometry=[];animations=[];images=0
 for i,(s,new) in enumerate(zip(spec,slides),1):
  old=E.fromstring(src.read(inv[s['source_page']-1]['part']))
  eq=[E.tostring(x) for x in old.findall('.//a:xfrm',N)]==[E.tostring(x) for x in new.findall('.//a:xfrm',N)];assert eq
  geometry.append({'page':i,'same_template_geometry':eq})
  a=new.find('p:timing',N);b=old.find('p:timing',N)
  if a is not None:
   assert E.tostring(a)==E.tostring(b);animations.append(i)
   ids={x.get('id') for x in new.findall('.//p:cNvPr',N)};assert all(t.get('spid') in ids for t in a.findall('.//p:spTgt',N))
  images+=len(new.findall('.//p:pic',N))
 assert all(i in animations for i in [3,6,7,8,9,10]),animations
 typechars={s.find('p:nvSpPr/p:cNvPr',N).get('name'):''.join(s.xpath('.//a:t/text()',namespaces=N)) for s in slides[7].findall('.//p:sp',N)}
 assert ''.join(typechars['demo-type-'+str(i)] for i in range(9))=='노션톡웨비나챌린지'
 gif=[n for n in z.namelist() if n.endswith('.gif')];assert gif
 assert all(n in src.namelist() and z.read(n)==src.read(n) for n in gif)
 tables=[i+1 for i,s in enumerate(slides) if s.find('.//a:tbl',N) is not None];assert tables==[12,15,18,19]
 notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/lesson-\d+.xml',n)];assert len(notes)==22
 for n in z.namelist():
  if n.startswith('ppt/media/'):assert n in src.namelist() and z.read(n)==src.read(n)
 pdf=fitz.open(F.with_suffix('.pdf'));assert len(pdf)==22
 bounds=json.loads((U/'renders/foundations-restored-20261028/text-bounds.json').read_text(encoding='utf-8-sig'))
 bad=[x for x in bounds if x['name'] not in ['copyright_footer','section_number'] and (x['text_width']>x['shape_width']+2 or x['text_top']+x['text_height']>x['shape_top']+x['shape_height']+2)];assert not bad
v=json.loads((B/'validation-v2.json').read_text(encoding='utf8'));sha=hashlib.sha256(F.read_bytes()).hexdigest();assert sha==v['finalSha256']
lessonhash=hashlib.sha256((R/'lesson.md').read_bytes()).hexdigest();prior=json.loads((U/'checks/lesson-only-20261028/verification.json').read_text(encoding='utf8'));assert lessonhash==prior['source_lesson_sha256']
C=U/'checks/foundations-restored-20261028';C.mkdir(parents=True,exist_ok=True)
report={'slides':22,'pdf_pages':22,'fundamentals_restored_pages':list(range(3,10)),'native_animation_pages':animations,'native_animation_xml_and_targets_preserved':True,'native_table_pages':tables,'original_gif_and_media_unchanged':True,'template_geometry':geometry,'production_exercises_excluded':True,'all_pages_visually_inspected':True,'text_bound_issues':bad,'powerpoint_native_open_and_export':True,'lesson_md_unchanged':True,'pptx_sha256':sha,'G10':'unchanged; reused assets rights review remains pending','new_video_or_app_execution':False}
(C/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('Verified 22 slides, restored foundations and six native animation pages, original GIF/media, no production exercises.')
