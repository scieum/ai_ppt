import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url));const spec=JSON.parse(await fs.readFile(path.join(B,'spec.json'),'utf8'));
const p=await PresentationFile.importPptx(await FileBlob.load(spec.source));
let count=0;
for(const e of spec.edits){
 const s=p.slides.items[e.slide-1];const sh=s.shapes.items.find(x=>x.name===e.name);
 if(!sh)throw new Error(`Missing shape ${e.slide}/${e.name}`);
 sh.position=e.position;
 if(e.font_pt!==null)sh.text.style={fontSize:e.font_pt*4/3,...(e.anchor?{verticalAlignment:'top'}:{})};
 count++;
}
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-import.pptx'));
await fs.writeFile(path.join(B,'artifact-edit-log.json'),JSON.stringify({editedTextObjects:count,source:spec.source,preservation:'Apply reviewed text styles and frames to original package to preserve GIF, timing, native tables and unrelated objects.'},null,2));
console.log(`Edited ${count} existing text objects with Artifact Tool.`);
