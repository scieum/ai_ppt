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
const renders=path.join(unit,'renders/orange-original-v4');
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
const white='#FFFFFF', gray='#9E9E9E', pink='#FF9228';
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

async function fiveCards(part,section,title,subtitle,items,summary) {
 const s=await base('five-elements'),t=spec.templates['five-elements'];
 heading(s,t,part,'01',section);
 slot(s,'title',title,t.title,white,true,'center');
 slot(s,'subtitle',subtitle,t.subtitle,white,false,'center',1.265);
 for(let i=0;i<5;i++){
  const x=t.card_lefts[i],w=t.card_width;
  txt(s,'number_'+i,String(i+1),[x,t.number_y,w,27],t.number_size,'#111820',true,'center');
  txt(s,'heading_'+i,items[i][0],[x,t.heading_y,w,45],t.heading_size,white,true,'center');
  txt(s,'description_'+i,items[i][1],[x,t.description_y,w,32],t.description_size,gray,false,'center');
  txt(s,'tag_'+i,items[i][2],[x,t.tag_y,w,27],t.tag_size,white,true,'center');
 }
 slot(s,'summary_label','수업 기준',t.summary_label,'#111820',true,'center');
 slot(s,'summary_text',summary,t.summary_text);
 common(s);return s;
}
{
 const s=await fiveCards('무료 웨비나  전체 흐름','다섯 단계로 직접 만들기',
  '수업 영상을 만드는 다섯 단계',
  '질문을 보여 주는 짧은 영상에서 시작해\n장면 계획과 외부 제작까지 연결합니다',
  [['단순 요청','수업 시작 질문 만들기','첫 결과'],['레퍼런스','토의 안내 배치 정하기','이미지 참고'],['모션 지식','읽기와 시선 확인','시간'],['문서 설계','활동 순서를 파일로','장면'],['외부 제작','교사 캐릭터 장면','클립 생성']],
  '내 수업에 필요한 결과부터 작게 만들어요');
 notes(s,'이번 사용자가 지정한 다섯 단계 순서로 새로 작성한 목차입니다. R02의 5칸 카드 구조만 사용하고 원래 모션 이론 문구는 가져오지 않았습니다. 수업 시작 질문과 짝 토의 안내는 이번 웨비나의 자체 실습 예시입니다.');
}
{
 const s=await fiveCards('Part 3  수업에 맞는 움직임 고르기','학생 화면으로 검토하기',
  '학생이 따라올 수 있는 영상인가요?',
  '보기 좋은 효과와 함께, 학생이 읽고 이해하고\n무엇을 할지 알 수 있는지 확인합니다',
  [['읽기','질문을 읽을 시간','문구 · 대비'],['시선','핵심어만 먼저 강조','크기 · 강조'],['순서','한 번에 하나씩','시간'],['행동','할 일을 구체적으로','안내'],['정리','마지막 과제 유지','마지막 화면']],
  '학생이 할 일을 순서대로 보여 줘요');
 notes(s,'교사용 자체 점검 기준으로 작성한 장표입니다. 원본의 대상·속성·시간·곡선·순서 목록을 문구만 바꿔 반복하지 않습니다. 예시 영상의 질문 가독성, 핵심어, 학생 행동과 마무리 과제를 실제 재생으로 확인합니다. 일반 모션 개념은 별도 근거와 함께 설명합니다.');
}
{
 const s=await base('brief'),t=spec.templates.brief;
 // Preserve the source raster's clipping and rounded header edges. Replace
 // only its accent node/wedge with vector geometry at the source coordinates.
 gradient(s,[433,580,70,350],'#000000');
 s.images.add({svg:'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 315"><defs><linearGradient id="w" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#FF9228" stop-opacity=".22"/><stop offset="1" stop-color="#FF9228" stop-opacity="0"/></linearGradient></defs><path d="M0 108 L70 0 V315 L0 207 Z" fill="url(#w)"/></svg>',position:P(433,589,70,315),alt:'원본 좌표를 유지하고 주황으로 바꾼 연결 면'});
 s.shapes.add({geometry:'roundRect',position:P(196,697,237,99),fill:'#2C1B0B',line:{fill:'#704418',width:.75}});
 heading(s,t,'Part 4  다음 수업에도 다시 쓰는 제작 문서','01','학습 목표와 화면 규칙');
 slot(s,'title','내 수업에 맞는 세 문서를 만들어요',t.title,white,true,'center');
 slot(s,'subtitle','학생이 할 일과 영상의 표현 규칙을 나누어 적습니다',t.subtitle,white,false,'center');
 for(const [i,v] of ['문서','이 강의에서 적을 내용','바꾸어 볼 수업 조건'].entries())txt(s,'table_header_'+i,v,t.column_headers[i],20,white,true,'center');
 slot(s,'start_label','짝 토의 안내',t.start,white,true,'center');
 const rows=[['LESSON_BRIEF.md','학생·학습 목표\n질문과 핵심 과제','오늘의 질문에 대해\n생각의 근거 한 가지 말하기'],
 ['VISUAL_RULES.md','읽는 시간·색\n강조·등장 규칙','주황 핵심어 / 긴 질문은\n읽는 구간을 늘리기'],
 ['SCENE_PLAN.md','4개 장면의\n시간·문구·행동','질문 4초 · 혼자 쓰기 6초\n짝 나눔 8초 · 함께 정리 6초']];
 for(let r=0;r<3;r++)for(let c=0;c<3;c++){
  const [x,w]=t.column_boxes[c],value=rows[r][c],lines=value.split('\n').length,size=c===0?25:t.detail_size;
  txt(s,`cell_${r}_${c}`,value,[x+25,t.row_tops[r]+(lines===2?19:34),w-50,76],size,c===1?'#000000':(c===2?'#BFBFBF':white),c===0,'left',1.42);
 }
 common(s);notes(s,'세 문서 이름과 교실 사례는 이번 강의를 위해 새로 작성했습니다. 4+6+8+6=24초는 활동 안내 영상의 네 장면 길이이며 학생의 실제 토의 시간이 아닙니다. 원본의 3열·3행 시각 구조만 참고했습니다. 실제 활동 안내 영상을 생성한 상태는 아니므로 도구 실행 성공 증빙으로 사용하지 않습니다.');
}
{
 const s=await base('prompt'),t=spec.templates.prompt;
 heading(s,t,'Part 5  외부 영상 제작 도구와 연결하기','01','교사 캐릭터 장면 만들기');
 slot(s,'title','장면표의 한 장면을 영상으로 확장해요',t.title,white,true,'center');
 slot(s,'subtitle','질문을 건네는 교사 장면과 정확한 문구를 따로 준비합니다',t.subtitle,white,false,'center');
 for(const [i,key] of ['claude','codex','higgsfield'].entries()){
  const icon=new Uint8Array(await fs.readFile(path.join(workspaceDir,'assets/tool-logos/orange-v2/png',key+'-front.png')));
  s.images.add({blob:icon,contentType:'image/png',fit:'contain',position:P(395+i*143,615,140,140),alt:key+' 주황 포인트 도구 소개 배지'});
 }
 txt(s,'tool_caption','대화형 AI와 외부 영상 제작 도구',[395,786,426,48],24,gray,false,'center');
 slot(s,'prompt_label','SCENE_PLAN.md의 한 장면',t.prompt_label,gray);
 slot(s,'prompt_body','교사 캐릭터가 질문하는\n짧은 영상을 만들어 줘.\n글자는 별도로 넣을게.',t.prompt_body,'#000000',true,'left',1.412);
 common(s);notes(s,'왼쪽은 실제 제품 화면이 아닌 도구 소개 배지입니다. 이번 웨비나용 새 요청 문구를 사용했습니다. 장면표를 AI가 해석한 뒤 실제 모델이 지원하는 입력과 길이·비율로 요청합니다. 도구가 확정되면 지원 조건을 검증합니다. 본 장표는 외부 업로드·생성 또는 모델별 기능 성공의 증거가 아닙니다.');
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
const finalPath=path.join(output,'NotionTalk_모션그래픽_주황포인트_자체사례_v5.pptx');
const result=await finalizePresentation({workspaceDir,candidatePath:draft,finalPath,pythonExecutable:PYTHON,
 integrityValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],
 explicitTotalSlideCount:5,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],
 fontPolicy:{basis:'design',families:['Pretendard']},verifyArtifactToolImport:true,receiptPath:path.join(build,'validation-orange-original-v5.json')});
console.log('Finalized',JSON.stringify(result));
