import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const source=path.join(R,'output/webinar-part1-developed/NotionTalk_Part1_내용디자인고도화_21장_v5.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load(source)),original=[...p.slides.items],additions=[],animations=[],notes=[];
const O='#FF9228',G='#A0A0A0',W='#FFFFFF',BLUE='#7DD3FC',S=2/3;
const P=(x,y,w,h)=>({left:x*S,top:y*S,width:w*S,height:h*S});
const common=new Set(['part_label','section_number','section_heading','title','subtitle','copyright_footer']);
const refs={lesson:'lesson.md: V1~V6의 자막·설명란 분석. 화면 배치나 프롬프트 전문의 검증 자료와 구분.',pdf:'docs/ai-training-reference-analysis.md: R02 23~24·52·91쪽, R03 31쪽, R05 31쪽의 설명·요청·결과 연결 원리.',ease:'https://www.adobe.com/uk/creativecloud/animation/discover/easing.html',notion:'https://www.notion.com/help/columns-headings-and-dividers',md:'https://www.markdownguide.org/basic-syntax/',science:'https://openstax.org/books/chemistry-2e/pages/6-2-the-bohr-model'};
function shape(s,name,box,fill,geometry='roundRect'){return s.shapes.add({name,geometry,position:P(...box),fill,line:{fill:'none',width:0},...(geometry==='roundRect'?{borderRadius:30*S}:{})});}
function text(s,name,value,box,size=34,color=W,bold=false,align='left'){
 const t=s.shapes.add({name,geometry:'textbox',position:P(...box),fill:'none',line:{fill:'none',width:0}});t.text=value;t.text.style={typeface:'Pretendard',fontSize:size*S,color,bold,alignment:align,verticalAlignment:'top',wrap:'word',autoFit:'none',insets:0,lineSpacing:1.12};return t;
}
function edit(s,name,value){const t=s.shapes.items.find(x=>x.name===name);if(!t)throw Error(name);t.text.replace(String(t.text),value);return t;}
function fresh(page,key,part,num,section,title,subtitle){
 const s=original[13].duplicate();for(const t of [...s.shapes.items])if(!common.has(t.name))t.delete();
 for(const[k,v]of Object.entries({part_label:part,section_number:num,section_heading:section,title,subtitle}))edit(s,k,v);
 shape(s,'full-clear',[100,495,1720,510],'#000000','rect');
 additions.push({key,page,template:14,slide:s,title,part,section,num});return s;
}
function speaker(s,page,body,sourceKeys=['lesson','pdf']){s.speakerNotes.text=body+'\n\n근거·참고: '+sourceKeys.map(k=>refs[k]||k).join('\n')+'\n수치와 요청문은 이번 강의를 위한 자체 예시입니다. 설계 예시는 실제 앱 실행 결과와 구분해 설명합니다.';notes.push({page,body,sources:sourceKeys});}
function foot(s,v){text(s,'full-foot',v,[260,952,1400,46],29,O,true,'center');}
function prompt(s,v,caption){shape(s,'full-prompt-panel',[260,540,1400,350],W);text(s,'full-prompt-text',v,[325,588,1270,300],35,'#000000');if(caption)foot(s,caption);}
function cols(s,leftTitle,left,rightTitle,right,{leftColor=W,rightColor=W}={}){
 text(s,'full-left-title',leftTitle,[285,535,620,46],29,G);text(s,'full-right-title',rightTitle,[1010,535,620,46],29,G);
 text(s,'full-left',left,[285,620,620,255],42,leftColor,true);text(s,'full-right',right,[1010,620,620,255],42,rightColor,true);
}
function table(s,values,widths,box=[245,530,1430,380],size=31){
 const tb=s.tables.add({rows:values.length,columns:values[0].length,left:box[0]*S,top:box[1]*S,width:box[2]*S,height:box[3]*S,columnWidths:widths.map(x=>x*S),values});
 tb.styleOptions={headerRow:false,bandedRows:false};tb.borders.assign({fill:'#414141',width:.65});
 for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){const cell=tb.getCell(r,c);cell.fill=r===0?'#303030':'#1D1D1D';cell.text.style={typeface:'Pretendard',fontSize:(r===0?size-1:size)*S,color:r===0?O:W,bold:r===0,alignment:'left',verticalAlignment:'middle'};}
 return tb;
}
const part2='Part 2  레퍼런스로 방향 잡기',part3='Part 3  첫 결과의 움직임 다듬기',part4='Part 4  다음 제작에도 쓰는 Markdown',part5='Part 5  외부 도구로 소재 확장하기';
{
 const s=fresh(20,'ref-scope',part2,'01','참고할 요소 정하기','레퍼런스에서 필요한 원리를 고릅니다','첫 결과의 어떤 문제를 해결할지 먼저 정합니다');
 text(s,'full-hero','등장 순서\n읽는 시간\n장면 전환',[285,560,650,280],64,O,true);
 text(s,'full-reasons','한꺼번에 나오는 정보를 나누기\n마지막 안내를 읽을 시간 확보하기\n설명이 끊기는 지점 연결하기',[1010,580,650,280],37,W);
 foot(s,'오늘은 두 가지 조건만 골라 같은 초안에 적용합니다');
 speaker(s,20,'Part 1에서 받은 첫 결과를 다시 봅니다. 참고 자료를 더하기 전에 어떤 부분이 아쉬웠는지 떠올리게 합니다. 정보가 한꺼번에 나오면 등장 순서를, 마지막 안내가 빠르면 읽는 시간을, 설명이 끊기면 장면 전환을 볼 수 있습니다. 필요한 두 조건과 이유를 먼저 정합니다. 같은 초안에 적용해야 어떤 조건이 결과를 바꿨는지 비교하기 쉽습니다. 참고 자료를 많이 모으는 것보다 무엇을 볼지 고르는 작업에 집중합니다.');
}
{
 const s=fresh(21,'content-vs-style',part2,'01','내용과 표현의 출처','내용의 근거와 시각 참고는 역할이 다릅니다','같은 URL을 두 역할로 사용한다면 각각의 이유를 따로 적습니다');
 table(s,[['구분','무엇을 가져올까','우리 예제'],['내용의 근거','설명할 사실·정보','Notion 문서의 기능과 쓰임'],['시각 참고','등장 순서·읽는 시간·전환','핵심어를 차례로 보여 주기'],['자체 기획','우리 문구·사례·장면 순서','교사가 자료를 정리하는 상황']],[290,570,570]);
 speaker(s,21,'웹사이트 URL은 먼저 무엇을 설명할지 정하는 내용의 근거입니다. 화면의 움직임이나 분위기를 참고하려면 그 역할을 별도로 지정합니다. B 예제에서는 Notion 문서의 블록·목차·공동 편집을 확인하고, 교사가 자료를 정리하는 상황으로 새 장면을 구성할 수 있습니다. 내용을 확인하는 일과 시각 참고를 선택하는 일을 구분하면 원문에 없는 기능이나 효과를 덧붙이는 문제를 줄일 수 있습니다.',['lesson','notion']);
}
{
 const s=fresh(22,'read-a-scene',part2,'01','한 장면 관찰하기','한 장면을 세 시점으로 나누어 봅니다','정지 이미지 한 장으로 실제 움직임과 속도를 단정하지 않습니다');
 cols(s,'먼저 볼 시점','등장 전\n움직이는 동안\n모두 나온 뒤','관찰할 내용','시선이 시작하는 위치\n이동 방향과 속도 변화\n문구가 머무는 시간',{leftColor:O});
 foot(s,'재생할 수 있는 자료에서는 시간도 직접 확인합니다');
 speaker(s,22,'재생 가능한 참고 자료를 잠시 멈추며 등장 전, 움직이는 동안, 모두 나온 뒤를 나누어 봅니다. 시작 위치와 이동 방향, 도착 후 머무는 시간을 말로 적습니다. 정지 이미지만 있으면 색·배치·서체 정도를 볼 수 있고 실제 속도나 전환을 관찰했다고 기록하지 않습니다. 이번 자료의 PDF는 정지 화면이며 기존 효과 시연은 PPT 슬라이드쇼로 확인합니다. 관찰과 추정을 구분하는 연습입니다.');
}
{
 const s=fresh(23,'reference-prompt',part2,'02','참고 범위를 요청에 넣기','참고할 요소와 이유를 함께 요청합니다','원본의 고유 문구·사례 대신 우리 강의의 표현을 사용합니다');
 prompt(s,'첨부한 레퍼런스의 등장 순서와 장면 전환을 분석해 줘.\n참고할 조건 두 가지와 우리 영상에 필요한 이유를 먼저 설명해 줘.\n우리 문구와 사례는 유지하고, 선택한 움직임의 원리를\nNotion 문서 소개 초안에 적용해 줘.\n참고한 부분과 새로 구성한 부분을 나누어 알려 줘.','내용을 바꾸는 요청과 움직임을 바꾸는 요청을 구분합니다');
 speaker(s,23,'레퍼런스를 첨부한 다음 바로 비슷하게 만들어 달라고 하기보다 참고 범위를 먼저 말합니다. 여기서는 등장 순서와 장면 전환을 골랐습니다. 적용 전에 이유를 설명하게 하면 목적에 맞지 않는 참고를 줄일 수 있습니다. 문구와 사례는 우리가 작성한 내용을 유지합니다. 원본의 독특한 서사나 캐릭터를 재현하는 요청으로 바꾸지 않습니다. 이 요청문은 실제 첨부 자료를 준비한 뒤 사용하며, 도구가 영상을 읽었는지도 별도로 확인합니다.');
}
{
 const s=fresh(24,'website-scene',part2,'02','웹사이트 소개에 적용','기능이 쓰이는 상황을 장면으로 만듭니다','사이트의 문구를 나열하는 단계에서 설명 흐름으로 발전시킵니다');
 cols(s,'원문에서 고른 정보','블록으로 구성\n목차로 이동\n함께 편집','우리가 설명할 상황','흩어진 자료를 한 문서에\n필요한 부분을 바로 찾기\n같은 문서를 함께 고치기',{leftColor:BLUE});
 foot(s,'정보의 근거는 원문에, 장면의 문구와 구성은 우리 목적에 맞춥니다');
 speaker(s,24,'Notion 문서 소개의 세 정보를 실제로 사용하는 상황과 연결합니다. 블록은 흩어진 자료를 구성하는 장면, 목차는 필요한 부분을 찾아가는 장면, 공동 편집은 같은 문서를 함께 고치는 장면으로 설명할 수 있습니다. 오른쪽은 우리 강의가 기획한 설명 예시이며 원문의 보장 문구를 그대로 옮긴 것이 아닙니다. 실제 기능과 영상의 주장이 대응하는지 확인한 뒤 시각 참고를 적용합니다.',['lesson','notion']);
}
{
 const s=fresh(25,'independent-expression',part2,'02','참고 원리와 자체 표현','참고한 원리와 새로 만든 표현을 대조합니다','색만 바꾸는 것에서 더 나아가 문구와 장면을 직접 구성합니다');
 table(s,[['부분','참고한 원리','우리 영상에서 정할 것'],['등장','중요한 정보부터 순서대로','우리 기능 설명의 순서'],['강조','핵심어 한 곳에 시선 모으기','어떤 문구를 강조할지'],['전환','같은 요소로 다음 설명 연결','우리 내용에 맞는 연결 장면'],['자산','사용 가능한 범위 확인','로고·이미지·음악의 출처']],[280,580,570],undefined,30);
 speaker(s,25,'레퍼런스에서 읽은 원리와 실제로 사용한 표현을 나누어 봅니다. 순서와 강조라는 원리를 참고하더라도 문구·사례·장면의 연결은 우리 목적에 맞게 새로 정합니다. 원본 파일을 가지고 있거나 출처를 적었다는 사실만으로 모든 재사용 조건이 확인되는 것은 아닙니다. 외부 자산을 실제로 쓴다면 출처와 이용 범위를 남깁니다. 이 페이지는 검토 방법을 설명하며 특정 결과의 법적 적합성이나 전체 권리 승인을 확정하지 않습니다.');
}
{
 const s=fresh(26,'reference-exercise',part2,'02','내 자료에 적용하기','참고 조건 두 가지로 다시 요청합니다','한 번의 수정에서 바뀐 부분을 눈으로 비교합니다');
 prompt(s,'우리 영상의 문구와 전체 길이는 유지해 줘.\n첫 번째 기능을 보여 준 뒤 다음 기능이 나타나도록 순서를 바꾸고,\n마지막 요약 문구는 충분히 읽을 수 있게 유지해 줘.\n적용한 참고 조건 두 가지를 설명하고 결과를 다시 보여 줘.','직접 만들기 또는 같은 조건의 시연을 관찰하기');
 speaker(s,26,'참가자가 고른 두 조건을 자기 영상의 다음 요청에 넣습니다. 이 예에서는 기능의 등장 순서와 마지막 요약의 읽는 시간을 고쳤습니다. 변경 전후를 같은 구간에서 재생하며 문구와 길이는 그대로인지 봅니다. 생성 대기나 접근 오류가 있으면 강사가 준비한 동일 조건의 예시를 관찰하고, 어떤 조건이 어떻게 바뀌어야 하는지 기록합니다. Part 3에서는 이 변화를 더 구체적인 모션 언어로 다듬습니다.');
}
{
 const s=fresh(27,'motion-diagnosis',part3,'01','첫 결과의 문제 읽기','첫 결과에서 고칠 조건을 찾습니다','Part 1의 용어를 실제 화면의 문제와 연결합니다');
 cols(s,'화면에서 본 문제','안내가 너무 빨리 지나감\n모든 요소가 동시에 움직임\n도착할 때 갑자기 멈춤','고칠 조건','마지막 안내의 유지 시간\n요소별 등장 순서\n끝부분의 속도 변화',{leftColor:G,rightColor:O});
 foot(s,'원하는 느낌을 화면에서 확인할 수 있는 조건으로 바꿉니다');
 speaker(s,27,'Part 3는 효과 이름을 다시 외우는 시간이 아닙니다. Part 1에서 배운 속성·시간·순서를 실제 문제에 붙이는 시간입니다. 마지막 안내가 빠르면 유지 시간, 모든 정보가 동시에 나오면 시작 순서, 멈춤이 거칠면 속도 변화를 고릅니다. 한 번의 요청에 한 조건부터 바꾸면 전후 차이를 확인하기 쉽습니다.');
}
{
 const s=fresh(28,'reading-time',part3,'01','읽는 시간 확보','전체 20초 안에서 안내 시간을 늘립니다','노션톡 홍보 영상 20초의 시간 배분 예시입니다');
 table(s,[['장면','수정 전 설계','수정 후 설계'],['주제·핵심어 전개','0~18초 · 18초','0~16초 · 16초'],['일정·참여 안내','18~20초 · 2초','16~20초 · 4초'],['전체 길이','20초','20초']],[450,490,490]);
 foot(s,'마지막 2초를 늘린 만큼 앞 장면에서 2초를 조정합니다');
 speaker(s,28,'이 표는 실제 출력 결과가 아니라 시간을 비교하기 위한 설계 예시입니다. 마지막 안내가 2초라 읽기 어렵다면 4초로 늘리고 앞의 전개를 18초에서 16초로 줄일 수 있습니다. 전체 길이는 20초로 유지합니다. 앞 장면을 줄였을 때 그 문구가 너무 빨라지면 문구를 간결하게 하거나 전체 길이를 다시 정해야 합니다. 4초는 이번 예제의 비교 값이며 모든 문장의 정답은 아닙니다.');
}
{
 const s=fresh(29,'one-emphasis',part3,'01','강조의 우선순위','가장 먼저 볼 핵심어를 하나 고릅니다','색과 크기의 변화에도 전달할 우선순위가 필요합니다');
 text(s,'emphasis-left-label','강조가 많을 때',[285,535,600,45],29,G);text(s,'emphasis-right-label','핵심어를 골랐을 때',[1010,535,620,45],29,G);
 text(s,'emphasis-left','노션톡\n웨비나\n챌린지',[285,615,620,270],64,O,true,'center');
 text(s,'emphasis-right-a','노션톡',[1010,615,620,65],46,W,false,'center');text(s,'emphasis-right-b','웨비나',[1010,695,620,100],78,BLUE,true,'center');text(s,'emphasis-right-c','챌린지',[1010,809,620,65],46,W,false,'center');
 foot(s,'핵심어는 화면에 나타날 때 한 번만 강조하는 예시입니다');
 animations.push({key:'one-emphasis',name:'emphasis-right-b',effect:23,duration:.8,delay:.4});
 speaker(s,29,'두 구성은 같은 문구를 사용합니다. 왼쪽처럼 모든 글자가 같은 색과 크기로 강조되면 무엇을 먼저 읽을지 분명하지 않을 수 있습니다. 오른쪽에서는 웨비나를 핵심어로 골랐습니다. 우리 영상의 목적에 따라 핵심어는 달라질 수 있습니다. 글자 하나를 크게 보여 주는 변화가 의미와 맞는지 확인합니다. 시연에서는 오른쪽 핵심어가 한 번 확대되어 나타나도록 구성했습니다.');
}
{
 const s=fresh(30,'ordered-features',part3,'02','등장 순서 조정','설명하는 순서대로 정보가 나타납니다','여러 기능을 한꺼번에 보여 줄 때와 차례로 볼 때를 비교합니다');
 text(s,'order-left-label','한꺼번에 제시',[285,535,620,45],29,G);text(s,'order-right-label','한 기능씩 제시',[1010,535,620,45],29,G);
 ['구성하기','찾아가기','함께 편집하기'].forEach((v,i)=>{text(s,'order-left-'+i,v,[285,625+i*90,620,65],48,W,true,'center');text(s,'order-right-'+i,v,[1010,625+i*90,620,65],48,BLUE,true,'center');animations.push({key:'ordered-features',name:'order-right-'+i,effect:10,duration:.5,delay:.4+i*.65});});
 foot(s,'앞의 설명이 끝나기 전에 다음 핵심어가 시선을 빼앗지 않게 합니다');
 speaker(s,30,'같은 세 기능을 한꺼번에 볼 때와 시간차를 두고 볼 때를 비교합니다. 중요한 것은 느리게 만드는 것 자체가 아니라 설명의 순서와 보이는 순서를 맞추는 것입니다. 한 기능을 설명하는 동안 다음 기능이 먼저 강조되면 시선이 분산될 수 있습니다. 이번 시연은 단어마다 0.65초의 시작 차이를 둔 예시이며 실제 내레이션 길이에 맞춰 조정합니다.');
}
{
 const s=original[9].duplicate();additions.push({key:'applied-easing',page:31,template:10,slide:s,title:'같은 이동도 멈추는 방식이 다릅니다',part:part3,section:'등장과 멈춤의 속도',num:'02',copyAnimation:true});
 for(const[k,v]of Object.entries({part_label:part3,section_number:'02',section_heading:'등장과 멈춤의 속도',title:'같은 이동도 멈추는 방식이 다릅니다',subtitle:'거리와 전체 이동 시간은 같게 두고, 끝부분의 속도만 비교합니다','timing-terms':'비교 시연: 같은 거리 · 같은 지속 시간 1.8초','easing-caption':'이즈 아웃은 끝에서 느려집니다 · 읽는 유지 시간은 별도로 정합니다'}))edit(s,k,v);
 speaker(s,31,'두 도형은 같은 거리와 1.8초라는 같은 지속 시간으로 이동합니다. 아래쪽은 끝부분에서 속도를 줄여 멈추도록 설정했습니다. 같은 시간이어도 속도 변화가 다르면 도착하는 느낌이 달라집니다. 이즈 아웃은 끝에서 느려지는 표현입니다. 이동을 부드럽게 만든 뒤에도 글자를 읽는 유지 시간은 따로 확보합니다. 아래 설명을 멈춤 애니메이션과 연결해 보여 줍니다.',['ease']);
}
{
 const s=fresh(32,'sound-and-reading',part3,'02','소리와 읽는 시간','소리를 더해도 글자는 읽을 수 있어야 합니다','먼저 무음으로 확인하고, 강조할 순간에 소리를 맞춥니다');
 cols(s,'먼저 확인','문구를 끝까지 읽을 수 있는가\n설명 순서를 따라갈 수 있는가','소리를 더한 뒤','강조되는 순간이 맞는가\n문구가 너무 빨리 사라지지 않는가',{leftColor:W,rightColor:BLUE});
 foot(s,'문구 유지 시간은 두고, 필요한 등장 시점부터 조정합니다');
 speaker(s,32,'음악의 박자에 맞춘다고 문구가 지나가는 시간을 무조건 줄이지 않습니다. 먼저 무음으로 읽히는지 확인한 뒤 핵심어가 나타나는 순간이나 전환 시점에 소리를 맞춥니다. 박자가 빨라서 안내 문구가 너무 빨리 사라지면 읽는 시간은 유지하고 등장 시점을 조정합니다. 이 페이지는 비교 방법을 설명하며 무음·유음 영상이 실제로 내장된 장표는 아닙니다. 음악과 음성을 사용할 때는 출처와 이용 조건도 남깁니다.');
}
{
 const s=fresh(33,'concrete-revision',part3,'02','수정 요청 정리','바꿀 조건과 유지할 조건을 함께 적습니다','서로 다른 세 사례에도 같은 요청 원리를 적용할 수 있습니다');
 table(s,[['사례','바꿀 조건','유지할 조건'],['A 타이포그래피','마지막 안내 4초','전체 20초·필수 문구'],['B 웹사이트 소개','기능별 순차 등장','원문 정보·전체 30초'],['C 수업 보조 영상','변화의 순서가 보이는 장면','확인한 사실·전체 45초']],[390,530,510]);
 speaker(s,33,'A는 마지막 안내의 유지 시간, B는 기능의 등장 순서, C는 변화가 보이는 장면 구성을 고칠 수 있습니다. 각각 무엇을 유지할지도 함께 말합니다. 이렇게 하면 수정 요청 때문에 날짜나 사실, 전체 길이까지 원치 않게 바뀌는 것을 줄일 수 있습니다. 참가자는 자기 사례에서 변경 조건 한 가지와 유지 조건 한 가지를 적습니다. 반복해서 쓸 기준은 다음 Part 4에서 문서로 남깁니다.');
}
{
 const s=fresh(35,'lesson-brief',part4,'01','목적과 규칙을 파일로','LESSON_BRIEF.md에 목적을 적습니다','누구에게 무엇을 설명할지 정하면 장면을 고를 기준이 생깁니다');
 prompt(s,'# 수업 보조 영상 브리프\n대상: 원자모형을 처음 배우는 학생\n목표: 세 모형의 차이와 변화의 순서를 설명한다\n길이: 45초 / 비율: 16:9\n소재: 톰슨·러더퍼드·보어의 개념 모식도\n근거: 확인한 원자료와 주장별 출처','학습 목표는 장면마다 무엇을 보여 줄지 정하는 기준입니다');
 speaker(s,35,'실습 자료의 LESSON_BRIEF.md를 열어 봅니다. Markdown은 제목과 목록 등으로 구조를 표현할 수 있는 텍스트 형식입니다. 여기서는 문법을 많이 배우기보다 목적을 파일로 남기는 데 사용합니다. 대상·목표·길이·비율·원자료를 한곳에 모으면 다음 생성에서도 기준을 다시 전달할 수 있습니다. 원자모형은 시계열 설명을 위한 구체 예시이며 다른 수업 주제로 교체할 수 있습니다. 실제 파일에는 주장별 근거와 미확인 상태도 남겨 둡니다.',['md','science']);
}
{
 const s=fresh(36,'visual-rules',part4,'01','목적과 규칙을 파일로','화면 규칙은 파일로 남깁니다','VISUAL_RULES.md에 다음 생성에도 적용할 기준을 적습니다');
 prompt(s,'# 화면과 움직임 규칙\n비율: 16:9 / 배경: 검정 / 기본 글자: 흰색\n주황: 주제 강조 / 하늘색: 비교 예시\n한 장면의 핵심어는 하나를 먼저 강조한다\n문구가 모두 나온 뒤 읽는 시간을 확보한다\n모식도는 실제 사진·정확한 비율과 구분한다','문구·로고·색과 시간의 기준을 구체적으로 남깁니다');
 speaker(s,36,'같은 요청을 반복할 때 매번 색과 문구, 모션 조건을 다시 설명하지 않도록 기준을 파일로 남깁니다. 흑백과 주황을 기본으로 쓰되 비교 예시는 하늘색으로 구분합니다. 로고는 사용자 제공 원본을 쓰고, 한글이나 날짜를 이미지에 섞어 정확도를 잃지 않도록 편집 가능한 글자로 처리합니다. 규칙은 도구가 실제로 읽고 반영했는지 결과에서 확인해야 합니다. 파일이 있다는 사실만으로 자동 적용되었다고 보지 않습니다.',['md','lesson']);
}
{
 const s=fresh(37,'scene-plan',part4,'02','네 장면과 시간표','SCENE_PLAN.md로 45초를 나눕니다','장면의 설명 역할과 움직임을 함께 적습니다');
 table(s,[['시간','설명의 역할','화면과 동작'],['0~5초','질문으로 주제 열기','비교 공간과 핵심 질문'],['5~17초','첫 모형의 특징','양전하 영역과 전자 구분'],['17~30초','관찰과 설명의 변화','관찰을 먼저, 핵 해석을 뒤에'],['30~45초','허용 궤도와 정리','상태 구분 후 비교 문장 유지']],[270,540,620],[245,525,1430,410],30);
 foot(s,'5 + 12 + 13 + 15 = 45초');
 speaker(s,37,'실습 자료의 SCENE_PLAN.md를 열어 네 장면을 봅니다. 질문 5초, 첫 모형 12초, 관찰과 해석 13초, 허용 궤도와 정리 15초로 전체 45초입니다. 이 시간표는 설계 예시이므로 실제 문구와 내레이션을 읽으며 조정합니다. 장면마다 무엇을 설명하는지와 움직임이 어떤 역할을 하는지를 함께 씁니다. 원자핵의 존재를 설명하는 모형과 실제 산란 관찰을 혼동하지 않도록 문구와 출처를 분리합니다.',['lesson','science']);
}
{
 const s=fresh(38,'use-three-files',part4,'02','문서로 다시 제작하기','세 문서를 참조해 같은 영상을 다시 만듭니다','문서를 읽었다는 설명과 실제 반영 결과를 함께 확인합니다');
 prompt(s,'첨부한 LESSON_BRIEF.md, VISUAL_RULES.md, SCENE_PLAN.md를 읽어 줘.\n먼저 세 파일에서 적용할 조건과 서로 충돌하는 부분을 정리해 줘.\n확인한 내용으로 45초 수업 보조 영상 초안을 구성하고,\n문구·장면 순서·시간표가 어떻게 반영되었는지 알려 줘.\n파일을 읽지 못했거나 구현하기 어려운 조건은 먼저 알려 줘.','파일 존재와 실제 참조·반영은 별도로 확인합니다');
 speaker(s,38,'세 파일을 실제 작업에 첨부하거나 현재 환경에서 읽을 수 있는 경로로 참조합니다. 먼저 적용 조건과 충돌을 정리하게 합니다. 전체 길이와 장면표가 다르거나 규칙과 필수 문구가 충돌하면 생성 전에 수정합니다. 그다음 결과에서 문구·장면 순서·시간이 어떻게 반영되었는지 봅니다. 도구가 파일을 읽었다고 답하는 것과 결과에 실제 반영되는 것은 별도 확인입니다. 앱마다 파일 참조 방법이 다르므로 존재하지 않는 메뉴나 기능을 가정하지 않습니다.',['lesson','md']);
}
{
 const s=fresh(39,'edit-one-row',part4,'02','문서로 다시 제작하기','정리 시간을 늘리면 다른 장면도 맞춥니다','전체 45초를 유지하는 시간표 수정 예시입니다');
 table(s,[['장면','수정 전','수정 후'],['질문','0~5초 · 5초','0~5초 · 5초'],['첫 모형','5~17초 · 12초','5~17초 · 12초'],['관찰·해석','17~30초 · 13초','17~27초 · 10초'],['정리 포함 마지막 장면','30~45초 · 15초','27~45초 · 18초']],[490,470,470],[245,525,1430,410],30);
 foot(s,'마지막 3초를 늘리고, 앞 장면의 문구·시간을 함께 조정합니다');
 speaker(s,39,'마지막 정리 시간이 부족해 3초를 더 주고 싶다면 앞 장면이나 전체 길이를 함께 조정해야 합니다. 이 표는 전체 45초를 유지하는 예입니다. 관찰과 해석 구간을 13초에서 10초로 줄이고 마지막을 15초에서 18초로 늘렸습니다. 앞의 설명이 너무 빨라지면 문구를 덜거나 전체 길이를 늘리는 선택도 필요합니다. 장면 시작·종료 시간과 내레이션, 마지막 요약 문구를 함께 맞춘 뒤 재생합니다. 표의 숫자만 바꾸고 실제 결과를 확인하지 않는 상태를 완료라고 하지 않습니다.');
}
{
 const s=fresh(40,'reuse-for-next-topic',part4,'03','다음 수업에 재사용','다음 영상에서는 주제와 근거를 교체합니다','파일의 역할은 유지하고, 새 내용에 맞춰 장면을 다시 설계합니다');
 table(s,[['문서','유지할 수 있는 것','새로 정할 것'],['LESSON_BRIEF.md','항목과 작성 구조','대상·목표·주제·원자료'],['VISUAL_RULES.md','브랜드·서체·기본 표현','핵심어·읽는 시간·소리'],['SCENE_PLAN.md','시간·문구·동작·근거 열','장면 수·순서·설명 내용']],[400,500,530]);
 speaker(s,40,'다음 수업에서 원자모형 대신 물의 순환이나 절차 안내를 선택해도 세 파일의 역할은 같습니다. 목적과 근거를 교체하고 그 설명에 맞는 장면을 다시 정합니다. 모든 주제를 네 장면 45초에 억지로 맞추지 않습니다. 반복해서 도움이 되는 규칙만 유지하고 주제에 맞지 않는 모션은 덜어 냅니다. 다음 제작에 실제로 어떤 파일을 첨부할지, 바꿔야 할 항목은 무엇인지 확인하며 Part 4를 마칩니다.',['md','lesson']);
}
{
 const s=fresh(42,'external-scene',part5,'01','장면 소재 선택','외부 소재가 필요한 장면 하나를 고릅니다','글자·수치와 별도로, 도입에 쓸 짧은 배경 장면을 설계합니다');
 s.images.add({blob:new Uint8Array(await fs.readFile(path.join(R,'assets/webinar-full/20261028/concept-background.png'))),contentType:'image/png',fit:'contain',position:P(245,535,850,410),alt:'Generated abstract conceptual still for introductory footage; not a scientific observation or finished video.'});
 text(s,'external-scene-label','소재 설계 예시',[1160,555,485,48],29,O,true);
 text(s,'external-scene-text','5초 · 16:9\n차분한 배경 움직임\n설명을 방해하지 않는 구도\n글자와 로고는 별도 합성',[1160,635,485,230],35,W);
 text(s,'external-scene-caption','생성한 정지 이미지 · 실제 관측이나 완성 영상이 아닌 구상 예시',[245,956,1420,40],25,G,false,'center');
 speaker(s,42,'먼저 어떤 장면에 외부 소재가 필요한지 고릅니다. 여기서는 영상의 도입에 쓸 추상 배경을 예로 듭니다. 화면의 이미지는 별도로 생성한 정지 구상 예시이고 실제 원자의 관측 자료나 완성된 동영상이 아닙니다. 정확한 과학 설명은 앞의 확인한 문구와 모식도로 전달하고, 이 소재는 분위기와 도입을 돕는 역할만 맡깁니다. 필요한 장면 하나를 고르면 외부 요청의 범위와 비용을 판단하기도 쉽습니다.');
}
{
 const s=fresh(43,'external-request',part5,'01','외부 제작 요청','외부 도구에 소재 조건을 전달합니다','연결된 도구와 계정에서 지원하는 기능을 먼저 확인합니다');
 prompt(s,'도입에 사용할 5초, 16:9 배경 영상 소재를 만들어 줘.\n검정 배경에 주황빛 유리 구체와 얇은 빛의 곡선이\n차분하게 움직이고, 카메라는 천천히 이동하게 해 줘.\n문자와 로고는 별도 편집에서 넣을 수 있게 여백을 남겨 줘.\n요청 조건·작업 상태·실제 출력 파일을 확인할 수 있게 알려 줘.','외부 도구가 없는 참가자는 시연과 같은 입력 조건을 관찰합니다');
 speaker(s,43,'힉스필드 같은 외부 제작 서비스는 현재 연결 상태와 계정에서 지원하는 기능을 먼저 확인합니다. 앱 이름만 언급했다고 자동으로 커넥터가 실행되는 것은 아닙니다. 필요한 소재의 길이·비율·움직임·여백을 명시하고 실제 작업을 요청합니다. 화면의 예시는 강의용 요청문이며 이미 실행된 작업 ID나 파일을 뜻하지 않습니다. 작업 상태와 결과 파일을 확인하고, 사용할 장면의 역할에 맞는지 재생해서 판단합니다. 계정이 없는 참가자는 같은 입력과 판단 기준을 관찰합니다.');
}
{
 const s=fresh(44,'composite-frame',part5,'02','정확한 글자와 합성','생성한 소재 위에 정확한 문구를 얹습니다','배경 소재와 편집 가능한 글자의 역할을 나눕니다');
 s.images.add({blob:new Uint8Array(await fs.readFile(path.join(R,'assets/webinar-full/20261028/concept-background.png'))),contentType:'image/png',fit:'contain',position:P(250,525,950,435),alt:'Abstract background in an illustrative composited frame.'});
 text(s,'composite-headline','보이지 않는 원자,\n설명은 어떻게 바뀌었을까?',[300,650,800,150],49,W,true);
 text(s,'composite-caption','합성 장면 예시 · 생성 정지 배경 + 편집 가능한 문구',[280,912,900,40],25,G);
 text(s,'composite-right','배경 소재에서 조정\n분위기·구도·카메라\n\n편집에서 조정\n한글·날짜·로고·읽는 시간',[1260,570,450,330],32,W);
 speaker(s,44,'이 장표는 생성한 정지 배경에 편집 가능한 문구를 얹은 합성 예시입니다. 외부 생성 영상이 완성되었다는 뜻은 아닙니다. 배경의 분위기와 구도는 소재 단계에서 조정하고 한글·날짜·브랜드·읽는 시간은 편집 가능한 요소로 관리합니다. 이렇게 나누면 글자 하나를 고치기 위해 배경 전체를 다시 만들 필요가 줄어듭니다. 실제 영상 소재를 받았을 때도 동일하게 원래 장면표의 시간에 맞춰 연결하고 끝까지 재생합니다.');
}
{
 const s=fresh(45,'external-fallback',part5,'02','상태와 결과 확인','작업 상태와 실제 파일을 구분합니다','실패나 지연이 생기면 확인한 지점에서 이어갑니다');
 table(s,[['상황','먼저 확인','이어가는 방법'],['요청이 시작되지 않음','연결·계정·지원 기능','조건을 확인하고 요청 다시 준비'],['생성 중 또는 지연','실제 작업 상태','같은 조건의 사전 예시 관찰'],['파일을 받음','재생·길이·비율·장면 의미','장면표에 연결한 뒤 다시 재생'],['출력 형식이 다름','미리보기와 파일 형식','필요한 내보내기 경로 확인']],[400,500,530],[245,525,1430,410],29);
 speaker(s,45,'요청 문구가 보이는 것, 작업이 시작된 것, 파일을 받은 것은 서로 다른 상태입니다. 시작되지 않으면 연결과 계정, 지원 기능을 확인합니다. 생성 중이면 실제 상태를 확인하고 기다리는 동안 같은 조건의 사전 예시를 사용합니다. 파일을 받으면 길이·비율·의미가 맞는지 재생한 뒤 장면표에 연결합니다. 재생 가능한 미리보기와 MP4 출력은 다를 수 있습니다. 사전 결과를 사용했다면 현재 생성 결과인 것처럼 소개하지 않습니다. 실제 수업에서 쓸 파일이 무엇인지 마지막으로 확인합니다.');
}
{
 const s=original[1].duplicate();additions.push({key:'five-stage-review',page:46,template:2,slide:s,title:'다섯 단계가 서로 다른 문제를 해결합니다',part:'마무리  오늘의 제작 흐름',section:'첫 요청부터 재사용까지',num:'01'});
 const values={part_label:'마무리  오늘의 제작 흐름',section_number:'01',section_heading:'첫 요청부터 재사용까지',title:'다섯 단계가 서로 다른 문제를 해결합니다',subtitle:'처음부터 완벽하게 요청하기보다, 필요한 조건을 하나씩 더합니다',summary_label:'다음 영상',summary_text:'잘 작동한 조건과 원자료를 함께 남깁니다'};
 const rows=[['첫 요청','목적·문구·기본 길이','초안'],['레퍼런스','참고 요소와 이유','참고 범위'],['모션 지식','시간·강조·순서 조정','수정 조건'],['Markdown','목적·규칙·장면표','재사용'],['외부 소재','필요한 장면 한 부분','확장']];
 rows.forEach((r,i)=>{values['heading_'+i]=r[0];values['description_'+i]=r[1];values['tag_'+i]=r[2];});for(const[k,v]of Object.entries(values))edit(s,k,v);
 speaker(s,46,'처음에는 목적과 문구, 길이로 초안을 만듭니다. 참고 자료는 방향을 정하고, 모션 지식은 관찰한 문제를 구체적인 조건으로 바꿉니다. 반복할 조건은 문서로 남기고 외부 소재는 필요한 장면에만 사용합니다. 타이포그래피·웹사이트 소개·수업 보조 영상 중 어느 예제로 시작했더라도 같은 흐름을 적용할 수 있습니다. 다음 영상에 가져갈 조건과 자료가 무엇인지 한 가지씩 떠올리게 합니다.');
}
{
 const s=fresh(47,'takeaway-files','마무리  다음 영상 준비','01','실습 자료 저장','오늘의 파일로 다음 영상을 시작합니다','실습 자료에는 요청문과 세 Markdown 예시를 함께 담았습니다');
 text(s,'files-list','LESSON_BRIEF.md\nVISUAL_RULES.md\nSCENE_PLAN.md\nPROMPTS.md',[300,550,900,310],48,W,true);
 text(s,'files-action','내 주제로 바꾸기\n근거 자료 연결하기\n수정한 조건 남기기\n결과와 함께 저장하기',[1270,575,430,300],34,O,true);
 foot(s,'파일 이름보다 중요한 것은, 다음 생성에서 실제로 참조하는 것입니다');
 speaker(s,47,'실습 자료 폴더에는 세 제작 문서와 요청문 모음을 제공합니다. 예시를 복사한 뒤 대상과 주제, 근거, 문구를 자기 상황으로 바꿉니다. 어떤 조건을 고쳤는지와 결과 파일 또는 작업 링크도 함께 저장합니다. 예제 파일에는 확인이 필요한 상태가 표시되어 있으므로 기록되지 않은 실제 실행이나 권리 확인을 완료로 바꾸지 않습니다. 다음 영상에서는 이 파일들을 실제 작업에 참조하고 변경이 반영되었는지 재생합니다.',['md','lesson']);
}
{
 const s=fresh(48,'questions','마무리  질의응답','02','함께 이야기하기','질의응답','만들고 싶은 영상이나 막힌 지점을 함께 이야기해 주세요');
 text(s,'questions-hero','다음에는 어떤 영상을\n만들고 싶으신가요?',[280,560,1360,220],76,W,true,'center');
 text(s,'questions-bottom','홍보 타이포그래피    웹사이트 소개    수업 보조 영상',[280,865,1360,65],36,O,true,'center');
 speaker(s,48,'질문을 받습니다. 만들고 싶은 결과, 사용한 입력 자료, 막힌 구간을 함께 말해 달라고 안내합니다. 모든 질문을 새 기능 설명으로 넓히기보다 오늘의 다섯 단계 중 어느 지점의 문제인지 연결합니다. 개별 환경의 오류는 실제 화면과 조건을 확인한 뒤 판단하고 확인하지 않은 기능이나 비용을 단정하지 않습니다. 마지막에는 다음 제작에서 할 한 가지를 정하고 마칩니다.',['lesson']);
}
if(additions.length!==27)throw Error('Expected 27 additions, got '+additions.length);
await fs.writeFile(path.join(B,'additions.json'),JSON.stringify(additions.map(x=>({...x,slide:undefined,export_slide:p.slides.items.findIndex(s=>s.id===x.slide.id)+1})),null,2));
await fs.writeFile(path.join(B,'animations.json'),JSON.stringify(animations,null,2));
await fs.writeFile(path.join(B,'new-notes.json'),JSON.stringify(notes,null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-roundtrip.pptx'));
console.log('Authored 27 additions for the complete 48-slide webinar.');
