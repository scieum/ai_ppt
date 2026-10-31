from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import posixpath,re
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1];OUT=R/'output/webinar-complete'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def target(p,t):return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(p),t))
def rel(p):return posixpath.join(posixpath.dirname(p),'_rels',posixpath.basename(p)+'.rels')
overrides={
1:('모션 그래픽을 이용한 수업 영상 제작하기','오늘은 AI에게 원하는 움직임을 말로 설명하고, 결과를 보면서 수정하는 방법을 익힙니다. 노션톡 웨비나 홍보 타이포그래피, 웹사이트 소개, 수업 보조 영상의 세 사례를 함께 살펴봅니다. 세 사례 중 직접 만들어 볼 하나를 골라 주세요.'),
2:('수업 영상을 만드는 다섯 단계','먼저 짧은 요청으로 초안을 만듭니다. 다음으로 레퍼런스에서 필요한 원리를 고르고, 시간과 강조 같은 모션 지식으로 수정합니다. 잘 작동한 조건은 Markdown 파일과 장면표에 남깁니다. 마지막에는 필요한 장면 한 부분만 외부 소재로 확장합니다. 오늘은 같은 결과를 이 다섯 단계를 통해 발전시킵니다.'),
3:('오늘의 준비물','코덱스 또는 클로드 중 하나의 유료 계정을 준비합니다. 힉스필드는 선택 사항이며 계정이 없으면 강사 시연을 보면 됩니다. 선택한 AI 환경에서 파일을 첨부하고 결과를 미리 볼 수 있는지 확인해 주세요. 생성이 지연되면 요청 조건을 함께 정리한 뒤 준비된 설계 예시를 보며 이어갑니다.'),
34:('내 수업에 맞는 세 문서를 만들어요','목적과 화면 규칙, 장면표를 세 파일로 나누어 남깁니다. LESSON_BRIEF.md에는 대상과 목표, 주제와 원자료를 적습니다. VISUAL_RULES.md에는 색과 글자, 강조와 움직임의 기준을 적습니다. SCENE_PLAN.md에는 장면별 시간과 문구, 동작과 근거를 연결합니다. 파일을 실제 작업에 첨부하거나 참조해야 다음 생성에도 조건이 이어집니다. 지금부터 실습 자료의 세 파일을 열어 하나씩 살펴봅니다.'),
41:('장면표의 한 장면을 영상으로 확장해요','장면표에서 외부 소재가 필요한 한 부분을 고릅니다. 도입 배경처럼 역할이 분명한 장면부터 시작합니다. 연결된 도구의 지원 기능과 계정 조건을 확인한 뒤 길이와 비율, 분위기와 움직임을 전달합니다. 요청 접수와 생성 완료, 실제 재생 결과를 나누어 확인합니다. 정확한 한글과 날짜, 브랜드 로고는 편집 가능한 요소로 합성합니다. 힉스필드 계정이 없는 참가자는 시연을 관찰합니다.')}
rows=[]
with ZipFile(B/'candidate.pptx') as z:
 ids=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldIdLst',N);rs={r.get('Id'):r.get('Target') for r in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 for i,sid in enumerate(ids,1):
  part=target('ppt/presentation.xml',rs[sid.get('{'+N['r']+'}id')]);s=E.fromstring(z.read(part));title=''.join(s.xpath('.//p:sp[p:nvSpPr/p:cNvPr[@name="title"]]//a:t/text()',namespaces=N));r=E.fromstring(z.read(rel(part)));note=target(part,next(x.get('Target') for x in r if x.get('Type').endswith('/notesSlide')));nt=E.fromstring(z.read(note));txt=''
  for sh in nt.findall('.//p:sp',N):
   ph=sh.find('.//p:ph',N)
   if ph is not None and ph.get('type')=='body':txt='\n'.join(''.join(p.xpath('.//a:t/text()',namespaces=N)) for p in sh.findall('p:txBody/a:p',N));break
  for sep in ['\n\n근거·참고:','\n\n참고·근거:','\nSource:','\n근거:','\n2026-10-28 이미지 개정:']:
   txt=txt.split(sep)[0]
  txt=txt.replace('발화: ','').replace('조작: ','시연 안내: ').replace('대기: ','진행 시간: ')
  if i in overrides:title,txt=overrides[i]
  txt=txt.replace('챌린지이라는','챌린지라는').replace('URL은 입력 방법, 과학사는 설명 주제입니다.','URL은 입력 방법, 수업 보조 영상은 활용 목적입니다.')
  rows.append((i,title,txt))
d=Document();sec=d.sections[0];sec.page_width=Inches(8.5);sec.page_height=Inches(11);sec.top_margin=Inches(.72);sec.bottom_margin=Inches(.7);sec.left_margin=Inches(.8);sec.right_margin=Inches(.8)
for key in ['Normal','Title','Heading 1','Heading 2']:
 st=d.styles[key];st.font.name='Pretendard';st._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Pretendard');st.font.color.rgb=RGBColor.from_string('000000')
