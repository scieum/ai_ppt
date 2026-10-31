import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
import {Presentation,PresentationFile} from '@oai/artifact-tool';

const build=path.dirname(fileURLToPath(import.meta.url));
const unit=path.resolve(build,'../../..');
const workspaceDir=path.resolve(unit,'../..');
const library=path.join(workspaceDir,'assets/reference-templates');
const output=path.join(workspaceDir,'output/webinar-samples');
const renders=path.join(unit,'renders/orange-cover-v3');
const spec=JSON.parse(await fs.readFile(path.join(library,'layouts.json'),'utf8'));
const catalog=JSON.parse(await fs.readFile(path.join(library,'catalog.json'),'utf8'));
const SKILL_DIR='C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.22136/skills/presentations';
const PYTHON='C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const S=2/3, P=(x,y,w,h)=>({left:x*S,top:y*S,width:w*S,height:h*S});
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
const {FontLibrary}=req('skia-canvas');
FontLibrary.use('Pretendard',[
 'C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf',
 'C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const white='#FFFFFF', gray='#9E9E9E', pink='#FB3890';
const logo=new Uint8Array(await fs.readFile(path.join(workspaceDir,'assets/branding/notiontalk-white.png')));
const poster=new Uint8Array(await fs.readFile(path.join(unit,'assets/webinar-poster.png')));
const coverArt=new Uint8Array(await fs.readFile(path.join(unit,'assets/cover-characters-orange-v3.png')));
const p=Presentation.create({slideSize:{width:1280,height:720}});
const roles=[],adoption=[];
function txt(s,role,value,box,size,color=white,bold=false,align='left',spacing=1.2){
 const [x,y,w,h]=box;
 const sh=s.shapes.add({geometry:'textbox',name:role,position:P(x,y,w,h),fill:'none',line:{fill:'none',width:0}});
 sh.text=value;
 sh.text.style={typeface:'Pretendard',fontSize:size*S,bold,color,alignment:align,verticalAlignment:'top',insets:0,autoFit:'none',wrap:'none',lineSpacing:spacing/1.2};
 roles.push({slide:p.slides.items.length,role,text:value,box:[x,y,w,h],size});return sh;
}
function slot(s,role,value,b,color=white,bold=false,align='left',spacing=1.2){return txt(s,role,value,b,b[4],color,bold,align,spacing)}
function gradient(s,box,fill){s.shapes.add({geometry:'rect',position:P(...box),fill,line:{fill:'none',width:0}})}
async function base(id){
 const s=p.slides.add();s.background.fill='#000000';
 const ref=catalog.templates.find(t=>t.id===id);
 if(id==='cover') {
  gradient(s,[0,0,1920,1080],'linear(0deg, #C66B11 0%, #C66B11 22.14%, #8C480B 35%, #2E1806 48%, #000000 58%, #000000 100%)');
  s.images.add({blob:logo,contentType:'image/png',fit:'contain',position:P(...spec.common.brand),alt:'사용자 제공 원본 NotionTalk 흰색 로고'});
 } else {
  const blob=new Uint8Array(await fs.readFile(path.join(build,'backgrounds',id+'.png')));
  s.images.add({name:'source-geometry-'+id,blob,contentType:'image/png',position:P(0,0,1920,1080),alt:`원본 ${ref.source_id} PDF ${ref.source_page}쪽에서 텍스트·교체 이미지·로고만 제거한 배경`});
 }
 adoption.push({slide:p.slides.items.length,template:id,source:ref.source_name,page:ref.source_page,background:ref.background,background_sha256:ref.background_sha256,geometry:'Original extracted background, no shape recreation or rescaling within the source canvas.'});
 return s;
}
function common(s){
 // Original selected brand is composed in the course background by
 // prepare_backgrounds.py. Reusable library backgrounds are brand-neutral.
 txt(s,'copyright_footer','© 2026. NotionTalk. All rights reserved.',spec.common.footer,spec.common.footer_size,'#999999',false,'right');
}
function heading(s,t,part,num,section){
 slot(s,'part_label',part,t.part,'#888888',true);
 slot(s,'section_number',num,t.section_number,pink,true);
 slot(s,'section_heading',section,t.section,white,true);
}
function notes(s,text){const a=adoption.at(-1);s.speakerNotes.text=[text,`레이아웃 출처: ${a.source}, PDF ${a.page}쪽.`,
 '원본에서 추출한 도형·배경은 고정 이미지이며 새 문구는 PowerPoint에서 편집 가능한 텍스트입니다.',
 '원본 PDF의 익명 Type3 글꼴은 정확한 패밀리를 확인할 수 없어 Pretendard로 대체했습니다. 크기와 좌표는 실측값을 사용합니다.',
 '사용자 요청에 따라 원본 로고를 NotionTalk으로 교체하고 저작권 푸터를 적용했습니다.',
 '대표 5장 수정 시안. 전체 강의 및 사용자 디자인 승인을 의미하지 않습니다.'].join('\n');}
{
 const s=await base('cover'),t=spec.templates.cover;
 s.images.add({blob:coverArt,contentType:'image/png',fit:'contain',position:P(...t.figure),alt:'참고 이미지의 여성·곰·남성 교사 외형을 유지하고 영상 제작 협업 장면으로 새로 생성한 일러스트'});
 slot(s,'cover_title','모션 그래픽을 이용한\n수업 영상 제작하기',t.title,white,true,'left',1.25);
 slot(s,'cover_subtitle','AI로 달라지는 선생님의 수업 영상 제작 · 무료 웨비나',t.subtitle);
 slot(s,'webinar_date','2026년 11월 1일(일) 20:00 LIVE',t.date);
 common(s);
 notes(s,'주제와 일정은 사용자 제공 홍보 이미지를 따릅니다. 표지의 두 줄 제목·보조 문장·하단 일정 좌표는 유지했습니다. 사용자 최신 요청에 따라 붉은 그라데이션을 주황색으로 바꾸고, 참고 이미지 속 세 캐릭터의 머리·얼굴·안경·의상 색을 유지한 새로운 영상 제작 협업 장면을 built-in image_gen으로 생성했습니다. 새 그림은 원본 포스터 복사나 비파괴 크롭이 아닙니다. 생성 프롬프트와 파일은 assets에 보관합니다. 종료 시각과 발표자 이름은 미제공입니다.');
}
{
 const s=await base('agenda'),t=spec.templates.agenda;
 slot(s,'title','오늘 웨비나는 이렇게 진행합니다',t.title,white,true,'center');
 const names=['수업 영상에\n모션 더하기','만들 영상의\n조건 정하기','장면표\n요청하기','결과 확인과\n질의응답'];
 for(let i=0;i<4;i++){
  const [x,y]=t.part_labels[i];txt(s,'part_'+(i+1),'Part '+(i+1),[x,y,210,45],t.part_size,pink,true);
  const [tx,ty]=t.part_titles[i];txt(s,'part_title_'+(i+1),names[i],[tx,ty,210,92],t.body_size,white,true,'left',1.2);
 }
 common(s);notes(s,'이 4개 Part는 웨비나 구성 제안입니다. 원본 네 개의 꺾인 목차 에셋과 각 라벨의 서로 다른 수직 위치까지 유지했습니다. Part 표기는 기존 사용자 규칙에 맞춰 대소문자만 변경했습니다.');
}
{
 const s=await base('five-elements'),t=spec.templates['five-elements'];
 heading(s,t,'Part 1  수업 영상에 모션 더하기','01','모션의 구성 요소');
 slot(s,'title','수업 영상의 모션을 정하는 5가지',t.title,white,true,'center');
 slot(s,'subtitle','무엇을, 어떻게, 얼마나 오래, 어떤 속도 변화로, 어떤 순서로 보여줄까요?\n설명에 맞춰 모션의 조건을 정합니다',t.subtitle,white,false,'center',1.265);
 const items=[['대상','무엇을 움직일까요','글자 · 그림'],['속성','무엇을 바꿀까요','위치 · 크기 · 투명도'],['시간','얼마나 유지할까요','duration'],['곡선','속도를 어떻게 바꿀까요','easing'],['순서','언제 보여줄까요','delay · stagger']];
 for(let i=0;i<5;i++){
  const x=t.card_lefts[i],w=t.card_width;
  txt(s,'number_'+i,String(i+1),[x,t.number_y,w,27],t.number_size,white,true,'center');
  txt(s,'heading_'+i,items[i][0],[x,t.heading_y,w,45],t.heading_size,white,true,'center');
  txt(s,'description_'+i,items[i][1],[x,t.description_y,w,32],t.description_size,gray,false,'center');
  txt(s,'tag_'+i,items[i][2],[x,t.tag_y,w,27],t.tag_size,white,true,'center');
 }
 slot(s,'summary_label','한 줄 정리',t.summary_label,white,true,'center');
 slot(s,'summary_text','설명할 내용에 맞춰 움직임의 조건을 정해요',t.summary_text);
 common(s);notes(s,'내용 근거: 같은 PDF 20~28쪽의 대상·속성·시간·곡선·순서 설명을 교사의 수업 영상 맥락으로 바꾸었습니다. 원본의 카드 5개, 원형 번호, 태그 폭, 하단 요약 바를 그대로 사용합니다. duration은 지속 시간, easing은 속도 변화 방식, delay는 지연, stagger는 차례로 시작하는 간격입니다.');
}
{
 const s=await base('brief'),t=spec.templates.brief;
 heading(s,t,'Part 2  만들 영상의 조건 정하기','01','제작 요청서');
 slot(s,'title','수업 영상을 요청하기 전에 정할 3가지',t.title,white,true,'center');
 slot(s,'subtitle','학습 목표와 영상 길이, 사용할 자료를 먼저 정리합니다',t.subtitle,white,false,'center');
 for(const [i,v] of ['먼저 정할 질문','정리할 내용','수업 영상 예시'].entries())txt(s,'table_header_'+i,v,t.column_headers[i],20,white,true,'center');
 slot(s,'start_label','수업 영상 시작',t.start,white,true,'center');
 const rows=[['무엇을 가르치나요?','대상과 학습 목표\n한 가지','초등학생 대상, 핵심 개념\n한 가지를 설명하는 영상'],['얼마나 보여줄까요?','길이와 화면 비율','20초, 가로 16:9'],['어떤 자료를 쓰나요?','수업 자료와\n사용할 이미지','내 수업 자료 한 장\n출처와 사용 범위 확인']];
 for(let r=0;r<3;r++)for(let c=0;c<3;c++){
  const [x,w]=t.column_boxes[c],str=rows[r][c],size=c===0?t.question_size:t.detail_size;
  const lines=str.split('\n').length;
  txt(s,`cell_${r}_${c}`,str,[x+25,t.row_tops[r]+(lines===2?19:34),w-50,76],size,c===1?'#000000':(c===2?'#BFBFBF':white),c===0,'left',1.42);
 }
 common(s);notes(s,'원본 91쪽의 시작 노드, 3열·3행, 가운데 흰색 설명 셀 구조를 그대로 사용했습니다. 20초와 16:9, 초등학생 대상은 시안용 제안이며 확정된 웨비나 실습 조건이 아닙니다. 실제 수업 자료나 생성 영상의 실행 결과는 아직 제공되지 않았습니다.');
}
{
 const s=await base('prompt'),t=spec.templates.prompt;
 heading(s,t,'Part 3  장면표 요청하기','01','AI에 요청하기');
 slot(s,'title','먼저 장면표를 요청해 볼까요?',t.title,white,true,'center');
 slot(s,'subtitle','장면별 화면 문구와 설명, 등장 순서를 확인합니다',t.subtitle,white,false,'center');
 s.images.add({blob:poster,contentType:'image/png',fit:'cover',crop:{left:0,top:.415,right:0,bottom:.065},position:P(...t.figure),alt:'웨비나 주제 삽화. 실제 도구 실행 화면이 아닙니다.'});
 slot(s,'prompt_label','수업 자료를 함께 넣고 입력',t.prompt_label,gray);
 slot(s,'prompt_body','내 자료로 20초 영상의\n장면표를 만들어 줘.\n질문·설명·확인 순서로.',t.prompt_body,'#000000',true,'left',1.412);
 common(s);notes(s,'레이아웃은 R05 31쪽의 왼쪽 자료·오른쪽 흰색 요청 상자입니다. 왼쪽은 사용자 제공 웨비나 삽화이며 실제 AI 실행 결과가 아닙니다. 화면의 짧은 요청과 별도로 복사 가능한 상세 프롬프트를 배포합니다. 결과에서는 학습 목표 하나, 문구의 읽는 시간, 원자료와의 일치를 확인합니다. 질문·설명·확인의 3장면은 실습 제안입니다.');
}
await fs.mkdir(renders,{recursive:true});await fs.mkdir(output,{recursive:true});
for(const [i,s] of p.slides.items.entries()){
 const stem=`slide-${String(i+1).padStart(2,'0')}`;
 const png=await p.export({slide:s,format:'png',scale:1.5});
 await fs.writeFile(path.join(renders,stem+'.png'),new Uint8Array(await png.arrayBuffer()));
 const layout=await s.export({format:'layout'});await fs.writeFile(path.join(renders,stem+'.layout.json'),await layout.text());
 console.log('Rendered',stem);
}
await fs.writeFile(path.join(build,'roles.json'),JSON.stringify(roles,null,2));
await fs.writeFile(path.join(build,'adoption.json'),JSON.stringify(adoption,null,2));
await fs.writeFile(path.join(build,'deck.json'),JSON.stringify(p.toProto()));
const draft=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(draft);
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL_DIR,'container_tools/artifact_tool_utils.mjs')).href);
const finalPath=path.join(output,'NotionTalk_모션그래픽_주황표지_대표5장_v3.pptx');
const result=await finalizePresentation({workspaceDir,candidatePath:draft,finalPath,pythonExecutable:PYTHON,
 integrityValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],
 explicitTotalSlideCount:5,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],
 fontPolicy:{basis:'design',families:['Pretendard']},verifyArtifactToolImport:true,receiptPath:path.join(build,'validation-orange-cover.json')});
console.log('Finalized',JSON.stringify(result));
