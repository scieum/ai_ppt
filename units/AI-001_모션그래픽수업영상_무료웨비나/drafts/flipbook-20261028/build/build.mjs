import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..'),A=path.join(R,'assets/flipbook/20261028');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-fundamentals/NotionTalk_모션그래픽_개념부터실습까지_21장_v2.pptx')));
const s=p.slides.items[3].duplicate(),S=2/3,P=(x,y,w,h)=>({left:x*S,top:y*S,width:w*S,height:h*S});
function edit(k,v){const x=s.shapes.items.find(x=>x.name===k);if(!x)throw Error(k);x.text.replace(String(x.text),v);}
for(const[k,v]of Object.entries({section_number:'01',section_heading:'모션 그래픽 이해하기 · 프레임과 움직임',title:'작은 차이가 움직임이 됩니다',subtitle:'플립북처럼, 조금씩 다른 그림을 빠르게 이어서 보여 줍니다'}))edit(k,v);
const keep=new Set(['part_label','section_number','section_heading','title','subtitle','copyright_footer']);
for(const x of [...s.shapes.items])if(!keep.has(x.name))x.delete();
function rect(name,box,fill,geometry='rect',line='none'){return s.shapes.add({name,geometry,position:P(...box),fill,line:{fill:line,width:line==='none'?0:1.2*S},...(geometry==='roundRect'?{borderRadius:10}:{})});}
function text(name,value,box,size=28,color='#A0A0A0',bold=false){const x=rect(name,box,'none','textbox');x.text=value;x.text.style={typeface:'Pretendard',fontSize:size*S,color,bold,alignment:'center',verticalAlignment:'top',insets:0,wrap:'none',autoFit:'none',lineSpacing:1};return x;}
rect('flipbook-content-clear',[100,490,1720,535],'#000000');
text('book-label','플립북',[270,505,440,40],30,'#FFFFFF',true);
s.images.add({blob:new Uint8Array(await fs.readFile(path.join(A,'flipbook-illustration.png'))),contentType:'image/png',position:P(260,535,460,285),fit:'contain',alt:'생성한 물리적 플립북 개념 삽화, 흰 종이와 주황 공'});
text('sequence-caption','그림을 조금씩 바꾸고',[780,600,300,45],30,'#FFFFFF');
text('sequence-caption-2','빠르게 이어서 보여 주면',[760,652,340,45],30,'#FFFFFF');
text('loop-label','이어지는 움직임',[1130,510,360,42],30,'#FF9228',true);
s.images.add({blob:new Uint8Array(await fs.readFile(path.join(A,'loop-preview.png'))),contentType:'image/png',position:P(1160,562,320,220),fit:'contain',alt:'flipbook-loop-preview'});
const data=JSON.parse(await fs.readFile(path.join(A,'frames.json'),'utf8'));const scale=210/240,y=830;
for(let i=0;i<6;i++){
 const x=255+i*240,[cx,cy]=data.poses[i];
 rect('frame-paper-'+i,[x,y,210,165*scale],'#FFFFFF','roundRect','#DDDDDD');
 rect('frame-baseline-'+i,[x+24*scale,y+137*scale,192*scale,1.5],'#CCCCCC');
 rect('frame-ball-'+i,[x+(cx-14)*scale,y+(cy-14)*scale,28*scale,28*scale],'#FF9228','ellipse');
 text('frame-label-'+i,(i+1)+'장',[x,983,210,27],24);
}
s.speakerNotes.text='발화: 플립북은 각 장의 그림이 조금씩 다릅니다. 이 장면들을 빠르게 이어 보면 움직임으로 보입니다. 영상의 각 장면을 프레임이라고 합니다. 모션 그래픽도 시간에 따라 위치·크기 등의 상태가 조금씩 달라지는 장면을 이어 보여 줍니다. 매 프레임을 손으로 그려야 한다는 뜻은 아닙니다. 코드·키프레임·도구가 중간 상태를 계산할 수 있습니다.\n조작: 왼쪽의 물리적 플립북 삽화와 아래 여섯 그림을 비교하고, 오른쪽의 내장 GIF를 슬라이드쇼에서 재생합니다. 공의 크기와 색은 유지하고 위치만 조금씩 바뀝니다. 반복 GIF는 앞으로 이동한 뒤 되돌아오는 루프입니다.\n대기: 별도 실습 없이 정의 설명 안에서 약 40초 관찰합니다.\n출처 구분: 플립북 삽화는 built-in image_gen으로 새로 생성한 개념 삽화이며 실제 촬영물이나 정확한 프레임 분해도가 아닙니다. 아래 여섯 프레임·SVG·GIF는 자체 수치에 따라 생성했습니다. 기존 대표 5장의 디자인·원본과 번호 묶음을 유지하며 G10 승인을 생성하지 않습니다.\nSource: https://www.adobe.com/uk/creativecloud/animation/discover/flipbook-animation.html ; https://helpx.adobe.com/ae_en/fresco/desktop/draw-paint-animate-and-share/apply-motion-to-artwork.html ; assets/flipbook/20261028/README.md';
await fs.writeFile(path.join(B,'edits.json'),'{}');
await fs.writeFile(path.join(B,'additions.json'),JSON.stringify([{key:'flipbook',template:4,export_slide:p.slides.items.findIndex(x=>x.id===s.id)+1}],null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-roundtrip.pptx'));
console.log('Authored one flipbook slide, six editable frame drawings, generated illustration and loop preview.');
