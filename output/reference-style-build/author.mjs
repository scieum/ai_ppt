import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {C,shape,text,arrow} from '../../assets/layout-library-20261028/recipes/components.mjs';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..'),U=path.join(R,'units/AI-001_모션그래픽수업영상_무료웨비나');
const p=Presentation.create({slideSize:{width:1280,height:720}}),spec=[];
const img=async file=>new Uint8Array(await fs.readFile(file));
const brand=await img(path.join(R,'assets/branding/notiontalk-white.png'));
const folder=await img(path.join(U,'assets/reference-style-20261029/orange-folder-v1.png'));
const poses=JSON.parse(await fs.readFile(path.join(U,'assets/character-sheets-20261028/poses.json'),'utf8'));
const charBlobs={woman:await img(poses.find(x=>x.character==='woman').file),man:await img(poses.find(x=>x.character==='man').file)};
function pic(s,blob,name,x,y,w,h){s.images.add({blob,contentType:'image/png',alt:name,fit:'contain',position:{left:x,top:y,width:w,height:h}});}
function pose(s,id,x,y,h){let d=poses.find(x=>x.id===id);pic(s,charBlobs[d.character],'pose:'+id,x,y,h*d.aspect_ratio,h);}
function page(n,title,sub,refs){const s=p.slides.add();s.background.fill=C.bg;const part=n<32?3:4;
 pic(s,brand,'NotionTalk original logo',1010,58,190,55);
 text(s,'part-label',part===3?'Part 3  스토리라인과 스틸컷 확인':'Part 4  수정 후 제작',60,55,800,27,17,C.muted,true);
 text(s,'group-number',part===3?'02':'01',60,91,45,36,28,C.orange,true);
 text(s,'group-label',part===3?'스타일 기준을 문서로 남기기':'피드백을 반영하고 진행하기',107,91,850,36,28,C.white,true);
 text(s,'slide-title',title,140,190,1000,65,40,C.white,true,'center');
 text(s,'slide-subtitle',sub,140,266,1000,42,23,C.white,false,'center');
 text(s,'copyright-footer','© 2026. NotionTalk. All rights reserved.',800,682,420,22,12,C.muted,false,'right');
 spec.push({page:n,title,refs});return s;
}
function take(s,t){text(s,'takeaway',t,150,638,980,34,20,C.orange,true,'center');}
function box(s,n,x,y,w,h,fill=C.card,stroke='none'){shape(s,n,x,y,w,h,fill,'roundRect',stroke);}
function label(s,n,t,x,y,w,size=24,col=C.white,bold=false,align='left',h=35){text(s,n,t,x,y,w,h,size,col,bold,align);}
function doc(s,n,file,lines,x,y,w,h,light=false){box(s,n,x,y,w,h,light?'#F3F1EC':C.card);label(s,n+'-file',file,x+24,y+17,w-48,25,light?'#222222':C.orange,true);shape(s,n+'-rule',x+24,y+62,w-48,1,light?'#D6D0C7':'#494949','rect');
 lines.forEach((t,i)=>label(s,n+'-line-'+i,t,x+24,y+77+i*(lines.length>6?27:32),w-48,lines.length>6?20:21,light?'#333333':C.white,false,'left',lines.length>6?27:31));}
function nativeTable(s,values,widths){const t=s.tables.add({rows:values.length,columns:values[0].length,left:170,top:343,width:940,height:280,columnWidths:widths,values});t.borders.assign({style:'solid',fill:'#555555',width:1});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){let cell=t.getCell(r,c);cell.fill=r===0?'#3C3C3C':(c===0?'#442A16':'#F1F0ED');cell.text.style={typeface:'Pretendard',fontSize:21,bold:r===0||c===0,color:r===0?C.white:c===0?C.orange:'#252525'};}spec.at(-1).native_table=true;}
function sample(s,n,x,y,w,h,title,large=false){box(s,n+'-frame',x,y,w,h,'#111111','#575757');pic(s,brand,n+'-logo',x+w-89,y+12,72,22);label(s,n+'-top','노션톡 웨비나',x+16,y+40,w-32,16,C.muted,true,'center',27);text(s,n+'-title',title,x+15,y+71,w-30,Math.max(h-100,45),w<250?18:large?34:25,C.orange,true,'center');}
function chip(s,n,t,x,y,w,fill=C.card,col=C.white){box(s,n,x,y,w,38,fill);label(s,n+'-text',t,x+10,y+3,w-20,20,col,true,'center',32);}

