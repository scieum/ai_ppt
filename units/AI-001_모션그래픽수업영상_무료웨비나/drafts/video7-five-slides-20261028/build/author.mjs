import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';import{createRequire}from'node:module';import{PresentationFile,FileBlob}from'@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..');const req=createRequire(import.meta.resolve('@oai/artifact-tool'));req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_14장_사전확인_v7.pptx')));const original=[...p.slides.items];const specs=[];
const source='참고: 헤이디_일잘러의 업무스킬, 이제 모션그래픽은 클로드한테 맡기세요. https://www.youtube.com/watch?v=7xOcIYWGG0A';
function sh(s,name,g,x,y,w,h,fill='#FF911D',rotation=0){return s.shapes.add({name:'lesson7-'+name,geometry:g,position:{left:x,top:y,width:w,height:h,rotation},fill,line:{fill:'none',width:0}});}
function txt(s,name,value,x,y,w,h,size=20,color='#AAAAAA',bold=false){const a=sh(s,name,'textbox',x,y,w,h,'none');a.text=value;a.text.style={typeface:'Pretendard',fontSize:size,color,bold,alignment:'center',verticalAlignment:'middle'};a.text.insets=0;return a;}
function make(page,source_page,edits,note,extra={}){
 const s=original[source_page-1].duplicate();const spec={page,source_page,export_id:s.id,remove:[],edits:{part_label:'제작 전 미리보기  영상 사례 확장',section_number:page<17?'01':'02',section_heading:page<17?'참고 자료의 역할':'스토리라인·스틸컷·피드백',...edits},notes:note,...extra};
 for(const[name,value]of Object.entries(spec.edits)){const a=s.shapes.items.find(x=>x.name===name);if(!a)throw Error(name);a.text.replace(String(a.text),value);}
 if(source_page===7)for(const a of [...s.shapes.items])if(a.name.startsWith('ex-')){spec.remove.push(a.name);a.delete();}
 specs.push(spec);return[s,spec];
}
{
 const[s,sp]=make(15,7,{title:'참고 자료가 하나뿐일 때',subtitle:'영상 속 두 시행착오와 보완한 방식을 비교합니다','effect-name-0':'이미지만 전달','effect-en-0':'모습을 보여 주기','effect-desc-0':'전개와 움직임 설명이 부족','effect-name-1':'영상만 전달','effect-en-1':'시간 흐름을 보여 주기','effect-desc-1':'원하는 장면 디자인이 부족','effect-name-2':'역할 나눠 전달','effect-en-2':'모습과 움직임을 함께','effect-desc-2':'두 기준을 나눠 구체화'},'원본의 제작자는 정지 행사 이미지로 시작한 첫 시도와 영상 참고 자료로 시작한 다음 시도 모두 원하는 결과와 달랐다고 설명합니다. 이 개인 사례를 자료의 역할 차이로 정리했습니다. 한 종류의 참고 자료가 언제나 실패한다는 일반 법칙이나 현재 도구의 성능 결론은 아닙니다.\n'+source+'&t=43 , 00:43~04:42. 원본 포스터나 결과 화면을 복사하지 않은 자체 도식입니다.');
 for(let i=0;i<3;i++)sh(s,'frame-'+i,'roundRect',264+i*320,464,112,66,'#303030');
 sh(s,'image-hill','triangle',279,483,54,37);sh(s,'image-sun','ellipse',341,475,15,15,'#75D3F7');
 sh(s,'video-play','triangle',624,478,32,37,'#FF911D',90);
 txt(s,'combined','이미지 + 영상',906,480,108,34,17,'#FF911D',true);
 txt(s,'failure-note','어떤 모습을 원하는지와 어떻게 움직일지를 따로 설명합니다',170,650,943.3,28,19,'#FF911D',true);
}
{
 const[s,sp]=make(16,3,{title:'이미지와 영상의 역할 나누기',subtitle:'이미지는 보이는 모습, 영상은 시간의 흐름을 전달합니다','still-label':'이미지에서 참고할 것','moving-label':'영상에서 참고할 것','still-title':'디자인','demo-definition':'모션','still-caption':'색·글자·소재·구도','moving-caption':'등장 순서·속도·장면 전환','dev-definition-takeaway':'각 자료에서 참고할 부분을 함께 적어 전달합니다'},'이미지 참고 자료와 영상 참고 자료를 함께 쓰되 역할을 나누는 설명입니다. 예시에서는 이미지에 색·글자·소재·구도를, 영상에 등장 순서·속도·장면 전환을 연결했습니다. 기존 노션톡 장표의 두 패널을 활용한 자체 설명이며 실제 앱 결과 화면이 아닙니다.\n'+source+'&t=286 , 04:46~06:38. 원본의 행사 사례·색상·서체 조합이나 프롬프트는 복제하지 않았습니다.',{keep_timing:true});
 sh(s,'color-chip-0','ellipse',328,526,10,10,'#FF911D');sh(s,'color-chip-1','ellipse',346,526,10,10,'#75D3F7');sh(s,'color-chip-2','ellipse',364,526,10,10,'#FFFFFF');
 for(let i=0;i<3;i++)sh(s,'motion-dot-'+i,'ellipse',835+i*42,526,10,10,'#FF911D');
}
{
 const[s,sp]=make(17,13,{title:'storyline.md로 흐름 확인',subtitle:'장면 순서와 문구, 움직임을 글로 먼저 정리합니다'},'스토리라인은 각 장면의 순서와 화면 내용을 글로 확인하는 자료입니다. 표의 15초 노션톡 예시는 이 웨비나를 위해 새로 작성했습니다. 구간 길이와 문구는 강의용 예시이며 원본 영상의 장면 계획을 옮긴 것이 아닙니다.\n'+source+'&t=564 , 09:24~10:40. .md 파일 형식은 사용자의 앞선 명시적 요청입니다.',{table:[['구간','핵심 문구','보이는 움직임'],['0~4초','배움이 움직이다','글자가 차례로 나타남'],['4~10초','AI로 설명하는 아이디어','도형이 모이며 화면 전환'],['10~15초','함께 배우는 노션톡','문구 뒤에 로고 등장']]});
 const tb=s.tables.items[0];for(let r=0;r<sp.table.length;r++)for(let c=0;c<3;c++)tb.getCell(r,c).value=sp.table[r][c];
 txt(s,'storyline-note','내용을 먼저 고치고, 대표 스틸컷을 확인한 뒤 영상 제작으로 넘어갑니다',170,640,943.3,30,18,'#FF911D',true);
}
{
 const[s,sp]=make(18,3,{title:'대표 스틸컷 2장으로 미리 보기',subtitle:'시작과 마무리 장면의 모습을 먼저 확인하는 예시입니다','still-label':'스틸컷 A · 시작 장면','moving-label':'스틸컷 B · 마무리 장면','still-title':'배움이\n움직이다','demo-definition':'함께 배우는\n노션톡','still-caption':'제목과 첫인상이 보이는 장면','moving-caption':'메시지와 브랜드가 남는 장면','dev-definition-takeaway':'색·문구·구도를 먼저 수정하면 전체 영상의 반복 생성을 줄일 수 있습니다'},'앞 장표의 storyline.md에서 시작과 마무리 장면을 뽑은 자체 편집 예시입니다. 대표 스틸컷은 영상 전체의 모든 프레임을 검증하는 자료가 아니므로 시간과 움직임은 영상에서 별도로 확인합니다. 두 장면은 현재 PPT의 편집 가능한 글자와 도형으로 구성했으며 실제 AI 앱에서 생성한 결과나 원본의 스틸컷으로 제시하지 않습니다.\n'+source+'&t=564 , 09:24~10:40 및 13:46~14:31. 시작·마무리를 고른 것은 이 강의의 자체 예시입니다.',{positions:{'still-title':{top:442,height:86},'demo-definition':{top:442,height:86}},styles:{'still-title':{fontSize:31},'demo-definition':{fontSize:31}},keep_timing:false});
 for(const[name,pos]of Object.entries(sp.positions)){const a=s.shapes.items.find(x=>x.name===name);a.position={...a.position,...pos};}
 for(const[name,style]of Object.entries(sp.styles))s.shapes.items.find(x=>x.name===name).text.style=style;
 sh(s,'still-a-orbit','ellipse',500,442,45,45,'#FF911D');sh(s,'still-a-dot','ellipse',525,471,12,12,'#75D3F7');
 sh(s,'still-b-bar','roundRect',804,528,190,4,'#FF911D');
}
{
 const[s,sp]=make(19,13,{title:'피드백은 고칠 대상을 구체적으로',subtitle:'어느 장면의 무엇을 바꿀지 정하고, 수정된 결과를 다시 확인합니다'},'영상 제작자는 행간·강조할 텍스트·장면 속 요소 등 수정 대상을 구체적으로 이야기하고, 수정 뒤 대표 이미지를 다시 확인하는 과정을 보여 줍니다. 표는 이를 노션톡 예시로 새로 구성했습니다. 정지 화면의 수정은 스틸컷에서, 등장 속도나 유지 시간의 수정은 영상의 해당 구간에서 확인하는 차이도 구분합니다.\n'+source+'&t=660 , 11:00~12:09 및 14:51~15:24. 원본의 문장과 행사 카피는 사용하지 않았습니다.',{table:[['고칠 부분','수정 요청 예시','다시 확인할 것'],['시작 장면의 제목','배움이 움직이다를 더 크게','새 스틸컷의 글자 크기'],['마지막 장면의 색','주황 배경의 밝기를 낮추기','새 스틸컷의 색과 대비'],['마지막 문구의 시간','읽을 수 있게 더 오래 유지','영상의 해당 구간']]});
 const tb=s.tables.items[0];for(let r=0;r<sp.table.length;r++)for(let c=0;c<3;c++)tb.getCell(r,c).value=sp.table[r][c];
 txt(s,'feedback-note','수정한 스틸컷과 영상 구간을 확인한 뒤 다음 제작을 진행합니다',170,640,943.3,30,19,'#FF911D',true);
}
for(const sp of specs)sp.export_page=p.slides.items.findIndex(x=>x.id===sp.export_id)+1;
await fs.writeFile(path.join(B,'edits.json'),JSON.stringify(specs,null,2));await(await PresentationFile.exportPptx(p)).save(path.join(B,'roundtrip.pptx'));console.log('Authored five substantive video-based slides with comparison panels and editable tables.');
