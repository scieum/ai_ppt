import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';
import{Presentation,PresentationFile}from'@oai/artifact-tool';
import{C,text,shape}from'../../assets/layout-library-20261028/recipes/components.mjs';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..');
const p=Presentation.create({slideSize:{width:1280,height:720}}),s=p.slides.add();s.background.fill=C.bg;
s.images.add({blob:new Uint8Array(await fs.readFile(path.join(R,'assets/branding/notiontalk-white.png'))),contentType:'image/png',fit:'contain',position:{left:1010,top:58,width:190,height:55}});
text(s,'part-label','Part 4  마무리',60,55,800,27,17,C.muted,true);
text(s,'group-number','02',60,91,45,36,28,C.orange,true);
text(s,'group-label','후속 활동 안내',107,91,850,36,28,C.white,true);
text(s,'title','노션톡 웨비나 챌린지 일정',130,186,1020,66,40,C.white,true,'center');
text(s,'dates','2026.11.2.(월) ~ 11.15.(일) · 총 2주',130,266,1020,40,24,C.muted,false,'center');
const x=255,w=850,gap=4,pad=12,cw=(w-2*pad-gap*6)/7;
['월','화','수','목','금','토','일'].forEach((day,i)=>text(s,'weekday-'+i,day,x+pad+i*(cw+gap),326,cw,31,22,C.white,true,'center'));
for(let row=0;row<2;row++){
 const y=374+row*132;
 text(s,'week-label-'+row,(row+1)+'주차',92,y+30,140,39,26,C.white,true,'center');
 text(s,'week-range-'+row,row===0?'11/2 ~ 11/8':'11/9 ~ 11/15',82,y+73,160,27,18,C.muted,false,'center');
 shape(s,'calendar-week-'+row,x,y,w,112,'#282B31','roundRect');
 for(let col=0;col<7;col++){
  const day=row*7+col+2,cx=x+pad+col*(cw+gap);
  shape(s,`date-cell-${day}`,cx,y+11,cw,90,'#17191D','roundRect');
  text(s,`date-${day}`,day===2?'11/2':String(day),cx+3,y+18,cw-6,29,20,day===2?C.orange:C.muted,day===2,'center');
 }
 shape(s,'cycle-band-'+row,x+25,y+57,w-50,38,row===0?'#9C4F22':'#365565','roundRect');
 text(s,'cycle-name-'+row,(row+1)+'차 사이클',x+35,y+57,w-70,38,25,C.white,true,'center');
}
text(s,'takeaway','첫 1주일은 1차 사이클, 다음 1주일은 2차 사이클로 진행합니다',130,643,1020,34,21,C.orange,true,'center');
text(s,'copyright','© 2026. NotionTalk. All rights reserved.',800,682,420,22,12,C.muted,false,'right');
const notes='사용자가 확정한 후속 일정: 2026년 11월 2일부터 2주간 진행한다. 1차 사이클은 11월 2일 월요일~11월 8일 일요일, 2차 사이클은 11월 9일 월요일~11월 15일 일요일이다. 양 끝 날짜를 포함해 각각 7일, 총14일이다. 이후 마감 시각·제출물·과제·참여 링크는 아직 지정되지 않았으므로 임의로 넣지 않는다. 레퍼런스는 기존 L18의 근거인 R01 99쪽과 R03 42쪽의 실제 달력을 다시 확인했다. 요일7칸·주차행·가로기간띠 구조를 재구성하고 날짜·문구·브랜드를 노션톡 일정으로 바꿨다. 원본 캐릭터나 화면 이미지를 복제하지 않았다. 두 번째 띠의 낮은 채도 파랑은 두 사이클을 구분하는 보조색이며 브랜드 강조색은 주황으로 유지한다. 롤백된 v23의 준비물·문서 카드·내레이션 변경은 복원하지 않는다.';
await fs.writeFile(path.join(B,'additions.json'),JSON.stringify([{key:'challenge-calendar',replace:41,before:null,title:'노션톡 웨비나 챌린지 일정',notes}],null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(B,'additions.pptx'));console.log('Authored 14-day calendar from R01/R03 calendar references');
