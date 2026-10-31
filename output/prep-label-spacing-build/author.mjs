import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';import {FileBlob,Presentation,PresentationFile} from '@oai/artifact-tool';
import {shape} from '../../assets/layout-library-20261028/recipes/components.mjs';
const B=path.dirname(fileURLToPath(import.meta.url));const R=path.resolve(B,'../..');
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_폰트간격점검_43장_v29.pptx')));
const s=p.slides.items[2];
for(const name of ['choose-one','watch-demo']){const sh=s.shapes.items.find(x=>x.name===name);if(!sh)throw Error(name);sh.position={...sh.position,top:616};}
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-import.pptx'));
const c=Presentation.create({slideSize:{width:1280,height:720}});const cs=c.slides.add();
shape(cs,'optional-container',760,564,380,38.666666666666664,'#242424','roundRect','#454545');
await(await PresentationFile.exportPptx(c)).save(path.join(B,'container.pptx'));
console.log('Authored matching optional label container and spaced both captions.');
