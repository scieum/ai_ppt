import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';import{PresentationFile,FileBlob}from'@oai/artifact-tool';import{C,shape,text}from'./components.mjs';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..');
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_캐릭터시트적용_21장_v14.pptx')));const specs=[];
for(const page of [15,17,21]){
 const s=p.slides.items[page-1],keep=new Set(['part_label','section_number','section_heading','title','subtitle','copyright_footer','clear-content']);if(page===17){keep.add('still-title');keep.add('demo-definition');}
 const remove=s.shapes.items.filter(x=>!keep.has(x.name)).map(x=>x.name);for(const x of [...s.shapes.items])if(!keep.has(x.name))x.delete();
 const sp={page,remove,positions:{},styles:{},picture_positions:{},layout_id:page===15?'L14':page===17?'L07':'L10'};
 const box=(name,x,y,w,h,fill=C.card,g='roundRect')=>shape(s,'asset-'+name,x,y,w,h,fill,g);
 const txt=(name,value,x,y,w,h,size=22,color=C.white,bold=false,align='left')=>text(s,'asset-'+name,value,x,y,w,h,size,color,bold,align);
 if(page===15){
  const heads=['기준 움직임','시작을 늦추기','지속시간 늘리기'];const defs=['바로 출발해 1초 동안 이동','0.7초 기다린 뒤 1초 동안 이동','바로 출발해 2초 동안 이동'];const tags=['Duration 1.0s','Delay 0.7s · Duration 1.0s','Duration 2.0s'];
  for(let i=0;i<3;i++){const y=350+i*96;box('time-row-'+i,170,y,943,82);txt('time-num-'+i,'0'+(i+1),190,y+16,55,43,27,C.orange,true,'center');txt('time-head-'+i,heads[i],270,y+8,240,31,23,C.white,true);txt('time-tag-'+i,tags[i],270,y+44,260,25,15,C.muted);txt('time-desc-'+i,defs[i],545,y+8,290,30,18,C.white);box('time-track-'+i,545,y+57,275,7,'#404040','rect');if(i===1)box('time-wait-'+i,545,y+57,77,7,'#999999','rect');box('time-active-'+i,545+(i===1?77:0),y+57,i===2?222:111,7,C.orange,'rect');sp.picture_positions[['type-example-normal','type-example-delay','type-example-long'][i]]={left:852,top:y+2,width:240,height:80};}
  txt('time-note','주황은 이동, 회색은 대기 구간입니다. 세 예시는 같은 거리로 비교합니다',170,649,943,30,19,C.orange,false,'center');
 }
 if(page===17){
  for(const[name,x]of[['still-title',445],['demo-definition',805]]){sp.positions[name]={left:x,top:354,width:300,height:55};sp.styles[name]={fontSize:32};const t=s.shapes.items.find(a=>a.name===name);t.position={...t.position,...sp.positions[name]};t.text.style={fontSize:32};}
  txt('ref-left-label','이미지에서 참고할 것',445,414,300,30,20,C.muted,false,'center');txt('ref-right-label','영상에서 참고할 것',805,414,300,30,20,C.muted,false,'center');
  for(let i=0;i<2;i++){const y=457+i*79;box('ref-left-row-'+i,430,y,330,63);box('ref-right-row-'+i,790,y,330,63);txt('ref-left-'+i,['색·글자·소재·구도','정지 화면의 모습'][i],447,y+10,296,42,21,C.white,false,'center');txt('ref-right-'+i,['등장 순서·속도·장면 전환','시간에 따른 변화'][i],807,y+10,296,42,21,C.white,false,'center');}
  txt('ref-note','각 자료에서 무엇을 참고할지 적어 함께 전달합니다',370,636,800,35,20,C.orange,true,'center');
 }
 if(page===21){
  for(let i=0;i<2;i++){const x=500+i*325;box('finish-input-'+i,x,345,303,90);txt('finish-input-title-'+i,['스토리라인 확정','스틸컷 수정 반영'][i],x+15,357,273,35,23,C.white,true,'center');txt('finish-input-desc-'+i,['장면 순서와 핵심 문구','색·구도·글자 확인'][i],x+15,398,273,25,18,C.muted,false,'center');}
  box('finish-arrow-1',798,443,26,23,C.orange,'downArrow');box('finish-confirm-bg',500,476,628,62,'#603B1D');txt('finish-confirm','수정 내용을 다시 확인',518,484,592,44,25,C.white,true,'center');box('finish-arrow-2',798,545,26,23,C.orange,'downArrow');box('finish-output-bg',500,580,628,62);txt('finish-output','전체 영상 제작',518,588,592,42,27,C.orange,true,'center');
  txt('finish-note','미리 확인하면 반복 생성에 드는 토큰과 시간을 줄일 수 있습니다',170,651,943,22,17,C.orange,false,'center');
 }
 specs.push(sp);
}
await(await PresentationFile.exportPptx(p)).save(path.join(B,'application-roundtrip.pptx'));await fs.writeFile(path.join(B,'application-edits.json'),JSON.stringify(specs,null,2));console.log('Applied reusable step rows, paired comparison and pipeline layouts.');