for st in d.styles:
 pp=st._element.find(qn('w:pPr'))
 if pp is not None:
  for border in list(pp.findall(qn('w:pBdr'))):pp.remove(border)
d.styles['Normal'].font.size=Pt(11.5);d.styles['Normal'].paragraph_format.line_spacing=1.22;d.styles['Normal'].paragraph_format.space_after=Pt(7)
d.styles['Title'].font.size=Pt(24);d.styles['Title'].font.bold=True;d.styles['Title'].paragraph_format.space_after=Pt(18)
d.styles['Heading 1'].font.size=Pt(15);d.styles['Heading 1'].font.bold=True;d.styles['Heading 1'].paragraph_format.space_before=Pt(15);d.styles['Heading 1'].paragraph_format.space_after=Pt(9)
d.styles['Heading 2'].font.size=Pt(11.5);d.styles['Heading 2'].font.bold=True
d.add_paragraph('노션톡 모션 그래픽 웨비나 진행 원고','Title');d.add_paragraph('전체 48장  90분 진행안')
d.add_paragraph('슬라이드를 보면서 설명할 핵심과 시연 안내를 장표 순서대로 정리했습니다. 참가자는 세 사례 중 하나를 선택해 첫 요청을 보내고, 같은 결과를 참고 원리와 모션 지식으로 다듬은 뒤 문서와 외부 소재로 발전시킵니다.')
d.add_paragraph('진행 시간','Heading 1')
for t in ['Part 0  오늘의 준비물  1부터 3쪽  5분','Part 1  기초와 첫 제작  4부터 19쪽  26분','Part 2  레퍼런스 활용  20부터 26쪽  10분','Part 3  움직임 다듬기  27부터 33쪽  10분','Part 4  Markdown 제작 문서  34부터 40쪽  14분','Part 5  외부 소재 확장  41부터 45쪽  10분','마무리와 질의응답  46부터 48쪽  15분']:d.add_paragraph(t)
d.add_paragraph('강의 운영','Heading 1');d.add_paragraph('PPT 효과 시연은 슬라이드쇼에서 재생합니다. PDF는 정지 화면입니다. 현재 생성과 사전 결과, 생성한 정지 구상 이미지와 실제 동영상 출력은 구분해 소개합니다. 생성이 지연되면 같은 입력의 예시 관찰로 이어갑니다.')
for pos,(page,title,body) in enumerate(rows):
 if pos%2==0:d.add_page_break()
 clean=re.sub(r'[^0-9A-Za-z가-힣\s]',' ',title);clean=re.sub(r'\s+',' ',clean).strip()
 d.add_paragraph(f'{page:02}  {clean}','Heading 1')
 paragraphs=[t.strip() for t in body.split('\n') if t.strip()]
 for para in paragraphs:d.add_paragraph(para)
 if page<=3:action='선택한 AI 계정과 준비물을 확인합니다. 힉스필드 등 외부 제작 도구는 선택이며 없으면 시연을 봅니다.'
 elif page<=11:action='해당 효과가 있는 장표는 슬라이드쇼로 재생하고, 무엇의 값과 시점이 달라졌는지 짚습니다.'
 elif page<=19:action='한 사례의 첫 요청이나 관찰을 남기고, 실제 재생 형태와 저장 위치를 확인합니다.'
 elif page<=26:action='참고할 조건 두 가지와 이유를 적고, 같은 초안에 적용할 요청을 작성합니다.'
 elif page<=33:action='바꿀 조건 한 가지와 유지할 조건 한 가지를 고르고 수정 전후를 비교합니다.'
 elif page<=40:action='실습 자료의 세 Markdown 파일을 열고, 대상과 주제에 맞게 수정합니다.'
 elif page<=45:action='현재 도구의 연결과 계정 조건을 확인하고, 상태와 실제 파일을 구분합니다.'
 else:action='다음 영상에 가져갈 문서와 요청을 정리하고 질문을 받습니다.'
 d.add_paragraph('시연과 참여','Heading 2');d.add_paragraph(action)
footer=sec.footer.paragraphs[0];footer.alignment=2;r=footer.add_run('NotionTalk  ');r.font.size=Pt(9);r.font.color.rgb=RGBColor.from_string('777777');fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
out=OUT/'NotionTalk_전체웨비나_강사용진행원고.docx';d.save(out);print(out)
md=['# 노션톡 모션 그래픽 웨비나 진행 원고\n','전체 48장 90분 진행안\n']
for page,title,body in rows:md.extend([f'## {page:02}. {title}\n',body+'\n'])
(OUT/'강사용_진행원고.md').write_text('\n'.join(md),encoding='utf8')
