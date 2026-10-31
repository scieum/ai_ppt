import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-part1-developed/NotionTalk_Part1_내용디자인고도화_21장_v2.pptx')));
const P=(x,y,w,h)=>({left:x*2/3,top:y*2/3,width:w*2/3,height:h*2/3});
function find(s,n){const x=s.shapes.items.find(x=>x.name===n);if(!x)throw Error(n);return x;}
const s8=p.slides.items[7],s9=p.slides.items[8],blue='#7DD3FC';
for(const n of ['demo-fade','demo-slide','demo-zoom'])find(s8,n).text='노션톡';
const wipe=find(s9,'demo-wipe');wipe.text='노션톡\n웨비나 챌린지';wipe.position=P(300,684,360,125);wipe.text.style={fontSize:40*2/3,color:blue,alignment:'center',lineSpacing:1.1};
for(const x of [...s9.shapes.items])if(/^demo-type-/.test(x.name))x.delete();
const chars=[...'노션톡웨비나챌린지'];
for(let i=0;i<chars.length;i++){
 const x=i<6?800+i*48+(i>=3?16:0):888+(i-6)*48;
 const t=s9.shapes.add({name:'demo-type-'+i,geometry:'textbox',position:P(x,i<6?685:745,48,58),fill:'none',line:{fill:'none',width:0}});t.text=chars[i];t.text.style={typeface:'Pretendard',fontSize:40*2/3,bold:true,color:blue,alignment:'center',verticalAlignment:'top',wrap:'none',insets:0,autoFit:'none'};
}
for(const [i,v] of ['노션톡','웨비나','챌린지'].entries()){
 const t=find(s9,'demo-stagger-'+i);t.text=v;t.position=P(1240+i*135,718,130,65);t.text.style={fontSize:32*2/3,color:blue,alignment:'center'};
}
s9.speakerNotes.text=String(s9.speakerNotes.text).replaceAll('수업 영상','노션톡 웨비나 챌린지')+'\n시연 문구: 노션톡 웨비나 챌린지. 왼쪽은 보이는 영역, 가운데는 아홉 글자, 오른쪽은 세 단어의 등장 순서를 비교합니다. 예시 글자는 밝은 하늘색으로 구분합니다.';
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-roundtrip.pptx'));
console.log('Updated page 8 text and page 9 text/color with native editable objects.');
