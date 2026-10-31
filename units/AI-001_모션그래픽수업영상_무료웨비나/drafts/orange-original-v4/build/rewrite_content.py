from pathlib import Path
p=Path(__file__).with_name('build.mjs')
s=p.read_text(encoding='utf-8')
start=s.index("{\n const s=await base('agenda')")
end=s.index('await fs.mkdir(renders',start)
new=r'''
async function fiveCards(part,section,title,subtitle,items,summary) {
 const s=await base('five-elements'),t=spec.templates['five-elements'];
 heading(s,t,part,'01',section);
 slot(s,'title',title,t.title,white,true,'center');
 slot(s,'subtitle',subtitle,t.subtitle,white,false,'center',1.265);
 for(let i=0;i<5;i++){
  const x=t.card_lefts[i],w=t.card_width;
  txt(s,'number_'+i,String(i+1),[x,t.number_y,w,27],t.number_size,'#111820',true,'center');
  txt(s,'heading_'+i,items[i][0],[x,t.heading_y,w,45],t.heading_size,white,true,'center');
  txt(s,'description_'+i,items[i][1],[x,t.description_y,w,32],t.description_size,gray,false,'center');
  txt(s,'tag_'+i,items[i][2],[x,t.tag_y,w,27],t.tag_size,white,true,'center');
 }
 slot(s,'summary_label','수업 기준',t.summary_label,'#111820',true,'center');
 slot(s,'summary_text',summary,t.summary_text);
 common(s);return s;
}
{
 const s=await fiveCards('무료 웨비나  전체 흐름','다섯 단계로 직접 만들기',
  '수업 영상을 만드는 다섯 단계',
  '질문을 보여 주는 짧은 영상에서 시작해\n장면 계획과 외부 제작까지 연결합니다',
  [['단순 요청','수업 시작 질문 만들기','첫 결과'],['레퍼런스','토의 안내 배치 정하기','이미지 참고'],['모션 지식','읽기와 시선 확인','시간'],['문서 설계','활동 순서를 파일로','장면'],['외부 제작','교사 캐릭터 장면','클립 생성']],
  '내 수업에 필요한 결과부터 작게 만들어요');
 notes(s,'이번 사용자가 지정한 다섯 단계 순서로 새로 작성한 목차입니다. R02의 5칸 카드 구조만 사용하고 원래 모션 이론 문구는 가져오지 않았습니다. 수업 시작 질문과 짝 토의 안내는 이번 웨비나의 자체 실습 예시입니다.');
}
{
 const s=await fiveCards('Part 3  수업에 맞는 움직임 고르기','학생 화면으로 검토하기',
  '학생이 따라올 수 있는 영상인가요?',
  '보기 좋은 효과와 함께, 학생이 읽고 이해하고\n무엇을 할지 알 수 있는지 확인합니다',
  [['읽기','질문을 읽을 시간','문구 · 대비'],['시선','핵심어만 먼저 강조','크기 · 강조'],['순서','한 번에 하나씩','시간'],['행동','할 일을 구체적으로','안내'],['정리','마지막 과제 유지','마지막 화면']],
  '학생이 할 일을 순서대로 보여 줘요');
 notes(s,'교사용 자체 점검 기준으로 작성한 장표입니다. 원본의 대상·속성·시간·곡선·순서 목록을 문구만 바꿔 반복하지 않습니다. 예시 영상의 질문 가독성, 핵심어, 학생 행동과 마무리 과제를 실제 재생으로 확인합니다. 일반 모션 개념은 별도 근거와 함께 설명합니다.');
}
{
 const s=await base('brief'),t=spec.templates.brief;
 heading(s,t,'Part 4  다음 수업에도 다시 쓰는 제작 문서','01','학습 목표와 화면 규칙');
 slot(s,'title','내 수업에 맞는 세 문서를 만들어요',t.title,white,true,'center');
 slot(s,'subtitle','학생이 할 일과 영상의 표현 규칙을 나누어 적습니다',t.subtitle,white,false,'center');
 for(const [i,v] of ['문서','이 강의에서 적을 내용','바꾸어 볼 수업 조건'].entries())txt(s,'table_header_'+i,v,t.column_headers[i],20,white,true,'center');
 slot(s,'start_label','짝 토의 안내',t.start,white,true,'center');
 const rows=[['LESSON_BRIEF.md','학생·학습 목표\n질문과 핵심 과제','오늘의 질문에 대해\n생각의 근거 한 가지 말하기'],
 ['VISUAL_RULES.md','읽는 시간·색\n강조·등장 규칙','주황 핵심어 / 긴 질문은\n읽는 구간을 늘리기'],
 ['SCENE_PLAN.md','4개 장면의\n시간·문구·행동','질문 4초 · 혼자 쓰기 6초\n짝 나눔 8초 · 함께 정리 6초']];
 for(let r=0;r<3;r++)for(let c=0;c<3;c++){
  const [x,w]=t.column_boxes[c],value=rows[r][c],lines=value.split('\n').length,size=c===0?25:t.detail_size;
  txt(s,`cell_${r}_${c}`,value,[x+25,t.row_tops[r]+(lines===2?19:34),w-50,76],size,c===1?'#000000':(c===2?'#BFBFBF':white),c===0,'left',1.42);
 }
 common(s);notes(s,'三个文档名称和课堂案例为本次新编内容。4+6+8+6=24秒是新编课堂活动说明视频的四镜头时长，不是学生实际讨论时长。这里仅沿用来源的三列三行视觉结构。尚未生成实际课堂视频，不能把本页视为工具执行成功证据。');
}
{
 const s=await base('prompt'),t=spec.templates.prompt;
 heading(s,t,'Part 5  外部 영상 제작 도구와 연결하기','01','교사 캐릭터 장면 만들기');
 slot(s,'title','장면표의 한 장면을 영상으로 확장해요',t.title,white,true,'center');
 slot(s,'subtitle','질문을 건네는 교사 장면과 정확한 문구를 따로 준비합니다',t.subtitle,white,false,'center');
 for(const [i,key] of ['claude','codex','higgsfield'].entries()){
  const icon=new Uint8Array(await fs.readFile(path.join(workspaceDir,'assets/tool-logos/orange-v2/png',key+'-front.png')));
  s.images.add({blob:icon,contentType:'image/png',fit:'contain',position:P(395+i*143,615,140,140),alt:key+' 주황 포인트 도구 소개 배지'});
 }
 txt(s,'tool_caption','대화형 AI와 외부 영상 제작 도구',[395,786,426,48],24,gray,false,'center');
 slot(s,'prompt_label','SCENE_PLAN.md의 한 장면',t.prompt_label,gray);
 slot(s,'prompt_body','교사 캐릭터가 질문하는\n짧은 영상을 만들어 줘.\n글자는 별도로 넣을게.',t.prompt_body,'#000000',true,'left',1.412);
 common(s);notes(s,'왼쪽은 실제 제품 화면이 아닌 도구 소개 배지입니다. 이번 웨비나용 새 요청 문구를 사용했습니다. 장면표를 AI가 해석한 뒤 실제 모델이 지원하는 입력과 길이·비율로 요청합니다. 도구가 확정되면 지원 조건을 검증합니다. 본 장표는 외부 업로드·생성 또는 모델별 기능 성공의 증거가 아닙니다.');
}
'''
s=s[:start]+new+s[end:]
s=s.replace("renders/orange-cover-v3","renders/orange-original-v4")
s=s.replace("pink='#FB3890'","pink='#FF9228'")
s=s.replace('NotionTalk_모션그래픽_주황표지_대표5장_v3.pptx','NotionTalk_모션그래픽_주황포인트_자체사례_v4.pptx')
s=s.replace('validation-orange-cover.json','validation-orange-original.json')
s=s.replace('三个文档名称和课堂案例为本次新编内容。4+6+8+6=24秒是新编课堂活动说明视频的四镜头时长，不是学生实际讨论时长。这里仅沿用来源的三列三行视觉结构。尚未生成实际课堂视频，不能把本页视为工具执行成功证据。',
 '세 문서 이름과 교실 사례는 이번 강의를 위해 새로 작성했습니다. 4+6+8+6=24초는 활동 안내 영상의 네 장면 길이이며 학생의 실제 토의 시간이 아닙니다. 원본의 3열·3행 시각 구조만 참고했습니다. 실제 활동 안내 영상을 생성한 상태는 아니므로 도구 실행 성공 증빙으로 사용하지 않습니다.')
s=s.replace('外部 영상','외부 영상')
p.write_text(s,encoding='utf-8')
print('Updated representative content and orange accent; source layouts and existing cover retained.')
