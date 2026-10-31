import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {C,text} from '../../assets/layout-library-20261028/recipes/components.mjs';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..'),U=path.join(R,'units/AI-001_모션그래픽수업영상_무료웨비나'),A=path.join(U,'assets/image-explain-20261029');
const p=Presentation.create({slideSize:{width:1280,height:720}}),spec=[];
const brand=new Uint8Array(await fs.readFile(path.join(R,'assets/branding/notiontalk-white.png')));
function page(n,title,subtitle,notes){const s=p.slides.add();s.background.fill=C.bg;const part=n<32?3:4;
 s.images.add({blob:brand,contentType:'image/png',fit:'contain',position:{left:1010,top:58,width:190,height:55}});
 text(s,'part-label',part===3?'Part 3  스토리라인과 스틸컷 확인':'Part 4  수정 후 제작',60,55,800,27,17,C.muted,true);
 text(s,'group-number',part===3?'02':'01',60,91,45,36,28,C.orange,true);
 text(s,'group-label',part===3?'스타일 기준을 문서로 남기기':'피드백을 반영하고 진행하기',107,91,850,36,28,C.white,true);
 text(s,'slide-title',title,140,190,1000,62,40,C.white,true,'center');
 if(subtitle)text(s,'slide-subtitle',subtitle,140,266,1000,43,23,C.white,false,'center');
 text(s,'copyright-footer','© 2026. NotionTalk. All rights reserved.',800,682,420,22,12,C.muted,false,'right');
 spec.push({page:n,title,notes});return s;
}
async function visual(s,file,x,y,w,h){s.images.add({blob:new Uint8Array(await fs.readFile(path.join(A,file))),contentType:'image/png',fit:'contain',position:{left:x,top:y,width:w,height:h}});}
function note(s,t){text(s,'visual-takeaway',t,150,637,980,37,22,C.orange,true,'center');}
{
 const s=page(24,'같은 톤, 서로 다른 장면','비슷한 톤을 이어가려면 design.md와 motion.md도 함께 만드는 것을 추천합니다',
 '같은 캐릭터가 소개·설명·마무리에서 다른 행동을 해도 색·외형·재질이 이어지면 같은 시리즈로 보인다. 이 이미지는 시각적 일관성을 설명하는 자체 생성 예시다. 움직임은 정지 이미지로 확인할 수 없으므로 motion.md와 재생 예시가 별도로 필요하다. design.md에는 화면 기준, motion.md에는 움직임 기준을 남기고 다음 작업에 함께 제공한다. 파일 이름 자체가 자동 설정이나 동일 결과를 보장하지 않는다.');
 await visual(s,'consistent-tone.png',150,316,980,282);
 ['소개','설명','마무리'].forEach((t,i)=>text(s,'scene-label-'+i,t,255+i*265,601,240,30,23,C.white,true,'center'));
 note(s,'장면이 달라져도 색·캐릭터·재질은 이어집니다');
}
{
 const s=page(30,'스틸컷은 모습, 재생은 움직임','',
 '왼쪽 한 컷에서 색·형태·구도를 확인한다. 오른쪽 네 컷은 시간에 따른 위치 변화를 표현한 정지 연속 장면 예시다. 이 그림만으로 실제 속도나 간격을 판정하지 않는다. design.md는 대표 스틸컷 두 장과 대조하고 motion.md는 짧은 영상 구간을 실제로 재생하며 확인한다. storyline.md는 장면표와 전체 흐름을 확인하는 기준이다.');
 text(s,'still-label','design.md  ·  스틸컷',145,302,330,41,28,C.orange,true,'center');
 text(s,'motion-label','motion.md  ·  구간 재생',565,302,550,41,28,C.orange,true,'center');
 await visual(s,'still-and-sequence.png',100,342,1080,300);
 text(s,'still-caption','색·형태·구도',145,569,330,35,25,C.white,true,'center');
 text(s,'motion-caption','위치·속도·간격의 변화',565,569,550,35,25,C.white,true,'center');
 text(s,'sequence-disclosure','오른쪽은 시간에 따른 변화를 펼친 정지 예시입니다',565,606,550,28,17,C.muted,false,'center');
 note(s,'실제 움직임은 짧은 구간을 재생해서 확인합니다');
}
{
 const s=page(38,'한 장면 수정과 공통 기준 변경','색을 바꾸더라도, 적용할 범위는 다릅니다',
 '처음 세 장면의 공 색은 모두 주황이라고 가정한다. 위쪽은 두 번째 장면의 공만 파란색으로 바꾼 경우다. storyline.md 장면표에 예외를 남기고 나머지 장면은 유지한다. 아래쪽은 공의 공통 기본색을 파란색으로 정한 경우다. design.md를 갱신하고 모든 장면을 다시 확인한다. 속도 같은 공통 움직임 기준을 바꿀 때는 motion.md에 같은 방식으로 반영한다. 파란색은 변경 범위를 드러내는 교육용 예시이며 웨비나 브랜드 색상 변경을 뜻하지 않는다.');
 await visual(s,'local-and-shared.png',355,326,800,294);
 text(s,'local','장면 2만 변경',130,365,220,43,27,C.white,true);
 text(s,'local-file','장면표에 예외 기록',130,413,220,36,20,C.muted);
 text(s,'shared','공통 기준 변경',130,505,220,43,27,C.orange,true);
 text(s,'shared-file','design.md 갱신',130,553,220,36,20,C.muted);
 note(s,'이번 장면의 예외인지, 다음에도 쓸 기본값인지 구분합니다');
}
await fs.writeFile(path.join(B,'additions.json'),JSON.stringify(spec,null,2));
await(await PresentationFile.exportPptx(p)).save(path.join(B,'additions.pptx'));
console.log('3 image-led replacement slides authored');

