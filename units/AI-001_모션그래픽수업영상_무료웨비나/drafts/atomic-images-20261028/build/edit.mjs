import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..'),A=path.join(R,'assets/atomic-models/20261028');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-cleanup/NotionTalk_검토장표삭제_21장_v1.pptx'))),s=p.slides.items[16];
if(!s.shapes.items.some(x=>String(x.text).includes('과학사의 변화를 영상으로 설명해요')))throw Error('Wrong image replacement target');
const remove=new Set(['thomson-positive','thomson-electron','orbit','nucleus','electron']);
for(const sh of [...s.shapes.items])if(remove.has(sh.name))sh.delete();
const S=2/3,P=(x,y,w,h)=>({left:x*S,top:y*S,width:w*S,height:h*S});
for(const [i,key]of ['thomson','rutherford','bohr'].entries()){
 s.images.add({blob:new Uint8Array(await fs.readFile(path.join(A,key+'.png'))),contentType:'image/png',fit:'contain',position:P(310+i*200,560,190,230),alt:'Generated conceptual '+key+' atomic model'});
 const label=s.shapes.items.find(x=>x.name==='model-label-'+i);label.position=P(300+i*200,807,210,42);
}
const caption=s.shapes.add({geometry:'textbox',name:'atomic-model-caption',position:P(305,867,600,34),fill:'none',line:{fill:'none',width:0}});caption.text='개념 모식도 · 전자 수와 크기 비율 단순화';caption.text.style={typeface:'Pretendard',fontSize:22*S,color:'#9E9E9E',alignment:'center',verticalAlignment:'top',wrap:'none',insets:0,autoFit:'none'};
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-roundtrip.pptx'));
console.log('Replaced the simple atomic model diagrams with three generated raster illustrations.');
