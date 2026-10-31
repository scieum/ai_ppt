import fs from 'node:fs/promises';import path from 'node:path';import{fileURLToPath}from'node:url';
import{Presentation,PresentationFile}from'@oai/artifact-tool';
import{C,text,shape,arrow}from'../../assets/layout-library-20261028/recipes/components.mjs';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..');
const p=Presentation.create({slideSize:{width:1280,height:720}}),spec=[];
const brand=new Uint8Array(await fs.readFile(path.join(R,'assets/branding/notiontalk-white.png')));
function page(key,replace,before,part,group,title,sub,notes){const s=p.slides.add();s.background.fill=C.bg;
 s.images.add({blob:brand,contentType:'image/png',fit:'contain',position:{left:1010,top:58,width:190,height:55}});
 text(s,'part',part,60,55,800,27,17,C.muted,true);
 if(/^0[12]  /.test(group)){text(s,'group-number',group.slice(0,2),60,91,45,36,28,C.orange,true);text(s,'group',group.slice(4),107,91,900,36,28,C.white,true);}else{text(s,'group',group,60,91,950,36,28,C.white,true);}
 text(s,'title',title,130,190,1020,65,40,C.white,true,'center');text(s,'subtitle',sub,130,265,1020,44,23,C.white,false,'center');
 text(s,'copyright','© 2026. NotionTalk. All rights reserved.',800,682,420,22,12,C.muted,false,'right');
 spec.push({key,replace,before,title,notes});return s;}
