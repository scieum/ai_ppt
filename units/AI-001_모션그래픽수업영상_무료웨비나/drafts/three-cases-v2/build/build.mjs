import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const build=path.dirname(fileURLToPath(import.meta.url));
const unit=path.resolve(build,'../../..'),root=path.resolve(unit,'../..');
const out=path.join(root,'output/webinar-three-cases-v2');
const renders=path.join(unit,'renders/three-cases-v2');
const assets=path.join(unit,'assets/three-cases-v2');
const skill='C:/Users/User/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.22136/skills/presentations';
const python='C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
const {FontLibrary}=req('skia-canvas');
FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const logo=new Uint8Array(await fs.readFile(path.join(root,'assets/branding/notiontalk-white.png')));
const rows=[
 {stem:'01-typography',number:'01',section:'텍스트로 만드는 타이포그래피',title:'홍보 문장을 움직이는 영상으로',subtitle:'노션톡 무료 웨비나를 소개하는 짧은 영상부터 만들어 봐요',label:'문장으로 요청하기',
 prompt:'‘수업 자료가 영상이 되는 순간’으로\n시작하는 노션톡 웨비나 홍보 영상을\n20초로 만들어 줘. 검정 바탕에\n주황색으로 핵심어를 강조해 줘.',duration:20,
 caption:'문장의 등장과 핵심어의 크기 변화',sources:[],
 notes:'문구와 길이만으로 시작한다. 전체 예제 영상에는 제공 포스터의 2026년 11월 1일 일요일 저녁 8시와 댓글 안내를 반영했다. 이 샘플은 장면 방향을 보여 주기 위해 코드로 직접 제작한 무음 영상이며, 앱에 위 프롬프트를 넣어 얻은 결과로 제시하지 않는다.'},
 {stem:'02-website',number:'02',section:'웹사이트 내용으로 만드는 소개 영상',title:'링크 하나로 사이트 소개 영상 만들기',subtitle:'페이지에서 읽은 내용을 핵심 메시지와 장면으로 바꿔요',label:'링크를 넣어 요청하기',
 prompt:'이 페이지를 읽고 Notion 문서를\n소개하는 30초 영상을 만들어 줘.\n콘텐츠 블록·목차·공동 편집을\n도형과 글자로 설명해 줘.',duration:30,
 caption:'콘텐츠 블록·목차·공동 편집을 장면으로',sources:['https://www.notion.com/ko/product/docs'],
 notes:'실제 공식 웹페이지 본문을 2026-10-27 열람했다. 콘텐츠 유형(텍스트·이미지/영상·코드), 목차, 공동 편집·댓글을 확인했다. 사이트의 사진·로고·UI와 원문 표현은 복사하지 않고 자체 글·도형으로 구성했다. 이 사례의 실습용 URL은 제작자가 선정했다. 사용자가 특정 URL까지 지정한 것은 아니다.'},
 {stem:'03-atomic-history',number:'03',section:'역사 지식을 설명하는 영상',title:'원자모형의 변화를 영상으로 설명하기',subtitle:'톰슨·러더퍼드·보어의 모형을 비교하며 변화의 이유를 전달해요',label:'주제로 요청하기',
 prompt:'톰슨·러더퍼드·보어의 원자모형이\n어떻게 달라졌는지 45초 영상으로\n설명해 줘. 모형을 도형으로 보여 주고\n연도와 설명의 출처도 적어 줘.',duration:45,
 caption:'새로운 증거와 설명에 따라 달라지는 모형',sources:['https://history.aip.org/exhibits/rutherford/sections/alpha-particles-atom.html','https://www.edu.gov.mb.ca/ks4/cur/science/found/s1/appen2.pdf'],
 notes:'AIP의 원자핵 발견사에서 톰슨의 분산된 양전하 모형과 러더퍼드의 1911년 집중된 중심 설명을 확인했다. Manitoba Education Senior 1 Science Appendix 2.3 A27~A29에서 각 모형과 보어 1913년의 정해진 궤도·에너지 설명을 교차 확인했다. 간단한 모식도는 실제 크기 비율·전자의 관측 경로가 아니며 보어 모형을 현대의 최종 모형으로 가르치지 않는다.'},
];
const p=Presentation.create({slideSize:{width:1280,height:720}}),S=2/3;
const pos=(x,y,w,h)=>({left:x*S,top:y*S,width:w*S,height:h*S});
function text(s,name,value,box,size,color='#FFFFFF',bold=false,align='left'){
 const sh=s.shapes.add({geometry:'textbox',name,position:pos(...box),fill:'none',line:{fill:'none',width:0}});
 sh.text=value;sh.text.style={typeface:'Pretendard',fontSize:size*S,bold,color,alignment:align,verticalAlignment:'top',insets:0,autoFit:'none',wrap:'none',lineSpacing:1.25};return sh;
}
await fs.mkdir(out,{recursive:true});await fs.mkdir(renders,{recursive:true});
for(const [i,r] of rows.entries()){
 const s=p.slides.add();s.background.fill='#000000';
 text(s,'part','Part 1',[90,89,1200,36],24,'#FF9228',true);
 text(s,'section-number',r.number,[90,131,65,60],44,'#FF9228',true);
 text(s,'section',r.section,[162,131,1250,60],44,'#FFFFFF',true);
 s.images.add({blob:logo,contentType:'image/png',fit:'contain',position:pos(1480,68,346,100),alt:'사용자 제공 NotionTalk 원본 흰색 로고'});
 text(s,'title',r.title,[280,299,1360,90],64,'#FFFFFF',true,'center');
 text(s,'subtitle',r.subtitle,[220,404,1480,55],34,'#FFFFFF',false,'center');
 // The reference's lower half has an example on the left and a white prompt
 // box on the right. These are rebuilt as native objects, not PDF pixels.
 text(s,'example-label','예제 영상 · '+r.duration+'초',[395,530,500,32],23,'#FF9228',true);
 s.shapes.add({geometry:'rect',name:'example-outline',position:pos(393,571,430,244),fill:'#111111',line:{fill:'#363636',width:1}});
 s.images.add({blob:new Uint8Array(await fs.readFile(path.join(assets,r.stem+'.png'))),contentType:'image/png',fit:'contain',position:pos(395,573,426,240),alt:r.caption+'; 로컬에서 직접 제작한 예제 영상의 프레임'});
 text(s,'caption',r.caption,[300,841,620,55],22,'#AAAAAA',false,'center');
 s.shapes.add({geometry:'roundRect',name:'prompt-card',position:pos(940,562,585,314),fill:'#FFFFFF',line:{fill:'none',width:0},borderRadius:42*S});
 text(s,'prompt-label',r.label,[1010,601,460,38],28,'#888888',true);
 if(r.number==='02'){
   text(s,'source-url','notion.com/ko/product/docs',[1010,644,460,34],26,'#555555',false);
   text(s,'prompt',r.prompt,[1010,689,460,167],30,'#000000',true);
 }else text(s,'prompt',r.prompt,[1010,654,460,200],30,'#000000',true);
 text(s,'footer','© 2026. NotionTalk. All rights reserved.',[1080,1030,760,30],20,'#999999',false,'right');
 s.speakerNotes.text=[
  '대표 시안 v2. Part 1 세 예제 방향은 사용자가 2026-10-27 명시적으로 선택했다. 디자인 승인·G10 승인과 구분한다.',
  '기능적 구조 참조: R05(초보자 3주 챌린지 2주차) PDF 31쪽. 검정 바탕, 상단 Part/번호/소주제, 중앙 제목과 부제, 하단 좌측 예시와 우측 흰 요청 박스. PDF 추출 배경·도형·이미지는 미사용. 제목 박스는 새 한국어 문구에 맞춰 좌우 여유를 확대했다. 글꼴은 익명 Type3 원문을 대신한 Pretendard이며 동일 폰트라고 주장하지 않는다.',
  '영상 파일: '+r.stem+'.mp4; '+r.duration+'초; 1280x720; 24fps; 무음. PPT에는 정지 프레임을 넣고 영상은 별도 동봉했다. 이 장표는 실제 앱의 새 실행 캡처가 아니다.',
  r.notes,...r.sources.map(u=>'내용 근거: '+u),
  '프롬프트: '+(r.number==='02'?'https://www.notion.com/ko/product/docs\n':'')+r.prompt.replaceAll('\n',' '),
  'G10: 이용 범위·시각 구성·글꼴·출처 표기 검토 미완료. 외부 배포 승인본으로 표시하지 않는다.'
 ].join('\n');
 const png=await p.export({slide:s,format:'png',scale:1.5});await fs.writeFile(path.join(renders,String(i+1).padStart(2,'0')+'.png'),new Uint8Array(await png.arrayBuffer()));
 console.log('Rendered',i+1);
}
const capDir=path.join(assets,'claude');
const capManifest=JSON.parse(await fs.readFile(path.join(capDir,'captures.json'),'utf8'));
const actualPrompt='‘수업 자료가 영상이 되는 순간’으로 시작하는\n노션톡 무료 웨비나 홍보 타이포그래피 영상을\n20초로 만들어 줘.\n\n글자가 차례로 이어지면서 핵심어의 크기와 위치가\n바뀌게 해 줘. 검정 바탕에 주황색 포인트를 쓰고,\n마지막에는 ‘2026년 11월 1일 일요일 저녁 8시’와\n‘댓글에 노션톡을 남겨 주세요’를 넣어 줘.\n바로 재생할 수 있는 아티팩트로 보여 줘.';
for(const [j,step,title] of [[4,'03-artifact-result','이 요청으로 홍보 영상을 만들어요'],[5,'05-artifact-seek','완성된 영상의 움직임을 확인해요']]){
 const record=capManifest.find(c=>c.step===step);if(!record)throw Error('Missing actual new capture '+step);
 const s=p.slides.add();s.background.fill='#000000';
 text(s,'part','Part 1',[90,89,1200,36],24,'#FF9228',true);
 text(s,'section-number','01',[90,131,65,60],44,'#FF9228',true);
 text(s,'section','텍스트로 만드는 타이포그래피',[162,131,1250,60],44,'#FFFFFF',true);
 s.images.add({blob:logo,contentType:'image/png',fit:'contain',position:pos(1480,68,346,100),alt:'사용자 제공 NotionTalk 원본 로고'});
 text(s,'title',title,[240,299,1440,90],64,'#FFFFFF',true,'center');
 if(j===4){
  s.shapes.add({geometry:'roundRect',name:'full-prompt-card',position:pos(134,480,1000,400),fill:'#202020',line:{fill:'none',width:0},borderRadius:22*S});
  text(s,'actual-prompt',actualPrompt,[174,516,920,340],26,'#FFFFFF',true);
  s.images.add({blob:new Uint8Array(await fs.readFile(path.join(capDir,record.file))),contentType:'image/jpeg',fit:'contain',position:pos(1168,480,640,322),alt:'실제 Claude Desktop에서 이 요청으로 생성한 홍보 아티팩트. 대화와 결과를 함께 보존한 전체 앱 캡처 원본.'});
  text(s,'capture-caption','이 요청으로 생성된 아티팩트',[1168,825,640,45],28,'#FFFFFF',true,'center');
 }else{
  s.images.add({blob:new Uint8Array(await fs.readFile(path.join(capDir,record.file))),contentType:'image/jpeg',fit:'contain',position:pos(364,420,1192,600),alt:'실제 Claude Desktop 대화·아티팩트·재생 컨트롤. 20초 중 3초 지점에서 핵심어 영상이가 커진 화면.'});
 }
 text(s,'footer','© 2026. NotionTalk. All rights reserved.',[1080,1030,760,30],20,'#999999',false,'right');
 s.speakerNotes.text=[
  '실제 Claude Desktop Windows 캡처: '+path.join(capDir,record.file),'SHA-256: '+record.sha256,'확인일: '+record.captured_at,
  '대화: https://claude.ai/chat/13929648-6e5f-432b-abdc-0ff7440bb057',
  '아티팩트: https://claude.ai/code/artifact/f98908a3-0dbc-4452-bbc8-e1ba05092b57',
  '모델 표시: Opus 5.5 높음. 계정·앱 버전에 따라 화면과 결과는 달라질 수 있다.',
  j===4?'기능적 배치 참조: R03 PDF 31쪽. 왼쪽에 읽을 수 있는 실제 전체 요청, 오른쪽에 편집되지 않은 전체 앱 결과 캡처. 문구와 사례는 새로 작성. 입력 전 캡처도 별도 원본으로 보존.':'기능적 배치 참조: R03 PDF 35쪽. 중앙 제목 아래 큰 결과 화면. 앱 종횡비를 유지하기 위해 원본 참조보다 좁고 높은 캡처를 사용. 대화와 결과·시간 컨트롤이 함께 보임.',
  '실제 요청: '+record.prompt,
  'HTML 아티팩트의 자동 재생·처음부터·3초 지점 이동을 실제 확인했다. 이 캡처는 MP4 내보내기 성공의 증거가 아니다. 별도 동봉 MP4는 로컬 코드 예제이며 이 아티팩트를 녹화한 파일이 아니다.',
  '입력·UI·결과 픽셀을 재생성하지 않았다. G10 권리 검토 및 사용자 디자인 확인은 미완료.'
 ].join('\n');
 const png=await p.export({slide:s,format:'png',scale:1.5});await fs.writeFile(path.join(renders,String(j).padStart(2,'0')+'.png'),new Uint8Array(await png.arrayBuffer()));
 console.log('Rendered',j);
}
await fs.writeFile(path.join(build,'slides.json'),JSON.stringify(rows,null,2));
const candidatePath=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidatePath);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
textSafe(await finalizePresentation({workspaceDir:root,candidatePath,finalPath:path.join(out,'NotionTalk_Part1_예제와실제시연_v4.pptx'),pythonExecutable:python,
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:5,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:['Pretendard']},verifyArtifactToolImport:true,receiptPath:path.join(build,'validation-v4.json')}));
function textSafe(r){console.log('Finalized',JSON.stringify(r));}
