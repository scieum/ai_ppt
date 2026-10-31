import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const build = path.dirname(fileURLToPath(import.meta.url));
const unit = path.resolve(build, '../../..');
const workspaceDir = path.resolve(unit, '../..');
const output = path.join(workspaceDir, 'output/webinar-samples');
const renders = path.join(unit, 'renders');
const SKILL_DIR = 'C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.22136/skills/presentations';
const PYTHON = 'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const poster = new Uint8Array(await fs.readFile(path.join(unit, 'assets/webinar-poster.png')));
const logo = new Uint8Array(await fs.readFile(path.join(unit, 'assets/notiontalk-white.png')));
const footer = '© 2026. NotionTalk. All rights reserved.';
const S = 2 / 3;
const pos = (x,y,w,h) => ({left:x*S,top:y*S,width:w*S,height:h*S});
const C = {bg:'#080D16', white:'#F6F9FF', muted:'#AAB7CB', blue:'#A8D2FF', line:'#2B3B54', panel:'#151E2D'};
const req = createRequire(import.meta.resolve('@oai/artifact-tool'));
const { FontLibrary } = req('skia-canvas');
if (!FontLibrary.families.includes('Pretendard')) throw new Error('Pretendard is not registered');
if (typeof FontLibrary.use === 'function') {
  FontLibrary.use('Pretendard', [
    'C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf',
    'C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf',
  ]);
}
const p = Presentation.create({slideSize:{width:1280,height:720}});
const roleMap = [];
function text(slide, role, value, x,y,w,h,size=40,color=C.white,bold=false,align='left') {
  const shape = slide.shapes.add({geometry:'textbox',name:role,position:pos(x,y,w,h),fill:'none',line:{fill:'none',width:0}});
  shape.text = value;
  shape.text.style = {typeface:'Pretendard',fontSize:size*S,bold,color,alignment:align,verticalAlignment:'top',
    insets:0,autoFit:'none',wrap:'none',lineSpacing:1.12};
  roleMap.push({slide:p.slides.items.length,role,text:value,position:[x,y,w,h]});
  return shape;
}
function rect(slide,role,x,y,w,h,fill,line='none',lw=0) {
  return slide.shapes.add({geometry:'rect',name:role,position:pos(x,y,w,h),fill,line:{fill:line,width:lw*S}});
}
function common(slide, number, part, subject) {
  slide.background.fill = C.bg;
  slide.images.add({blob:logo,contentType:'image/png',alt:'사용자 제공 NotionTalk 흰색 로고',fit:'contain',position:pos(1560,32,280,94)});
  text(slide,'copyright_footer',footer,1050,1020,790,36,24,C.muted,false,'right');
  text(slide,'page_number',String(number).padStart(2,'0'),80,1020,70,36,24,C.muted);
  if(part) {
    text(slide,'part_label',part,80,48,1200,46,28,C.muted);
    text(slide,'section_heading',subject,80,112,1460,60,38,C.white,true);
  }
}
function note(slide, lines, refs) {
  slide.speakerNotes.text = ['검토용 대표 시안. 전체 웨비나의 확정 교안이나 실제 모션 영상이 아님.', ...lines,
    '출처: '+refs].join('\n');
}
const motionRef = '[사이클 라이브] 클로드 코드로 만드는 일관된 모션 시스템.pdf';

