import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const build=path.dirname(fileURLToPath(import.meta.url)),unit=path.resolve(build,'../../..'),root=path.resolve(unit,'../..');
const source=path.join(root,'output/webinar-samples/NotionTalk_모션그래픽_주황포인트_자체사례_v5.pptx');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
const {FontLibrary}=req('skia-canvas');
FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(source));
const base=p.slides.items.slice(),created=[];
const S=2/3,P=(x,y,w,h)=>({left:x*S,top:y*S,width:w*S,height:h*S});
function edit(s,name,value){const shape=s.shapes.items.find(v=>v.name===name);if(!shape)throw Error('Missing original slot '+name);shape.text.replace(String(shape.text),value);return shape;}
function text(s,name,value,box,size,color='#FFFFFF',bold=false,alignment='center'){
 const x=s.shapes.add({geometry:'textbox',name,position:P(...box),fill:'none',line:{fill:'none',width:0}});
 x.text=value;x.text.style={typeface:'Pretendard',fontSize:size*S,color,bold,alignment,verticalAlignment:'top',insets:0,autoFit:'none',wrap:'none',lineSpacing:1};return x;
}
function notes(s,body){s.speakerNotes.text=[body,'디자인 기준: 사용자가 유지하라고 지정한 대표 5장 v5의 해당 장표를 직접 복제하고 텍스트와 예제 내용만 교체했습니다. 기존 대표 5장은 변경하지 않았습니다.','브랜드: NotionTalk. 주황 #FF9228. 기존 제목·상단 안내·흰 프롬프트 박스·회색 카드·로고·푸터·글꼴·간격 유지.','이 장표는 예제 요청과 표현 설명입니다. 실제 앱 실행이나 MP4 내보내기 완료의 증거가 아닙니다. 기존 G10 권리 검토 상태는 미완료이며 승인 기록을 새로 만들지 않았습니다.'].join('\n');}
{
 const s=base[1].duplicate();
 edit(s,'part_label','Part 0  오늘의 준비물');edit(s,'section_number','01');edit(s,'section_heading','실습 시작 전 확인하기');
 edit(s,'title','오늘의 준비물을 확인해요');edit(s,'subtitle','코덱스 or 클로드 유료 요금제');
 const items=[['컴퓨터','노트북 또는 데스크톱','인터넷'],['AI 계정','사용할 앱에 로그인','유료 요금제'],['홍보 문장','움직이게 할 짧은 문장','문장 입력'],['웹사이트','소개할 공개 페이지','URL'],['과학사 주제','원자모형의 변화','지식 전달']];
 for(let i=0;i<5;i++){edit(s,'heading_'+i,items[i][0]);edit(s,'description_'+i,items[i][1]);edit(s,'tag_'+i,items[i][2]);}
 edit(s,'summary_label','시작 전');edit(s,'summary_text','로그인하고 작업 폴더를 열어 두세요');
 notes(s,'Part 0 준비물. AI 준비물은 사용자의 정확한 표현인 ‘코덱스 or 클로드 유료 요금제’로 간단히 표기했습니다. 선택한 한 도구의 유료 계정을 준비합니다. 가격·상품별 설명은 추가하지 않았습니다. 대표본 2장의 5칸 카드 장표를 복제했습니다.');
 created.push({kind:'preparation',template:2,slide:s});
}
const examples=[
 {key:'typography',number:'01',section:'노션톡 웨비나 홍보 타이포그래피',title:'홍보 문장을 움직이는 영상으로 만들어요',subtitle:'문장이 이어지는 흐름과 핵심어의 크기 변화를 만들어 봐요',label:'문장으로 요청하기',prompt:'노션톡 무료 웨비나를 알리는\n20초 타이포그래피 영상을\n주황색으로 만들어 줘.',caption:'문장을 차례로 크게 보여 주기',note:'사용자가 선택한 사례 A: 노션톡 웨비나 홍보 타이포그래피. 검정 바탕·주황 포인트로 시작해 20초 초안을 요청합니다. 왼쪽은 장면 표현을 설명하는 편집 가능한 글자 예시이며 실제 앱 결과 화면이 아닙니다. 필요하면 제공 포스터의 행사 일정과 참가 안내를 후속 요청에 추가합니다.'},
 {key:'website',number:'02',section:'웹사이트 링크로 만드는 소개 영상',title:'웹사이트 내용을 소개 영상으로 바꿔요',subtitle:'링크의 내용을 읽고 중요한 정보를 새 장면으로 재구성해요',label:'notion.com/ko/product/docs',prompt:'이 페이지의 내용을 읽고\nNotion 문서를 소개하는\n30초 영상을 만들어 줘.',caption:'웹페이지 내용을 새 장면으로',note:'사용자가 선택한 사례 B: 실제 웹사이트 내용 기반 소개 영상. 구체 URL은 제작자가 선정한 https://www.notion.com/ko/product/docs 입니다. 2026-10-27 실제 공식 본문에서 콘텐츠 유형·목차·공동 편집과 댓글을 확인했습니다. 왼쪽은 원자료와 영상의 관계를 설명하는 자체 텍스트이며 실제 Notion UI가 아닙니다. AI가 해당 URL을 읽지 못하면 제공할 수 있는 본문으로 전환하고 직접 열람 성공과 구분합니다.'},
 {key:'history',number:'03',section:'원자모형 변천 지식 전달 영상',title:'과학사의 변화를 영상으로 설명해요',subtitle:'원자모형의 차이와 바뀐 이유를 글자·도형으로 보여 줘요',label:'주제로 요청하기',prompt:'원자모형이 바뀐 과정을\n45초 영상으로 만들어 줘.\n모형과 출처도 보여 줘.',note:'사용자가 선택한 사례 C: 톰슨·러더퍼드·보어의 원자모형 변천. 왼쪽 세 모형은 설명용 모식도이며 입자 수·크기 비율·전자의 실제 관측 경로를 나타내지 않습니다. 보어 모형을 현대 원자모형의 최종 형태로 설명하지 않습니다. 근거: AIP https://history.aip.org/exhibits/rutherford/sections/alpha-particles-atom.html 및 Manitoba Education Senior 1 Science Appendix 2.3 A27~A29 https://www.edu.gov.mb.ca/ks4/cur/science/found/s1/appen2.pdf . 확인일 2026-10-27. 연도·모형의 특징은 실제 자료와 대조한 뒤 영상에 사용합니다.'},
];
function ellipse(s,name,cx,cy,r,fill='none',line='#777777',width=1.5){return s.shapes.add({geometry:'ellipse',name,position:P(cx-r,cy-r,r*2,r*2),fill,line:{fill:line,width:width*S}});}
for(const r of examples){
 const s=base[4].duplicate();
 edit(s,'part_label','Part 1  단순 프롬프트로 시작하기');edit(s,'section_number',r.number);edit(s,'section_heading',r.section);
 edit(s,'title',r.title);edit(s,'subtitle',r.subtitle);edit(s,'prompt_label',r.label);edit(s,'prompt_body',r.prompt);
 // Keep the original full-canvas background, including its prompt box and
 // logo. Replace only the three tool pictures used by the old Part 5 example.
 for(const im of [...s.images.items])if(im.position.width<1000)im.delete();
 if(r.key==='typography'){
  text(s,'sample-line-1','수업 자료가',[395,585,426,52],40,'#FFFFFF',false);
  text(s,'sample-focus','영상이',[395,641,426,93],80,'#FF9228',true);
  text(s,'sample-line-3','되는 순간',[395,734,426,44],36,'#FFFFFF',false);
  edit(s,'tool_caption',r.caption);
 }else if(r.key==='website'){
  text(s,'website-input','notion.com',[395,610,426,48],40,'#FFFFFF',true);
  text(s,'website-contents','콘텐츠 · 목차 · 공동 편집',[395,675,426,38],25,'#9E9E9E',false);
  text(s,'website-output','30초 소개 영상',[395,726,426,49],40,'#FF9228',true);
  edit(s,'tool_caption',r.caption);
 }else{
  s.shapes.items.find(v=>v.name==='tool_caption').delete();
  for(let i=0;i<3;i++){
   const cx=465+i*143,cy=685;
   if(i===0){
    ellipse(s,'thomson-positive',cx,cy,49,'#3F2A17','#FF9228');
    for(const [dx,dy] of [[-20,-20],[22,-9],[-10,25]])ellipse(s,'thomson-electron',cx+dx,cy+dy,5,'#FFFFFF','none',0);
   }else{
    for(const rad of (i===1?[49]:[31,52]))ellipse(s,'orbit',cx,cy,rad);
    ellipse(s,'nucleus',cx,cy,7,'#FF9228','none',0);
    const rad=i===1?49:31;ellipse(s,'electron',cx+rad*.7,cy+rad*.714,5,'#FFFFFF','none',0);
   }
   text(s,'model-label-'+i,['톰슨','러더퍼드','보어'][i],[395+i*143,786,140,48],24,'#9E9E9E',false);
  }
 }
 notes(s,r.note+' 대표본 5장의 흰 프롬프트 박스 형식을 그대로 복제했으며 원문 레퍼런스의 사례·문구를 복제하지 않았습니다.');
 created.push({kind:r.key,template:5,slide:s});
}
const render=path.join(unit,'renders/append-part01/artifact');await fs.mkdir(render,{recursive:true});
const mapping=[];
for(const [i,r] of created.entries()){
 const n=p.slides.items.findIndex(s=>s.id===r.slide.id)+1;
 mapping.push({key:r.kind,template_slide:r.template,export_slide:n});
 const png=await p.export({slide:r.slide,format:'png',scale:1.5});await fs.writeFile(path.join(render,'new-'+(i+1)+'.png'),new Uint8Array(await png.arrayBuffer()));
 console.log('Rendered addition',r.kind,'export slide',n);
}
await fs.writeFile(path.join(build,'additions.json'),JSON.stringify(mapping,null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(build,'roundtrip-with-additions.pptx'));
console.log('Exported duplicated source slides; original package will be preserved during insertion.');
