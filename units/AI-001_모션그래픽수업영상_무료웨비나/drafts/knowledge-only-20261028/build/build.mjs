import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-complete/NotionTalk_모션그래픽_전체웨비나_48장_v2.pptx')));
const original=[...p.slides.items],specs=JSON.parse(await fs.readFile(path.join(B,'content.json'),'utf8'));
for(const spec of specs){
 const s=original[spec.source_page-1].duplicate();
 for(const [name,value]of Object.entries(spec.edits)){
  const sh=s.shapes.items.find(x=>x.name===name);if(!sh)throw Error(`Missing ${name} on source ${spec.source_page}`);
  sh.text.replace(String(sh.text),value);
 }
 for(const [name,style]of Object.entries(spec.styles||{})){
  const sh=s.shapes.items.find(x=>x.name===name);if(!sh)throw Error(name);sh.text.style={...style};
 }
 for(const name of spec.remove||[]){const sh=s.shapes.items.find(x=>x.name===name);if(sh)sh.delete();}
 if(spec.table){const tb=s.tables.items[0];for(let r=0;r<spec.table.length;r++)for(let c=0;c<spec.table[r].length;c++)tb.getCell(r,c).value=spec.table[r][c];}
 s.speakerNotes.text=spec.note+'\n\n근거: '+spec.sources.join('\n')+'\n'+spec.refs.map(x=>`V${x.video} ${x.channel}: ${x.url}`).join('\n');
 spec.export_id=s.id;
}
for(const spec of specs)spec.export_page=p.slides.items.findIndex(x=>x.id===spec.export_id)+1;
await fs.writeFile(path.join(B,'edited-index.json'),JSON.stringify(specs,null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(B,'roundtrip.pptx'));
console.log('Authored ten knowledge-only slides using the existing templates.');