// 1. Cover: original artwork is retained and cropped only in the image object.
{
  const s=p.slides.add(); common(s,1);
  s.background.fill='#14233F';
  s.images.add({blob:poster,contentType:'image/png',alt:'사용자 제공 웨비나 홍보 이미지의 인물 영역',fit:'cover',
    crop:{left:0,top:0.415,right:0,bottom:0.065},position:pos(930,280,990,645)});
  rect(s,'cover-image-edge',860,280,260,645,'linear(0deg, #14233F 0%, #14233F/0 100%)');
  text(s,'cover_kicker','무료 웨비나',95,186,700,60,36,C.blue,true);
  text(s,'title_line_1','모션 그래픽을 이용한',95,282,940,110,80,C.white,true);
  text(s,'title_line_2','수업 영상',95,400,790,140,114,C.white,true);
  text(s,'title_line_3','제작하기',95,530,790,140,114,C.white,true);
  text(s,'cover_description','수업 자료 한 장으로 시작하는 AI 영상 제작',100,694,850,60,33,'#D7E5F8');
  text(s,'webinar_date','2026.11.1.(일) 20:00',100,790,830,76,46,C.white,true);
  text(s,'registration','댓글에 ‘노션톡’을 남기면\n참가 링크를 보내드려요',100,894,780,88,29,C.muted);
  note(s,[
    '발화: 오늘은 모션 그래픽을 이용해 수업 영상을 만드는 흐름을 살펴봅니다. 이 자료는 대표 5장 시안입니다.',
    '운영 정보: 일정과 댓글 신청 안내는 사용자 제공 이미지의 문구를 따랐습니다. 종료 시각과 발표자 이름은 미제공 상태입니다.',
    '원본 이미지 전체를 보존하고 장표에서는 하단 인물 영역만 비파괴 크롭했습니다. 제목·일정·푸터는 편집 가능한 텍스트입니다.'
  ],'사용자 제공 codex-clipboard-24232e50-681c-4306-9379-1d4bcf10ef14.png; 사용자 제공 NotionTalk 흰색 로고');
}
// 2. Motion vocabulary translated into a classroom-oriented explanation.
{
  const s=p.slides.add(); common(s,2,'Part 1 모션 그래픽 이해','01 모션의 기본');
  text(s,'title','모션은 보여주는 순서를 설계합니다',80,244,1760,118,76,C.white,true,'center');
  text(s,'subtitle','무엇을 움직일지보다, 어떤 설명을 언제 보여줄지 먼저 정합니다',120,367,1680,65,34,C.muted,false,'center');
  const cols=[
    {x:130,n:'01',title:'등장 시점',desc:'설명에 필요한 순간에\n자료와 문장을 보여줍니다'},
    {x:735,n:'02',title:'유지 시간',desc:'내용을 읽고 생각할\n시간을 확보합니다'},
    {x:1340,n:'03',title:'강조 순서',desc:'핵심어와 변화에\n시선을 모읍니다'},
  ];
  for(const c of cols) {
    text(s,'motion-number-'+c.n,c.n,c.x,510,430,125,106,C.blue,true);
    text(s,'motion-title-'+c.n,c.title,c.x,660,440,90,58,C.white,true);
    text(s,'motion-detail-'+c.n,c.desc,c.x,774,450,115,35,C.muted);
  }
  note(s,[
    '발화: 화면 전체가 계속 움직일 필요는 없습니다. 설명할 때 문장이 들어오고, 읽을 시간을 둔 뒤, 핵심어를 강조하는 순서를 설계합니다.',
    '강사 안내: 이 장은 모션의 시간·순서 개념을 수업 설명에 맞춰 해석한 예시입니다. 효과의 교육적 성과 수치를 주장하지 않습니다.',
    '예상 질문: 효과는 많이 넣을수록 좋나요? 답변 방향: 학습 목표에 필요한 등장·유지·강조부터 정하고 읽을 시간을 확인합니다.'
  ],motionRef+' PDF 20~28쪽(시간·속성·순서와 모션 기준); 수업 적용 문구는 본 시안의 제안');
}
// 3. Editable process, not a simulated software screenshot.
{
  const s=p.slides.add(); common(s,3,'Part 2 수업 영상 제작 흐름','01 자료부터 결과 확인까지');
  text(s,'title','한 장의 자료로 시작하는\n수업 영상 제작 흐름',80,230,1740,220,76,C.white,true);
  const cols=[
    {x:85,n:'01',title:'학습 목표',desc:'설명할 핵심을\n한 문장으로 정리'},
    {x:535,n:'02',title:'장면표',desc:'화면 문구와\n나레이션을 나누기'},
    {x:985,n:'03',title:'모션 요청',desc:'등장 순서와\n강조할 대상을 지정'},
    {x:1435,n:'04',title:'결과 확인',desc:'내용의 정확성과\n읽는 시간을 점검'},
  ];
  for(const c of cols) {
    text(s,'process-number-'+c.n,c.n,c.x,498,390,100,76,C.blue,true);
    text(s,'process-title-'+c.n,c.title,c.x,618,390,90,52,C.white,true);
    text(s,'process-detail-'+c.n,c.desc,c.x,729,390,112,34,C.muted);
  }
  rect(s,'process-summary-rule',85,907,1745,2,C.line);
  text(s,'process_summary','교사가 학습 내용을 정하고, AI와 함께 장면과 움직임을 구체화합니다',85,937,1745,56,33,C.blue);
  note(s,[
    '발화: 먼저 실제로 수업에 쓰는 자료 한 장과 학습 목표를 정합니다. 바로 영상을 요청하기보다 장면표로 화면과 나레이션을 확인합니다.',
    '조작: 실제 제작 도구는 아직 정하지 않았으므로 이 대표 시안에는 특정 서비스의 설치·기능 화면을 넣지 않았습니다.',
    '강사 안내: 학습 목표와 내용의 정확성은 교사가 확인합니다. AI가 만든 초안은 결과를 보며 수정합니다.'
  ],motionRef+' PDF 91~99쪽(브리프·장면표·시안 확인); 4단계 수업 전개는 본 시안의 제안');
}
// 4. Native editable storyboard evidence. All three intervals add up to 20 seconds.
{
  const s=p.slides.add(); common(s,4,'Part 2 수업 영상 제작 흐름','02 장면 구성 예시');
  text(s,'title','20초 수업 영상의 장면 구성',80,240,1760,118,76,C.white,true);
  text(s,'subtitle','질문을 열고, 개념을 설명한 뒤, 학습자의 말로 확인합니다',85,363,1750,62,34,C.muted);
  const scenes=[
    {x:85,time:'0–4초',title:'질문',screen:'왜 그럴까요?',desc:'익숙한 상황이나 질문으로\n설명할 주제를 보여줍니다'},
    {x:685,time:'4–14초',title:'핵심 설명',screen:'핵심 개념 하나',desc:'문장을 차례로 제시하고\n중요한 낱말만 강조합니다'},
    {x:1285,time:'14–20초',title:'확인 질문',screen:'내 말로 설명하기',desc:'짧은 질문으로 마무리하고\n답을 생각할 시간을 둡니다'},
  ];
  for(const c of scenes) {
    text(s,'scene-time-'+c.x,c.time,c.x,455,520,62,37,C.blue,true);
    rect(s,'scene-frame-'+c.x,c.x,540,545,285,C.panel,C.line,1.5);
    text(s,'scene-label-'+c.x,c.title,c.x+30,569,485,50,28,C.muted);
    text(s,'scene-screen-'+c.x,c.screen,c.x+25,676,495,78,46,C.white,true,'center');
    text(s,'scene-description-'+c.x,c.desc,c.x,854,550,108,32,C.muted);
  }
  text(s,'example_caveat','구성 예시입니다. 실제 길이는 학습 내용과 읽는 속도에 맞춰 조정합니다',85,976,1740,38,27,C.blue);
  note(s,[
    '발화: 20초를 예로 들면 질문 4초, 핵심 설명 10초, 확인 6초로 나눌 수 있습니다. 모든 영상을 이 길이에 맞춰야 하는 규칙은 아닙니다.',
    '화면 안내: 세 프레임은 장면 구성용 편집 객체이며 실제 제작 도구의 화면이나 완성 영상 캡처가 아닙니다.',
    '확인: 구간 4+10+6=20초. 실제 나레이션 길이와 수강생의 읽는 속도를 보고 시간을 조정합니다.'
  ],motionRef+' PDF 97~99쪽의 장면표 사전 확인 방식에서 착안; 시간 배분·화면 문구는 본 시안의 예시');
}
// 5. The prompt is native text and supplied separately as a plain-text convenience file.
const prompt = [
  '대상: [학년·수준]',
  '학습 목표: [핵심 개념 한 가지]',
  '자료: [수업 자료 붙여 넣기]',
  '영상: 20초, 16:9',
  '',
  '질문, 핵심 설명, 확인 질문의 3장면으로 구성해 주세요.',
  '장면마다 화면 문구, 나레이션, 등장 순서,',
  '길이를 써 주세요.',
  '제공 자료에 없는 사실은 추가하지 마세요.',
].join('\n');
{
  const s=p.slides.add(); common(s,5,'Part 3 함께 만들어 보기','01 장면표부터 요청하기');
  text(s,'title','첫 영상의 장면표를 요청하는 프롬프트',80,240,1770,110,70,C.white,true);
  text(s,'subtitle','아래 빈칸을 내 수업 자료로 바꾸어 입력합니다',85,361,1700,65,34,C.muted);
  rect(s,'prompt-background',85,465,1150,475,C.panel);
  text(s,'prompt',prompt,125,500,1068,410,32,C.white);
  text(s,'check_heading','결과 확인',1315,485,500,76,46,C.blue,true);
  text(s,'check_1','01  학습 목표가 하나인가요?',1315,597,510,70,35,C.white);
  text(s,'check_2','02  화면 문구를 읽을\n      시간이 있나요?',1315,697,510,112,35,C.white);
  text(s,'check_3','03  원자료와 설명 내용이\n      일치하나요?',1315,835,510,112,35,C.white);
  text(s,'next_step','다음 단계는 장면표를 확인한 뒤 실제 영상을 제작하는 것입니다',85,970,1745,44,29,C.blue);
  note(s,[
    '발화: 대괄호 부분을 자신의 대상과 자료로 바꿔 입력합니다. 바로 영상을 만드는 대신 장면표를 먼저 검토해 보겠습니다.',
    '조작: 선택한 AI 도구의 대화창에 프롬프트와 수업 자료를 넣습니다. 이번 시안은 특정 제품의 실행 성공을 검증한 사용법이 아닙니다.',
    '대기: 참가자가 자신의 학습 목표와 자료를 정리할 시간을 둡니다. 정리하지 못한 경우 강사 예시 자료로 장면표를 읽는 활동에 합류할 수 있습니다.',
    '결과 확인: 학습 목표 한 가지, 화면 문구의 읽는 시간, 원자료와의 일치를 확인합니다. 생성 결과가 예시와 동일할 필요는 없습니다.',
    '프롬프트 원문은 요청 범위에 맞춰 새로 작성한 수업용 제안입니다.'
  ],'본 시안에서 작성한 교육용 프롬프트; '+motionRef+' PDF 91~99쪽의 작업 조건·장면표 확인 흐름 참고');
}

