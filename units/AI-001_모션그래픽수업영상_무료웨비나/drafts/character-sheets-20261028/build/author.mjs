import fs from 'node:fs/promises';import path from 'node:path';import{fileURLToPath}from'node:url';import{PresentationFile,FileBlob}from'@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_톤과움직임확장_21장_v13.pptx')));
const poses=JSON.parse(await fs.readFile(path.join(U,'assets/character-sheets-20261028/poses.json'),'utf8'));
const placements=[{page:4,pose:'bear-thinking',x:115,y:355,h:300},{page:16,pose:'bear-stopwatch',x:30,y:452,h:190},{page:17,pose:'woman-compare',x:125,y:350,h:305},{page:21,pose:'man-approve',x:190,y:340,h:310}];
const specs=[];
for(const page of [4,6,16,17,18,19,21]){
 const s=p.slides.items[page-1],deleted=[];
 for(const im of [...s.images.items]){
  // Names survive current source import; record source mascots separately in the package stage.
  if((im.name??'').startsWith('mascot-')){deleted.push(im.name);im.delete();}
 }
 const spec={page,remove_old_mascots:true,positions:{},images:[]};
 if(page===19){
  spec.positions={'still-title':{left:185,width:390},'demo-definition':{left:705,width:390}};
  for(const[name,position]of Object.entries(spec.positions)){const sh=s.shapes.items.find(x=>x.name===name);sh.position={...sh.position,...position};}
 }
 const slot=placements.find(x=>x.page===page);
 if(slot){
  const pose=poses.find(x=>x.id===slot.pose),position={left:slot.x,top:slot.y,width:slot.h*pose.aspect_ratio,height:slot.h};
  s.images.add({blob:new Uint8Array(await fs.readFile(pose.file)),contentType:'image/png',fit:'cover',crop:pose.crop,position,alt:'NotionTalk '+pose.id});
  spec.images.push({...pose,name:'character-pose-'+pose.id,position});
 }
 specs.push(spec);
}
await(await PresentationFile.exportPptx(p)).save(path.join(B,'roundtrip.pptx'));
await fs.writeFile(path.join(B,'edits.json'),JSON.stringify(specs,null,2));console.log('Authored four contextual character poses and removed repetitive decoration.');
