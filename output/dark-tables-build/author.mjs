import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)), R=path.resolve(B,'../..');
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_이미지설명강화_40장_v21.pptx')));
await fs.writeFile(path.join(B,'before-inspect.json'),JSON.stringify(await p.inspect({kind:'table,layout',maxChars:25000})));
for(const n of [25,34]){
 const s=p.slides.getItem(n-1),t=s.tables.items[0];
 if(!t)throw Error('Missing table '+n);
 t.borders.assign({style:'solid',fill:'#454545',width:0.65});
 t.cells.block({row:0,column:0,rowCount:5,columnCount:3}).assign({margins:{left:20,right:16,top:12,bottom:10},anchor:'center'});
 for(let r=0;r<5;r++)for(let c=0;c<3;c++){
  const cell=t.getCell(r,c);
  cell.fill=r===0?'#2D2D2D':c===0?'#303030':'#1E1E1E';
  cell.text.style={typeface:'Pretendard',fontSize:21,bold:r===0||c===0,color:r>0&&c===0?'#FF9228':'#FFFFFF'};
 }
}
await (await PresentationFile.exportPptx(p)).save(path.join(B,'restyled.pptx'));
console.log('Restyled tables 25 and 34');
