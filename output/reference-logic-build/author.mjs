import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {C,shape,text,band,line,stepCard,compareRow,criteriaRow} from '../../assets/layout-library-20261028/logic-patterns-20261030/components.mjs';
const B=path.dirname(fileURLToPath(import.meta.url));const p=Presentation.create({slideSize:{width:1280,height:720}});const spec=[];
function slide(page,pattern,refs){const s=p.slides.add();s.background.fill='#000000';spec.push({page,pattern,refs});return s;}
{
 const s=slide(20,'질문에서 이미지·영상 두 기준으로 분기',['첨부 3 / R01 p17']);
 shape(s,'reference-question-box',430,441,420,42,'#2D2D2D','roundRect');
 text(s,'reference-question','어떤 특징을 함께 참고할까요?',444,444,392,36,24,C.white,true,'center');
 line(s,'branch-trunk',639,483,2,18);line(s,'branch-horizontal',430,500,420,2);line(s,'branch-left',430,500,2,20);line(s,'branch-right',849,500,2,20);
 for(const [n,x,title,desc,tag,col] of [['image',245,'디자인','색·글자·소재·구도','이미지 레퍼런스',C.white],['motion',665,'모션','등장 순서·속도·장면 전환','영상 레퍼런스',C.orange]]){
  shape(s,n+'-branch',x,520,370,104,'#242424','roundRect');
  text(s,n+'-branch-title',title,x+22,532,130,31,25,col,true);
  text(s,n+'-branch-tag',tag,x+156,535,191,27,19,C.muted,false,'right');
  text(s,n+'-branch-detail',desc,x+22,580,326,30,23,C.white,false,'center');
 }
 band(s,'함께 보기','정지 화면의 모습과 시간에 따른 변화를 함께 전달합니다');
}
{
 const s=slide(36,'스틸컷→짧은 구간→전체 영상의 세 단계',['첨부 5 / R01 p23']);
 for(const [x,n,title] of [[140,1,'스틸컷'],[490,2,'짧은 구간'],[840,3,'전체 영상']])stepCard(s,'step-'+n,n,title,x);
 text(s,'step-arrow-1','→',447,456,35,40,30,C.orange,true,'center');text(s,'step-arrow-2','→',797,456,35,40,30,C.orange,true,'center');
 // Original editable miniature still and its original logo are inserted here by the package-preserving assembly.
 shape(s,'segment-preview',510,421,260,114,'#171717','roundRect');
 text(s,'segment-time','4–7초',526,432,228,51,40,C.white,true,'center');text(s,'segment-description','예: 3초 구간 재생',526,492,228,28,20,C.orange,false,'center');
 shape(s,'whole-preview',860,421,260,114,'#171717','roundRect');
 text(s,'whole-time','15초',876,432,228,51,40,C.white,true,'center');text(s,'whole-description','예: 영상 전체 재생',876,492,228,28,20,C.orange,false,'center');
 for(const [x,caption] of [[140,'색·글자·잘림·구도'],[490,'등장·속도·전환'],[840,'앞뒤 연결·마무리']])text(s,'step-check-'+x,caption,x+20,556,260,40,23,C.white,false,'center');
 band(s,'확인 순서','수정한 부분부터 작게 확인하고, 마지막에 전체 흐름을 봅니다');
}
{
 const s=slide(37,'점검 기준·질문·확인 자료를 연결한 행별 비교',['첨부 1 / R01 p11','첨부 4 / R01 p20']);
 for(const [x,w,value] of [[274,132,'점검 기준'],[414,427,'확인할 질문'],[849,317,'함께 볼 자료']]){
  shape(s,'criteria-tab-'+x,x,328,w,34,'#333333','roundRect');text(s,'criteria-tab-text-'+x,value,x+10,330,w-20,30,21,C.white,true,'center');
 }
 const rows=[['내용','문구·순서·전달 내용이 맞나?','storyline.md'],['디자인','글자가 읽히고 자산이 맞나?','design.md + 스틸컷'],['모션','등장·유지·전환이 맞나?','motion.md + 구간 재생'],['전체 연결','장면·소리가 자연스럽게 이어지나?','전체 영상 + 구간표']];
 rows.forEach((r,i)=>criteriaRow(s,'criteria-row-'+i,r,369+i*62));
 band(s,'점검 기준','읽힘·움직임·내용을 따로 확인한 뒤, 전체 연결을 봅니다');
}
{
 const s=slide(39,'혼동되는 보관과 재사용 가능한 보관의 대조',['첨부 2 / R01 p15','첨부 6 / 결론 띠']);
 text(s,'compare-left-heading','기준이 섞이면 확인하기 어렵습니다',150,327,470,35,23,'#BCA79B',true,'center');
 text(s,'compare-right-heading','확인한 버전으로 묶어 둡니다',660,327,470,35,23,'#9DC7F5',true,'center');
 compareRow(s,'files','이전 문서와 최신 문서가 섞임','확인한 design.md · motion.md',378);
 compareRow(s,'assets','자산과 결과물이 따로 보관됨','자산 + 스틸컷 2장 + 확인 영상',460);
 compareRow(s,'storyline','이전 주제의 장면표를 그대로 사용','새 주제의 storyline.md로 갱신',542);
 band(s,'다음 작업','같은 버전을 전달하고, 스틸컷과 짧은 구간으로 다시 확인합니다');
}
{
 const s=slide(40,'기준 확인→수정 확인→제작, 중간 확인 지점 표시',['첨부 7·8 / R01 p29','첨부 6 / 결론 띠']);
 shape(s,'phase-panel',355,329,815,292,'#202020','roundRect');
 for(const [y,num,action,result] of [[352,'01','내용·화면·움직임 기준 확인','기준 문서'],[412,'02','색·구도·글자 수정 반영','스틸컷 2장'],[553,'03','확정한 기준으로 이어서 제작','전체 영상']]){
  shape(s,'phase-number-bg-'+num,379,y,50,36,'#363636','roundRect');text(s,'phase-number-'+num,num,379,y,50,36,21,C.orange,true,'center');
  text(s,'phase-action-'+num,action,449,y,443,36,23,C.white);
  text(s,'phase-arrow-'+num,'→',894,y,35,36,24,C.muted,false,'center');
  shape(s,'phase-output-bg-'+num,948,y,194,36,num==='03'?'#513218':'#373737','roundRect');text(s,'phase-output-'+num,result,958,y+1,174,34,22,num==='03'?C.orange:C.white,true,'center');
 }
 line(s,'gate-rule',379,484,763,1);
 text(s,'gate-label','확인 지점',379,493,115,34,22,C.orange,true);
 text(s,'gate-question','수정한 결과가 의도에 맞나요?',497,493,442,34,23,C.white,true);
 shape(s,'gate-pass-outline',948,492,194,36,'#242424','roundRect','#FF9228');text(s,'gate-pass','맞으면 진행',958,493,174,34,21,C.orange,true,'center');
 band(s,'핵심','중간 확인으로 불필요한 재생성과 토큰 낭비를 줄입니다');
}
await(await PresentationFile.exportPptx(p)).save(path.join(B,'bodies.pptx'));
await fs.writeFile(path.join(B,'spec.json'),JSON.stringify(spec,null,2));console.log('Created 5 logical reference adaptations.');
