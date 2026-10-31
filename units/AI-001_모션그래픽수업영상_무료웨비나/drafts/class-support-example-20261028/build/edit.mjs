import path from 'node:path';
import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-part1-developed/NotionTalk_Part1_내용디자인고도화_21장_v4.pptx')));
const edits={12:{subtitle:'문장·웹사이트·수업 내용을 각각 어떤 영상으로 바꿀지 살펴봅니다','dev-case-2-0':'C  수업 보조 영상','dev-case-2-1':'45초 시계열 설명','dev-case-2-2':'순서·변화·핵심 내용'},17:{section_heading:'제작 예제 · 시계열 설명 예시',title:'수업 보조 영상의 시계열 설명 예시',subtitle:'원자모형 변천을 시간의 흐름에 따라 보여 줍니다'}};
for(const [page,values] of Object.entries(edits)){
 const s=p.slides.items[Number(page)-1];
 for(const [name,value] of Object.entries(values)){const sh=s.shapes.items.find(x=>x.name===name);if(!sh)throw Error(name);sh.text.replace(String(sh.text),value);}
 if(Number(page)===12)s.speakerNotes.text=String(s.speakerNotes.text).replace('C는 과학사의 차이와 변화 이유를 사실에 맞게 설명하는 작업입니다.','C는 수업 내용을 짧게 설명하는 수업 보조 영상입니다. 이번에는 원자모형 변천을 이용해 시간에 따른 변화를 보여 주는 시계열 설명을 예로 듭니다.');
 if(Number(page)===17)s.speakerNotes.text='이 장표는 수업 보조 영상의 시계열 설명 예시입니다. 원자모형 변천이라는 소재를 이용해 변화의 순서와 핵심 차이를 시간의 흐름에 따라 보여 줍니다.\n'+String(s.speakerNotes.text);
}
await fs.writeFile(path.join(B,'edits.json'),JSON.stringify(edits,null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-roundtrip.pptx'));
console.log('Updated pages 12 and 17 to class-support and chronological-example framing.');