await fs.mkdir(renders,{recursive:true}); await fs.mkdir(output,{recursive:true});
for(const [i,s] of p.slides.items.entries()) {
  const stem=`slide-${String(i+1).padStart(2,'0')}`;
  const png=await p.export({slide:s,format:'png',scale:1.5});
  await fs.writeFile(path.join(renders,stem+'.png'),new Uint8Array(await png.arrayBuffer()));
  const layout=await s.export({format:'layout'});
  await fs.writeFile(path.join(renders,stem+'.layout.json'),await layout.text());
  console.log('Rendered',stem);
}
await fs.writeFile(path.join(build,'roles.json'),JSON.stringify(roleMap,null,2));
await fs.writeFile(path.join(build,'deck.json'),JSON.stringify(p.toProto()));
await fs.writeFile(path.join(output,'장면표_요청_프롬프트.txt'),prompt,'utf8');
const draft=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(draft);
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL_DIR,'container_tools/artifact_tool_utils.mjs')).href);
const name='NotionTalk_모션그래픽_무료웨비나_대표5장_v1';
const finalPath=path.join(output,name+'.pptx');
const result=await finalizePresentation({
  workspaceDir,candidatePath:draft,finalPath,pythonExecutable:PYTHON,
  integrityValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],
  explicitTotalSlideCount:5,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],
  fontPolicy:{basis:'design',families:['Pretendard']},verifyArtifactToolImport:true,
  receiptPath:path.join(build,'validation.json'),
});
console.log('Finalized',JSON.stringify(result));
try {
  const pdf=await p.export({format:'pdf'});
  await fs.writeFile(path.join(output,name+'.pdf'),new Uint8Array(await pdf.arrayBuffer()));
} catch(error) {
  console.warn('Artifact PDF export unavailable; use export-powerpoint.ps1 for the PDF and native verification:',error.message);
}
await fs.writeFile(path.join(build,'font-evidence.json'),JSON.stringify({family:'Pretendard',available:FontLibrary.families.includes('Pretendard'),canvas:[1280,720],render:[1920,1080]}));
console.log('Output',finalPath);
