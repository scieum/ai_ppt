import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-atomic-images/NotionTalk_원자모형_생성이미지반영_21장_v1.pptx')));
const S=2/3,P=(x,y,w,h)=>({left:x*S,top:y*S,width:w*S,height:h*S});
const orange='#FF9228',gray='#A0A0A0',white='#FFFFFF';
const manifest=[];
function sh(s,n){const x=s.shapes.items.find(x=>x.name===n);if(!x)throw Error('Missing '+n);return x;}
function set(s,n,v,box,size,color){const x=sh(s,n);x.text.replace(String(x.text),v);if(box)x.position=P(...box);if(size||color)x.text.style={...(size?{fontSize:size*S}:{}),...(color?{color}:{})};return x;}
function txt(s,n,v,box,size=32,color=white,bold=false,align='left'){
 const x=s.shapes.add({name:'dev-'+n,geometry:'textbox',position:P(...box),fill:'none',line:{fill:'none',width:0}});x.text=v;x.text.style={typeface:'Pretendard',fontSize:size*S,color,bold,alignment:align,verticalAlignment:'top',wrap:'word',insets:0,autoFit:'none',lineSpacing:1.12};return x;
}
function panel(s,n,box,fill){return s.shapes.add({name:'dev-'+n,geometry:'roundRect',position:P(...box),fill,line:{fill:'none',width:0},borderRadius:30*S});}
const common=new Set(['part_label','section_number','section_heading','title','subtitle','copyright_footer']);
function clear(s){for(const x of [...s.shapes.items])if(!common.has(x.name))x.delete();s.shapes.add({name:'dev-content-clear',geometry:'rect',position:P(100,490,1720,510),fill:'#000000',line:{fill:'none',width:0}});}
function base(n,title,sub){const s=p.slides.items[n-1];set(s,'title',title);set(s,'subtitle',sub);manifest.push({slide:n,title});return s;}
function note(s,text,refs){s.speakerNotes.text=text+'\n\n참고·근거: '+refs.join('\n')+'\n확인일: 2026-10-28. 장면 문구와 요청문은 이번 웨비나를 위한 자체 예시입니다. 수치는 비교를 위한 제안값입니다.';}
const refs={definition:'https://www.autodesk.com/uk/solutions/motion-graphics',properties:'https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/animation-basics/animation-basics.html',easing:'https://www.adobe.com/uk/creativecloud/animation/discover/easing.html',text:'https://support.apple.com/guide/motion/intro-to-animated-text-motn17692a95/6.3/mac/15.6',effects:'https://learn.microsoft.com/en-us/office/vba/api/powerpoint.msoanimeffect',notion:'https://www.notion.com/ko/product/docs',notionHelp:'https://www.notion.com/help/columns-headings-and-dividers',notionCollab:'https://www.notion.com/ko/help/collaborate-within-a-workspace',thomson:'https://history.aip.org/exhibits/electron/jjelectr.htm',rutherford:'https://history.aip.org/exhibits/rutherford/sections/alpha-particles-atom.html',bohr:'https://www.nobelprize.org/uploads/2018/06/bohr-lecture.pdf'};
{
 const s=base(4,'모션 그래픽은 디자인에 시간을 더합니다','같은 정보도 언제 등장하고 얼마나 머무는지에 따라 다르게 전달됩니다');
 set(s,'still-caption','한 번에 배치된 정보',[300,820,540,50],30);
 set(s,'moving-caption','등장하는 순간과 읽는 시간을 설계',[1050,820,600,65],30);
 txt(s,'definition-takeaway','글자·도형·이미지의 변화로 정보를 설명합니다',[300,950,1320,45],32,orange,true,'center');
 note(s,'같은 수업 영상이라는 글자를 비교합니다. 왼쪽은 배치한 상태이고, 오른쪽은 등장하는 시간을 정한 예시입니다. 모션 그래픽은 그래픽 디자인 요소를 움직여 정보를 전달하는 표현입니다. 그림이 움직인다는 사실만이 아니라 어떤 정보부터 보이게 할지 정하는 것이 중요합니다. 애니메이션은 더 넓은 범주이고, 여기서는 글자·도형·이미지 중심의 정보 전달에 집중합니다. 슬라이드쇼에서 오른쪽의 페이드를 재생한 뒤, 참가자가 먼저 시선을 준 곳을 짚습니다. 오늘은 편집기 메뉴를 외우기보다 이런 변화를 AI에게 말로 설명하는 방법을 익힙니다.',[refs.definition,'R07 PDF 3~12쪽: 익숙한 상황에서 개념으로 연결하는 구성']);
}
{
 const s=base(5,'작은 차이가 이어지면 움직임이 됩니다','플립북처럼 연속된 상태를 보여 주되, 모든 프레임을 손으로 그릴 필요는 없습니다');
 set(s,'sequence-caption','각 장의 상태를 바꾸고');set(s,'sequence-caption-2','시간 순서대로 이어 보면');
 note(s,'플립북의 공이 조금씩 다른 위치에 있는 모습을 먼저 봅니다. 여섯 그림과 오른쪽 반복 재생을 연결해 설명합니다. 모션 그래픽도 시간에 따라 상태가 달라지는 이미지를 이어 보여 줍니다. 이 비유가 모든 프레임을 직접 그려야 한다는 뜻은 아닙니다. 시작과 끝처럼 특정 시점의 상태를 정하고 그 사이 변화를 계산하게 할 수 있으며, 상태를 정하는 기준점을 키프레임이라고 부릅니다. 이 단계에서는 FPS 수치나 편집기 조작까지 확장하지 않습니다. PDF의 이미지는 정지 상태이고 PPT의 GIF는 연속 움직임을 보여 줍니다.',[refs.properties,'assets/flipbook/20261028/README.md']);
}
{
 const s=base(6,'모션 그래픽의 다섯 가지 표현','다섯 표현 유형은 한 영상에서 함께 사용할 수 있습니다');clear(s);
 const xs=[255,730,1110],ws=[440,335,560];
 ['표현 유형','중심이 되는 요소','교실에서 쓰는 장면'].forEach((v,i)=>txt(s,'format-head-'+i,v,[xs[i],510,ws[i],45],27,gray));
 const rows=[['키네틱 타이포그래피','문장과 핵심어','질문·정의·행사 안내'],['인포그래픽','수치와 관계','비율·변화·과정 비교'],['UI·서비스 소개','화면과 기능','학습 도구의 사용 맥락'],['로고·타이틀','브랜드와 제목','강의 시작·영상 마무리'],['일러스트·캐릭터','그림과 인물','상황·역사·과학 개념']];
 rows.forEach((r,i)=>r.forEach((v,j)=>txt(s,'format-'+i+'-'+j,v,[xs[j],575+i*73,ws[j],52],j===0?34:31,j===0?white:gray,j===0)));
 txt(s,'formats-foot','오늘은 홍보 문장·웹사이트 내용·원자모형 변천에 적용합니다',[255,960,1415,42],29,orange,true,'center');
 note(s,'움직이는 글자를 중심으로 하면 키네틱 타이포그래피입니다. 수치나 관계를 설명하면 인포그래픽, 화면과 기능의 사용 맥락을 보여 주면 UI·서비스 소개에 가깝습니다. 로고·타이틀은 시작과 끝을 정리하고, 일러스트·캐릭터는 상황과 개념을 설명합니다. 서로 겹칠 수 있는 실용적 분류입니다. 예를 들어 원자모형 영상 안에서도 그림과 핵심어를 함께 씁니다. 오늘 세 사례는 같은 기준의 세 장르가 아닙니다. 타이포그래피는 표현 형식, URL은 입력 방법, 과학사는 설명 주제입니다. 참가자에게 자기 수업에서는 어떤 요소를 움직일지 한 가지를 떠올리게 합니다.',[refs.definition,refs.text,'R02 PDF 23쪽: 요소를 분리해 설명하는 방식']);
}
{
 const s=base(7,'효과를 이해하려면 바뀌는 값을 봅니다','위치·크기·각도·불투명도는 시간에 따라 바꿀 수 있는 속성입니다');
 const vals=['왼쪽에서 가운데로','작게 시작해 크게','기울였다가 바르게','투명하게 시작해 선명하게'];
 for(let i=0;i<4;i++){set(s,'property-desc-'+i,vals[i],[255+i*380,835,300,78],29);sh(s,'property-panel-'+i).position=P(240+i*380,540,330,400);}
 txt(s,'property-note','특정 시점의 값이 바뀌면, 그 사이에 움직임이 생깁니다',[260,963,1400,42],29,orange,true,'center');
 note(s,'위치·크기·각도·불투명도는 효과 이름이 아니라 바꾸는 속성입니다. 이동에서는 위치, 확대에서는 크기, 회전에서는 각도, 페이드에서는 불투명도가 변합니다. 네 개의 자체 예시를 재생하며 어떤 값이 달라졌는지 묻습니다. 불투명도는 흐림 정도와 구분합니다. 투명한 상태에서 보이는 상태로 바뀌는 것이며, 초점이 흐린 이미지를 선명하게 만드는 효과를 뜻하지 않습니다. 하나의 표현에 두 속성을 함께 쓸 수도 있습니다. 이 구분을 알면 AI가 예상과 다른 변화를 만들었을 때 수정 대상을 명확히 말할 수 있습니다.',[refs.properties]);
}
{
 const s=base(8,'등장 효과는 무엇이 바뀌는지로 구분합니다','페이드는 불투명도, 슬라이드는 위치, 줌·스케일은 크기가 바뀝니다');
 const uses=['제목을 차분하게 소개할 때','다음 정보의 방향을 안내할 때','핵심어에 시선을 모을 때'];
 for(let i=0;i<3;i++){sh(s,'effect-card-'+i).position=P(270+i*480,545,420,415);set(s,'effect-desc-'+i,['서서히 나타나기','옆에서 들어오기','작게 시작해 커지기'][i],[290+i*480,819,380,48],29);txt(s,'effect-use-'+i,uses[i],[290+i*480,894,380,52],25,orange,false,'center');}
 note(s,'먼저 세 예시를 보고 효과 이름을 붙입니다. 페이드는 불투명도, 슬라이드는 위치, 줌·스케일은 크기 변화입니다. 오늘 PPT에는 들어오는 방향의 예시를 넣었습니다. 사라지거나 작아지는 반대 표현은 아웃이라고 부릅니다. 제목을 차분히 소개할 때 페이드를, 정보가 이어지는 방향을 알릴 때 슬라이드를, 핵심어에 시선을 모을 때 크기 변화를 선택할 수 있습니다. 이는 수업용 활용 예이지 의무 규칙은 아닙니다. 줌은 카메라 확대를 뜻할 수도 있으므로 글자 크기를 바꾸는지 화면을 확대하는지 대상을 붙여 요청합니다.',[refs.properties,refs.effects]);
}
{
 const s=base(9,'한 글자와 여러 요소의 순서는 다릅니다','드러내는 영역·글자 단위·요소의 시작 간격을 나누어 봅니다');
 for(let i=0;i<3;i++){sh(s,'reveal-card-'+i).position=P(270+i*480,545,420,415);set(s,'reveal-desc-'+i,['보이는 영역이 열림','글자를 하나씩 표시','요소마다 시작을 늦춤'][i],[290+i*480,819,380,48],28);txt(s,'reveal-use-'+i,['제목의 일부를 드러낼 때','짧은 질문을 입력하듯 보여 줄 때','여러 핵심어를 차례로 볼 때'][i],[290+i*480,894,380,52],25,orange,false,'center');}
 note(s,'같은 수업 영상이라는 글자라도 보이는 영역을 열면 리빌, 한 글자씩 표시하면 타이프라이터가 됩니다. 세 단어를 따로 두고 시작 시점을 나누면 순차 등장입니다. 순차 등장, 즉 Stagger는 여러 요소에 간격을 주는 규칙이며 모든 앱에 같은 효과 메뉴가 있다는 뜻은 아닙니다. 리빌은 드러내기 표현을 넓게 부르는 말이고, 마스크를 써서 구현할 수도 있습니다. 긴 본문을 한 글자씩 보이게 하면 읽기보다 기다림이 길어질 수 있으므로 오늘은 짧은 문장과 핵심어에 사용합니다. 세 예시를 재생하며 무엇을 단위로 순서를 나눴는지 비교합니다.',[refs.text,refs.effects]);
}
{
 const s=base(10,'움직이는 시간과 읽는 시간을 나눕니다','같은 거리·같은 시간이어도 이징에 따라 속도의 느낌이 달라집니다');
 set(s,'timing-terms','시작 전 0.3초     움직임 0.8초     읽기 유지 3초',[290,515,1340,50],32,orange);
 set(s,'easing-caption','한 요소의 예시: 0.3 + 0.8 + 3 = 4.1초  ·  순차 간격은 요소들의 시작 시점 차이',[250,927,1420,70],28);
 note(s,'먼저 기다리는 시간, 움직이는 시간, 다 나온 뒤 읽는 시간을 나눕니다. 이 예에서는 시작 전 0.3초, 이동 0.8초, 읽기 유지 3초를 합쳐 4.1초입니다. 모든 영상에 적용하는 정답이 아니라 조건을 구분하기 위한 숫자입니다. 여러 요소가 있으면 시작 시점 사이의 간격도 정할 수 있습니다. 아래 두 시연은 같은 거리와 같은 지속 시간에서 일정 속도와 끝 감속을 비교합니다. 이징은 이동 중 속도가 달라지는 방식입니다. 이즈 인은 천천히 시작하고 이즈 아웃은 끝에서 느려집니다. 시연 자체는 1.8초로 설정되어 있으므로 위의 0.8초 요청 예시와 구분해 설명합니다. 빠르게 움직인 뒤 충분히 멈추는 방법도 가능하다는 점을 짚습니다.',[refs.easing,refs.properties]);
}
{
 const s=base(11,'원하는 변화를 요청 문장으로 정리합니다','대상과 변화, 움직이는 시간과 읽는 시간을 구체적으로 말합니다');clear(s);
 panel(s,'request-panel',[300,540,1320,320],white);
 txt(s,'request-body','제목을 왼쪽에서 0.8초 동안 들어오게 해 줘.\n끝부분에서는 속도를 줄여 부드럽게 멈추게 해 줘.\n세 핵심어는 0.15초 간격으로 차례로 나타내 줘.\n모두 나온 뒤 3초 동안 읽을 수 있게 유지해 줘.',[365,588,1190,230],36,'#000000');
 txt(s,'request-key1','무엇을',[350,910,240,42],30,orange,true,'center');txt(s,'request-key2','어떻게 바꿀지',[660,910,360,42],30,orange,true,'center');txt(s,'request-key3','얼마나 움직이고 읽을지',[1060,910,510,42],30,orange,true,'center');
 note(s,'같은 요청을 쉬운 말로도 효과 이름으로도 쓸 수 있습니다. 왼쪽에서 들어오기는 슬라이드 인, 끝에서 천천히 멈추기는 이즈 아웃과 연결됩니다. 중요한 것은 용어를 많이 넣는 것이 아니라 어떤 대상에 어떤 변화가 필요한지 정하는 것입니다. 첫 요청은 짧게 하고, 결과를 본 다음 부족한 조건을 더합니다. 지금 문장은 움직임과 읽는 시간을 구분하는 연습용입니다. 처음부터 네 조건을 모두 외우게 하지 않습니다. 참가자는 수업 제목이나 핵심어 하나를 골라 자신이 원하는 변화를 한 문장으로 말합니다. 다음 세 사례에서는 목적과 입력이 어떻게 달라지는지 살펴봅니다.',[refs.properties,refs.easing,'lesson.md V1 3:22~4:18 / V6: 관찰 가능한 수정 조건']);
}
{
 const s=base(12,'세 예제는 출발점과 설명 목적이 다릅니다','문장·웹사이트·지식을 각각 어떤 영상으로 바꿀지 살펴봅니다');clear(s);
 const cols=[250,725,1200],widths=[430,430,470];['출발점','만들 영상','먼저 살펴볼 것'].forEach((v,i)=>txt(s,'case-head-'+i,v,[cols[i],510,widths[i],45],28,gray));
 const rows=[['A  홍보 문장','20초 타이포그래피','문구·일정·읽는 시간'],['B  웹사이트 URL','30초 기능 소개','원문과 설명의 대응'],['C  과학사 주제','45초 지식 전달','차이와 바뀐 이유']];
 rows.forEach((r,i)=>r.forEach((v,j)=>txt(s,'case-'+i+'-'+j,v,[cols[j],604+i*110,widths[j],65],j===0?37:34,j===0?orange:white,j===0)));
 txt(s,'case-choice','직접 만들 사례 하나를 고르고, 나머지 사례는 비교하며 봅니다',[250,958,1420,45],30,gray,false,'center');
 note(s,'세 사례를 먼저 비교하고 직접 따라 만들 한 가지를 선택하게 합니다. A는 정해진 행사 문구를 시간에 맞춰 보여 주는 작업입니다. B는 웹사이트의 내용을 확인하고 기능이 쓰이는 장면을 새로 구성하는 작업입니다. C는 과학사의 차이와 변화 이유를 사실에 맞게 설명하는 작업입니다. 첫 결과에서 볼 기준도 달라집니다. 세 개를 모두 생성해야 하는 과제로 만들지 않고, 한 사례를 요청하는 동안 다른 사례를 관찰합니다. 결과 형식은 환경에 따라 다를 수 있으므로 HTML 재생과 MP4 파일을 구분해 기록합니다. 뒤의 장면 구성 예시는 설명을 위한 자체 설계이며 실제 앱 결과라고 소개하지 않습니다.',['lesson.md 4절','R05 PDF 24~35쪽: 작은 실습부터 확인하는 구성']);
}
{
 const s=base(13,'타이포그래피는 문장을 시간에 배치합니다','질문을 열고 핵심어를 강조한 뒤, 마지막 안내를 읽게 합니다');
 set(s,'sample-line-1','수업 자료가',[245,555,620,65],48);
 set(s,'sample-focus','영상이',[245,635,620,100],84,orange);
 set(s,'sample-line-3','되는 순간',[245,750,620,70],52);
 set(s,'tool_caption','장면 구성 예시',[245,858,620,40],25);
 set(s,'prompt_label','20초의 흐름',[1010,607,440,45],28);
 set(s,'prompt_body','처음에는 주제를 열고,\n중간에는 핵심어를 강조.\n마지막 4초는 일정과\n참여 안내를 읽게 해 줘.',[1010,665,440,185],32);
 txt(s,'type-time','0~4초  주제 소개     4~16초  핵심어 전개     16~20초  일정·참여 안내',[245,940,1430,52],28,orange,true,'center');
 note(s,'이 장면은 AI 앱의 생성 결과가 아니라 오늘 만들 영상의 자체 구성 예시입니다. 문구를 읽어 준 뒤, 글자의 등장 순서가 설명의 순서와 같다는 점을 짚습니다. 첫 4초에는 주제를 열고, 다음 12초에는 핵심어를 전개하며, 마지막 4초에는 일정과 참여 안내를 둡니다. 4+12+4는 전체 20초입니다. 문구가 길면 시간을 억지로 맞추지 말고 문구나 전체 길이를 다시 조정합니다. 핵심어 하나를 주황색과 크기로 강조하되 모든 글자가 동시에 커지지 않게 합니다. 마지막 안내는 화려한 전환보다 읽을 시간이 우선입니다. 다음 장의 짧은 요청으로 시작한 뒤 이 흐름을 수정 조건으로 더합니다.', ['lesson.md V1 4:22~5:49 / V2 0:55~4:08','자체 장면 설계 A']);
}
function promptSlide(n,title,sub,body,side,notes,refsForNote){
 const s=base(n,title,sub);clear(s);panel(s,'prompt-page',[230,530,1100,400],white);txt(s,'prompt-page-body',body,[290,580,980,305],32,'#000000');
 side.forEach((r,i)=>{txt(s,'prompt-side-head-'+i,r[0],[1400,560+i*126,310,44],30,orange,true);txt(s,'prompt-side-desc-'+i,r[1],[1400,608+i*126,320,65],27,gray);});
 note(s,notes,refsForNote);return s;
}
promptSlide(14,'첫 요청에는 목적과 필수 문구를 담습니다','첫 결과를 재생한 뒤, 마지막 안내의 읽는 시간을 조정합니다', '',[], '',[]);
{
 const s=p.slides.items[13];set(s,'title','첫 요청에는 목적과 필수 문구를 담습니다');set(s,'subtitle','첫 결과를 재생한 뒤, 마지막 안내의 읽는 시간을 조정합니다');
 const body='‘수업 자료가 영상이 되는 순간’으로 시작하는\n노션톡 무료 웨비나 홍보 타이포그래피를 20초로 만들어 줘.\n글자가 차례로 이어지고 핵심어가 강조되게 해 줘.\n검정 바탕에 주황색 포인트를 써 줘.\n마지막에는 ‘2026년 11월 1일 일요일 저녁 8시’와\n‘댓글에 노션톡을 남겨 주세요’를 넣어 줘.\n지금 환경에서 재생할 수 있는 결과로 보여 줘.';
 sh(s,'dev-prompt-page-body').text=body;
 [['목적','노션톡 무료 웨비나 홍보'],['고정할 내용','첫 문장·일정·참여 안내'],['첫 수정','전체 20초, 마지막 안내 4초']].forEach((r,i)=>{txt(s,'prompt-side-head-'+i,r[0],[1400,560+i*126,310,44],30,orange,true);txt(s,'prompt-side-desc-'+i,r[1],[1400,608+i*126,320,65],27,gray);});
 note(s,'복사해서 사용할 첫 요청을 보여 줍니다. 목적과 길이, 필수 문구를 먼저 읽습니다. 글자와 날짜가 정확한지, 한글이 깨지지 않는지, 끝까지 재생되는지 봅니다. 마지막 안내가 빠르면 전체 20초를 유지하면서 마지막 4초를 확보하도록 요청합니다. 처음부터 모든 움직임을 세세하게 정하기보다 결과를 본 다음 필요한 조건을 더하는 흐름입니다. 참가자가 현재 환경에서 어떤 형태로 결과를 받았는지 확인합니다. 재생 가능한 HTML이나 미리보기는 MP4 파일 출력과 구분합니다. 세부 버튼 이름이나 현재 모델·요금제 비교로 범위를 넓히지 않습니다.', ['lesson.md V1·V6','R03 PDF 31쪽 / R05 PDF 31쪽: 입력과 확인할 결과를 함께 제시']);
 manifest.find(x=>x.slide===14).title='첫 요청에는 목적과 필수 문구를 담습니다';
}
{
 const s=base(15,'웹사이트의 기능을 쓰임이 보이는 장면으로','URL은 내용의 근거입니다. 확인한 정보를 새 설명 순서로 구성합니다');
 set(s,'website-input','Notion 문서',[245,550,620,65],46,white);
 set(s,'website-contents','블록으로 내용 구성하기\n목차로 찾아가기\n함께 편집하기',[245,640,620,195],38,white);
 set(s,'website-output','30초 소개 영상',[245,860,620,60],40,orange);
 set(s,'tool_caption','공식 페이지에서 확인한 설명',[245,935,620,42],25);
 set(s,'prompt_label','장면으로 바꾸는 요청',[1010,607,440,45],28);
 set(s,'prompt_body','기능을 나열하는 대신,\n각 기능을 쓰는 상황을\n한 장면씩 설명해 줘.\n사용한 원문도 연결해 줘.',[1010,665,440,180],32);
 note(s,'Notion 공식 문서 소개 페이지를 내용의 출발점으로 사용합니다. 블록으로 내용을 구성하고, 목차로 필요한 부분으로 이동하고, 함께 편집하는 쓰임을 골랐습니다. 공식 제품 페이지의 검색 수집 내용과 공식 도움말을 대조했습니다. 이것을 세 장면의 설명으로 바꾸는 것은 우리 강의의 기획입니다. 웹사이트를 그대로 스크롤해 녹화하는 대신 각 기능을 쓰는 이유가 드러나게 설명합니다. URL이 곧 시각 레퍼런스를 뜻하지는 않습니다. 원문의 문구와 이미지를 그대로 가져오는 문제와 정보의 근거로 읽는 문제를 나누어 설명합니다. 실제 화면이 필요하면 실제 캡처를 사용하고 개념 장면을 실제 UI라고 표시하지 않습니다.',[refs.notion,refs.notionHelp,refs.notionCollab,'lesson.md V3 3:40~6:25 / V4: 내용 출처와 시각 참고 구분']);
}
promptSlide(16,'원문을 읽고, 장면과 문구를 연결합니다','본문을 확인하지 못했다면 확인한 텍스트를 제공하고 다시 시작합니다',
 '다음 공식 페이지를 읽고 Notion 문서를 소개하는\n30초 모션 그래픽 초안을 만들어 줘.\nhttps://www.notion.com/ko/product/docs\n블록으로 내용 구성하기, 목차로 찾아가기,\n함께 편집하기를 각각 한 장면으로 설명해 줘.\n원문과 영상 문구를 짝지어 보여 줘.\n페이지를 읽지 못하면 먼저 알려 줘.',
 [['내용 선택','원문에서 확인한 정보'],['장면 구성','기능이 쓰이는 상황'],['접근 실패','확인한 본문을 직접 제공']],
 'URL만 붙였다고 실제 본문을 읽은 것으로 가정하지 않습니다. 접근했는지 먼저 확인하고, 사용한 원문과 영상 문구를 짝지어 보게 합니다. 원문에 없는 효과나 기능을 더한 경우에는 지웁니다. 페이지를 열 수 없다면 강사가 확인한 본문을 제공한 뒤 입력 방식을 기록합니다. AI에게 장면의 분위기를 요청하기 전에 무엇을 설명할지 고르는 단계가 있습니다. 영상 초안은 실제 사이트 화면을 재현한 자료와 구분합니다. 참가자는 자기 수업의 안내 사이트나 자료 페이지에도 같은 방법을 적용할 수 있지만 원문과 이미지의 재사용 조건은 별도로 확인합니다.',[refs.notion,refs.notionHelp,refs.notionCollab,'lesson.md 4절 B']);
{
 const s=base(17,'원자모형은 바뀐 설명이 드러나야 합니다','이름을 바꾸는 타임라인보다, 모형의 차이와 변화 이유를 보여 줍니다');
 const imgs=[...s.images.items].filter(x=>x.position.width<500).sort((a,b)=>a.position.left-b.position.left);if(imgs.length!==3)throw Error('Atomic pictures '+imgs.length);
 imgs.forEach((x,i)=>x.position=P(170+i*250,535,245,270));
 ['양전하가 퍼진 모형','작은 중심 핵','구분된 허용 궤도'].forEach((v,i)=>{set(s,'model-label-'+i,['톰슨','러더퍼드','보어'][i],[167+i*250,814,250,46],30,white);txt(s,'atomic-difference-'+i,v,[160+i*250,874,270,58],25,orange,false,'center');});
 set(s,'atomic-model-caption','개념 모식도 · 전자 수와 크기 비율 단순화',[155,960,760,36],23);
 set(s,'prompt_label','설명과 동작을 연결하기',[1010,607,440,45],28);
 set(s,'prompt_body','각 모형에서 달라진 점을\n먼저 문장으로 정리하고,\n그 차이가 보이게 움직여 줘.\n근거 없는 연출은 빼 줘.',[1010,665,440,180],32);
 note(s,'생성한 세 모형 이미지를 비교합니다. 톰슨은 양전하가 퍼진 영역에 전자가 들어 있는 모형, 러더퍼드는 작은 중심 핵, 보어는 구분된 허용 궤도를 강조합니다. 실제 원자의 사진이나 정확한 비율이 아니고 전자 수로 특정 원소를 나타내지 않습니다. 러더퍼드의 경로선도 관측한 전자 궤적이 아닌 설명용 표시입니다. 원자모형이 바뀐 역사는 인물 이름만 교체하는 타임라인으로 끝내지 않습니다. 산란 관찰과 그 해석, 보어의 허용 상태를 설명하면서 왜 이전 설명만으로 부족했는지 연결합니다. 보어 모형은 현대 원자모형의 최종 형태가 아닙니다. 각 모형의 차이를 문장으로 정한 다음 그 의미를 보여 주는 움직임을 고릅니다.',[refs.thomson,refs.rutherford,refs.bohr,'assets/atomic-models/20261028/README.md']);
}
promptSlide(18,'지식 영상은 설명의 순서를 먼저 정합니다','초안을 받은 뒤 핵심 주장과 근거를 대조하고, 움직임을 다듬습니다',
 '톰슨·러더퍼드·보어의 원자모형 변천을 설명하는\n45초 모션 그래픽 초안을 만들어 줘.\n각 모형의 특징, 이전 설명의 한계, 바뀐 이유를\n짧은 문장과 개념 모식도로 보여 줘.\n핵심 주장에 사용한 근거를 연결하고,\n새로 확인해야 할 사실은 따로 표시해 줘.\n보어 모형을 현대 원자모형의 최종 형태로 설명하지 마.',
 [['비교할 것','세 모형의 핵심 차이'],['이어 줄 것','관찰과 설명의 변화'],['구분할 것','모식도·사실·미확인 내용']],
 '첫 결과는 검토할 설명 초안입니다. 주제와 길이뿐 아니라 모형별 특징, 이전 설명의 한계, 변화의 이유를 요청합니다. 주장과 근거의 연결을 먼저 확인한 뒤 문장과 움직임을 맞춥니다. 예를 들어 원자핵을 발견하는 과정에서 관찰한 것과 그 관찰을 설명하는 모형을 구분합니다. 전자가 실제로 보이는 사진처럼 연출하거나 현대의 오비탈을 고전적인 궤도와 같은 뜻으로 쓰지 않게 합니다. 처음부터 완성된 과학 영상이라고 소개하지 않고, 사실을 확인한 설명을 장면표로 바꾸는 다음 단계와 연결합니다. 자료의 정확한 위치는 강사용 사실 기록을 함께 봅니다.',[refs.thomson,refs.rutherford,refs.bohr,'lesson.md 4절 C / 6절 장면표']);
{
 const s=base(19,'관찰한 문제를 한 가지 수정 조건으로','바꿀 부분과 유지할 부분을 함께 말하면 다음 결과를 비교하기 쉽습니다');clear(s);
 txt(s,'feedback-observe','관찰한 문제',[285,535,600,48],29,gray);
 txt(s,'feedback-quote','“마지막 일정이\n너무 빨리 지나가요.”',[285,614,610,170],50,white,true);
 panel(s,'feedback-panel',[970,535,650,345],white);
 txt(s,'feedback-label','다음 요청',[1030,580,530,42],28,'#909090');
 txt(s,'feedback-request','전체 길이는 20초로 유지하고,\n마지막 안내를 4초 동안\n읽을 수 있게 앞 장면의\n시간을 조정해 줘.',[1030,640,530,195],34,'#000000',true);
 txt(s,'feedback-foot','문제: 일정이 빠름     변경: 마지막 안내 4초     유지: 전체 20초',[285,955,1335,50],29,orange,true,'center');
 note(s,'세 예제의 첫 결과에서 발견한 문제를 한 문장으로 바꿉니다. 여기서는 마지막 일정이 빠르다는 관찰을 마지막 안내 4초라는 조건으로 바꿨습니다. 전체 길이 20초는 유지하므로 앞 장면의 시간을 함께 조정해야 합니다. 예쁘게나 자연스럽게 같은 평가만 남기기보다 화면에서 볼 수 있는 조건을 적습니다. B라면 원문에 없는 주장을 지우고, C라면 모형이 달라진 이유를 설명하는 순서를 보완할 수 있습니다. 한 번에 많은 부분을 바꾸지 않고 필요한 한 조건부터 비교합니다. 참가자는 선택한 사례에서 다음 요청 한 문장과 작업의 저장 위치를 남깁니다. 다음 파트에서는 레퍼런스에서 참고할 요소와 이유를 골라 같은 결과를 발전시킵니다.', ['lesson.md V1 3:22~4:18 / V2·V5: 문구와 시간의 일치','R01 PDF 73~77쪽 / R05 PDF 49쪽: 피드백을 다음 기준으로 연결']);
}
await fs.writeFile(path.join(B,'manifest.json'),JSON.stringify({source:'output/webinar-atomic-images/NotionTalk_원자모형_생성이미지반영_21장_v1.pptx',slides:manifest,preserve:[1,2,3,20,21],originalAnimations:true},null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-roundtrip.pptx'));
console.log('Developed Part 1 on slides 4–19; source-brand template and all other slides retained.');
