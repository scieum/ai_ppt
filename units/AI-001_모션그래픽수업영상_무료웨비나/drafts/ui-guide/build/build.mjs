import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
import {Presentation,PresentationFile} from '@oai/artifact-tool';

const build=path.dirname(fileURLToPath(import.meta.url));
const unit=path.resolve(build,'../../..'),root=path.resolve(unit,'../..');
const captures=path.join(unit,'assets/ui-captures/20261027');
const manifest=JSON.parse(await fs.readFile(path.join(captures,'captures.json'),'utf8'));
const out=path.join(root,'output/webinar-ui-guide');
const renders=path.join(unit,'renders/ui-guide');
const skill='C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.22136/skills/presentations';
const python='C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
const {FontLibrary}=req('skia-canvas');
FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const logo=new Uint8Array(await fs.readFile(path.join(root,'assets/branding/notiontalk-white.png')));
const rows=[
 ['codex','01-prompt-submitted','첫 요청 전달',[820,130,545,155],'10초 길이와\n세 문구의 순서,\n원하는 색을 적습니다'],
 ['codex','03-first-result-playing','첫 영상 재생',[607,275,720,448],'재생 버튼을 누르고\n문구가 순서대로\n나오는지 확인합니다\n\n이번 결과는 MP4입니다'],
 ['codex','04-revision-submitted','유지 시간 수정 요청',[820,185,540,110],'같은 대화에서\n질문이 머무는 시간만\n1초 늘려 달라고\n요청합니다'],
 ['codex','06-revised-question-seek','수정된 질문 확인',[610,400,715,450],'재생 위치를 움직여\n질문 장면을 확인합니다\n\n전체 길이도\n11초인지 확인합니다'],
 ['codex','07-personalization-entered','내 수업 질문 입력',[605,910,755,105],'가운데 질문만\n‘두 그림에서\n달라진 점은?’으로\n바꿔 봅니다'],
 ['codex','09-personalized-result','바뀐 문구와 길이 확인',[610,360,715,445],'새 질문이 보이는지\n확인합니다\n\n다른 문구와 순서,\n11초 길이는 유지합니다'],
 ['claude','01-prompt-entered','첫 프롬프트 입력',[620,470,690,178],'새 대화의 입력창에\n같은 요청을 넣고\n보내기 버튼을 누릅니다'],
 ['claude','02-generating','생성 상태 확인',[580,60,770,305],'요청을 보낸 뒤\n생성이 끝날 때까지\n기다립니다\n\n완료 후 실제로\n재생해 봅니다'],
 ['claude','03-first-artifact','아티팩트 재생',[570,190,1250,725],'오른쪽 미리보기에서\n재생·처음부터\n버튼을 사용합니다\n\n이번 결과는 HTML입니다'],
 ['claude','05-revision-entered','같은 대화에서 시간 수정',[12,910,540,115],'첫 결과를 보면서\n질문의 유지 시간만\n1초 늘려 달라고\n요청합니다'],
 ['claude','07-revised-question-playing','11초 아티팩트 확인',[570,190,1250,725],'질문이 더 오래\n머무는지 재생합니다\n\n화면 아래의\n전체 시간도 확인합니다'],
 ['claude','04-export-menu','아티팩트 내보내기 위치',[570,30,270,475],'제목의 메뉴에서\n내보내기를 찾습니다\n\n이번 HTML 결과와\nMP4 파일을 구분합니다'],
];
const p=Presentation.create({slideSize:{width:1280,height:720}}),S=2/3;
const pos=(x,y,w,h)=>({left:x*S,top:y*S,width:w*S,height:h*S});
function text(s,name,value,box,size,color='#FFFFFF',bold=false,align='left'){
 const sh=s.shapes.add({geometry:'textbox',name,position:pos(...box),fill:'none',line:{fill:'none',width:0}});
 sh.text=value;sh.text.style={typeface:'Pretendard',fontSize:size*S,bold,color,alignment:align,verticalAlignment:'top',insets:0,autoFit:'none',wrap:'none',lineSpacing:1.25};return sh;
}
await fs.mkdir(out,{recursive:true});await fs.mkdir(renders,{recursive:true});
const mapping=[];
for(const [i,[app,step,title,crop,body]] of rows.entries()){
 const record=manifest.captures.find(c=>c.app===app&&c.step===step);
 if(!record)throw new Error('Missing real screenshot '+app+'/'+step);
 const s=p.slides.add();s.background.fill='#000000';
 text(s,'part','Part 1  짧은 요청으로 수업 시작 영상 만들기',[90,44,1300,46],30,'#969696');
 text(s,'step',String(i%6+1).padStart(2,'0'),[90,116,115,80],64,'#FF9228',true);
 text(s,'title',(app==='codex'?'Codex':'Claude')+' '+title,[225,116,1410,95],64,'#FFFFFF',true);
 s.images.add({blob:logo,contentType:'image/png',fit:'contain',position:pos(1685,32,164,55),alt:'사용자 제공 NotionTalk 원본 흰색 로고'});
 const [x,y,w,h]=crop,W=record.width,H=record.height;
 const factor=Math.min(1120/w,650/h),iw=w*factor,ih=h*factor;
 s.images.add({blob:new Uint8Array(await fs.readFile(path.join(captures,record.path))),contentType:'image/jpeg',
  crop:{left:x/W,top:y/H,right:1-(x+w)/W,bottom:1-(y+h)/H},fit:'cover',
  position:pos(90+(1120-iw)/2,280+(650-ih)/2,iw,ih),alt:record.caption+'; 원본 캡처의 조작 영역만 확대'});
 text(s,'instruction',body,[1300,350,545,560],40,'#F4F4F4');
 text(s,'scope','2026.10.27 실제 실행 화면',[90,985,900,35],22,'#888888');
 text(s,'footer','© 2026. NotionTalk. All rights reserved.',[960,1035,890,30],20,'#999999',false,'right');
 s.speakerNotes.text=[
  'Source: '+path.join(captures,record.path), 'SHA-256: '+record.sha256,
  '실제 앱 원본 캡처의 일부 영역을 PowerPoint 이미지 크롭으로 확대했습니다. UI 글자·버튼·생성 결과를 재생성하거나 덧그리지 않았습니다.',
  '환경: Windows 데스크톱. Codex 실습 GPT-6.1 Sol Medium, Claude Desktop 3.6556.2.0의 Opus 5.5 높음. 확인일 2026-10-27. 계정·버전에 따라 결과와 화면은 달라질 수 있습니다.',
  app==='codex'?'첫 요청·시간 수정은 사용자가 허용한 별도 실습 채팅 도구로 전달했습니다. 개인화 요청은 실제 인앱 입력창에서 입력·제출했습니다.':'실제 Claude 데스크톱 새 대화에서 입력·제출·수정했습니다. HTML 아티팩트의 첫 결과는 10초, 수정 결과는 11초입니다.',
  step==='04-export-menu'?'내보내기 메뉴의 위치만 확인했습니다. 이 캡처는 HTML 다운로드 완료나 MP4 내보내기 성공의 증거가 아닙니다.':'',
  '교수 진행: '+body.replaceAll('\n',' '),
  '이 장표는 파트 1의 조작별 보조 자료입니다. 전체 웨비나 승인·G10 권리 검토 완료를 의미하지 않습니다.'
 ].filter(Boolean).join('\n');
 mapping.push({slide:i+1,app,step,title,capture:record.path,sha256:record.sha256,crop_pixels:crop});
 const stem=String(i+1).padStart(2,'0');
 const png=await p.export({slide:s,format:'png',scale:1.5});await fs.writeFile(path.join(renders,stem+'.png'),new Uint8Array(await png.arrayBuffer()));
 console.log('Rendered',i+1);
}
await fs.writeFile(path.join(build,'slide-map.json'),JSON.stringify(mapping,null,2));
const candidatePath=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidatePath);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const result=await finalizePresentation({workspaceDir:root,candidatePath,finalPath:path.join(out,'NotionTalk_Part1_실제앱_단계별캡처_v1.pptx'),pythonExecutable:python,
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],
 explicitTotalSlideCount:rows.length,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:['Pretendard']},verifyArtifactToolImport:true,receiptPath:path.join(build,'validation.json')});
console.log('Finalized',JSON.stringify(result));
