from pathlib import Path
from copy import deepcopy
import json
B=Path(__file__).resolve().parent;U=B.parents[2]
prior=json.loads((U/'drafts/foundations-restored-20261028/build/content.json').read_text(encoding='utf8'))
rows=deepcopy(prior[:9])
rows[0]['note']='모션 그래픽의 뜻과 움직임의 원리, 표현 종류와 효과 이름을 설명합니다. 글자·도형의 변화, 프레임과 속도 변화의 개념을 살펴봅니다.'
a=rows[1];a['edits'].update(section_heading='뜻과 종류, 움직임과 효과',subtitle='모션 그래픽의 기본 개념과 용어를 살펴봅니다',**{'dev-case-head-0':'구분','dev-case-head-1':'기본 용어','dev-case-head-2':'설명하는 내용','dev-case-0-0':'01  모션 그래픽','dev-case-0-1':'뜻·프레임·표현 종류','dev-case-0-2':'그래픽과 움직임의 개념','dev-case-1-0':'02  속성과 효과','dev-case-1-1':'위치·크기·각도·불투명도','dev-case-1-2':'대상에서 바뀌는 값','dev-case-2-0':'03  시간과 속도','dev-case-2-1':'지속시간·이징','dev-case-2-2':'움직임의 시간적 변화','dev-case-choice':'용어의 뜻과 움직이는 모습을 함께 살펴봅니다'})
a['note']='뜻과 표현의 종류, 기본 속성과 효과 이름, 지속시간과 이징으로 구성합니다. 종류는 영상의 표현 방식, 속성은 대상의 값, 효과는 시간에 따른 변화입니다.'
rows[2]['note']='모션 그래픽은 글자·도형·이미지 같은 그래픽 요소에 시간에 따른 변화를 더한 표현입니다. 왼쪽은 정지된 상태이고 오른쪽은 글자가 나타나는 예시입니다. 이동·크기 변화·회전·등장처럼 상태가 달라질 수 있습니다. 애니메이션은 더 넓은 범주입니다.'
rows[3]['edits'].update(**{'sequence-caption':'프레임은 한 장의 화면','sequence-caption-2':'다른 상태가 이어집니다'})
rows[3]['note']='프레임은 영상을 이루는 한 장의 화면입니다. 플립북의 여섯 프레임에서 공의 위치가 조금씩 다르고 이어 보면 움직임으로 보입니다. 키프레임은 변화의 기준이 되는 특정 시점의 상태입니다. 오른쪽 GIF는 같은 상태들의 연속을 반복합니다.'
rows[4]['note']='키네틱 타이포그래피는 글자와 문장을, 인포그래픽은 수치와 관계를 중심으로 합니다. UI·서비스 소개는 화면과 기능, 로고·타이틀은 브랜드와 제목, 일러스트·캐릭터는 그림과 인물을 중심으로 표현합니다. 서로 겹칠 수 있는 실용적 분류입니다.'
rows[5]['note']='위치가 바뀌면 이동, 크기가 바뀌면 확대·축소, 각도가 바뀌면 회전입니다. 불투명도는 얼마나 불투명하게 보이는지를 나타내며 흐림과 다른 속성입니다. 한 효과에서 여러 속성이 함께 바뀔 수도 있습니다.'
rows[6]['remove']=['dev-effect-use-0','dev-effect-use-1','dev-effect-use-2']
rows[6]['note']='페이드 인은 불투명도가 높아지며 나타나는 표현이고 페이드 아웃은 반대로 사라지는 표현입니다. 슬라이드 인은 위치가 바뀌며 화면으로 들어옵니다. 이 예시의 줌·스케일은 글자 크기의 변화입니다. 화면에는 들어오는 방향의 예시가 있습니다.'
rows[7]['remove']=['dev-reveal-use-0','dev-reveal-use-1','dev-reveal-use-2']
rows[7]['note']='와이프는 방향에 따라 화면이나 요소가 드러나는 표현입니다. 리빌은 가려졌던 부분이 나타나는 표현을 넓게 부릅니다. 타이프라이터는 글자를 하나씩 표시합니다. 순차 등장인 Stagger는 여러 요소의 시작 시점에 간격을 두는 규칙입니다. 예시는 노션톡 웨비나 챌린지의 아홉 글자와 세 단어를 비교합니다.'
rows[8]['title']='지속시간과 이징'
rows[8]['edits'].update(title='지속시간과 이징',subtitle='지속시간은 움직임이 이어지는 시간, 이징은 그 사이의 속도 변화입니다',**{'easing-caption':'이즈 인은 천천히 시작합니다 · 이즈 아웃은 끝에서 느려집니다'})
rows[8]['note']='지속시간은 변화가 이어지는 시간입니다. 이징은 그 시간 안에서 속도가 달라지는 방식입니다. 이즈 인은 천천히 시작하고 이즈 아웃은 끝에서 느려집니다. 두 도형은 같은 거리를 같은 1.8초 동안 이동하며, 일정한 속도와 끝 감속을 비교합니다.'
s=deepcopy(prior[17]);s['title']='표현 종류·속성·효과의 차이';s['edits'].update(part_label='모션 그래픽  기본 용어 정리',section_number='01',section_heading='용어의 구분',title=s['title'],subtitle='표현의 종류와 대상의 속성, 시간에 따른 변화를 구분합니다')
s['table']=[['구분','뜻','예'],['표현 종류','무엇을 중심으로 표현하는가','타이포그래피·인포그래픽'],['기본 속성','대상이 가진 값','위치·크기·각도·불투명도'],['효과와 시간 규칙','값이 변하거나 나타나는 방식','페이드·슬라이드·순차 등장']]
s['note']='타이포그래피는 글자 중심의 표현 종류입니다. 위치와 크기, 각도와 불투명도는 대상의 속성입니다. 페이드나 슬라이드는 그 값이 시간에 따라 바뀌는 표현이고 순차 등장은 여러 요소의 시작 시점을 나누는 규칙입니다.'
s['sources']=sorted(set(x for r in rows[2:] for x in r['sources']));s['refs']=[];rows.append(s)
for i,s in enumerate(rows,1):s['page']=i;s['refs']=[]
assert len(rows)==10
(B/'content.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print('Prepared ten knowledge-only slides.')