{
const s=page(24,'비슷한 톤을 다시 얻고 싶다면','design.md와 motion.md도 함께 만드는 것을 추천합니다',['R01:18','R01:54']);
doc(s,'design','design.md',['색 · 글꼴 · 구도','로고 · 캐릭터 · 이미지'],190,349,330,220,true);
doc(s,'motion','motion.md',['등장 · 속도 · 간격','유지 · 전환 · 박자'],755,349,330,220);
pose(s,'woman-explain',554,349,263);
label(s,'design-role','보이는 스타일의 기준',190,583,330,23,C.white,true,'center');label(s,'motion-role','움직이는 방식의 기준',755,583,330,23,C.white,true,'center');
take(s,'마음에 든 결과에서 반복할 특징을 문장과 수치로 남깁니다');
}
{
const s=page(25,'세 문서와 스틸컷의 역할','내용·화면·움직임을 나누어 정리합니다',['R01:10','R01:64']);
nativeTable(s,[['자료','답하는 질문','담을 내용'],['storyline.md','무엇을 어떤 순서로?','장면 · 문구 · 구간'],['design.md','어떤 모습으로?','색 · 글꼴 · 구도 · 자산'],['motion.md','어떻게 움직이게?','등장 · 속도 · 전환 · 유지'],['스틸컷 2장','화면은 어떻게 보이나?','시작과 마무리의 대표 모습']],[235,350,355]);
take(s,'스틸컷은 화면을 보여 줍니다. 속도는 재생해서 확인합니다');
}
{
const s=page(26,'design.md에 담을 화면 기준','색 이름보다 구체적인 값과 배치를 함께 기록합니다',['R01:33','R01:54']);
sample(s,'design-sample',415,350,450,254,'배움이\n움직인다',true);
chip(s,'color','강조색  #FF9228',130,365,245,'#512F12',C.orange);arrow(s,'color-link',380,373,24,22);
label(s,'color-note','배경은 검정, 본문은 흰색',130,412,245,20,C.muted,false,'center');
chip(s,'type','Pretendard · 굵은 제목',905,365,245);shape(s,'type-link',876,373,24,22,C.orange,'leftArrow');
label(s,'type-note','글꼴·위계·강조 방식',905,412,245,20,C.muted,false,'center');
chip(s,'layout','제목 중앙 · 로고 우측 위',130,491,245);arrow(s,'layout-link',380,499,24,22);
label(s,'layout-note','여백과 정렬 기준',130,538,245,20,C.muted,false,'center');
chip(s,'asset','원본 로고 · 같은 삼인방',905,491,245);shape(s,'asset-link',876,499,24,22,C.orange,'leftArrow');
label(s,'asset-note','사용 파일과 외형 고정',905,538,245,20,C.muted,false,'center');
take(s,'같은 브랜드로 보이게 하는 요소부터 정리합니다');
}
{
const s=page(27,'design.md 예시','노션톡 15초 소개 영상에 사용할 시각 기준입니다',['R01:40','R01:50']);
doc(s,'design-example','design.md',['배경 #000000  /  본문 #FFFFFF','강조색 #FF9228','글꼴 Pretendard  /  제목은 굵게','제목 중앙 정렬, 두 줄 이내','로고 우측 위, 원본 비율 유지','캐릭터의 헤어·안경·의상 고정','이미지는 의미가 있는 장면에만 사용','문구가 길면 줄이고 여백 유지'],365,326,745,303,true);
// Compact line spacing in the large source-style document panel.
chip(s,'fixed','고정할 기준',150,355,180,'#512F12',C.orange);label(s,'fixed-desc','색·글꼴·브랜드',150,402,180,21,C.white,false,'center');
chip(s,'variable','장면별 선택',150,467,180);label(s,'variable-desc','문구·이미지 비중',150,514,180,21,C.white,false,'center');
take(s,'실제 로고·캐릭터 파일과 참고 스틸컷도 함께 보관합니다');
}
{
const s=page(28,'motion.md에 담을 움직임 기준','시작·움직임·멈춤·장면 연결을 나누어 기록합니다',['R01:99','R01:44']);
const names=['등장','순차 등장','유지','전환'];const sub=['어디서 얼마나 빠르게?','몇 초 간격으로?','얼마나 머물게?','어떻게 이어지게?'];const widths=[180,240,260,200];let x=175;
for(let i=0;i<4;i++){box(s,'time-'+i,x,370,widths[i],94,i===0||i===3?'#553212':'#292929');label(s,'time-title-'+i,names[i],x+12,384,widths[i]-24,28,i===0||i===3?C.orange:C.white,true,'center');label(s,'time-small-'+i,['효과·방향·시간','요소 사이 시작 간격','읽는 시간','장면 연결'][i],x+10,425,widths[i]-20,19,C.muted,false,'center',30);label(s,'question-'+i,sub[i],x-8,479,widths[i]+16,21,C.white,false,'center',43);x+=widths[i]+16;}
shape(s,'timeline-base',175,536,928,2,'#555555','rect');label(s,'timeline-start','시작',175,548,120,19,C.muted);label(s,'timeline-end','다음 장면',1010,548,130,19,C.muted,false,'left');
chip(s,'easing','가감속과 박자',535,557,210,'#512F12',C.orange);label(s,'easing-desc','처음 빠르게, 끝은 천천히 · 소리가 있다면 시점도 기록',335,599,610,19,C.muted,false,'center',29);
take(s,'“부드럽게”라는 말에 방향·초·간격을 덧붙입니다');
}
{
const s=page(29,'motion.md 예시','아래 수치는 이번 소개 영상의 출발 기준입니다',['R01:54','R03:31']);
doc(s,'motion-example','motion.md',['15초 / 30fps / 16:9','등장 0.45초, 페이드 + 위로 이동','최종 위치보다 아래 16px에서 시작','처음 빠르게, 끝은 천천히','다음 요소는 0.12초 뒤에 등장','퇴장 0.25초 페이드','장면 연결 0.3초 겹쳐 전환','끝 문구 1.2초 이상 유지'],160,329,590,300);
label(s,'stagger-title','시작 간격 0.12초',812,347,300,27,C.orange,true,'center');
['첫 문구','다음 문구','끝 문구'].forEach((t,i)=>{label(s,'bar-label-'+i,t,795,402+i*52,90,21,C.white);box(s,'bar-'+i,888+i*24,410+i*52,160,23,i===0?C.orange:'#865222');});
label(s,'stagger-explain','같은 규칙으로\n순서와 속도를 비교합니다',795,565,330,23,C.white,false,'center',63);
take(s,'정지 스틸컷과 함께 짧은 구간을 재생해 확인합니다');
}
{
const s=page(30,'문서와 확인 자료를 함께 봅니다','문서의 기준이 실제 결과에 반영됐는지 확인합니다',['R03:31','R01:39']);
const rows=[['storyline.md','장면·핵심 문구','장면표와 전체 흐름'],['design.md','색·글자·구도','대표 스틸컷 두 장'],['motion.md','시간·간격·전환','짧은 영상 구간 재생']];
rows.forEach(([file,desc,result],i)=>{let y=342+i*96;box(s,'left-'+i,175,y,330,77,'#292929');label(s,'file-'+i,file,198,y+8,283,28,C.orange,true);label(s,'desc-'+i,desc,198,y+43,283,20,C.muted,false,'left',28);arrow(s,'arrow-'+i,552,y+23,33,29);box(s,'right-'+i,635,y,470,77,'#F1F0ED');label(s,'result-'+i,result,658,y+16,424,27,'#222222',true,'center',45);});
take(s,'화면은 스틸컷으로, 시간의 변화는 재생 구간으로 확인합니다');
}
{
const s=page(31,'다음 영상에도 기준 문서를 전달합니다','주제가 바뀌어도 공통 스타일을 다시 참고할 수 있습니다',['R01:12','R03:29']);
pic(s,folder,'orange folder with reference documents',140,338,305,305);label(s,'bundle','노션톡 영상 기준',135,603,315,23,C.orange,true,'center');arrow(s,'bundle-link',460,459,35,36);
[['storyline.md','이번 주제·장면으로 새로 정리'],['design.md','확정한 화면 스타일을 함께 제공'],['motion.md','확정한 움직임 기준을 함께 제공'],['assets / references','같은 자산·스틸컷·기준 영상']].forEach(([file,role],i)=>{let y=345+i*68;box(s,'file-box-'+i,527,y,265,52,'#292929');label(s,'file-'+i,file,545,y+7,230,23,C.white,true);label(s,'role-'+i,role,821,y+7,355,21,C.muted);});
take(s,'확인한 버전의 문서와 실제 자산을 한 묶음으로 전달합니다');
}
{
const s=page(34,'수정 대상을 기준 파일과 연결합니다','무엇을 바꾸는지에 따라 먼저 볼 문서가 달라집니다',['R01:39','R01:47']);
nativeTable(s,[['고칠 부분','먼저 볼 기준','다시 확인할 결과'],['제목·장면 순서','storyline.md','내용과 전체 흐름'],['색·글꼴·로고 위치','design.md','수정된 스틸컷'],['등장 속도·장면 전환','motion.md','해당 영상 구간'],['읽을 시간·장면 길이','storyline.md + motion.md','구간과 전체 영상 길이']],[260,350,330]);
take(s,'내용·화면·움직임 중 어디를 고치는지 먼저 구분합니다');
}
{
const s=page(35,'바꿀 것과 유지할 것을 정합니다','제목 크기를 바꾸는 경우를 비교해 봅니다',['R01:18','R01:39','R01:60']);
sample(s,'before',190,350,365,194,'배움이 움직인다');sample(s,'after',725,350,365,194,'배움이\n움직인다',true);arrow(s,'compare-arrow',616,420,45,47);
label(s,'before-caption','수정 전',190,552,365,23,C.muted,true,'center');label(s,'after-caption','제목을 더 크게',725,552,365,23,C.orange,true,'center');
label(s,'preserve','유지: 배경·강조색·글꼴·로고',190,593,900,22,C.white,true,'center');
take(s,'등장 속도를 바꿀 때는 위치·순서를, 유지 시간을 늘릴 때는 문구·구도를 유지');
}
{
const s=page(36,'짧은 구간부터 다시 확인합니다','작게 확인한 뒤 전체 흐름으로 넓혀 봅니다',['R01:44','R01:99']);
chip(s,'still','스틸컷',150,344,225,'#512F12',C.orange);chip(s,'segment','짧은 구간',526,344,225,'#512F12',C.orange);chip(s,'whole','전체 영상',902,344,225,'#512F12',C.orange);arrow(s,'a1',425,444,30,32);arrow(s,'a2',801,444,30,32);
sample(s,'still-sample',150,403,225,128,'배움이 움직인다');
box(s,'segment-bg',526,403,225,128,'#242424');label(s,'segment-time','4–7초',543,428,191,39,C.white,true,'center',55);label(s,'segment-unit','예: 3초 구간',543,487,191,20,C.orange,false,'center');
box(s,'whole-bg',902,403,225,128,'#242424');label(s,'whole-time','15초',919,428,191,39,C.white,true,'center',55);label(s,'whole-unit','예: 전체 길이',919,487,191,20,C.orange,false,'center');
[['색·글자·잘림·구도',150],['등장·속도·전환',526],['앞뒤 연결·마무리',902]].forEach(([t,x])=>label(s,'check-'+x,t,x,552,225,22,C.white,false,'center',52));
take(s,'변경한 구간을 먼저 보고, 마지막에는 전체 영상을 봅니다');
}
{
const s=page(37,'내용·디자인·모션을 나누어 점검합니다','예쁘게 보이는 것과 정확하게 전달되는 것을 함께 봅니다',['R01:74','R03:34']);
const qs=[['내용','문구·순서·전달 내용이 맞나?','storyline.md'],['디자인','글자가 읽히고 자산이 맞나?','design.md + 스틸컷'],['모션','등장·유지·전환이 맞나?','motion.md + 구간 재생'],['전체 연결','장면과 소리가 자연스럽게 이어지나?','전체 영상과 구간표']];
box(s,'checklist-panel',240,330,845,294,'#181818','#555555');
qs.forEach(([area,q,file],i)=>{let y=348+i*66;shape(s,'empty-checkbox-'+i,264,y+8,21,21,'none','rect','#FF9228');label(s,'area-'+i,area,303,y,117,22,C.orange,true);label(s,'q-'+i,q,425,y,625,23,C.white);label(s,'file-'+i,file,425,y+32,625,18,C.muted,false,'left',29);});
pose(s,'man-review',96,410,245);take(s,'읽힘·움직임·내용을 각각 확인한 뒤 함께 봅니다');
}
{
const s=page(38,'한 장면 수정과 공통 규칙의 변경','이번 영상에만 적용할지, 다음 작업에도 쓸지 구분합니다',['R01:18','R01:28']);
label(s,'local-title','이번 장면만 수정',180,337,420,28,C.white,true,'center');label(s,'global-title','공통 기준을 변경',680,337,420,28,C.orange,true,'center');
for(let group=0;group<2;group++){let x0=180+group*500;for(let i=0;i<3;i++){let x=x0+i*143;box(s,'film-'+group+'-'+i,x,404,132,102,group===1||i===1?'#513012':'#232323');label(s,'scene-'+group+'-'+i,'장면 '+(i+1),x+8,415,116,20,C.muted,false,'center');label(s,'duration-'+group+'-'+i,group===1||i===1?'0.6초':'0.45초',x+8,454,116,27,group===1||i===1?C.orange:C.white,true,'center');}}
label(s,'local-record','장면표에 예외로 기록\n다른 장면의 기준은 유지',180,535,420,23,C.white,false,'center',73);
label(s,'global-record','motion.md 기본값 갱신\n다른 장면도 다시 확인',680,535,420,23,C.white,false,'center',73);
take(s,'장면별 예외와 공통 기본값을 구분해 남깁니다');
}
{
const s=page(39,'확인한 기준을 다음 작업에 남깁니다','문서·자산·결과물의 버전을 맞춰 보관합니다',['R01:62','R01:64','R01:79']);
doc(s,'confirmed','확인한 문서',['storyline.md  이번 내용과 장면','design.md  확인한 화면 기준','motion.md  확인한 움직임 기준'],170,354,435,218);
arrow(s,'save-link',631,438,35,35);
box(s,'version-bundle',710,354,400,218,'#F1F0ED');label(s,'version-label','같은 버전으로 보관',737,375,346,27,'#222222',true,'center');
label(s,'version-files','실제 사용한 자산\n대표 스틸컷 두 장\n확인한 영상 구간',739,426,342,24,'#333333',false,'center',123);
label(s,'next-project','다음 주제의 새 storyline.md와 묶어서 제공',170,592,940,26,C.orange,true,'center');
take(s,'새 작업에서도 스틸컷과 짧은 구간으로 적용 상태를 확인합니다');
}
await fs.writeFile(path.join(B,'additions.json'),JSON.stringify(spec,null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(B,'additions.pptx'));
console.log('Authored 14 reference-led replacement slides');