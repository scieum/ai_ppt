import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {conclusionBar} from '../../assets/layout-library-20261028/logic-patterns-20261030/conclusion-bar.mjs';
const B=path.dirname(fileURLToPath(import.meta.url));const spec=JSON.parse(await fs.readFile(path.join(B,'spec.json'),'utf8'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
for(const item of spec){const s=p.slides.add();s.background.fill='#000000';conclusionBar(s,item.message,item.page===6?{x:430,width:700}:{});}
await(await PresentationFile.exportPptx(p)).save(path.join(B,'bars.pptx'));console.log('Authored 11 editable reference-style conclusion bars.');
