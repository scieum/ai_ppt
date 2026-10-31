import{roundedAgendaContent}from'./rounded-agenda.mjs';
import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';import{Presentation,PresentationFile}from'@oai/artifact-tool';
import{layouts}from'./layouts.mjs';import{C,shape,text,panel,arrow,imageSlot,smallTag}from'./components.mjs';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../../..'),A=path.resolve(B,'..');await fs.mkdir(A,{recursive:true});
const p=Presentation.create({slideSize:{width:1280,height:720}});const brand=new Uint8Array(await fs.readFile(path.join(R,'assets/branding/notiontalk-white.png')));
for(const L of layouts){
 const s=p.slides.add();s.background.fill=C.bg;
 text(s,'asset-id',L.id+'  '+L.name,60,55,760,30,18,C.muted,true);
 s.images.add({blob:brand,contentType:'image/png',fit:'contain',position:{left:1010,top:58,width:190,height:55},alt:'사용자 제공 NotionTalk 원본 로고'});
 text(s,'copyright-footer','© 2026. NotionTalk. All rights reserved.',800,682,420,22,12,C.muted,false,'right');
 if(!['cover','divider'].includes(L.key)){
  text(s,'slot-title',L.name,170,195,943,65,40,C.white,true,'center');text(s,'slot-subtitle',L.use_case,170,272,943,38,23,C.muted,false,'center');
 }
 switch(L.key){
 case'cover':
  shape(s,'cover-accent',0,0,17,720,C.orange,'rect');text(s,'slot-title','[강의 제목]\n[핵심 부제]',90,245,570,170,52,C.white,true);text(s,'slot-subtitle','[대상·주제·한 줄 소개]',90,425,570,50,24,C.muted);text(s,'slot-date','[일시 · 진행자]',90,592,550,35,22,C.orange);imageSlot(s,'slot-hero',760,235,400,350,'대표 장면 1개');break;
 case'agenda':
  for(const sh of [...s.shapes.items])if(sh.name!=='copyright-footer')sh.delete();
  roundedAgendaContent(s);break;
 case'divider':
  text(s,'slot-part','Part [번호]',135,278,750,44,28,C.orange,true);text(s,'slot-title','[파트 제목]\n[핵심 단어]',135,337,900,140,54,C.white,true);text(s,'slot-subtitle','[이 파트에서 다룰 내용을 한 줄로]',138,501,900,45,24,C.muted);break;
 case'focus':
  text(s,'slot-key-sentence','[가장 중요한 한 문장]',215,365,850,65,36,C.orange,true,'center');imageSlot(s,'slot-visual',430,456,420,165,'개념 그림 또는 짧은 예시 1개');break;
 case'cards':
  for(let i=0;i<3;i++){panel(s,'card-'+i,170+i*320,350,285,280,'[유형 '+(i+1)+']','[핵심 특징]\n\n[한 줄 설명]');smallTag(s,'slot-card-number-'+i,'0'+(i+1),257+i*320,577,110);}break;
 case'matrix':{
  const values=[['비교 기준','대상 A','대상 B'],['기준 1','[특징 A1]','[특징 B1]'],['기준 2','[특징 A2]','[특징 B2]'],['기준 3','[특징 A3]','[특징 B3]'],['기준 4','[특징 A4]','[특징 B4]']];
  const tb=s.tables.add({rows:5,columns:3,left:170,top:350,width:943,height:275,columnWidths:[243,350,350],values});
  tb.borders.assign({style:'solid',fill:'#464646',width:1});for(let r=0;r<5;r++)for(let c=0;c<3;c++){const cell=tb.getCell(r,c);cell.fill=r===0?'#333333':C.card;cell.text.style={typeface:'Pretendard',fontSize:20,color:r===0?C.orange:C.white,bold:r===0};}break;}
 case'paired-rows':
  text(s,'slot-left-heading','[대상 A]',225,345,350,35,26,C.white,true,'center');text(s,'slot-right-heading','[대상 B]',705,345,350,35,26,C.orange,true,'center');
  for(let i=0;i<3;i++){shape(s,'left-row-'+i,170,402+i*76,430,61,C.card);shape(s,'right-row-'+i,680,402+i*76,430,61,C.card);text(s,'slot-left-'+i,'[관찰 내용 '+(i+1)+']',190,410+i*76,390,45,22);text(s,'slot-right-'+i,'[대응·차이 '+(i+1)+']',700,410+i*76,390,45,22);arrow(s,'compare-arrow-'+i,627,418+i*76,25,25);}break;
 case'dialogue':
  for(let i=0;i<4;i++){const left=i%2===0,x=left?220:455,y=350+i*67;shape(s,'bubble-'+i,x,y,610,52,left?C.card:'#4D331D');text(s,'slot-message-'+i,left?'[질문 또는 상황 설명]':'[답변 또는 다음 질문]',x+22,y+7,566,38,22);text(s,'slot-speaker-'+i,left?'질문':'답변',left?135:1075,y,75,52,18,left?C.muted:C.orange,true,'center');}break;
 case'document':
  for(let i=0;i<3;i++)panel(s,'context-'+i,170,350+i*88,250,72,'[맥락 '+(i+1)+']',null);
  shape(s,'document-paper',465,350,648,280,'#F5F2EE');text(s,'slot-document-heading','[문서·요청문의 제목]',490,369,596,38,24,'#222222',true);text(s,'slot-document-body','[대상과 목적]\n\n[전달할 내용·조건]\n\n[확인할 결과]',490,425,596,180,22,'#333333');break;
 case'pipeline':
  for(let i=0;i<3;i++)panel(s,'input-'+i,170+i*320,350,285,73,'[입력 '+(i+1)+']',null);
  shape(s,'down-link',625,434,22,24,C.orange,'downArrow');shape(s,'process-bg',170,470,925,62,'#5E3818');text(s,'slot-process','[함께 처리·검토하는 과정]',195,481,875,40,26,C.white,true,'center');shape(s,'down-link-2',625,540,22,24,C.orange,'downArrow');shape(s,'output-bg',170,576,925,61,C.card);text(s,'slot-output','[최종 결과]',195,586,875,40,26,C.orange,true,'center');break;
 case'screen-callouts':
  imageSlot(s,'slot-screen',170,350,620,280,'화면 캡처 또는 결과 이미지');for(let i=0;i<3;i++){smallTag(s,'callout-number-'+i,'0'+(i+1),835,365+i*88,60);text(s,'slot-callout-'+i,'[화면에서 볼 핵심 지점]',835,400+i*88,290,42,20,C.white);}break;
 case'before-after':
  imageSlot(s,'slot-before',170,385,410,225,'이전·시작 장면');imageSlot(s,'slot-after',700,385,410,225,'이후·마무리 장면');text(s,'slot-before-label','[전 / 시작]',170,337,410,35,25,C.white,true,'center');text(s,'slot-after-label','[후 / 마무리]',700,337,410,35,25,C.orange,true,'center');arrow(s,'before-after-arrow',620,470,30,40);break;
 case'checklist':
  for(let col=0;col<2;col++){shape(s,'check-panel-'+col,170+col*490,350,450,280,C.card);text(s,'slot-list-heading-'+col,col===0?'[확인할 것]':'[다시 볼 것]',195+col*490,367,400,35,26,C.white,true);for(let i=0;i<4;i++){shape(s,'check-square-'+col+'-'+i,195+col*490,430+i*42,15,15,'none','rect',C.muted);text(s,'slot-check-'+col+'-'+i,'[짧은 확인 문장]',225+col*490,418+i*42,370,35,21);}}break;
 case'step-rows':
  for(let i=0;i<3;i++){const y=350+i*96;shape(s,'step-row-'+i,170,y,943,81,C.card);text(s,'slot-number-'+i,'0'+(i+1),192,y+18,60,42,30,C.orange,true,'center');text(s,'slot-label-'+i,'[단계·조건]',278,y+8,300,33,24,C.white,true);text(s,'slot-description-'+i,'[설명 또는 짧은 비교]',278,y+43,365,28,19,C.muted);imageSlot(s,'slot-step-visual-'+i,760,y+7,330,65,'움직임·결과·예시');}break;
 case'hub':
  for(const[i,x,y,w,h]of[[0,450,386,25,2],[1,474,386,2,74],[2,805,386,25,2],[3,804,386,2,74],[4,450,591,25,2],[5,474,520,2,71],[6,805,591,25,2],[7,804,520,2,71]])shape(s,'hub-link-'+i,x,y,w,h,C.line,'rect');panel(s,'central',475,440,330,100,'[중심 개념]',null);for(const[x,y,label]of[[170,350,'[연결 A]'],[830,350,'[연결 B]'],[170,555,'[연결 C]'],[830,555,'[연결 D]']])panel(s,'node-'+label,x,y,280,73,label,null);break;
 case'file-tree':
  panel(s,'root',170,422,230,105,'[작업 폴더]',null);shape(s,'root-link',400,474,25,2,C.line,'rect');for(let i=0;i<4;i++){const y=350+i*70;shape(s,'branch-'+i,425,y+25,55,2,C.line,'rect');panel(s,'file-'+i,480,y,270,55,'[file-'+(i+1)+'.md]',null);text(s,'slot-file-role-'+i,'[파일의 역할]',810,y,280,55,22,C.muted);}shape(s,'tree-trunk',425,375,2,210,C.line,'rect');break;
 case'gallery':
  for(let i=0;i<4;i++){imageSlot(s,'slot-case-'+i,170+i*240,350,220,215,'사례 '+(i+1));text(s,'slot-case-caption-'+i,'[사례 특징]',170+i*240,584,220,35,21,C.white,true,'center');}break;
 case'timeline':
  for(let i=0;i<6;i++)text(s,'slot-time-'+i,'[구간 '+(i+1)+']',320+i*126,340,115,30,17,C.muted,false,'center');for(let row=0;row<3;row++){const y=402+row*75;text(s,'slot-track-'+row,'[흐름 '+(row+1)+']',170,y,130,40,22,C.white,true);shape(s,'track-'+row,320,y,756,44,C.card);shape(s,'slot-range-'+row,320+row*120,y+7,360-row*45,30,row===0?'#8D5525':'#4F3A29');}break;
 case'assignment':
  panel(s,'task',170,350,570,278,'[다음에 할 일]','[목표와 수행 내용]\n\n[제출물 또는 결과물]');text(s,'slot-criteria-heading','[확인 기준]',790,365,320,35,25,C.orange,true);for(let i=0;i<3;i++){text(s,'slot-criterion-'+i,'[기준 '+(i+1)+']',800,427+i*60,300,40,23);}break;
 case'summary':
  for(let i=0;i<5;i++){const x=i<2?330+i*330:170+(i-2)*320,y=i<2?350:498,w=i<2?300:285;panel(s,'summary-'+i,x,y,w,120,'[핵심 '+(i+1)+']','[한 줄 정리]');}break;
 }
 s.speakerNotes.text=L.use_case+'. 문구와 시각 자료 슬롯을 강의 목적에 맞게 바꾸어 사용합니다.\n디자인 참고: '+L.references.map(x=>x.source_id+' PDF '+x.pages.join(', ')+'쪽').join(' / ')+'. 일반적인 장표 역할을 분류하고 노션톡의 자체 문구와 네이티브 도형·표로 구성했습니다. 원본 화면·캐릭터·로고·요청문을 포함하지 않습니다.';
}
await(await PresentationFile.exportPptx(p)).save(path.join(B,'library-candidate.pptx'));
await fs.writeFile(path.join(A,'catalog.json'),JSON.stringify({version:'1.0',canvas:{width:1280,height:720},brand:'NotionTalk',font:'Pretendard',accent:C.orange,mode:'reference-inspired-native-editable-layouts',layouts},null,2));
console.log('Authored 20 editable situational layout assets.');
