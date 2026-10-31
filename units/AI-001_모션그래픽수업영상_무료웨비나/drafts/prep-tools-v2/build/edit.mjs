import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const b=path.dirname(fileURLToPath(import.meta.url)),u=path.resolve(b,'../../..'),root=path.resolve(u,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const source=path.join(root,'output/webinar-part01-added/NotionTalk_대표5장유지_Part0_Part1추가_9장_v1.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load(source));
const s=p.slides.items[2];
const keep=new Set(['part_label','section_number','section_heading','title','copyright_footer']);
for(const sh of [...s.shapes.items])if(!keep.has(sh.name))sh.delete();
for(const im of [...s.images.items])im.delete();
s.background.fill='#000000';
function replace(name,value){const x=s.shapes.items.find(v=>v.name===name);x.text.replace(String(x.text),value);}
replace('section_heading','실습에 사용할 도구');replace('title','오늘의 준비물');
const S=2/3,pos=(x,y,w,h)=>({left:x*S,top:y*S,width:w*S,height:h*S});
function text(name,value,box,size,color='#FFFFFF',bold=false){
 const sh=s.shapes.add({geometry:'textbox',name,position:pos(...box),fill:'none',line:{fill:'none',width:0}});
 sh.text=value;sh.text.style={typeface:'Pretendard',fontSize:size*S,color,bold,alignment:'center',verticalAlignment:'top',insets:0,autoFit:'none',wrap:'none',lineSpacing:1};
}
s.images.add({blob:new Uint8Array(await fs.readFile(path.join(root,'assets/branding/notiontalk-white.png'))),contentType:'image/png',fit:'contain',position:pos(1480,68,346,100),alt:'사용자 제공 NotionTalk 원본 로고'});
for(const [key,x,label] of [['claude',370,'클로드'],['codex',760,'코덱스'],['higgsfield',1310,'힉스필드']]){
 s.images.add({blob:new Uint8Array(await fs.readFile(path.join(root,'assets/tool-logos/orange-v2/png',key+'-front.png'))),contentType:'image/png',fit:'contain',position:pos(x,500,230,230),alt:'앞서 제작한 '+label+' 주황 포인트 도구 배지'});
 text(key+'-label',label,[x-30,757,290,55],34,'#FFFFFF',true);
}
text('or','또는',[632,584,96,60],36,'#9E9E9E');
s.shapes.add({geometry:'rect',name:'requirements-separator',position:pos(1090,520,2,420),fill:'#333333',line:{fill:'none',width:0}});
text('required','유료 계정 필수',[300,846,760,58],38,'#FF9228',true);
text('choose-one','클로드 또는 코덱스 중 하나',[300,906,760,50],30);
text('optional','있으면 좋아요',[1140,846,570,58],38,'#FF9228',true);
text('watch-demo','없으면 시연을 보세요',[1140,906,570,50],30);
s.speakerNotes.text='사용자 최신 지시: 추가 4장 미리보기의 1번인 Part 0 준비물 장표(전체 PPT 3쪽)의 이전 카드·내용을 제거하고 앞서 제작한 Claude·Codex·Higgsfield 로고 배지를 사용했습니다. 클로드 또는 코덱스 중 하나의 유료 계정은 필수이며 힉스필드는 선택입니다. 힉스필드 계정이 없으면 강사 시연을 관찰합니다. 두 AI 도구 모두 구독하거나 힉스필드를 유료로 구매하라는 뜻이 아닙니다. 기존 대표 5장과 나머지 예제 3장은 변경하지 않습니다. 도구 배지는 assets/tool-logos/orange-v2의 기존 파일 그대로이며 생성한 새 공식 로고라고 표시하지 않습니다. 기존 G10 검토 상태는 유지합니다.';
const render=path.join(u,'renders/prep-tools-v2');await fs.mkdir(render,{recursive:true});
const png=await p.export({slide:s,format:'png',scale:1.5});await fs.writeFile(path.join(render,'preparation.png'),new Uint8Array(await png.arrayBuffer()));
await(await PresentationFile.exportPptx(p)).save(path.join(b,'edited-roundtrip.pptx'));
console.log('Edited preparation slide only; ready to preserve all unrelated package parts.');
