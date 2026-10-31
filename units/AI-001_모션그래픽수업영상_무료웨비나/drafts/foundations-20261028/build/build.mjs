import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const src=path.join(R,'output/webinar-lesson-applied/NotionTalk_웨비나_계획반영_Part1_15장_v1.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load(src)),base=[...p.slides.items],added=[],animations=[];
const S=2/3,P=(x,y,w,h)=>({left:x*S,top:y*S,width:w*S,height:h*S});
const orange='#FF9228',gray='#A0A0A0';
const sources={definition:'https://www.autodesk.com/uk/solutions/motion-graphics',properties:'https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/animation-basics/animation-basics.html',text:'https://support.apple.com/guide/motion/intro-to-animated-text-motn17692a95/6.3/mac/15.6',easing:'https://www.adobe.com/uk/creativecloud/animation/discover/easing.html',effects:'https://learn.microsoft.com/en-us/office/vba/api/powerpoint.msoanimeffect'};
function edit(s,k,v){const x=s.shapes.items.find(x=>x.name===k);if(!x)throw Error(k);x.text.replace(String(x.text),v);}
function edits(s,values){for(const[k,v]of Object.entries(values))edit(s,k,v);}
function text(s,name,value,box,size=32,color='#FFFFFF',bold=false,align='left'){
 const x=s.shapes.add({geometry:'textbox',name,position:P(...box),fill:'none',line:{fill:'none',width:0}});x.text=value;x.text.style={typeface:'Pretendard',fontSize:size*S,color,bold,alignment:align,verticalAlignment:'top',wrap:'word',autoFit:'none',insets:0,lineSpacing:1.12};return x;
}
function shape(s,name,box,fill='#202020',geometry='roundRect',line='none'){
 return s.shapes.add({geometry,name,position:P(...box),fill,line:{fill:line,width:line==='none'?0:1.5*S},...(geometry==='roundRect'?{borderRadius:20}:{})});
}
function demo(key,name,effect,duration=1,delay=.4,other={}){animations.push({key,name,effect,duration,delay,...other});}
function notes(s,message,refs){s.speakerNotes.text=message+'\n시각 예시는 자체 글자·도형으로 만들었습니다. 효과 이름과 시간·속도 규칙을 구분합니다. 네이티브 효과는 PowerPoint 슬라이드쇼에서 재생하고 PDF에는 정지 상태가 표시됩니다. 새 AI 앱 실행·영상 생성의 증거가 아닙니다. 기존 대표 5장 디자인·원본 파일·G10 상태를 유지합니다.\nSource: '+refs.map(k=>sources[k]).join('\n')+'\n확인일: 2026-10-28. 종류 분류와 수업 활용 예시는 강의를 위한 실용적 구성입니다.';}
function fresh(key,number,title,subtitle){
 const s=base[6].duplicate();added.push({key,template:7,slide:s});
 edits(s,{part_label:'Part 1  모션 그래픽 기초 이해',section_number:number,section_heading:'뜻·종류·효과 이름',title,subtitle});
 const keep=new Set(['part_label','section_number','section_heading','title','subtitle','copyright_footer']);
 for(const x of [...s.shapes.items])if(!keep.has(x.name))x.delete();
 shape(s,'clear-content',[100,500,1720,500],'#000000','rect');
 return s;
}
{
 const s=fresh('definition','01','모션 그래픽이란 무엇일까요?','글자·도형·이미지에 움직임을 더해 정보를 전달하는 시각 표현입니다');
 shape(s,'still-panel',[255,545,630,360]);shape(s,'moving-panel',[1035,545,630,360]);
 text(s,'still-label','정지 디자인',[295,575,550,45],28,gray,false,'center');text(s,'moving-label','움직이는 디자인',[1075,575,550,45],28,gray,false,'center');
 text(s,'still-title','수업 영상',[320,690,500,90],68,'#FFFFFF',true,'center');
 text(s,'demo-definition','수업 영상',[1100,690,500,90],68,orange,true,'center');
 text(s,'still-caption','한 화면에 정보를 놓습니다',[315,825,510,40],28,gray,false,'center');text(s,'moving-caption','등장 순서와 강조를 시간으로 만듭니다',[1070,825,560,40],27,gray,false,'center');
 demo('definition','demo-definition',10,1.2,.4);
 notes(s,'발화: 그래픽 디자인에 시간을 더한 표현으로 생각하면 쉽습니다. 왼쪽은 정보를 배치한 상태이고 오른쪽은 등장하는 순간을 정한 예시입니다. 애니메이션은 더 넓은 말이며 모션 그래픽은 디자인 요소를 움직여 정보를 전하는 데 주로 사용합니다.\n조작: 오른쪽 페이드 예시를 슬라이드쇼로 보여 줍니다.\n대기: 1.5분. 무엇이 움직였는지 질문합니다.',['definition','properties']);
}
{
 const s=base[1].duplicate();added.push({key:'formats',template:2,slide:s});
 edits(s,{part_label:'Part 1  모션 그래픽 기초 이해',section_number:'02',section_heading:'영상의 표현 유형',title:'모션 그래픽의 다섯 가지 표현',subtitle:'어떤 요소를 중심으로 정보를 전달하는지 살펴봅니다',summary_label:'오늘 사례',summary_text:'홍보 문장·웹사이트·과학사 주제에 적용합니다'});
 const rows=[['타이포그래피','움직이는 문장과 핵심어','글자'],['인포그래픽','수치·관계·과정 설명','정보'],['UI·서비스','화면과 기능의 쓰임','화면'],['로고·타이틀','브랜드·영상의 시작','브랜드'],['일러스트','그림·캐릭터로 설명','그림']];
 for(let i=0;i<5;i++)edits(s,{['heading_'+i]:rows[i][0],['description_'+i]:rows[i][1],['tag_'+i]:rows[i][2]});
 notes(s,'발화: 움직이는 글자를 중심으로 하면 키네틱 타이포그래피, 수치·관계를 설명하면 인포그래픽, 서비스의 화면과 기능을 보여 주면 UI·서비스 소개입니다. 로고·타이틀과 일러스트·캐릭터도 자주 쓰입니다. 서로 배타적인 장르가 아니라 함께 조합하는 표현 유형입니다. 원자모형 변천은 주제이며 인포그래픽·일러스트·타이포그래피를 함께 쓸 수 있습니다. URL은 입력 방법이므로 영상 종류와 구분합니다.\n대기: 2분. 각 유형의 수업 활용 상황을 하나씩 연결합니다.',['definition','text']);
}
{
 const s=fresh('properties','03','움직임을 만드는 네 가지 변화','위치·크기·각도·불투명도의 값이 시간에 따라 바뀝니다');
 const rows=[['위치','Position','어디에 있는가','position',2],['크기','Scale','얼마나 큰가','scale',23],['각도','Rotation','얼마나 돌아갔는가','rotation',61],['불투명도','Opacity','얼마나 선명하게 보이는가','opacity',10]];
 rows.forEach((r,i)=>{const x=240+i*380;shape(s,'property-panel-'+i,[x,540,330,390]);text(s,'property-name-'+i,r[0],[x+20,570,290,46],38,'#FFFFFF',true,'center');text(s,'property-english-'+i,r[1],[x+20,625,290,36],25,gray,false,'center');
 const name='demo-property-'+r[3];if(r[3]==='rotation')shape(s,name,[x+100,730,130,30],orange,'rect');else shape(s,name,[x+125,700,80,80],orange,'ellipse');
 text(s,'property-desc-'+i,r[2],[x+15,840,300,58],26,gray,false,'center');demo('properties',name,r[4],1.1,.5,r[3]==='position'?{direction:4}:{});});
 notes(s,'발화: 효과를 외우기 전에 무엇의 값이 바뀌는지 봅니다. 위치는 이동, 크기는 확대·축소, 각도는 회전, 불투명도는 나타나고 사라지는 표현과 연결됩니다. 이 네 개는 속성이며 다음 장표의 효과 이름과 구분합니다.\n조작: 이동·줌·회전·페이드의 자체 도형 예시를 재생합니다.\n대기: 1분. 소프트웨어의 숫자 입력법은 설명하지 않습니다.',['properties']);
}
{
 const s=fresh('entrances','04','기본 등장 효과의 이름','페이드·슬라이드·줌은 서로 다른 변화를 만듭니다');
 const rows=[['페이드 인 / 아웃','Fade In / Out','서서히 나타나거나 사라지기','fade',10],['슬라이드 인','Slide In','화면 밖에서 안으로 이동하기','slide',2],['줌 인 / 아웃','Zoom / Scale','크기를 키우거나 줄이기','zoom',23]];
 rows.forEach((r,i)=>{const x=270+i*480;shape(s,'effect-card-'+i,[x,545,420,380]);text(s,'effect-name-'+i,r[0],[x+20,575,380,50],34,'#FFFFFF',true,'center');text(s,'effect-en-'+i,r[1],[x+20,630,380,38],25,gray,false,'center');text(s,'demo-'+r[3],'수업',[x+60,705,300,75],58,orange,true,'center');text(s,'effect-desc-'+i,r[2],[x+20,840,380,54],27,gray,false,'center');demo('entrances','demo-'+r[3],r[4],.9,.5,r[3]==='slide'?{direction:4}:{});});
 notes(s,'발화: 페이드는 불투명도가 변하고 슬라이드는 위치가 바뀝니다. 줌·스케일은 크기 변화입니다. 오늘 예시는 페이드 인·슬라이드 인·줌 인이며 아웃은 반대로 사라지거나 작아지는 방향입니다. 줌이라는 말은 카메라 확대를 뜻할 수도 있으므로 AI에게는 글자나 도형의 크기를 바꾼다고 대상을 명시합니다.\n조작: 세 예시를 재생하며 무엇이 바뀌었는지 비교합니다.\n대기: 1.5분. 교사의 핵심어 강조·등장에 연결합니다.',['properties','effects']);
}
{
 const s=fresh('reveals','05','글자와 순서를 만드는 효과','와이프·타이프라이터·순차 등장을 구분합니다');
 const rows=[['와이프 / 리빌','Wipe / Reveal','가려진 부분을 차례로 드러내기'],['타이프라이터','Typewriter','글자를 한 글자씩 나타내기'],['순차 등장','Stagger','여러 요소의 시작 시점 나누기']];
 rows.forEach((r,i)=>{const x=270+i*480;shape(s,'reveal-card-'+i,[x,545,420,380]);text(s,'reveal-name-'+i,r[0],[x+20,575,380,50],34,'#FFFFFF',true,'center');text(s,'reveal-en-'+i,r[1],[x+20,630,380,38],25,gray,false,'center');text(s,'reveal-desc-'+i,r[2],[x+20,840,380,58],26,gray,false,'center');});
 text(s,'demo-wipe','수업 영상',[310,705,340,75],50,orange,true,'center');demo('reveals','demo-wipe',22,1.1,.4,{direction:4});
 for(let i=0;i<4;i++){text(s,'demo-type-'+i,'수업영상'[i],[815+i*65,705,68,75],50,orange,true,'center');demo('reveals','demo-type-'+i,1,.05,.4+i*.2);}
 ['생각','연결','설명'].forEach((v,i)=>{text(s,'demo-stagger-'+i,v,[1255+i*120,715,110,65],38,orange,true,'center');demo('reveals','demo-stagger-'+i,10,.5,.4+i*.35);});
 notes(s,'발화: 와이프는 보이는 영역이 열리는 방식이고 타이프라이터는 글자 단위로 표시합니다. 순차 등장은 효과 하나의 고유 이름이라기보다 여러 요소에 시작 간격을 주는 규칙입니다. 와이프와 리빌을 소프트웨어에서 언제나 동일한 메뉴로 취급하지 않습니다. 마스크 리빌은 특정 영역을 이용한 드러내기 방식입니다.\n조작: 글자 네 개와 요소 세 개의 차이를 재생합니다.\n대기: 1.5분. 목록을 한꺼번에 보여 줄 때와 연결합니다.',['text','effects']);
}
{
 const s=fresh('timing','06','효과의 이름 다음에는 시간과 속도','지속 시간·시작 지연·순차 간격·이징을 구분합니다');
 text(s,'timing-terms','지속 시간 0.8초     시작 지연 0.3초     순차 간격 0.15초',[300,530,1320,50],30,orange,true,'center');
 shape(s,'timing-linear-panel',[300,610,1320,120]);shape(s,'timing-ease-panel',[300,760,1320,120]);
 text(s,'linear-label','일정한 속도',[340,646,360,45],32);text(s,'ease-label','끝에서 느리게',[340,796,360,45],32);
 shape(s,'linear-track',[780,669,670,3],'#555555','rect');shape(s,'ease-track',[780,819,670,3],'#555555','rect');
 shape(s,'demo-linear',[1420,646,50,50],orange,'ellipse');shape(s,'demo-ease',[1420,796,50,50],orange,'ellipse');
 demo('timing','demo-linear',2,1.8,.5,{direction:4,decelerate:0});demo('timing','demo-ease',2,1.8,.5,{direction:4,decelerate:.7});
 text(s,'easing-caption','이징(Easing)은 이동 중 속도가 달라지는 방식입니다',[300,920,1320,45],30,gray,false,'center');
 notes(s,'발화: 지속 시간은 움직임에 걸리는 시간, 지연은 시작 전 기다리는 시간입니다. 순차 간격은 요소들의 시작 차이입니다. 이징은 속도가 변하는 방식으로, 이즈 인은 천천히 시작하고 이즈 아웃은 끝에서 느려지는 표현입니다. 읽는 유지 시간은 이동 시간과 별도로 줍니다. 키프레임은 특정 시점의 상태를 지정하는 기준점입니다. 키프레임·속도 곡선 편집은 Part 3에서 필요할 때만 더 설명합니다.\n조작: 같은 효과·지속 시간의 일정 속도와 끝 감속 예시를 비교합니다.\n대기: 1.5분. 수치는 비교용 예시입니다.',['properties','easing']);
}
{
 const s=fresh('vocabulary-prompt','07','효과 이름을 요청 문장으로 바꿉니다','대상·효과·시간·순서와 읽는 시간을 함께 적습니다');
 shape(s,'vocabulary-panel',[300,550,1320,300],'#FFFFFF');
 text(s,'vocabulary-body','제목을 왼쪽에서 0.8초 동안 슬라이드 인 해 줘.\n끝부분에서 천천히 멈추게 해 줘.\n세 핵심어는 0.15초 간격으로 페이드 인 해 줘.\n모든 글자가 나온 뒤 3초 동안 읽을 수 있게 유지해 줘.',[365,595,1190,220],36,'#000000');
 text(s,'vocabulary-caption','이제 같은 언어로 세 가지 제작 예제를 시작합니다',[300,910,1320,45],30,orange,true,'center');
 notes(s,'발화: 예쁘게 해 달라는 요청에서 무엇을 어떻게 바꿀지 말할 수 있는 요청으로 넘어갑니다. 이 문장은 개념을 연결하는 예시이며 시작부터 모든 전문 용어를 넣을 필요는 없습니다.\n대기: 1분. 원하는 변화 하나를 골라 쉬운 말 또는 효과 이름으로 적고 A·B·C의 첫 요청으로 이어갑니다.\n출처 구분: 효과 원리는 공식 문서를 참고했고 문구·수치는 강의용 자체 예시입니다.',['properties','text','easing']);
}
const overview={description_0:'기초 이해와 첫 제작',subtitle:'모션 그래픽의 뜻과 표현부터 이해하고\n세 가지 초안을 직접 만들어 봅니다'};
edits(base[1],overview);
await fs.writeFile(path.join(B,'edits.json'),JSON.stringify({2:{values:overview,notes:'발화: Part 0 준비 후 Part 1에서 뜻·표현 유형·기본 효과 이름을 먼저 익힙니다. 그다음 타이포그래피·웹사이트·원자모형의 세 예제 중 하나로 출발합니다. 레퍼런스·모션 지식·Markdown·외부 연결의 순서는 유지합니다. 전체 48장·90분 제안이며 이번 PPT는 대표본과 Part 1을 확장한 21장입니다. 새 AI 앱 실행·영상 출력과 G10 승인을 기록하지 않습니다.\nSource: plan.md; part-1.md; research/motion-foundations-20261028.md'}},null,2));
await fs.writeFile(path.join(B,'additions.json'),JSON.stringify(added.map(x=>({key:x.key,template:x.template,export_slide:p.slides.items.findIndex(s=>s.id===x.slide.id)+1})),null,2));
await fs.writeFile(path.join(B,'animations.json'),JSON.stringify(animations,null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-roundtrip.pptx'));
console.log('Authored seven introductory slides and',animations.length,'native animation instructions.');
