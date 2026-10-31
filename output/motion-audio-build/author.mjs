import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath}from'node:url';
import {Presentation,PresentationFile}from'@oai/artifact-tool';
import {shape,text,C}from'../../assets/layout-library-20261028/recipes/components.mjs';
import {conclusionBar}from'../../assets/layout-library-20261028/logic-patterns-20261030/conclusion-bar.mjs';
const B=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(B,'../..'),A=path.join(R,'units/AI-001_모션그래픽수업영상_무료웨비나/assets/motion-audio-20261030');
const p=Presentation.create({slideSize:{width:1280,height:720}}),spec=[];
function slide(d){spec.push(d);const s=p.slides.add();s.background.fill=C.bg;s.speakerNotes.text=d.notes;return s;}
async function pic(s,name,file,x,y,w,h){s.images.add({name,blob:new Uint8Array(await fs.readFile(file)),contentType:'image/png',fit:'contain',position:{left:x,top:y,width:w,height:h},alt:name});}
async function demo(s,x,kind,title,en,desc,states){
 shape(s,kind+'-card',x,336,470,282,C.card,'roundRect');
 text(s,kind+'-name',title,x+20,350,430,34,27,C.white,true,'center');
 text(s,kind+'-english',en,x+20,389,430,26,20,C.muted,false,'center');
 await pic(s,'motion-'+kind,path.join(A,kind+'-poster.png'),x+20,423,430,153.57);
 text(s,kind+'-description',desc,x+20,574,430,28,22,C.muted,false,'center');
}
{
 const s=slide({id:'text-effects',after:14,base:14,title:'글자가 들어와 자리를 잡는 움직임',subtitle:'지나쳤다가 멈추는 스냅, 흐림에서 선명해지는 블러 인',notes:'스냅 텍스트는 도착점을 살짝 지나친 뒤 돌아오는 움직임입니다. 블러 인은 흐림이 사라지는 표현이며 이 예시는 크기와 회전도 함께 변합니다. 두 GIF는 자체 제작한 4초 반복 예시입니다. 출처: 사용자 제공 @mynameisjaemin 캡처(2026-10-30), 원 게시물 URL 미제공. 원본 영상이나 시각 자산을 복제하지 않았습니다.'});
 await demo(s,150,'snap','스냅 텍스트','Snap text','빠르게 들어와 살짝 지나친 뒤 멈춤');
 await demo(s,660,'blur','블러 인','Blur in','흐릿한 글자가 모이며 또렷해짐');
 conclusionBar(s,'등장하는 경로와 멈추는 방식에 따라 글자의 느낌이 달라집니다');
}
{
 const s=slide({id:'number-elastic',after:14,base:14,title:'숫자의 변화와 탄성 있는 움직임',subtitle:'카운터는 값의 변화를, 스쿼시 앤 스트레치는 탄성을 보여줍니다',notes:'왼쪽은 설명용 가상 진행률 0~100%입니다. 오른쪽은 공이 낙하할 때 늘어나고 바닥에 닿아 눌렸다 다시 튀는 예시입니다. 효과 이름과 변화하는 속성을 연결해 설명합니다. 각 GIF는 자체 제작했습니다. 출처: 사용자 제공 @mynameisjaemin 캡처(2026-10-30), 원 게시물 URL 미제공.'});
 await demo(s,150,'counter','카운터','Counter','숫자가 목표값까지 바뀜');
 await demo(s,660,'squash','스쿼시 앤 스트레치','Squash & stretch','눌렸다 늘어나며 다시 튀어 오름');
 conclusionBar(s,'숫자는 변화량을, 형태의 늘어남과 눌림은 탄성을 드러냅니다');
}
{
 const s=slide({id:'sound-compare',after:16,base:16,title:'같은 움직임에 효과음을 더하면',subtitle:'같은 영상에서 제목의 등장과 완료 순간을 비교합니다',notes:'왼쪽 무음 영상을 먼저 클릭한 뒤 오른쪽 효과음 영상을 클릭해 비교합니다. 영상은 각 4초입니다. 오른쪽은 제목이 멈추는 0.85초의 팝, 카드가 나타나는 1.45초의 짧은 스윽 소리, 준비 완료를 알리는 2.8초의 알림음을 담았습니다. 두 영상의 화면은 동일합니다. 모두 자체 제작한 설명용 예시이며 Real SFX나 earshot의 실행 결과가 아닙니다. 효과음 도구 역할의 출처: https://clipwing.pro/skills/real-sfx 및 https://github.com/Leonxlnx/earshot (2026-10-30 확인).'});
 for(const [x,key,label]of[[150,'silent','무음'],[660,'with-sound','효과음 있음']]){
  shape(s,key+'-card',x,336,470,278,C.card,'roundRect');text(s,key+'-label',label,x+20,350,430,34,27,key==='silent'?C.white:C.orange,true,'center');
  // Native embedded video objects are inserted at these same frames during assembly.
  await pic(s,'video-placeholder-'+key,path.join(A,'sound-poster.png'),x+20,405,430,153.57);
  text(s,key+'-caption','클릭해서 4초 영상 재생',x+20,574,430,28,20,C.muted,false,'center');
 }
 conclusionBar(s,'중요한 움직임에 맞춘 짧은 소리가 장면의 변화를 또렷하게 만듭니다');
}
{
 const s=slide({id:'sound-tools',after:16,base:16,title:'효과음 도구의 서로 다른 역할',subtitle:'필요한 소리를 찾거나, 장면에 배치하거나, 새로 합성할 수 있어요',notes:'Openverse는 기존 오디오 검색 서비스입니다. 개별 파일의 원출처와 라이선스를 확인합니다. Real SFX는 녹음 효과음을 영상에 배치하는 Clipwing의 Claude Code 스킬로 Python 3.9 이상과 FFmpeg 및 사용 가능한 효과음이 필요합니다. earshot은 Leonxlnx/earshot 저장소의 소리 분석·코드 합성 도구입니다. 무료 배포와 AI 계정·음원·모델 이용 조건은 별개이며 이 세 도구를 필수 준비물로 추가하지 않습니다. 자동 분석 후에도 실제 소리를 들어 확인합니다. 출처: https://api.openverse.org/v1/ https://docs.openverse.org/terms_of_service.html https://clipwing.pro/skills/real-sfx https://github.com/Leonxlnx/earshot (2026-10-30 확인).'});
 for(const [i,role,name,a,b]of[[0,'검색','Openverse','이미 공개된 소리 찾기','원출처와 이용 조건 확인'],[1,'배치','Real SFX','녹음 효과음을 장면에 맞추기','사용할 음원 라이브러리 필요'],[2,'합성·분석','earshot','코드로 소리를 만들고 비교','마지막에는 직접 듣고 확인']]){
  const x=150+i*336;shape(s,'tool-card-'+i,x,343,308,257,C.card,'roundRect');
  text(s,'tool-role-'+i,role,x+22,363,264,52,36,C.orange,true,'center');
  text(s,'tool-name-'+i,name,x+22,432,264,39,27,C.white,true,'center');
  text(s,'tool-desc-'+i,a,x+16,494,276,37,21,C.white,false,'center');
  text(s,'tool-check-'+i,b,x+16,550,276,32,18,C.muted,false,'center');
 }
 conclusionBar(s,'소리를 찾는 도구와 배치하는 도구, 합성하는 도구는 역할이 다릅니다');
}
{
 const s=slide({id:'image-layers',after:20,base:20,title:'이미지를 움직일 요소로 나누어 봅니다',subtitle:'글자·캐릭터·배경을 따로 구성하면 움직임도 따로 정할 수 있어요',notes:'오디씨 LAB의 JPG 한 장으로 AE 모션그래픽 사례를 개념 수준으로 설명합니다. 원본 사례는 이미지를 잘라 붙이는 대신 AE 셰이프·솔리드·텍스트 레이어로 재구성한 뒤 정지 화면을 확인하고 모션을 추가합니다. 화면은 노션톡 자체 자산으로 만든 설명용 도식이며 실제 AE 실행 결과가 아닙니다. JPG에 편집 가능한 레이어가 원래 들어 있다는 뜻도 아닙니다. 원 작성자는 Mac에서 확인했고 Windows는 미검증입니다. AE와 스크립트 환경은 선택 심화이며 공통 준비물이 아닙니다. 출처: https://odssilab.com/recipes/ae-motion/ (2026-10-30 확인).'});
 shape(s,'image-example-panel',150,337,360,277,C.card,'roundRect');
 text(s,'image-example-label','한 장의 화면',170,348,320,30,23,C.muted,true,'center');
 text(s,'image-example-title','노션톡 웨비나',170,396,320,44,32,C.orange,true,'center');
 // Preserve the user's existing character asset as part of this editable explanatory diagram.
 const poses=JSON.parse(await fs.readFile(path.join(R,'units/AI-001_모션그래픽수업영상_무료웨비나/assets/character-sheets-20261028/poses.json'),'utf8'));
 const d=poses.find(x=>x.id==='bear-thinking');
 const sh=s.images.add({name:'original-bear-character',blob:new Uint8Array(await fs.readFile(d.file)),contentType:'image/png',fit:'contain',position:{left:276,top:448,width:108,height:149},crop:d.crop,alt:'노션톡 곰 캐릭터, 설명용 화면 구성'});
 text(s,'layer-arrow','→',535,450,70,54,40,C.orange,true,'center');
 for(const [i,label,detail]of[[0,'글자','제목이 나타나는 순서'],[1,'캐릭터','캐릭터의 위치와 움직임'],[2,'배경','화면의 색과 깊이']]){
  const y=342+i*73;shape(s,'layer-'+i,630,y,500,62,C.card,'roundRect');
  text(s,'layer-label-'+i,label,650,y+12,110,36,25,C.orange,true);text(s,'layer-detail-'+i,detail,774,y+12,334,36,23,C.white);
 }
 text(s,'ae-optional','AE 활용 사례 · 선택 심화',630,572,500,32,20,C.muted,false,'center');
 conclusionBar(s,'이미지의 구성을 먼저 확인하고, 요소별로 움직임을 더합니다');
}
await(await PresentationFile.exportPptx(p)).save(path.join(B,'additions.pptx'));
await fs.writeFile(path.join(B,'spec.json'),JSON.stringify(spec,null,2));console.log('Authored 5 slides with the existing style and conclusion bar.');
