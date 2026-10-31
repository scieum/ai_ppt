import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');
const req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const source=path.join(R,'output/webinar-part01-added/NotionTalk_대표5장유지_Part0_Part1추가_9장_v2.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load(source)),base=[...p.slides.items],created=[];
const text=await fs.readFile(path.join(U,'part-1.md'),'utf8');
const prompts=[...text.matchAll(/```text\s*\n([\s\S]*?)\n```/g)].map(m=>m[1]);
if(prompts.length!==6)throw Error('Expected six actual prompt blocks in revised Part 1');
const S=2/3,P=(x,y,w,h)=>({left:x*S,top:y*S,width:w*S,height:h*S});
function edit(s,name,value){const x=s.shapes.items.find(x=>x.name===name);if(!x)throw Error('Missing '+name);x.text.replace(String(x.text),value);}
function edits(s,values){for(const [k,v]of Object.entries(values))edit(s,k,v);}
const changes={};
function original(n,values,notes){edits(base[n-1],values);changes[n]={values,notes};base[n-1].speakerNotes.text=notes;}
const common='\n제작 상태: 이 파일은 강의 설명·요청·자체 모식도를 반영한 장표입니다. 이번에 새 앱 실행·영상 생성·MP4 내보내기를 수행한 증거가 아닙니다. HTML 미리보기와 MP4 파일을 구분합니다. 실제 앱 캡처와 수정 결과는 별도로 확보합니다.\n디자인: 대표 5장 v5의 배치·색·서체·로고·푸터를 유지했습니다. 문구는 이번 세 사례에 맞게 교체했습니다. G10 검토 상태와 실제 승인 기록은 변경하지 않았습니다.\nSource: units/AI-001_모션그래픽수업영상_무료웨비나/plan.md; part-1.md; lesson.md (2026-10-27 자막·설명란 분석).';
original(2,{subtitle:'세 가지 초안에서 시작해\n장면 계획과 외부 제작까지 이어갑니다',description_0:'문장·URL·과학사 초안',description_1:'참고할 요소와 이유',description_2:'읽는 시간·강조·순서',description_3:'네 장면 45초 계획',description_4:'필요한 소재 한 장면',tag_1:'참고 범위',tag_3:'장면표',summary_text:'첫 결과를 보고 필요한 조건을 하나씩 더해요'},'발화: 단순 프롬프트, 레퍼런스, 모션 지식, Markdown 장면표, 외부 커넥터의 다섯 단계입니다. Part 0 5분, Part 1 18분, Part 2 12분, Part 3 12분, Part 4 16분, Part 5 12분, 정리·질문 15분으로 전체 90분 제안입니다. 표지 도입은 Part 0 시간에 포함합니다. 이번 15장은 대표본과 Part 1을 확장한 구성이고 전체 42장 완성본이 아닙니다.'+common);
original(4,{subtitle:'필수 문구·날짜와 마지막 안내를 읽는 시간을 확인합니다',tool_caption:'자체 타이포그래피 예시',prompt_label:'다음에 고칠 조건',prompt_body:'전체 20초를 유지하고,\n마지막 안내를 4초 동안\n읽을 수 있게 조정해 줘.'},'발화: 입력은 홍보 문장과 행사 정보입니다. 첫 결과에서 필수 한글 문구, 2026년 11월 1일 일요일 저녁 8시, 댓글 안내를 확인합니다. 4초는 비교용 예시 값입니다. 현재 결과가 충분히 읽히면 실제로 부족한 다른 조건을 고릅니다.\n조작: 다음 장표의 시작 요청을 입력하고 실제 재생을 확인합니다.\n대기: 생성이 지연되면 같은 조건의 사전 결과임을 표시하고 관찰을 계속합니다. Part 1에서는 수정 문장 한 개를 남기고 Part 3에서 전후 비교합니다.\n시작 요청 전문:\n'+prompts[0]+'\n보완 요청:\n'+prompts[1]+common);
original(5,{subtitle:'페이지 접근 여부와 원문·영상 문구의 대응을 확인합니다',tool_caption:'내용의 근거와 영상의 관계',prompt_label:'원문과 영상 대조하기',prompt_body:'사용한 원문 근거와\n영상 문구를 짝지어 줘.\n없는 주장은 제거해 줘.'},'발화: 실습 URL은 제작자가 고른 https://www.notion.com/ko/product/docs 입니다. 기존 공식 본문 확인 기록과 현재 AI가 URL을 읽은 성공은 별도입니다. 원문에 없는 기능이나 효과를 덧붙였는지 확인합니다.\n조작: 시작 요청 후 원문 근거와 영상 문구 한 쌍을 실제 본문과 대조합니다.\n대기: URL 접근이 안 되면 강사가 확인한 본문을 제공하고 입력 방식을 기록합니다. 왼쪽은 실제 사이트 UI가 아닌 자체 도식입니다.\n시작 요청:\n'+prompts[2]+'\n확인 요청:\n'+prompts[3]+'\nSource: https://www.notion.com/ko/product/docs (기존 본문 확인일 2026-10-27, 이번 작업에서 새 접근 성공으로 표시하지 않음).'+common);
original(6,{subtitle:'모형의 차이·바뀐 이유와 설명의 근거를 확인합니다',prompt_label:'설명과 움직임 연결하기',prompt_body:'모형마다 바뀐 설명을\n문장과 동작으로 연결해 줘.\n근거 없는 연출은 빼 줘.'},'발화: 인물 이름이 바뀌는 영상보다 모형의 설명이 왜 달라졌는지 이해하는 것이 목적입니다. 관찰 결과와 해석을 구분하고 새 주장은 자료에서 확인합니다.\n조작: 초안의 근거가 필요한 주장 하나를 표시합니다. 모식도는 실제 크기 비율·관측 궤적이 아니며 보어 모형을 현대 원자모형의 최종 형태로 설명하지 않습니다.\n시작 요청:\n'+prompts[4]+'\n후속 요청:\n'+prompts[5]+'\nSource: https://history.aip.org/exhibits/rutherford/sections/alpha-particles-atom.html ; https://www.edu.gov.mb.ca/ks4/cur/science/found/s1/appen2.pdf Appendix 2.3 A27–A29 (기존 대조 기록, 새 생성 주장 재확인 필요).'+common);
original(7,{subtitle:'같은 결과에서 읽는 시간·강조·순서를 하나씩 바꿉니다',description_0:'마지막 안내 4초',tag_0:'문구·일정',description_1:'핵심어 하나 강조',description_2:'질문 다음에 설명',description_3:'관찰 다음에 해석',description_4:'정리 문구 유지',summary_text:'한 조건을 고치고 전후 결과를 재생해요'},'발화: A의 마지막 안내를 4초 유지하면서 전체 20초는 맞춰 봅니다. 문구와 색은 유지하고 시간만 조정해야 차이를 비교할 수 있습니다. 소리를 더하더라도 읽는 시간을 먼저 확보합니다.\n조작: 같은 입력의 전후 결과를 재생합니다. 실제 수정 실행 전에는 완료로 표시하지 않습니다.'+common);
original(8,{subtitle:'원자모형 영상의 목적·규칙·장면을 나누어 적습니다',start_label:'원자모형 변천',cell_0_1:'대상·학습 목표\n원자료·확인한 사실',cell_0_2:'모형의 차이와\n바뀐 이유 설명하기',cell_1_1:'읽는 시간·색\n강조·등장·소리',cell_1_2:'주황 핵심어\n정리 문구 읽는 시간',cell_2_1:'네 장면의 시간\n문구·동작·근거',cell_2_2:'질문 5초·톰슨 12초\n러더퍼드 13초·보어와 정리 15초'},'발화: LESSON_BRIEF.md에는 대상·학습 목표·확인한 사실과 원자료를, VISUAL_RULES.md에는 읽는 시간·색·강조·등장·소리를, SCENE_PLAN.md에는 시간·문구·동작·소재·근거 위치·확인 상태를 적습니다.\n조작: 세 파일을 실제 작업에 첨부·참조하고 장면표 한 행의 시간을 바꾼 뒤 총길이를 맞춰 재생합니다.\n설계 초안: 질문 0–5초, 톰슨 5–17초, 러더퍼드 17–30초, 보어와 정리 30–45초. 5+12+13+15=45초입니다. 사실 검토·실제 생성 완료를 뜻하지 않습니다.'+common);
original(9,{section_heading:'설명에 필요한 장면 만들기',subtitle:'장면 소재와 정확한 글자·날짜·로고를 따로 준비합니다',prompt_body:'필요한 장면 소재를\n짧은 영상으로 만들어 줘.\n글자와 로고는 따로 넣을게.'},'발화: 장면표에서 외부 생성 소재가 필요한 부분 하나만 고릅니다. 계정·연결·지원 입력·길이·비율을 확인하고 한 번 요청합니다. 접수·대기·완료와 실제 재생 결과를 구분합니다. 정확한 한글·날짜·브랜드 로고는 편집 가능한 요소로 합성합니다.\n조작: 실제 생성 소재를 원래 영상에 연결하고 의미·길이·비율·권리를 검토합니다.\n대기: 힉스필드 계정이 없는 참가자는 시연을 관찰합니다. 이번 장표 개정에서 새 외부 생성은 실행하지 않았습니다.'+common);
function added(key,template){const s=base[template-1].duplicate();created.push({key,template,slide:s});return s;}
{
const s=added('types',2);edits(s,{part_label:'Part 1  모션 그래픽의 활용',section_number:'00',section_heading:'수업에서 쓸 수 있는 영상',title:'모션 그래픽으로 무엇을 만들까요?',subtitle:'글자·도형·자료의 움직임으로\n전달할 내용을 더 잘 보이게 합니다',summary_label:'수업 적용',summary_text:'내 수업에 필요한 영상 하나를 떠올려요'});
const rows=[['타이포그래피','문장과 핵심어 강조','글자'],['인포그래픽','수치와 관계 설명','정보'],['서비스 소개','기능과 쓰임 소개','URL'],['과학사','모형과 설명의 변화','지식'],['절차 안내','단계별 행동 안내','캐릭터 설명']];
for(let i=0;i<5;i++)edits(s,{['heading_'+i]:rows[i][0],['description_'+i]:rows[i][1],['tag_'+i]:rows[i][2]});
s.speakerNotes.text='발화: 타이포그래피·인포그래픽·서비스 소개·타임라인·절차 안내·캐릭터 설명처럼 여러 영상을 만들 수 있습니다. 과학사도 설명 주제의 한 예입니다. 이 목록은 서로 배타적인 장르 분류가 아니라 수업 활용 범위를 보여 줍니다.\n대기: 2분. 자기 수업의 활용 상황 한 가지를 떠올립니다.'+common;
}
{
const s=added('compare',8);edits(s,{part_label:'Part 1  오늘 만들어 볼 사례',section_number:'00',section_heading:'입력과 목적 비교',title:'세 가지 입력으로 시작합니다',subtitle:'하나를 골라 첫 요청을 보내고 다른 사례도 함께 살펴봅니다',start_label:'하나 선택',table_header_0:'사례',table_header_1:'시작 입력',table_header_2:'첫 결과의 확인 기준',cell_0_0:'타이포그래피',cell_0_1:'홍보 문장\n행사 정보',cell_0_2:'필수 문구·일정\n마지막 안내를 읽는 시간',cell_1_0:'웹사이트 소개',cell_1_1:'실제 URL\n확인한 본문',cell_1_2:'실제 본문 접근\n원문과 영상 문구의 대응',cell_2_0:'원자모형 변천',cell_2_1:'설명 주제\n근거 자료',cell_2_2:'모형의 차이·바뀐 이유\n주요 주장의 근거'});
s.speakerNotes.text='발화: A는 표현 형식, B는 원자료 입력 방식, C는 설명 주제에서 출발합니다. 세 사례는 같은 기준의 세 장르가 아닙니다.\n조작: 참가자는 하나를 선택해 시작 요청을 먼저 전송할 수 있습니다.\n대기: 1분. 전체 Part 1 18분 동안 세 영상을 모두 완성하도록 요구하지 않습니다.'+common;
}
function bodyText(s,name,value,box,size,color='#000000',bold=false){const sh=s.shapes.add({geometry:'textbox',name,position:P(...box),fill:'none',line:{fill:'none',width:0}});sh.text=value;sh.text.style={typeface:'Pretendard',fontSize:size*S,color,bold,alignment:'left',verticalAlignment:'top',insets:0,wrap:'word',autoFit:'none',lineSpacing:1.15};return sh;}
for(const [key,template,prompt,heading,title,sub]of [
 ['prompt-a',4,prompts[0],'노션톡 홍보 타이포그래피의 첫 요청','문장과 행사 정보를 입력합니다','20초 초안에서 문구·일정·읽는 시간을 확인합니다'],
 ['prompt-b',5,prompts[2],'웹사이트 소개 영상의 첫 요청','공식 페이지의 내용을 입력합니다','URL을 읽지 못하면 확인한 본문으로 전환합니다'],
 ['prompt-c',6,prompts[4],'원자모형 설명 영상의 첫 요청','주제와 확인할 사실을 입력합니다','45초 설명 초안에서 모형의 차이와 근거를 확인합니다']]){
 const s=added(key,template);edits(s,{section_heading:heading,title,subtitle:sub});
 const keep=new Set(['part_label','section_number','section_heading','title','subtitle','copyright_footer']);
 for(const x of [...s.shapes.items])if(!keep.has(x.name))x.delete();
 s.shapes.add({geometry:'rect',name:'content-clear',position:P(250,520,1450,470),fill:'#000000',line:{fill:'none',width:0}});
 s.shapes.add({geometry:'roundRect',name:'full-prompt-panel',position:P(300,540,1320,400),fill:'#FFFFFF',line:{fill:'none',width:0},borderRadius:26});
 bodyText(s,'full-prompt-body',prompt,[365,582,1190,320],32);
 s.speakerNotes.text='발화: 이 시작 요청 전문은 개정한 Part 1에서 가져왔습니다. 긴 지시서나 전문 모션 용어 대신 목적·길이·필수 조건으로 시작합니다.\n조작: 아래 요청 전문을 복사해 실제 앱에서 입력합니다. 형식과 재생 성공은 실제 결과로 확인합니다.\n대기: 생성이 오래 걸리면 같은 입력의 사전 결과임을 표시하고 관찰합니다.\n시작 요청 전문:\n'+prompt+common;
}
{
const s=added('reflection',2);edits(s,{part_label:'Part 1  첫 결과 돌아보기',section_number:'04',section_heading:'내 수업에 적용하기',title:'고칠 조건 하나를 남깁니다',subtitle:'선택한 사례의 첫 결과를 보고\n다음 요청을 한 문장으로 적습니다',summary_label:'다음 단계',summary_text:'대상과 시간·강조·순서 중 필요한 조건을 적어요'});
const rows=[['사례','A·B·C 중 하나','목적'],['입력','문장·URL·주제','원자료'],['관찰','재생·문구·근거','확인'],['수정','바꿀 조건 한 가지','요청'],['저장','파일 또는 작업 링크','다음 작업']];
for(let i=0;i<5;i++)edits(s,{['heading_'+i]:rows[i][0],['description_'+i]:rows[i][1],['tag_'+i]:rows[i][2]});
s.speakerNotes.text='발화: 내 결과 또는 관찰에서 바꿀 대상과 조건을 한 문장으로 적습니다. A는 읽는 시간, B는 원문에 없는 주장, C는 근거 없는 설명 등을 확인합니다.\n조작: 결과 또는 작업 링크와 수정 요청을 저장합니다.\n대기: 2분. 생성 지연·접근 불가 시 관찰 기록으로 합류합니다. Part 2는 참고 요소와 이유, Part 3은 구체적인 수정, Part 4는 장면표, Part 5는 필요한 소재 한 장면으로 이어집니다.'+common;
}
await fs.writeFile(path.join(B,'edits.json'),JSON.stringify(changes,null,2));
const mapping=created.map(x=>({key:x.key,template:x.template,export_slide:p.slides.items.findIndex(s=>s.id===x.slide.id)+1}));
await fs.writeFile(path.join(B,'additions.json'),JSON.stringify(mapping,null,2));
await fs.writeFile(path.join(B,'inspect-before.ndjson'),(await p.inspect({kind:'slide,textbox,shape,image',maxChars:20000})).ndjson??'');
await(await PresentationFile.exportPptx(p)).save(path.join(B,'edited-roundtrip.pptx'));
console.log(JSON.stringify({editedOriginals:Object.keys(changes),newSlides:mapping,total:p.slides.items.length}));
