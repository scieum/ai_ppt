import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';import{Presentation,PresentationFile}from'@oai/artifact-tool';
import{C,text,shape}from'../../assets/layout-library-20261028/recipes/components.mjs';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..');
const p=Presentation.create({slideSize:{width:1280,height:720}}),spec=[];
const brand=new Uint8Array(await fs.readFile(path.join(R,'assets/branding/notiontalk-white.png')));
function txt(s,n,t,x,y,w,h=40,size=23,color=C.white,bold=false,align='left'){return text(s,n,t,x,y,w,h,size,color,bold,align);}
function page(key,before,title,sub,notes){const s=p.slides.add();s.background.fill=C.bg;s.images.add({blob:brand,contentType:'image/png',fit:'contain',position:{left:1010,top:58,width:190,height:55}});
 txt(s,'part','Part 4  마무리',60,55,800,27,17,C.muted,true);txt(s,'group-number','02',60,91,45,36,28,C.orange,true);txt(s,'group','후속 활동 안내',107,91,850,36,28,C.white,true);
 txt(s,'title',title,110,190,1060,64,38,C.white,true,'center');txt(s,'subtitle',sub,130,266,1020,42,23,C.muted,false,'center');
 txt(s,'copyright','© 2026. NotionTalk. All rights reserved.',800,682,420,22,12,C.muted,false,'right');
 spec.push({key,replace:null,before,title,notes});return s;}
function action(s,n,heading,sub,y){txt(s,'action-'+n,heading,805,y,360,38,26,C.white,true);txt(s,'action-sub-'+n,sub,805,y+42,360,32,20,C.muted);}
{
 const s=page('cycle1',42,'1차 사이클: 수업에 쓸 영상 만들기','11/2(월) ~ 11/8(일) · 이번 웨비나에서 배운 내용 적용',
 '사용자가 정한 1차 활동은 이번 웨비나 내용을 적용해 수업에서 활용할 만한 영상을 제작하는 것이다. 11월2일~8일에 진행한다. 주제는 자신의 수업에서 보여 주고 싶은 내용으로 선택한다. 수업 도입, 개념 설명, 내용 정리는 선택 가능한 예시이며 필수 유형을 정하지 않는다. 영상 길이·제출 플랫폼·마감 시각·심사 기준은 아직 정해지지 않았으므로 안내하지 않는다. 결과물은 수업에 활용할 영상이다. 이 장표는 기존 L19 과제·다음 행동 레이아웃의 큰 과제 영역과 오른쪽 짧은 설명 구조를 따랐다. 전체 41장 및 취소된 v23 내용은 변경하지 않는다.');
 shape(s,'task-panel',150,345,585,277,C.card,'roundRect');
 txt(s,'task-kicker','이번 주 활동',180,366,525,33,21,C.orange,true);
 txt(s,'task-title','내 수업에서\n보여 주고 싶은 장면',180,416,525,94,35,C.white,true);
 txt(s,'task-desc','웨비나에서 배운 움직임을\n내 수업 주제에 적용합니다',180,536,525,62,24,C.muted);
 txt(s,'right-heading','이렇게 진행해요',805,350,350,38,25,C.orange,true);
 action(s,1,'수업 주제 정하기','도입·개념 설명·내용 정리 등',405);
 action(s,2,'배운 모션 적용하기','유형과 효과를 골라 영상으로 표현',485);
 action(s,3,'수업용 영상으로 완성하기','실제 수업에서 보여 줄 장면 만들기',565);
 txt(s,'takeaway','완성할 것: 수업에 활용할 영상',150,642,980,34,22,C.orange,true,'center');
}
{
 const s=page('cycle2',43,'2차 사이클: 기준 문서로 일관성 유지하기','11/9(월) ~ 11/15(일) · 추가 자료를 활용한 모션그래픽 제작',
 '사용자가 정한 2차 활동은 추가 자료를 제공하고 motion.md, video.md 등을 작성해 일관성을 유지하면서 토큰을 아끼는 모션그래픽을 제작하는 것이다. 11월9일~15일에 진행한다. 추가 자료는 제공 예정이며 이미 배포했다고 표현하지 않는다. motion.md는 등장·전환·속도·간격 같은 움직임 기준, video.md는 화면 비율·배경·전체 영상 톤 같은 영상 전체 기준을 정리하는 작업용 Markdown 문서로 설명한다. 앞선 storyline.md는 내용과 장면 순서, design.md는 색·글꼴·배치 기준으로 유지하며 video.md가 이들을 대체하거나 파일명만으로 자동 실행된다고 설명하지 않는다. 기준과 대표 장면을 먼저 확인하고 확정 기준을 다음 장면에 재사용해 반복 생성 범위를 줄이는 방식을 안내한다. 토큰 절약은 기대 효과이며 특정 절감률이나 자동 보장을 약속하지 않는다. 완성할 것은 기준 문서와 같은 톤을 유지한 모션그래픽이다. 새 앱 설치·버튼 조작·API·긴 프롬프트 실습은 추가하지 않는다. L19 과제 안내와 L16 파일 역할 표현을 조합한 편집 가능한 자체 장표다.');
 const data=[['motion.md','등장·전환·속도·간격'],['video.md','화면 비율·배경·전체 영상 톤']];
 data.forEach(([file,desc],i)=>{let y=352+i*127;shape(s,'file-panel-'+i,150,y,585,110,C.card,'roundRect');txt(s,'file-'+i,file,180,y+15,525,43,31,C.white,true);txt(s,'file-desc-'+i,desc,180,y+67,525,29,22,C.muted);});
 txt(s,'right-heading','토큰을 아끼는 제작 흐름',805,350,360,38,25,C.orange,true);
 action(s,1,'추가 자료 확인','제공 자료에서 필요한 기준 찾기',405);
 action(s,2,'기준 문서 작성','대표 장면으로 톤과 움직임 확인',485);
 action(s,3,'확정한 기준을 다음 장면에 적용','같은 톤을 유지하며 영상 완성',565);
 txt(s,'takeaway','완성할 것: 기준 문서 + 일관성을 유지한 모션그래픽',150,642,980,34,22,C.orange,true,'center');
}
await fs.writeFile(path.join(B,'additions.json'),JSON.stringify(spec,null,2));await(await PresentationFile.exportPptx(p)).save(path.join(B,'additions.pptx'));console.log('Authored two cycle activity guides');