function txt(s,n,t,x,y,w,h=40,size=23,col=C.white,bold=false,align='left'){text(s,n,t,x,y,w,h,size,col,bold,align);}
function box(s,n,x,y,w,h,fill=C.card){shape(s,n,x,y,w,h,fill,'roundRect');}
function takeaway(s,t){txt(s,'takeaway',t,130,636,1020,36,21,C.orange,true,'center');}
{
 const s=page('tools',3,null,'Part 0  시작 전 준비','오늘 사용할 도구','앱에서 만들고, 자료와 목소리를 더합니다','클로드 또는 코덱스 중 하나의 유료 계정을 준비해 주세요',
 '이번 웨비나의 선택 도구: Claude 또는 Codex 데스크탑 앱, yt-dlp, ElevenLabs. 유료 계정 안내는 강의 운영상 준비 기준이며 각 서비스의 모든 이용 방식에 대한 요금제 단정이 아니다. 힉스필드는 현재 준비물에서 제외한다. Node.js는 앱 로그인 자체의 조건과 구분한다. npm 기반 영상 프로젝트를 실행할 때 필요하므로 준비를 권장한다. Remotion 공식 안내 https://www.remotion.dev/docs/ai/coding-agents . yt-dlp의 YouTube 전체 지원에는 EJS와 지원 JS 런타임이 필요하며 Deno가 권장·기본 활성화된다. Node도 지원하지만 --js-runtimes node로 활성화해야 하며 현재 문서상 최소22다. https://github.com/yt-dlp/yt-dlp/wiki/EJS . FFmpeg/ffprobe는 영상·음성 병합 등에 사용한다. https://github.com/yt-dlp/yt-dlp . ElevenLabs 웹 TTS 사용은 Node 설치와 별개다. https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech . Claude Desktop은 Code를 포함한다 https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code . 공식 OpenAI 앱 문서 https://learn.chatgpt.com/docs/app . 2026-10-29 확인.');
 const apps=[['Claude 데스크탑','기획·장면·영상 코드 작업','claude'],['Codex 데스크탑','기획·장면·영상 코드 작업','codex']];
 for(let i=0;i<2;i++){let x=150+i*500;box(s,'app'+i,x,337,480,112);s.images.add({blob:new Uint8Array(await fs.readFile(path.join(R,`assets/tool-logos/orange-v2/png/${apps[i][2]}-front.png`))),contentType:'image/png',fit:'contain',position:{left:x+15,top:350,width:85,height:85}});txt(s,'app-name'+i,apps[i][0],x+116,355,340,36,27,C.white,true);txt(s,'app-desc'+i,apps[i][1],x+116,402,340,28,20,C.muted);}
 for(const [i,name,role,desc] of [[0,'yt-dlp','영상 레퍼런스 자료 확보','영상·자막을 확인할 때 사용'],[1,'ElevenLabs','내레이션 음성 제작','확정한 대본을 목소리로 변환']]){let x=150+i*500;box(s,'service'+i,x,465,480,112);txt(s,'service-name'+i,name,x+24,481,190,38,27,C.orange,true);txt(s,'service-role'+i,role,x+215,481,245,37,22,C.white,true);txt(s,'service-desc'+i,desc,x+24,532,432,28,20,C.muted);}
 txt(s,'runtime','실행 환경  Node.js 권장 · yt-dlp는 Deno도 가능 · 병합 작업에는 FFmpeg',150,598,980,33,20,C.muted,false,'center');
 takeaway(s,'두 AI 앱은 택 1 · 내레이션을 넣을 때 ElevenLabs를 활용합니다');
}
{
 const s=page('mdroles',25,null,'Part 3  스토리라인과 스틸컷 확인','02  스타일 기준을 문서로 남기기','영상의 기준을 세 문서에 나누어 담습니다','.md는 글로 읽고 고칠 수 있는 Markdown 문서입니다',
 '첨부한 파일별 카드 레퍼런스의 설명 구조만 참고하고 문구와 정보는 자체 구성한다. 우리 기존 흐름의 storyline.md, design.md, motion.md를 유지한다. 원본 레퍼런스의 video.md로 임의 교체하지 않는다. 파일 이름만으로 AI가 자동 적용하거나 같은 결과가 보장되는 것은 아니다. 다음 작업에 문서와 실제 자산을 명시적으로 함께 전달한다. 스틸컷은 문서와 다른 확인 자료로 23·30쪽에서 설명한다.');
 const rows=[['storyline.md','내용과 장면 순서','무엇을 말할까?','장면 순서·핵심 문구·내레이션'],['design.md','화면의 시각 기준','어떤 모습일까?','색·글꼴·배치·캐릭터'],['motion.md','움직임의 기준','어떻게 움직일까?','등장·속도·간격·장면 전환']];
 rows.forEach(([file,role,question,items],i)=>{let x=150+i*330;box(s,'file-card'+i,x,350,310,143,'#262626');txt(s,'file'+i,file,x+25,374,260,42,29,C.white,true);txt(s,'role'+i,role,x+25,430,260,37,23,C.muted);box(s,'explain'+i,x,511,310,92,'#171717');txt(s,'question'+i,question,x+18,520,274,35,25,C.orange,true,'center');txt(s,'items'+i,items,x+13,562,284,28,19,C.white,false,'center');});
 takeaway(s,'내용·화면·움직임을 나누어 두면, 고칠 기준을 찾기 쉽습니다');
}
{
 const s=page('narration',null,37,'Part 4  수정 후 제작','01  피드백을 반영하고 진행하기','내레이션이 필요하면 ElevenLabs를 활용합니다','확정한 대본을 음성으로 만들고, 장면과 함께 들어봅니다',
 'ElevenLabs Text to Speech는 입력한 대본과 선택한 목소리로 음성을 생성한다. 웹 화면에서 이용할 수 있으므로 이 소개를 위해 API나 Node.js 연결을 필수로 안내하지 않는다. 사용자는 기존 제작 방법 제외 범위의 좁은 추가로 내레이션 활용 소개를 요청했다. 장황한 앱 조작·명령어·음성 복제 실습은 추가하지 않는다. 슬라이드의 설명은 제안 흐름이며 실제 음성을 생성하거나 검증했다는 의미가 아니다. 음성 실제 길이와 발음·쉼을 듣고 장면 타이밍을 조정한다. ElevenLabs 공식 안내 https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech (2026-10-29 확인).');
 const rows=[['대본','storyline.md','장면마다 읽을 문장'],['음성','ElevenLabs','목소리 선택 · 음성 생성'],['영상과 확인','내레이션 + 장면','발음 · 쉼 · 장면 길이']];
 rows.forEach(([role,file,desc],i)=>{let x=150+i*340;box(s,'narration-card'+i,x,355,300,180);txt(s,'role'+i,role,x+20,375,260,34,21,C.muted,false,'center');txt(s,'file'+i,file,x+12,422,276,45,29,C.orange,true,'center');txt(s,'desc'+i,desc,x+12,484,276,31,20,C.white,false,'center');if(i<2)arrow(s,'next'+i,x+312,427,18,27);});
 txt(s,'example','“배움이 움직입니다. 함께 배우는 노션톡.”',200,563,880,46,28,C.white,true,'center');
 takeaway(s,'목소리를 듣고, 설명이 끝나는 지점에 장면의 길이를 맞춥니다');
}
await fs.writeFile(path.join(B,'additions.json'),JSON.stringify(spec,null,2));await(await PresentationFile.exportPptx(p)).save(path.join(B,'additions.pptx'));console.log('Prepared 2 replacements and 1 narration slide');
