import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';import{Presentation,PresentationFile}from'@oai/artifact-tool';
import{C,text}from'../../assets/layout-library-20261028/recipes/components.mjs';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..');
const parts=[
 {part:0,before:2,title:'오늘의\n준비물',sub:'함께 사용할 도구를 먼저 확인합니다.'},
 {part:1,before:4,title:'모션 그래픽\n기본 지식',sub:'종류와 효과를 움직이는 예시로 살펴봅니다.'},
 {part:2,before:17,title:'이미지·영상\n레퍼런스',sub:'보이는 스타일과 움직이는 방식을 함께 참고합니다.'},
 {part:3,before:18,title:'스토리라인과\n스틸컷 확인',sub:'이야기 흐름과 대표 장면 두 장을 먼저 봅니다.'},
 {part:4,before:20,title:'수정 후\n영상 제작',sub:'수정 사항을 확인하고 전체 영상으로 이어갑니다.'}
];
const p=Presentation.create({slideSize:{width:1280,height:720}});const brand=new Uint8Array(await fs.readFile(path.join(R,'assets/branding/notiontalk-white.png')));
for(const d of parts){
 const s=p.slides.add();s.background.fill=C.bg;
 s.images.add({blob:brand,contentType:'image/png',fit:'contain',position:{left:1010,top:58,width:190,height:55},alt:'사용자 제공 NotionTalk 원본 로고'});
 text(s,'slot-part','Part '+d.part,135,278,750,44,28,C.orange,true);
 text(s,'slot-title',d.title,135,337,900,140,54,C.white,true);
 text(s,'slot-subtitle',d.sub,138,501,1020,45,24,C.muted);
 text(s,'copyright-footer','© 2026. NotionTalk. All rights reserved.',800,682,420,22,12,C.muted,false,'right');
 s.speakerNotes.text='Part '+d.part+' 시작. '+d.sub ;
}
await(await PresentationFile.exportPptx(p)).save(path.join(B,'dividers.pptx'));await fs.writeFile(path.join(B,'parts.json'),JSON.stringify(parts,null,2));console.log('Authored 5 dividers using L03.');
