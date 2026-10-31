from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile
from lxml import etree as E
import json,re,posixpath
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
prev=json.loads((U/'drafts/lesson-only-20261028/build/content.json').read_text(encoding='utf8'))
inv=json.loads((B/'source-inventory.json').read_text(encoding='utf8'))
rows=[]
def use(page,changes=None):
 s=deepcopy(prev[page-1]);s.update(changes or {});rows.append(s);return s
def common(s,part,num,group,title,subtitle):
 s['title']=title;s['edits'].update(part_label=part,section_number=num,section_heading=group,title=title,subtitle=subtitle)
def fresh(src,part,num,group,title,subtitle,edits,note,refs=None,styles=None):
 s={'source_page':src,'title':title,'edits':{},'note':note,'refs':refs or [],'styles':styles or {}}
 common(s,part,num,group,title,subtitle);s['edits'].update(edits);rows.append(s);return s
P1='Part 1  모션 그래픽 이해하기';P2='Part 2  움직임과 효과';P3='Part 3  사례로 보는 표현';P4='Part 4  레퍼런스와 전달력'
cover=use(1);cover['title']='모션 그래픽 기초와 표현 이해하기';cover['edits'].update(cover_title='모션 그래픽\n기초와 표현 이해하기',cover_subtitle='뜻·종류·효과를 예시로 익히는 무료 웨비나')
cover['note']='모션 그래픽이 무엇인지부터 살펴봅니다. 정지된 디자인과 움직이는 디자인을 비교하고, 표현의 종류와 효과 이름을 구분합니다. 뒤에서는 타이포그래피·웹사이트 소개·수업 보조 영상의 장면을 보며 같은 개념을 연결합니다.'
agenda=use(3);common(agenda,'무료 웨비나  오늘 살펴볼 내용','01','기초부터 사례까지','오늘 살펴볼 내용','뜻을 이해하고 효과를 구분한 뒤, 실제 쓰임을 사례로 연결합니다')
agenda['edits'].update({'dev-case-head-0':'이야기 묶음','dev-case-head-1':'살펴볼 내용','dev-case-head-2':'중심 질문','dev-case-0-0':'01  모션 그래픽 이해','dev-case-0-1':'뜻·플립북·표현 종류','dev-case-0-2':'무엇이 움직일까?','dev-case-1-0':'02  움직임과 효과','dev-case-1-1':'속성·효과 이름·시간','dev-case-1-2':'어떻게 달라질까?','dev-case-2-0':'03  사례와 레퍼런스','dev-case-2-1':'글자·서비스·수업 설명','dev-case-2-2':'무엇을 전달할까?','dev-case-choice':'정지 화면과 움직이는 예시를 함께 비교합니다'})
agenda['note']='앞부분에서 기본 개념을 익힌 뒤 효과의 이름과 역할을 연결합니다. 마지막에는 같은 표현이 홍보 문구와 서비스 설명, 수업 보조 영상에서 어떻게 쓰이는지 살펴봅니다.'
fresh(4,P1,'01','뜻과 움직임','모션 그래픽이란?','글자·도형·이미지를 움직여 정보를 전달하는 표현입니다',{'still-title':'노션톡','demo-definition':'노션톡','still-caption':'정지된 위치와 크기','moving-caption':'나타나는 순간과 머무는 시간','dev-definition-takeaway':'그래픽에 시간에 따른 변화를 더합니다'},'왼쪽과 오른쪽은 같은 노션톡이라는 글자입니다. 왼쪽은 배치한 상태이고 오른쪽은 시간에 따라 나타나는 예시입니다. 모션 그래픽은 그래픽 요소의 움직임으로 정보를 전달하는 표현입니다. 어떤 정보부터 보여 줄지와 얼마나 머물게 할지가 함께 작동합니다. 애니메이션은 더 넓은 범주이며 여기서는 글자·도형·이미지 중심의 표현을 살펴봅니다.')
fresh(5,P1,'01','프레임과 움직임','플립북으로 보는 움직임','공의 위치가 조금씩 다른 그림을 시간 순서대로 이어 봅니다',{},'플립북의 여섯 그림에서 공의 위치가 조금씩 다릅니다. 그림을 빠르게 이어 보면 움직임으로 보입니다. 오른쪽 반복 재생과 아래 프레임을 연결해 봅니다. 특정 시점의 상태를 정하는 기준점을 키프레임이라고 부릅니다. 모든 프레임을 직접 그려야 한다는 뜻은 아닙니다. PDF는 정지 화면이고 PPT에는 반복 GIF가 들어 있습니다.')
fresh(6,P1,'01','표현의 종류','모션 그래픽의 다섯 가지 표현','글자·수치·화면·브랜드·캐릭터 중 무엇이 중심인지로 살펴봅니다',{'dev-formats-foot':'여러 표현을 한 영상 안에서 함께 사용할 수 있습니다'},'글자 중심은 키네틱 타이포그래피, 수치와 관계 중심은 인포그래픽입니다. UI·서비스 소개는 화면과 기능의 쓰임을 보여 주고 로고·타이틀은 브랜드와 영상의 첫인상을 전달합니다. 일러스트·캐릭터는 상황과 이야기를 표현합니다. 서로 겹치는 실용적 구분이며 같은 영상에 여러 종류가 함께 들어갈 수 있습니다. 활용 예시는 광고·행사·통계·서비스·스토리 등 일반적인 상황입니다.',styles={f'dev-format-{r}-{c}':{'color':'#DADADA'} for r in range(5) for c in [1,2]})
fresh(7,P2,'01','기본 속성','움직일 때 바뀌는 네 가지 값','위치·크기·각도·불투명도는 효과를 이루는 기본 속성입니다',{'property-desc-3':'투명한 상태에서 보이게','dev-property-note':'같은 요소도 어떤 값을 바꾸는지에 따라 다르게 움직입니다'},'위치를 바꾸면 이동하고 크기를 바꾸면 확대·축소됩니다. 각도 변화는 회전이고 불투명도를 바꾸면 서서히 보이거나 사라집니다. 불투명도는 흐림 정도와 다릅니다. 하나의 표현에 여러 속성 변화가 함께 쓰일 수도 있습니다. 네 예시를 재생하며 바뀌는 값을 구분합니다.')
fresh(8,P2,'01','등장 효과의 이름','기본 등장 효과 세 가지','페이드는 불투명도, 슬라이드는 위치, 줌·스케일은 크기가 바뀝니다',{},'서서히 나타나는 페이드 인, 옆에서 들어오는 슬라이드 인, 작게 시작해 커지는 줌·스케일을 비교합니다. 아웃은 사라지거나 작아지는 반대 방향의 표현을 가리킵니다. 여기서는 들어오는 예시를 재생합니다. 줌은 카메라 확대를 뜻할 수도 있으므로 이 장표에서는 글자 크기의 변화로 구분합니다. 예시 문구는 모두 노션톡입니다.')
fresh(9,P2,'01','글자와 순서 효과','리빌·타이프라이터·순차 등장','보이는 영역, 한 글자, 단어별 시작 시점의 차이를 비교합니다',{},'리빌은 가려졌던 부분이 드러나는 표현입니다. 여기서는 와이프로 보이는 영역이 열리는 예를 보여 줍니다. 타이프라이터는 노션톡 웨비나 챌린지의 아홉 글자가 하나씩 나타납니다. 순차 등장인 Stagger는 여러 요소의 시작 시점에 간격을 주는 규칙입니다. 세 단어의 순서와 글자 하나씩의 순서를 구분합니다.')
fresh(10,P2,'02','시간과 속도','움직이는 속도와 멈춰 읽는 시간','이즈 인은 천천히 시작하고, 이즈 아웃은 끝에서 느려집니다',{'timing-terms':'속도 비교   같은 거리 · 같은 이동 시간 1.8초','easing-caption':'이징은 움직이는 동안의 속도 변화입니다 · 읽는 유지 시간은 별도로 봅니다'},'이징은 이동 중 속도가 달라지는 방식입니다. 이즈 인은 천천히 시작하고 이즈 아웃은 끝에서 느려집니다. 아래 두 예시는 같은 거리와 1.8초라는 같은 이동 시간에서 일정한 속도와 끝 감속을 비교합니다. 움직이는 시간과 그 뒤 문구가 머무는 시간은 서로 다릅니다. 읽는 시간은 다음 타이포그래피 사례에서도 연결합니다.')
s=use(9);common(s,P2,'02','등장 순서의 쓰임','정보가 차례로 나타날 때','한꺼번에 보는 장면과 설명 순서대로 보는 장면을 비교합니다')
s['edits']['full-foot']='설명 중인 정보와 화면에서 강조되는 정보가 맞아야 합니다'
s=use(6);common(s,P3,'01','타이포그래피','문장이 영상의 중심이 되는 장면','노션톡 홍보 문구에서 핵심어와 안내의 순서를 봅니다')
s['edits']['prompt_label']='문구가 이어지는 흐름';s['edits']['prompt_body']='수업 자료가\n영상이\n되는 순간\n마지막에는 일정과 참여 안내'
s=use(7);common(s,P3,'01','타이포그래피와 시간','마지막 안내가 읽히는 시간','같은 20초라도 일정과 안내에 배분한 시간이 다릅니다')
s=use(16);common(s,P3,'02','웹사이트 소개','기능을 사용하는 상황이 보이는 장면','기능 이름과 그 기능이 필요한 이유를 함께 설명합니다')
s['edits']['prompt_label']='기능이 필요한 순간';s['edits']['prompt_body']='흩어진 자료를 한곳에\n필요한 부분으로 바로 이동\n같은 문서를 함께 수정\n기능 이름이 쓰임과 연결됩니다'
s=use(19);common(s,P3,'02','수업 보조 영상','수업 보조 영상의 시계열 설명 예시','원자모형은 변화의 순서와 차이를 보여 주는 한 가지 소재입니다')
s['edits']['prompt_body']='어떤 설명이 달라졌는지\n왜 모형이 바뀌었는지\n각 모형의 차이를 비교\n관찰한 것과 해석은 구분'
s=use(13);common(s,P4,'01','내용과 표현의 출처','내용의 근거와 시각 참고','무엇을 설명할지와 어떻게 보여 줄지는 서로 다른 역할입니다')
s=use(12);common(s,P4,'01','움직임 관찰','한 장면에서 살펴볼 세 시점','등장 전·움직이는 동안·모두 나온 뒤를 나누어 봅니다')
s=use(11);common(s,P4,'02','소리와 읽는 시간','음악의 박자와 글자의 등장','음악에 맞는 순간과 글자를 읽을 시간을 함께 봅니다')
s=use(5);common(s,P4,'02','시각적 일관성','장면이 바뀌어도 이어지는 시각 요소','같은 문구·서체·색과 캐릭터의 특징이 연결감을 만듭니다')
s=use(23);common(s,'마무리  세 사례 정리','01','목적과 표현','세 사례에서 먼저 볼 것','홍보·서비스·수업 설명에서 중요한 정보를 다시 연결합니다')
for page in [25,26]:
 s=use(page);common(s,'참고 자료  제공 영상 여섯 편','01','참고 영상',f"참고 영상 {page-24}",'영상의 자막과 설명란에서 정리한 원리를 참고했습니다')
