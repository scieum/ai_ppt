import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';import{Presentation,PresentationFile}from'@oai/artifact-tool';
import{roundedAgendaContent}from'../../assets/layout-library-20261028/recipes/rounded-agenda.mjs';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..');
for(const job of[{key:'library',labels:['기본\n이해','자료\n살펴보기','미리\n확인하기','정리와\n다음 단계']},{key:'application',labels:['기본 지식','이미지·영상\n레퍼런스','스토리라인 .md\n스틸컷 2장','수정 후\n영상 제작']}]){
 const p=Presentation.create({slideSize:{width:1280,height:720}}),s=p.slides.add();s.background.fill='#000000';
 s.images.add({blob:new Uint8Array(await fs.readFile(path.join(R,'assets/branding/notiontalk-white.png'))),contentType:'image/png',fit:'contain',position:{left:1010,top:58,width:190,height:55},alt:'사용자 제공 NotionTalk 원본 로고'});
 roundedAgendaContent(s,{labels:job.labels});await(await PresentationFile.exportPptx(p)).save(path.join(B,job.key+'-agenda.pptx'));
}console.log('Authored both agendas with rounded freeform blocks, left-aligned PART labels and minimal heading.');
