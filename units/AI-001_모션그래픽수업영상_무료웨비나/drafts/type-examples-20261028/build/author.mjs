import fs from 'node:fs/promises';import path from 'node:path';import{fileURLToPath}from'node:url';import{createRequire}from'node:module';import{PresentationFile,FileBlob}from'@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_10장_효과예시_v4.pptx')));
const specs=[];const reference='학습 참고: [사이클 라이브] 클로드 코드로 만드는 일관된 모션 시스템 (1).pdf';
function edit(s,changes){for(const[name,value]of Object.entries(changes)){const sh=s.shapes.items.find(x=>x.name===name);if(!sh)throw Error(name);sh.text.replace(String(sh.text),value);}}
function shape(s,name,geo,x,y,w,h,fill){return s.shapes.add({name,geometry:geo,position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}});}
function text(s,name,value,x,y,w,h,size=16,color='#AAAAAA'){const sh=shape(s,name,'textbox',x,y,w,h,'none');sh.text=value;sh.text.style={typeface:'Pretendard',fontSize:size,color,alignment:'center',verticalAlignment:'middle'};sh.text.insets=0;return sh;}
async function image(s,spec,kind,x,y,w,h){s.images.add({blob:new Uint8Array(await fs.readFile(path.join(B,'assets',kind+'-poster.png'))),contentType:'image/png',fit:'contain',position:{left:x,top:y,width:w,height:h}});spec.images.push({kind,x,y});}
{
 const s=p.slides.items[4],spec={page:5,source_page:5,edits:{'dev-format-head-2':'움직이는 예시','dev-format-0-1':'문장과 핵심어','dev-format-1-1':'수치와 관계','dev-format-2-1':'화면과 기능','dev-format-3-1':'브랜드와 제목','dev-format-4-1':'그림과 인물'},remove:[],images:[],notes:'유형별 예시는 글자 등장, 0~100% 변화, 가상의 UI 반응, 노션톡 로고 등장, 종이비행기 일러스트의 이동입니다. 수치는 개념 설명용 가상 값이고 UI는 실제 서비스 화면이 아닌 자체 예시입니다. 로고는 사용자가 제공한 원본을 사용했습니다.'};
 edit(s,spec.edits);
 for(let i=0;i<5;i++){const name=`dev-format-${i}-2`;spec.remove.push(name);s.shapes.items.find(x=>x.name===name).delete();await image(s,spec,['typography','infographic','interface','logo','illustration'][i],740,383.3+i*48.67,373.3,36);}
 specs.push(spec);
}
for(const [page,kind]of [[10,'timing'],[11,'easing']]){
 const s=p.slides.items[6].duplicate();
 const spec={page,source_page:7,export_id:s.id,edits:{part_label:'Part 2  움직임과 효과',section_number:'02',section_heading:'시간과 속도'},remove:[],images:[],notes:''};
 const titles=kind==='timing'?['기준 움직임','시작을 늦추기','지속시간 늘리기']:['이즈 인','이즈 아웃','이즈 인아웃'];
 const english=kind==='timing'?['Duration 1.0s','Delay 0.7s','Duration 2.0s']:['Ease In','Ease Out','Ease In Out'];
 const desc=kind==='timing'?['바로 출발해 1초 동안 이동','기다렸다 같은 속도로 이동','같은 거리를 2초 동안 이동']:['천천히 시작해 빨라짐','빠르게 시작해 느려짐','천천히 출발하고 멈춤'];
 Object.assign(spec.edits,{title:kind==='timing'?'시작 시점과 지속시간': '가속과 감속의 세 가지 모습',subtitle:kind==='timing'?'지연시간은 출발 전 대기, 지속시간은 움직이는 데 걸린 시간입니다':'세 공은 같은 거리를 1.8초 동안 이동하며 속도 변화만 다릅니다'});
 for(let i=0;i<3;i++)Object.assign(spec.edits,{[`effect-name-${i}`]:titles[i],[`effect-en-${i}`]:english[i],[`effect-desc-${i}`]:desc[i]});
 edit(s,spec.edits);
 for(const sh of [...s.shapes.items])if(sh.name.startsWith('ex-')){spec.remove.push(sh.name);sh.delete();}
 for(let i=0;i<3;i++){
  const x=180+i*320;await image(s,spec,kind==='timing'?['normal','delay','long'][i]:['ease-in','ease-out','ease-in-out'][i],x+20,451,240,80);
  if(kind==='timing'){
   const origin=x+22,sc=100;
   // A static timeline distinguishes waiting from movement in PDF.
   const wait=i===1?.7:0,dur=i===2?2:1;
   shape(s,`type-time-axis-${i}`,'rect',origin,601,236,2,'#555555');
   if(wait)shape(s,`type-time-wait-${i}`,'rect',origin,594,wait*sc,14,'#666666');
   shape(s,`type-time-active-${i}`,'rect',origin+wait*sc,594,dur*sc,14,'#FF911D');
   text(s,`type-time-note-${i}`,i===1?'회색은 대기 · 주황은 이동':i===2?'이동 2.0초':'이동 1.0초',x+15,615,250,18,13);
  }else{
   for(let j=0;j<5;j++){const u=j/4,v=i===0?u*u:i===1?1-(1-u)**2:u*u*(3-2*u),xx=x+28+224*v;shape(s,`type-ease-dot-${i}-${j}`,'ellipse',xx-4,597,8,8,'#FF911D');}
   text(s,`type-ease-note-${i}`,'작은 점은 같은 시간 간격의 위치',x+15,615,250,18,12);
  }
 }
 spec.notes=kind==='timing'?'지연시간은 대상이 움직이기 전까지 기다리는 시간입니다. 지속시간은 실제 변화가 이어지는 시간입니다. 세 공의 이동 거리는 같습니다. 가운데는 0.7초 늦게 시작하지만 1초 동안 이동하고, 오른쪽은 2초 동안 이동합니다. 시작 대기와 이동 시간을 구분하는 기초 예시입니다.\n'+reference+' 20·23쪽의 시간·순서 개념을 별개의 자체 예시와 설명으로 재구성.':'이즈 인은 점차 빨라지는 변화, 이즈 아웃은 점차 느려지는 변화, 이즈 인아웃은 출발과 도착 구간 모두 천천히 움직이는 변화입니다. 이동 거리와 1.8초의 지속시간을 같게 두어 비교합니다. 작은 점은 같은 시간 간격의 위치입니다.\n'+reference+' 24쪽의 이징 분류를 새 설명과 자체 도형 예시로 재구성. 수치나 용도별 제작 규칙은 인용하지 않음.';
 specs.push(spec);
}
for(const sp of specs)sp.export_page=sp.export_id?p.slides.items.findIndex(s=>s.id===sp.export_id)+1:5;
await fs.writeFile(path.join(B,'edits.json'),JSON.stringify(specs,null,2));await(await PresentationFile.exportPptx(p)).save(path.join(B,'roundtrip.pptx'));console.log('Authored type examples and two basic timing/easing pages using existing templates.');
