import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const here=path.dirname(fileURLToPath(import.meta.url));
const runtime=process.env.RUNTIME_NODE_MODULES;
if(!runtime)throw new Error('RUNTIME_NODE_MODULES must point to the bundled packages.');
const req=createRequire(path.join(runtime,'@oai/artifact-tool/package.json'));
const {Canvas,loadImage}=req('skia-canvas');
for(const [source,dest] of [['svg','png'],['marks','marks']]) {
 for(const name of (await fs.readdir(path.join(here,source))).filter(x=>x.endsWith('.svg'))) {
  const canvas=new Canvas(1024,1024),context=canvas.getContext('2d');
  const image=await loadImage(await fs.readFile(path.join(here,source,name)));
  context.drawImage(image,0,0,1024,1024);
  await canvas.saveAs(path.join(here,dest,name.replace(/\.svg$/,'.png')));
 }
}
console.log('Rendered SVG gradients and clipping with Skia.');