s=use(27);common(s,'마무리  질의응답','02','함께 이야기하기','질의응답','기본 개념과 사례에서 궁금한 점을 이야기합니다');s['edits']['questions-hero']='어떤 효과가\n어떤 정보를 돕고 있나요?'
s['edits']['questions-bottom']='효과 이름    읽는 시간    설명의 순서'
assert len(rows)==22
# Cite the previously verified primary sources for restored fundamentals.
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(R/'output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx') as z:
 for i,s in enumerate(rows,1):
  s['page']=i
  if 4<=s['source_page']<=10:
   part=inv[s['source_page']-1]['part'];rp=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
   rels=E.fromstring(z.read(rp));t=next(x.get('Target') for x in rels if x.get('Type').endswith('/notesSlide'));np=t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part),t))
   txt='\n'.join(E.fromstring(z.read(np)).xpath('.//a:t/text()',namespaces=N));s['sources']=sorted(set(re.findall(r'https?://[^\s]+',txt)))
  else:s['sources']=['lesson.md, 2절·4절·5절, 자막·설명란 기반 분석']
  s['note']=s['note'].replace('이 장표는 소리를 합성한 결과물이 아니라 관계를 설명하는 자료입니다.','음악의 강조와 문구 유지 시간을 구분해 설명합니다.')
(B/'content.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print('Prepared 22 slides with foundational concepts restored and production exercises excluded.')
