import fs from 'node:fs/promises';import path from 'node:path';import{fileURLToPath}from'node:url';import{createRequire}from'node:module';import{PresentationFile,FileBlob}from'@oai/artifact-tool';
const B=path.dirname(fileURLToPath(import.meta.url)),U=path.resolve(B,'../../..'),R=path.resolve(U,'../..'),req=createRequire(import.meta.resolve('@oai/artifact-tool'));
req('skia-canvas').FontLibrary.use('Pretendard',['C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf','C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf']);
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_준비물복원_17장_v11.pptx'))),template=p.slides.items[7];
const definitions=[
 {page:7,title:'같은 내용도 톤에 따라 달라집니다',subtitle:'종류가 표현의 중심이라면, 톤은 그림의 질감과 분위기입니다',number:'01',heading:'뜻과 종류',kinds:['hand','blueprint','neon'],labels:['손그림','청사진','다크 네온'],ens:['Hand-drawn','Blueprint','Dark Neon'],descs:['불규칙한 선과 따뜻한 질감','도면 같은 선과 격자','어둠 속에서 강조되는 빛'],bottom:'같은 원과 같은 이동도 서로 다른 분위기로 보입니다',time:'00:14–00:42, 02:06–02:25, 05:00–05:22',note:'종류와 톤의 구분은 기존 강의와 연결하기 위한 자체 정리입니다. 영상의 손그림·청사진·다크 네온 설명을 재구성하고 같은 원·이동을 세 질감으로 표현한 새 비교 예시를 사용합니다.'},
 {page:8,title:'재질에 따라 움직임의 인상도 달라집니다',subtitle:'빛이 흐르는 표면, 칸 단위 이동, 눌렸다 튀는 탄성을 비교합니다',number:'01',heading:'뜻과 종류',kinds:['chrome','pixel','clay'],labels:['크롬·유리','픽셀','클레이'],ens:['Chrome / Glass','Pixel','Clay'],descs:['표면을 따라 미끄러지는 빛','격자에 맞춰 끊어지는 이동','눌렸다가 다시 튀는 형태'],bottom:'부드러움과 끊김, 단단함과 말랑함도 표현의 차이입니다',time:'02:45–03:06, 03:43–04:04, 06:25–06:44',note:'영상의 재질·픽셀·클레이 톤을 초보자용 질감과 운동감 비교로 재구성했습니다. 자체 그래픽 모형이며 실제 3D 렌더 결과나 원본 영상 프레임이 아닙니다. 픽셀 예시는 의도적으로 계단식 이동을 사용합니다.'},
 {page:13,title:'장면도 움직임으로 이어질 수 있습니다',subtitle:'형태 변화, 앞뒤의 속도 차이, 시점 변화가 화면을 연결합니다',number:'02',heading:'움직임과 효과',kinds:['morph','parallax','camera'],labels:['형태 전환','시차 이동','카메라 이동'],ens:['Morph Transition','Parallax','Camera Move'],descs:['앞 모양이 다음 모양으로 변화','가까운 층과 먼 층의 속도 차이','시점이 움직이며 공간을 탐색'],bottom:'한 장면 안의 효과를 넘어 화면 전체의 연결로 살펴봅니다',time:'03:06–03:23, 04:38–05:00, 05:22–05:44; 설명란의 장면 전환 설명',note:'영상 설명란의 세계가 다음 세계로 변하는 연결, 시네마틱 3D의 카메라 이동, 사이버펑크의 원근 시차를 자체 도식으로 다시 구성했습니다. 앞서 설명한 모핑의 정의를 반복하는 대신 장면을 잇는 역할을 비교합니다. 실제 인앱 생성 결과가 아닙니다.'},
 {page:14,title:'소리의 박자가 움직임의 기준이 됩니다',subtitle:'같은 박자에 크기·선·글자가 서로 다른 방식으로 반응합니다',number:'02',heading:'움직임과 효과',kinds:['pulse','wave','words'],labels:['크기의 반응','선의 반응','글자의 반응'],ens:['Pulse','Wave','Rhythmic Type'],descs:['박자에 맞춰 커졌다 작아짐','소리의 느낌을 떨리는 선으로','강조되는 단어가 박자마다 바뀜'],bottom:'박자 점등과 화면 반응을 맞춘 무음 예시입니다',time:'04:04–04:38 및 설명란의 악기별 움직임 설명',note:'영상은 악기별 소리와 화면 움직임의 연결을 소개합니다. 여기서는 원본 음악을 사용하지 않고 점등되는 네 박자와 동기화된 크기·선·글자의 자체 반복 GIF를 제시합니다. GIF에는 소리가 없으며 음성 분석이나 실제 음원에 반응하는 결과라고 설명하지 않습니다.'}
];
const specs=[];
for(const def of definitions){
 const s=template.duplicate(),keep=new Set(['part_label','section_number','section_heading','title','subtitle','copyright_footer','clear-content',...Array.from({length:3},(_,i)=>'effect-card-'+i),...Array.from({length:3},(_,i)=>'effect-name-'+i),...Array.from({length:3},(_,i)=>'effect-en-'+i),...Array.from({length:3},(_,i)=>'effect-desc-'+i)]);
 const remove=s.shapes.items.filter(x=>!keep.has(x.name)).map(x=>x.name);for(const x of [...s.shapes.items])if(!keep.has(x.name))x.delete();
 const edits={part_label:'Part 1  모션 그래픽 기본 지식',section_number:def.number,section_heading:def.heading,title:def.title,subtitle:def.subtitle};
 for(let i=0;i<3;i++){edits['effect-name-'+i]=def.labels[i];edits['effect-en-'+i]=def.ens[i];edits['effect-desc-'+i]=def.descs[i];}
 for(const[name,value]of Object.entries(edits)){const sh=s.shapes.items.find(x=>x.name===name);sh.text.replace(String(sh.text),value);if(name.startsWith('effect-desc-'))sh.position={...sh.position,top:606,height:28};}
 const images=[];
 for(let i=0;i<3;i++){
  const kind=def.kinds[i],file=path.join(U,'assets/video-tones-20261028',kind+'.gif'),poster=path.join(U,'assets/video-tones-20261028',kind+'-poster.png');
  const pos={left:196+i*320,top:451,width:248,height:139.26};
  const before=new Set(s.images.items.map(x=>x.id));s.images.add({blob:new Uint8Array(await fs.readFile(poster)),contentType:'image/png',fit:'contain',position:pos});
  images.push({file,poster,name:'tone-demo-'+kind,position:pos});
 }
 const bottom=s.shapes.add({name:'tone-takeaway',geometry:'textbox',position:{left:170,top:650,width:943,height:30},fill:'none',line:{fill:'none',width:0}});bottom.text=def.bottom;bottom.text.style={typeface:'Pretendard',fontSize:19,color:'#FF9228',alignment:'center',verticalAlignment:'middle'};bottom.text.insets=0;
 const notes=def.note+'\n참고: Ai-Con Lab, 「클로드로 만든 모션그래픽 20가지 톤, 전부 코드로 그렸습니다」 https://www.youtube.com/watch?v=oCRQP5S-900 , '+def.time+'. 한국어 자막과 설명란을 분석했습니다. 원본 화면·음원·캐릭터·문구는 복제하지 않았습니다.';s.speakerNotes.text=notes;
 specs.push({page:def.page,source_page:8,export_id:s.id,edits,remove,images,notes});
}
await(await PresentationFile.exportPptx(p)).save(path.join(B,'roundtrip.pptx'));
for(const sp of specs)sp.export_page=p.slides.items.findIndex(x=>x.id===sp.export_id)+1;
await fs.writeFile(path.join(B,'edits.json'),JSON.stringify(specs,null,2));console.log('Authored four new slides using the current three-card layout.');
