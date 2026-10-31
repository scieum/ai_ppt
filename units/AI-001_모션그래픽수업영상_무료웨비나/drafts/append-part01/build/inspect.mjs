import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const build=path.dirname(fileURLToPath(import.meta.url)),unit=path.resolve(build,'../../..'),root=path.resolve(unit,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
const {FontLibrary}=req('skia-canvas');
FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(root,'output/webinar-samples/NotionTalk_모션그래픽_주황포인트_자체사례_v5.pptx')));
for(const n of [1,4]){
const s=p.slides.items[n];console.log(JSON.stringify({slide:n+1,shapes:s.shapes.items.map(x=>({id:x.id,name:x.name,text:String(x.text)})),images:s.images.items.map(x=>({id:x.id,alt:x.alt,position:x.position})),shapeMethods:Object.getOwnPropertyNames(Object.getPrototypeOf(s.shapes.items[0])),imageMethods:Object.getOwnPropertyNames(Object.getPrototypeOf(s.images.items[0]))}));
}
await fs.writeFile(path.join(build,'imported.json'),JSON.stringify(p.toProto()));
