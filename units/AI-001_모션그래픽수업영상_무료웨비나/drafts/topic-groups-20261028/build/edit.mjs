import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const source=path.join(R,'output/webinar-fundamentals/NotionTalk_모션그래픽_개념부터실습까지_21장_v1.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load(source));
const groups=[
 [4,'01','모션 그래픽 이해하기 · 뜻'],[5,'01','모션 그래픽 이해하기 · 표현 유형'],
 [6,'02','움직임과 효과 · 기본 속성'],[7,'02','움직임과 효과 · 등장 효과'],
 [8,'02','움직임과 효과 · 글자와 순서'],[9,'02','움직임과 효과 · 시간과 속도'],[10,'02','움직임과 효과 · 요청 문장'],
 [11,'03','제작 예제 · 세 사례 비교'],[12,'03','제작 예제 · 타이포그래피'],[13,'03','제작 예제 · 타이포그래피 요청'],
 [14,'03','제작 예제 · 웹사이트 소개'],[15,'03','제작 예제 · 웹사이트 요청'],
 [16,'03','제작 예제 · 원자모형 변천'],[17,'03','제작 예제 · 원자모형 요청'],[18,'04','내 수업에 적용하기']
];
for(const[page,number,heading]of groups){
 const s=p.slides.items[page-1];
 for(const[name,text]of [['section_number',number],['section_heading',heading]]){
  const shape=s.shapes.items.find(x=>x.name===name);if(!shape)throw Error('Missing '+name);shape.text.replace(String(shape.text),text);
 }
}
await fs.writeFile(path.join(B,'groups.json'),JSON.stringify(groups,null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-roundtrip.pptx'));
console.log('Edited semantic topic numbers and headings on existing slides.');
