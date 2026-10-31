import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_기초지식_10장_v2.pptx')));
const edits={7:{'effect-desc-0':'나타났다 서서히 사라지기','effect-desc-1':'왼쪽에서 제자리로 이동','effect-desc-2':'커졌다 다시 작아지기'},8:{'reveal-desc-0':'왼쪽부터 영역이 열림','reveal-desc-1':'한 글자씩 차례로 표시','reveal-desc-2':'단어가 시간차를 두고 등장'}};
const all=[];
function addShape(s,name,geo,x,y,w,h,fill,rot=0){const sh=s.shapes.add({name,geometry:geo,position:{left:x,top:y,width:w,height:h,rotation:rot},fill,line:{fill:'none',width:0}});return sh;}
function text(s,name,txt,x,y,w,h,size,color='#AAAAAA',bold=false){const sh=addShape(s,name,'textbox',x,y,w,h,'none');sh.text=txt;sh.text.style={typeface:'Pretendard',fontSize:size,color,bold,alignment:'center',verticalAlignment:'middle'};sh.text.insets=0;return sh;}
const orange='#FF911D',blue='#75D3F7';
for(const page of [6,7,8,9]){
 const s=p.slides.items[page-1],spec={page,remove:[],edits:Object.keys(edits[page]||{}),images:[],notes:''};
 for(const [name,value]of Object.entries(edits[page]||{})){const sh=s.shapes.items.find(x=>x.name===name);sh.text.replace(String(sh.text),value);}
 if(page===7||page===8){
  spec.remove=s.shapes.items.filter(x=>page===7?['demo-fade','demo-slide','demo-zoom'].includes(x.name):x.name.startsWith('demo-')).map(x=>x.name);
  for(const name of spec.remove)s.shapes.items.find(x=>x.name===name).delete();
  const kinds=page===7?['fade','slide','zoom']:['reveal','typewriter','stagger'];
  for(let c=0;c<3;c++){
   const x=180+c*320,kind=kinds[c];
   const image=s.images.add({blob:new Uint8Array(await fs.readFile(path.join(B,'assets',kind+'-poster.png'))),contentType:'image/png',alt:`motion-example-${kind}`,fit:'contain',position:{left:x+20,top:451,width:240,height:80}});
   spec.images.push({alt:`motion-example-${kind}`,kind});
   // Three editable snapshots show the temporal change in PDF and handouts.
   for(let k=0;k<3;k++){
    const xx=x+16+k*84,cy=594;
    addShape(s,`ex-${kind}-cell-${k}`,'rect',xx,583,80,35,'#292929');
    text(s,`ex-${kind}-time-${k}`,['시작','중간','끝'][k],xx,621,80,14,12);
    if(kind==='fade')text(s,`ex-${kind}-state-${k}`,'노션톡',xx,586,80,27,19,[orange,orange,'#51402D'][k]);
    if(kind==='slide'){
     addShape(s,`ex-${kind}-track-${k}`,'rect',xx+8,606,64,1,'#555555');
     text(s,`ex-${kind}-state-${k}`,'톡',xx+1+k*23,586,32,27,19,orange);
    }
    if(kind==='zoom')text(s,`ex-${kind}-state-${k}`,'노션톡',xx,584,80,31,[12,25,12][k],orange);
    if(kind==='reveal'){
     // Different visible widths distinguish a mask reveal from whole glyphs.
     text(s,`ex-${kind}-state-${k}`,'노션톡',xx,585,80,28,20,blue);
     if(k<2){const edge=xx+12+56*[.15,.55][k];addShape(s,`ex-${kind}-mask-${k}`,'rect',edge,584,xx+80-edge,30,'#292929');}
    }
    if(kind==='typewriter')text(s,`ex-${kind}-state-${k}`,['노','노션','노션톡'][k],xx,585,80,28,20,blue);
    if(kind==='stagger'){
     for(let j=0;j<=k;j++)addShape(s,`ex-${kind}-tile-${k}-${j}`,'roundRect',xx+10+j*21,594,16,13,blue);
    }
   }
  }
  // A faint first stage makes fade in/out visible in the static sequence.
  if(page===7)s.shapes.items.find(x=>x.name==='ex-fade-state-0').text.style={color:'#51402D'};
  spec.notes=page===7?'같은 노션톡 글자로 페이드 인·아웃, 슬라이드 인, 확대·축소가 반복됩니다. 아래 세 상태는 왼쪽부터 시간 순서입니다. 페이드는 불투명도, 슬라이드는 위치, 줌·스케일은 크기가 변합니다.':'세 반복 예시는 같은 노션톡 웨비나 챌린지를 보여줍니다. 리빌은 가려진 영역이 연속해서 열리고, 타이프라이터는 완성된 글자가 하나씩 추가됩니다. 순차 등장은 세 단어가 시차를 두고 나타나는 모습입니다. 아래 세 상태는 시간 순서입니다.';
 }
 if(page===6){
  for(let c=0;c<4;c++){
   const x=160+c*(760/3),kind=['position','scale','rotation','opacity'][c];
   for(let k=0;k<3;k++){
    const xx=x+16+k*62;
    if(c===0){addShape(s,`ex-${kind}-track-${k}`,'rect',xx,607,56,1,'#555555');addShape(s,`ex-${kind}-state-${k}`,'ellipse',xx+3+k*16,593,12,12,orange);}
    if(c===1){const r=8+k*5;addShape(s,`ex-${kind}-state-${k}`,'ellipse',xx+28-r/2,601-r/2,r,r,orange);}
    if(c===2)addShape(s,`ex-${kind}-state-${k}`,'rect',xx+12,598,32,7,orange,[-35,-17,0][k]);
    if(c===3)addShape(s,`ex-${kind}-state-${k}`,'ellipse',xx+20,593,16,16,['#4D3926','#A46024',orange][k]);
   }
  }
  spec.notes='각 카드의 큰 도형은 위치·크기·각도·불투명도의 변화를 보여줍니다. 카드 아래의 세 작은 상태는 왼쪽부터 시작·중간·끝입니다.';
 }
 if(page===9){
  // Equal-time positions remain visible in static PDF while the large balls animate.
  for(let row=0;row<2;row++)for(let k=0;k<5;k++){
   const u=k/4,px=520+(row===0?u:1-(1-u)**2)*443.3;
   addShape(s,`ex-easing-${row}-${k}`,'ellipse',px-5,443.3+row*100,10,10,'#77512D');
   text(s,`ex-easing-time-${row}-${k}`,['0','¼','½','¾','1'][k],px-14,461+row*100,28,16,12,'#AAAAAA');
  }
  spec.notes='큰 공 두 개는 같은 거리와 1.8초 동안 이동합니다. 일정한 속도는 같은 시간마다 같은 거리를 이동하고, 끝 감속은 끝에 가까워질수록 같은 시간 동안 이동하는 거리가 짧습니다. 작은 점은 전체 시간을 네 구간으로 나눈 각 시점의 위치입니다.';
 }
 all.push(spec);
}
await fs.writeFile(path.join(B,'edits.json'),JSON.stringify(all,null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(B,'roundtrip.pptx'));
console.log('Authored editable effect snapshots and six animation panels inside the existing design.');
