import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';import{createRequire}from'node:module';import{PresentationFile,FileBlob}from'@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');const req=createRequire(import.meta.resolve('@oai/artifact-tool'));req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_19장_영상핵심5장확장_v8.pptx')));const original=[...p.slides.items];
const mapping=[1,2,3,4,5,6,7,8,9,11,12,16,17,18,19,14],specs=[];
function shape(s,name,g,x,y,w,h,fill='#FF911D'){return s.shapes.add({name:'reflow-'+name,geometry:g,position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}});}
function text(s,name,value,x,y,w,h,size=20,color='#AAAAAA',bold=false,align='center'){const sh=shape(s,name,'textbox',x,y,w,h,'none');sh.text=value;sh.text.style={typeface:'Pretendard',fontSize:size,color,bold,alignment:align,verticalAlignment:'middle'};sh.text.insets=0;return sh;}
function panelPositions(){return{'still-panel':{left:430,width:330},'moving-panel':{left:790,width:330},'still-label':{left:445,width:300},'moving-label':{left:805,width:300},'still-title':{left:445,width:300},'demo-definition':{left:805,width:300},'still-caption':{left:445,width:300},'moving-caption':{left:805,width:300}};}
async function addImage(s,sp,file,name,x,y,w,h,layer='front'){s.images.add({blob:new Uint8Array(await fs.readFile(file)),contentType:'image/png',fit:'contain',position:{left:x,top:y,width:w,height:h}});sp.images.push({file,name,x,y,w,h,layer});}
async function mascot(s,sp,kind,x,y,w,h){await addImage(s,sp,path.join(U,'assets/mascots-20261028',kind+'-guide-v1.png'),'mascot-'+kind,x,y,w,h);}
for(let i=0;i<mapping.length;i++){
 const page=i+1,src=mapping[i],s=original[src-1].duplicate(),sp={page,source_page:src,export_id:s.id,edits:{},remove:[],positions:{},styles:{},images:[]};
 if(page>=3&&page<=11){Object.assign(sp.edits,{part_label:'Part 1  모션 그래픽 기본 지식',section_number:page<=5?'01':page<=9?'02':'03',section_heading:page<=5?'뜻과 종류':page<=9?'움직임과 효과':'시간과 속도'});}
 if(page===2){
  Object.assign(sp.edits,{part_label:'오늘의 흐름',section_number:'01',section_heading:'기본 개념부터 제작까지',title:'오늘은 이 순서로 진행합니다',subtitle:'기본을 익히고, 두 레퍼런스를 모아, 미리 확인한 뒤 제작합니다'});
  sp.remove=s.shapes.items.filter(x=>x.name.startsWith('dev-case')||x.name.includes('clear')).map(x=>x.name);
  await addImage(s,sp,path.join(R,'assets/reference-templates/agenda/background.png'),'roadmap-reference-background',0,0,1280,720,'back');
  for(let k=0;k<4;k++){
   const x=202+k*240;text(s,'roadmap-step-'+k,'0'+(k+1),x,373,170,24,17,'#FF911D',true);
   text(s,'roadmap-label-'+k,['기본 지식','이미지·영상\n레퍼런스','스토리라인 .md\n스틸컷 2장','수정 후\n영상 제작'][k],x,410,170,85,23,'#FFFFFF',true);
  }
  text(s,'roadmap-bottom','모습과 움직임을 함께 정하고, 작은 결과부터 확인합니다',170,600,943,35,21,'#FF911D',true);
  sp.notes='오늘의 순서는 기본 지식, 이미지·영상 레퍼런스, 스토리라인 .md와 대표 스틸컷 두 장, 수정 후 제작입니다. 중복되던 개념 소개와 용어 정리, 레퍼런스 비교, 사전 확인 개요는 각 단계에 통합했습니다.';
 }
 if(page===3){sp.positions=panelPositions();await mascot(s,sp,'bear',70,335,220,330);}
 if(page===5)await mascot(s,sp,'woman',1130,402,128,192);
 if(page===10)sp.notes='지연시간은 출발 전 기다림, 지속시간은 실제 변화의 길이입니다. 기존 지속시간·이징 개요 장표의 시간 정의를 여기로 통합했습니다. 세 예시의 이동 거리와 원래 GIF를 유지합니다.';
 if(page===11)sp.notes='이즈 인·아웃·인아웃은 움직이는 동안의 속도 변화입니다. 기존 개요의 이징 정의와 일정 속도의 차이를 이 설명에 묶었습니다. 같은 거리·같은 1.8초를 유지한 기존 GIF와 같은 시간 간격의 위치 표시를 보존합니다.';
 if(page===12){
  Object.assign(sp.edits,{part_label:'Part 2  이미지·영상 레퍼런스',section_number:'01',section_heading:'두 자료를 함께 넣기',title:'이미지·영상 레퍼런스 함께 넣기','dev-definition-takeaway':'각 자료에서 무엇을 참고할지 적어 함께 전달합니다'});
  sp.positions=panelPositions();sp.remove=s.shapes.items.filter(x=>x.name.startsWith('lesson7-color-chip')||x.name.startsWith('lesson7-motion-dot')).map(x=>x.name);
  for(let k=0;k<3;k++)shape(s,'ref-color-'+k,'ellipse',555+k*20,526,10,10,['#FF911D','#75D3F7','#FFFFFF'][k]);
  for(let k=0;k<3;k++)shape(s,'ref-time-'+k,'ellipse',915+k*22,526,10,10);
  await mascot(s,sp,'woman',70,335,220,330);
  sp.notes='정지 이미지와 영상은 전달하는 정보가 다르므로 함께 제공합니다. 이미지에서는 색·글자·소재·구도, 영상에서는 등장 순서·속도·전환을 참고한다고 구체적으로 적습니다. 기존 두 시행착오 비교 장표는 이 역할 구분에 통합했습니다. 참고 자료가 하나뿐이면 반드시 실패한다는 뜻은 아닙니다.\n참고: https://www.youtube.com/watch?v=7xOcIYWGG0A&t=43 , 00:43~04:42 및 04:46~06:38. 캐릭터와 패널은 자체 구성입니다.';
 }
 if(page===13||page===14)Object.assign(sp.edits,{part_label:'Part 3  스토리라인과 스틸컷 확인',section_number:'01',section_heading:'글과 두 장면으로 미리 보기'});
 if(page===13)await mascot(s,sp,'man',1130,402,128,192);
 if(page===14){
  Object.assign(sp.positions,{'still-title':{left:205,width:255},'demo-definition':{left:720,width:255},'still-caption':{top:568,height:28},'moving-caption':{top:568,height:28}});
  sp.remove=s.shapes.items.filter(x=>x.name.startsWith('lesson7-still-a-')).map(x=>x.name);
  await mascot(s,sp,'bear',488,421,82,123);await mascot(s,sp,'woman',1000,421,82,123);
 }
 if(page===15||page===16)Object.assign(sp.edits,{part_label:'Part 4  수정 후 제작',section_number:'01',section_heading:'피드백을 반영하고 진행하기'});
 if(page===15)Object.assign(sp.edits,{title:'고칠 부분을 정하고 다시 확인','lesson7-feedback-note':'수정된 스틸컷과 해당 영상 구간을 확인한 뒤 제작을 진행합니다'});
 if(page===16){
  Object.assign(sp.edits,{title:'확인한 방향으로 영상을 제작합니다',subtitle:'스토리라인과 스틸컷을 확정한 뒤 전체 제작으로 넘어갑니다'});
  sp.remove=s.shapes.items.filter(x=>x.name.startsWith('effect-')||x.name.startsWith('preview-')).map(x=>x.name);
  await mascot(s,sp,'man',150,335,220,330);
  for(let k=0;k<3;k++){
   const y=371+k*89;shape(s,'finish-row-'+k,'roundRect',500,y,640,72,'#202020');
   text(s,'finish-count-'+k,'0'+(k+1),520,y+19,60,35,24,'#FF911D',true);
   text(s,'finish-head-'+k,['스토리라인 확정','스틸컷 수정 반영','전체 영상 제작'][k],595,y+8,510,30,24,'#FFFFFF',true,'left');
   text(s,'finish-body-'+k,['장면 순서와 핵심 문구 확인','색·구도·글자 등 시각 요소 확인','확인한 내용으로 움직임과 시간을 완성'][k],595,y+39,510,24,17,'#AAAAAA',false,'left');
  }
  text(s,'finish-saving','미리 확인하면 반복 생성에 드는 토큰과 시간을 줄일 수 있습니다',170,650,943,28,19,'#FF911D',true);
  sp.notes='스토리라인과 대표 스틸컷을 먼저 확인하고 필요한 수정을 반영한 다음 전체 영상 제작을 진행합니다. 중복되던 사전 확인 개요는 이 마지막 진행 순서와 앞선 두 장면 확인에 통합했습니다. 반복 생성을 줄이면 토큰과 시간을 아낄 수 있으나 수치나 절감률을 보장하지 않습니다.\n참고: https://www.youtube.com/watch?v=7xOcIYWGG0A&t=564 , 09:24~10:13. .md 형식과 새 노션톡 장면은 사용자 요청/자체 구성입니다.';
 }
 for(const[name,value]of Object.entries(sp.edits)){const sh=s.shapes.items.find(x=>x.name===name);if(!sh)throw Error(`${page}: ${name}`);sh.text.replace(String(sh.text),value);}
 for(const name of sp.remove){const sh=s.shapes.items.find(x=>x.name===name);if(sh)sh.delete();}
 for(const[name,pos]of Object.entries(sp.positions)){const sh=s.shapes.items.find(x=>x.name===name);sh.position={...sh.position,...pos};}
 for(const[name,style]of Object.entries(sp.styles))s.shapes.items.find(x=>x.name===name).text.style=style;
 sp.export_page=p.slides.items.findIndex(x=>x.id===sp.export_id)+1;specs.push(sp);
}
await fs.writeFile(path.join(B,'edits.json'),JSON.stringify(specs,null,2));await(await PresentationFile.exportPptx(p)).save(path.join(B,'roundtrip.pptx'));console.log('Authored 16-slide narrative with consolidated content and recurring NotionTalk characters.');
