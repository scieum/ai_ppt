import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';import{Presentation,PresentationFile}from'@oai/artifact-tool';
import{C,shape,text,arrow}from'../../assets/layout-library-20261028/recipes/components.mjs';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..');
const p=Presentation.create({slideSize:{width:1280,height:720}}),brand=new Uint8Array(await fs.readFile(path.join(R,'assets/branding/notiontalk-white.png')));const spec=[];
function page(part,key,title,subtitle,layout,notes){
 const s=p.slides.add();s.background.fill=C.bg;
 s.images.add({blob:brand,contentType:'image/png',fit:'contain',position:{left:1010,top:58,width:190,height:55},alt:'사용자 제공 NotionTalk 원본 로고'});
 text(s,'part-label',part===3?'Part 3  스토리라인과 스틸컷 확인':'Part 4  수정 후 제작',60,55,800,27,17,C.muted,true);
 text(s,'group-number',part===3?'02':'01',60,91,45,36,28,C.orange,true);
 text(s,'group-label',part===3?'스타일 기준을 문서로 남기기':'피드백을 반영하고 진행하기',107,91,850,36,28,C.white,true);
 text(s,'slide-title',title,150,194,980,62,40,C.white,true,'center');
 text(s,'slide-subtitle',subtitle,150,270,980,46,23,C.white,false,'center');
 text(s,'copyright-footer','© 2026. NotionTalk. All rights reserved.',800,682,420,22,12,C.muted,false,'right');
 s.speakerNotes.text=notes+'\n이 강의의 design.md와 motion.md는 사용자가 요청한 일반 Markdown 기준 문서의 이름이다. 작업에 함께 제공해 참고하도록 한다. 아래 수치와 문장은 노션톡의 교육용 자체 예시이며 특정 서비스의 전용 설정이나 보편적인 제작 규격을 뜻하지 않는다.';
 spec.push({key,part,title,before:part===3?24:26,authored_slide:spec.length+1,layout});return s;
}
function takeaway(s,value){text(s,'takeaway',value,170,639,943,35,19,C.orange,true,'center');}
function table(s,values,widths=[235,355,353],font=20){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:170,top:350,width:943,height:278,columnWidths:widths,values});
 t.borders.assign({style:'solid',fill:'#414141',width:1});
 for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){const cell=t.getCell(r,c);cell.fill=r===0?'#303030':C.card;cell.text.style={typeface:'Pretendard',fontSize:font,color:r===0?C.orange:C.white,bold:r===0};}
 spec.at(-1).native_table=true;return t;
}
function panel(s,key,x,y,w,h,title,body){shape(s,key+'-bg',x,y,w,h,C.card);text(s,key+'-title',title,x+22,y+18,w-44,40,28,C.orange,true,'center');text(s,key+'-body',body,x+22,y+(h<150?61:77),w-44,h<150?34:h-94,h<150?20:23,C.white,false,'center');}
function pairRows(s,leftHeading,rightHeading,rows){
 text(s,'left-heading',leftHeading,170,337,430,38,25,C.white,true,'center');text(s,'right-heading',rightHeading,680,337,430,38,25,C.orange,true,'center');
 rows.forEach(([l,r],i)=>{const y=392+i*78;shape(s,'left-bg-'+i,170,y,430,65,C.card);shape(s,'right-bg-'+i,680,y,430,65,C.card);text(s,'left-text-'+i,l,190,y+7,390,51,21,C.white,false,'center');text(s,'right-text-'+i,r,700,y+7,390,51,21,C.white,false,'center');arrow(s,'pair-arrow-'+i,627,y+22,25,25);});
}
function document(s,file,contexts,lines){
 contexts.forEach(([title,desc],i)=>{const y=350+i*96;shape(s,'context-bg-'+i,170,y,250,80,C.card);text(s,'context-title-'+i,title,189,y+8,212,31,23,C.orange,true,'center');text(s,'context-desc-'+i,desc,187,y+40,216,30,18,C.muted,false,'center');});
 shape(s,'document-page',465,337,648,293,'#F5F2EE','roundRect');text(s,'document-file',file+'  ·  교육용 예시',490,351,596,32,23,'#222222',true);
 text(s,'document-content',lines.join('\n'),490,393,596,224,20,'#333333');
}
// Part 3 — one role, one example and one review step per slide.
{
 const s=page(3,'recommendation','비슷한 톤을 다시 얻고 싶다면','design.md와 motion.md도 함께 만드는 것을 추천합니다','L12','같은 브랜드의 다음 영상도 비슷한 인상을 원한다면, 좋았던 화면과 움직임의 기준을 함께 문서로 남기는 방법을 권한다. 스토리라인은 이번 이야기, 디자인과 모션 문서는 반복 사용할 기준을 담는다.');
 panel(s,'design',170,360,430,250,'design.md','색·글꼴·구도·이미지\n\n보이는 스타일의 기준');panel(s,'motion',680,360,430,250,'motion.md','속도·등장·전환·박자\n\n움직이는 방식의 기준');takeaway(s,'마음에 든 결과에서 반복하고 싶은 특징을 문장과 수치로 남깁니다');
}
{
 const s=page(3,'roles','세 문서와 스틸컷의 역할','내용·화면·움직임을 나누어 정리합니다','L06','장면표에는 이번 영상의 이야기와 시간 구간, design.md에는 공통 시각 기준, motion.md에는 공통 시간과 움직임 기준을 담는다. 대표 스틸컷 두 장은 정지 화면의 확인 자료다. 스틸컷만으로 속도를 확인할 수는 없다.');
 table(s,[['자료','답하는 질문','담을 내용'],['storyline.md','무엇을 어떤 순서로?','장면·문구·구간'],['design.md','어떤 모습으로?','색·글꼴·구도·자산'],['motion.md','어떻게 움직이게?','등장·속도·전환·유지'],['스틸컷 2장','화면은 어떻게 보이나?','시작과 마무리의 대표 모습']]);takeaway(s,'파일 이름과 함께, 각 문서에서 확인할 항목도 정합니다');
}
{
 const s=page(3,'design-fields','design.md에 담을 화면 기준','색 이름보다 구체적인 값과 배치를 함께 기록합니다','L06','막연히 깔끔하게라고 쓰는 대신 반복할 시각 요소를 구분한다. 사용할 색상 값, 글꼴과 강조 방식, 제목과 로고 배치, 캐릭터와 이미지 자산의 고정 특징을 기록한다. 모든 장면의 구도를 복제하기보다 같은 브랜드로 보이게 하는 기준을 정한다.');
 table(s,[['항목','기록할 기준','노션톡 예시'],['색','배경·본문·강조색','검정·흰색·주황 #FF9228'],['글자','글꼴·위계·강조 방식','Pretendard / 제목은 굵게'],['구도','여백·정렬·로고 위치','제목 중앙 / 로고 우측 위'],['자산','사용 파일·캐릭터 특징','원본 로고 / 같은 삼인방']]);takeaway(s,'같은 브랜드로 보이게 하는 요소부터 정리합니다');
}
{
 const s=page(3,'design-example','design.md 예시','노션톡 15초 소개 영상에 사용할 시각 기준입니다','L09','이 장은 다운로드 예시 design.md의 핵심을 줄여 보여 준다. 주황 색상과 Pretendard, 로고, 사용자 캐릭터의 외형을 고정한다. 이 파일은 영상용 예시이므로 이 PPT 하네스의 디자인 지침 파일과는 별도 위치에 보관한다.');
 document(s,'design.md',[['고정할 것','색·글꼴·브랜드'],['장면에 맞출 것','문구·이미지의 비중'],['함께 줄 것','로고·캐릭터 원본']],['배경: #000000 / 본문: #FFFFFF','강조색: #FF9228','글꼴: Pretendard / 제목은 굵게','제목: 중앙 정렬, 두 줄 이내','로고: 우측 위, 원본 비율 유지','캐릭터: 헤어·안경·의상 고정','이미지: 의미가 있는 장면에만 사용','문구가 길면 줄이고 여백 유지']);takeaway(s,'실제 사용할 자산 파일과 참고 스틸컷도 함께 보관합니다');
}
{
 const s=page(3,'motion-fields','motion.md에 담을 움직임 기준','시작·움직임·멈춤·장면 연결을 나누어 기록합니다','L06','디자인이 같아도 등장 속도와 전환 방식이 달라지면 인상이 달라질 수 있다. 등장과 퇴장의 종류 및 지속시간, 여러 요소 사이의 지연, 읽는 시간을 위한 정지 구간, 전환과 오디오가 있다면 동기화 기준을 기록한다.');
 table(s,[['항목','기록할 기준','확인할 질문'],['등장·퇴장','효과·방향·지속시간','어디서 얼마나 빠르게?'],['순서·간격','요소 사이의 시작 간격','함께 나오나, 차례로 나오나?'],['유지·전환','머무는 시간·장면 연결','읽은 뒤 자연스럽게 이어지나?'],['속도·박자','가감속·소리와 맞는 시점','부드럽나, 강하게 반응하나?']]);takeaway(s,'“부드럽게”라는 말에 방향·초·간격을 덧붙입니다');
}
{
 const s=page(3,'motion-example','motion.md 예시','아래 수치는 이번 소개 영상의 출발 기준입니다','L09','교육용 예시의 등장 시간은 0.45초, 시작 위치는 아래쪽 16px, 요소 간 지연은 0.12초다. 끝 문구는 1.2초 이상 유지하되 장면 구간 안에서 조정한다. 이를 보편적 정답으로 외우게 하지 않고 같은 기준으로 비교하기 위한 출발점으로 설명한다.');
 document(s,'motion.md',[['등장 규칙','시간·방향·가감속'],['간격 규칙','여러 요소의 순서'],['확인 자료','짧은 영상 구간']],['길이: 15초 / 30fps / 16:9','등장: 0.45초, 페이드 + 위로 이동','시작 위치: 최종 위치보다 아래 16px','가감속: 처음 빠르게, 끝은 천천히','순차 등장: 다음 요소는 0.12초 뒤','퇴장: 0.25초 페이드','장면 연결: 0.3초 겹쳐 전환','끝 문구: 1.2초 이상 멈춰 보여 주기']);takeaway(s,'정지 스틸컷과 함께 짧은 구간을 재생해 움직임도 확인합니다');
}
{
 const s=page(3,'review-links','문서와 확인 자료를 함께 봅니다','문서의 기준이 실제 결과에 반영됐는지 확인합니다','L07','디자인 문서를 읽고 스틸컷의 색과 글자를 본다. 모션 문서는 짧은 영상 구간을 재생하면서 시작 간격과 전환을 확인한다. 스토리라인은 전체 장면의 순서와 전달할 내용을 대조한다. 내용·화면·움직임 확인 자료를 서로 바꾸어 생각하지 않는다.');
 pairRows(s,'기준 문서','함께 확인할 자료',[['storyline.md\n장면과 핵심 문구','장면표와 전체 흐름'],['design.md\n색·글자·구도','대표 스틸컷 두 장'],['motion.md\n시간·간격·전환','짧은 영상 구간의 재생']]);takeaway(s,'스틸컷은 화면을, 재생 구간은 시간의 변화를 보여 줍니다');
}
{
 const s=page(3,'reuse','다음 영상에도 기준 문서를 전달합니다','주제가 바뀌어도 공통 스타일을 다시 참고할 수 있습니다','L16','다음 주제에서는 스토리라인을 새로 작성하되, 확정한 design.md와 motion.md, 실제 로고와 캐릭터 파일, 기준 스틸컷을 함께 제공한다. 같은 이름의 파일만 있다고 도구가 자동으로 읽는다고 가정하지 않는다. 사용한 버전을 명시하고 이번 프로젝트의 작업 자료로 함께 전달한다.');
 text(s,'folder-label','노션톡 영상 기준',170,371,300,45,28,C.orange,true);text(s,'folder-description','내용이 달라져도\n다시 참고할 자료',170,437,270,92,24,C.muted);
 const rows=[['storyline.md','이번 주제·장면으로 새로 정리'],['design.md','확정한 화면 스타일을 함께 제공'],['motion.md','확정한 움직임 기준을 함께 제공'],['assets / references','같은 자산·스틸컷·기준 영상']];
 rows.forEach(([file,role],i)=>{const y=350+i*68;shape(s,'file-bg-'+i,490,y,270,54,C.card);text(s,'file-'+i,file,509,y+7,232,40,23,C.white,true);text(s,'file-role-'+i,role,788,y+6,325,43,21,C.muted);});takeaway(s,'확인한 버전의 문서와 실제 자산을 한 묶음으로 전달합니다');
}
// Part 4 — focused revision, review and a deliberate update to shared rules.
{
 const s=page(4,'route-edits','수정 대상을 기준 파일과 연결합니다','무엇을 바꾸는지에 따라 먼저 볼 문서가 달라집니다','L06','문장을 바꾸려는지, 시각 디자인을 바꾸려는지, 시간과 움직임을 바꾸려는지부터 구분한다. 파일은 기준의 담당 영역이지 자동 실행 명령이 아니다. 실제 수정은 작업 결과와 함께 확인한다.');
 table(s,[['고칠 부분','먼저 볼 기준','다시 확인할 결과'],['제목·장면 순서','storyline.md','내용과 전체 흐름'],['색·글꼴·로고 위치','design.md','수정된 스틸컷'],['등장 속도·장면 전환','motion.md','해당 영상 구간'],['읽을 시간·장면 길이','storyline.md + motion.md','구간과 전체 영상 길이']]);takeaway(s,'내용·화면·움직임 중 어디를 고치는지 먼저 구분합니다');
}
{
 const s=page(4,'scope','바꿀 것과 유지할 것을 정합니다','이번 수정에서 움직일 범위를 분명하게 합니다','L07','장면, 바꿀 항목, 원하는 변화, 유지할 항목을 함께 정리한다. 아래 문장은 긴 생성 프롬프트가 아니라 수정 내용을 비교하기 위한 짧은 교육 예시다. 화면 기준과 움직임 기준을 한꺼번에 새로 만들지 않도록 범위를 특정한다.');
 pairRows(s,'이번에 바꿀 것','이번에 유지할 것',[['첫 장면 제목\n“배움이 움직인다”를 더 크게','배경·강조색·글꼴·로고'],['두 번째 장면\n카드 등장 시간을 더 천천히','카드 위치·크기·등장 순서'],['마무리 문구\n읽을 수 있게 더 오래 유지','문구 내용·색·마무리 구도']]);takeaway(s,'장면·항목·변화·유지할 기준을 함께 남깁니다');
}
{
 const s=page(4,'review-sequence','짧은 구간부터 다시 확인합니다','작게 확인한 뒤 전체 흐름으로 넓혀 봅니다','L14','정지 화면이 바뀌었다면 스틸컷부터 확인한다. 시간과 모션이 바뀌면 예를 들어 4~7초의 3초 구간을 재생한다. 마지막으로 15초 전체를 보면서 앞뒤 연결과 마지막 문구의 읽는 시간을 확인한다. 구간 검토가 전체 검토를 대체하지 않는다.');
 [['스틸컷','색·글자·잘림·구도','화면을 확인'],['짧은 구간','예: 4~7초의 3초 구간','움직임을 확인'],['전체 영상','예: 15초 전체의 연결과 마무리','앞뒤 흐름 확인']].forEach(([label,desc,result],i)=>{const y=350+i*96;shape(s,'row-bg-'+i,170,y,943,81,C.card);text(s,'row-label-'+i,label,194,y+19,205,43,27,C.orange,true);text(s,'row-desc-'+i,desc,420,y+15,430,52,21,C.white);text(s,'row-result-'+i,result,868,y+16,220,50,21,C.muted,false,'center');});takeaway(s,'변경한 구간을 먼저 보고, 마지막에는 전체 영상을 봅니다');
}
{
 const s=page(4,'review-criteria','내용·디자인·모션을 나누어 점검합니다','예쁘게 보이는 것과 정확하게 전달되는 것을 함께 봅니다','L06','검토 질문을 내용과 디자인과 모션으로 나누어 읽는다. 설명 문구는 정확한지, 글자가 잘리지 않는지, 브랜드 자산과 색이 맞는지, 등장과 전환이 기준에 맞는지 확인한다. 소리를 사용하는 영상에서만 말과 화면의 시점도 함께 확인한다.');
 table(s,[['검토 영역','확인할 질문','함께 볼 기준'],['내용','문구·순서·전달 내용이 맞나?','storyline.md'],['디자인','글자가 읽히고 자산이 맞나?','design.md + 스틸컷'],['모션','등장·유지·전환이 맞나?','motion.md + 구간 재생'],['전체 연결','장면·소리가 자연스럽게 이어지나?','전체 영상과 구간표']]);takeaway(s,'읽힘·움직임·내용을 각각 확인한 뒤 함께 봅니다');
}
{
 const s=page(4,'local-global','한 장면 수정과 공통 규칙의 변경','이번 영상에만 적용할지, 다음 작업에도 쓸지 구분합니다','L12','한 장면이 특별히 더 천천히 등장해야 한다면 스토리라인의 장면별 예외로 기록한다. 앞으로의 모든 제목에 더 느린 등장을 쓰기로 했다면 motion.md의 기본값을 바꾸고 다른 장면도 재검토한다. 색이나 자산의 공통 변경은 design.md에 같은 방식으로 반영한다.');
 panel(s,'local',170,350,430,275,'이번 장면만 수정','장면 2의 등장만 0.6초\n\n장면표에 예외로 기록\n다른 장면의 기준은 유지');panel(s,'global',680,350,430,275,'공통 기준을 변경','모든 제목의 등장을 0.6초로\n\nmotion.md 기본값 갱신\n다른 장면도 다시 확인');takeaway(s,'장면별 예외와 공통 기본값을 구분해 남깁니다');
}
{
 const s=page(4,'version','확인한 기준을 다음 작업에 남깁니다','문서·자산·결과물의 버전을 맞춰 보관합니다','L10','확인한 결과와 같은 버전의 세 문서와 자산 목록을 함께 보관한다. 다음 프로젝트에서는 새 스토리라인과 기존 공통 스타일 기준을 묶어 제공하고, 시작 스틸컷과 짧은 구간으로 적용 상태를 다시 본다. 파일이 있으면 동일 결과가 보장된다고 설명하지 않는다.');
 [['storyline.md','이번 내용과 장면'],['design.md','확인한 화면 기준'],['motion.md','확인한 움직임 기준']].forEach(([file,desc],i)=>{panel(s,'input-'+i,170+i*320,350,285,105,file,desc);});
 shape(s,'down-link',625,462,22,24,C.orange,'downArrow');shape(s,'confirm-bg',170,496,943,58,'#5E3818');text(s,'confirm-text','같은 버전의 자산·스틸컷·확인 영상과 함께 보관',188,503,907,44,24,C.white,true,'center');shape(s,'down-link-2',625,562,22,24,C.orange,'downArrow');shape(s,'next-bg',170,596,943,39,C.card);text(s,'next-text','다음 주제의 새 스토리라인과 묶어서 제공',187,598,909,35,23,C.orange,true,'center');
}
await fs.writeFile(path.join(B,'additions.json'),JSON.stringify(spec,null,2));await(await PresentationFile.exportPptx(p)).save(path.join(B,'additions.pptx'));console.log('Authored '+spec.length+' slides: Part 3 +8 and Part 4 +6.');
