from pathlib import Path
import shutil,re
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
prior=U/'drafts/reflow-mascots-20261028/build'
script=(prior/'finalize.mjs').read_text(encoding='utf-8').replace('NotionTalk_모션그래픽_19장_영상핵심5장확장_v8.pptx','NotionTalk_모션그래픽_흐름정리_캐릭터_16장_v10.pptx').replace('const tables=[13,15]','const tables=[14,16]').replace('NotionTalk_모션그래픽_흐름정리_캐릭터_16장_v10.pptx\'),pythonExecutable','NotionTalk_모션그래픽_준비물복원_17장_v11.pptx\'),pythonExecutable').replace('explicitTotalSlideCount:16','explicitTotalSlideCount:17').replace('validation-v10.json','validation-v11.json')
(B/'finalize.mjs').write_text(script,encoding='utf-8')
export=(prior/'export.ps1').read_text(encoding='utf-8-sig').replace('NotionTalk_모션그래픽_흐름정리_캐릭터_16장_v10','NotionTalk_모션그래픽_준비물복원_17장_v11').replace('renders/reflow-mascots-20261028','renders/restore-preparation-20261028').replace('-ne 16','-ne 17').replace('Expected 16','Expected 17').replace('opened 16','opened 17')
(B/'export.ps1').write_text(export,encoding='utf-8-sig')
archive=U/'history/before-preparation-restore-20261028';archive.mkdir(parents=True,exist_ok=True)
for name in ['plan.md','design.md']+[f'part-{i}.md' for i in range(6)]:
 if not (archive/name).exists():shutil.copy2(U/name,archive/name)
plan=(U/'plan.md').read_text(encoding='utf-8')
plan=plan.replace('16장_v10','17장_v11').replace('흐름정리_캐릭터_17장_v11','준비물복원_17장_v11')
plan=plan.replace('## 진행 흐름','## 준비물 복원\n\n최신 사용자 지시에 따라 기존 준비물 장표를 2쪽에 복원했다. 표지 → 준비물 → 전체 흐름 → 기본 지식으로 시작한다. 클로드 또는 코덱스 중 하나의 유료 계정이 필수이며, 힉스필드는 선택 사항이다. 힉스필드 계정이 없으면 강사 시연을 본다. 앞서 제작한 세 도구 배지와 원래 준비물 장표의 디자인을 그대로 사용한다. 기존 16장과 움직임 예시는 보존해 총 17장이다. 아래 네 단계는 준비물 확인 후 시작한다.\n\n## 진행 흐름')
plan=plan.replace('| 도입 | 1–2 | 기존 표지와 네 단계 목차 |','| 도입·Part 0 | 1–3 | 기존 표지, 준비물, 네 단계 목차 |').replace('| 3–11 |','| 4–12 |').replace('| 12 |','| 13 |').replace('| 13–14 |','| 14–15 |').replace('| 15–16 |','| 16–17 |')
start=plan.index('## 전체 장표');end=plan.index('## 중복 통합')
titles=['표지','오늘의 준비물','오늘의 네 단계','모션 그래픽이란?','플립북으로 보는 움직임','모션 그래픽의 다섯 종류','움직임을 만드는 네 가지 속성','페이드·슬라이드·줌','리빌·타이프라이터·순차 등장','모핑·입체 회전·그라데이션 흐름','시작 시점과 지속시간','가속과 감속의 세 가지 모습','이미지·영상 레퍼런스 함께 넣기','storyline.md로 흐름 확인','대표 스틸컷 두 장으로 미리 보기','고칠 부분을 정하고 다시 확인','확인한 방향으로 영상 제작']
plan=plan[:start]+'## 전체 장표\n\n| 쪽 | 주제 |\n|---:|---|\n'+'\n'.join(f'| {i} | {t} |' for i,t in enumerate(titles,1))+'\n\n'+plan[end:]
# Keep the prior consolidation mapping as explicitly historical rather than current page numbers.
plan=plan.replace('## 중복 통합','## 이전 16장 구성의 중복 통합 이력').replace('기존 19장 원본','이전 19장 원본')
plan=plan.replace('3·5·12·13·14·16쪽','4·6·13·14·15·17쪽')
(U/'plan.md').write_text(plan,encoding='utf-8')
design=(U/'design.md').read_text(encoding='utf-8').replace('16장 흐름 정리','17장 준비물 복원').replace('v10','v11')
design=design.replace('2쪽은 기존 레퍼런스','3쪽은 기존 레퍼런스')
for old,new in [(16,17),(14,15),(13,14),(12,13),(5,6),(3,4)]:design=design.replace(f'| {old} |',f'| PAGE{new} |')
design=re.sub(r'PAGE(\d+)',r'\1',design).replace('3·12쪽','4·13쪽').replace('5·13쪽','6·14쪽').replace('14쪽 문구','15쪽 문구').replace('16쪽은 기존','17쪽은 기존').replace('16장 PNG','17장 PNG')
design=design.replace('## 유지','## 준비물 복원\n\n2쪽에 이전 준비물 장표를 원본 그대로 복원했다. 앞서 제작한 Claude·Codex·Higgsfield 도구 배지, 문구, 구분선, 위치, Pretendard, 로고와 푸터를 유지한다. 그 외 기존 16장 슬라이드 XML과 모든 미디어·움직임을 보존한다.\n\n## 유지')
(U/'design.md').write_text(design,encoding='utf-8')
(U/'part-0.md').write_text('# 도입과 준비물\n\n2026-10-28 / 현재 17장 v11 기준.\n\n1쪽 표지 → 2쪽 오늘의 준비물 → 3쪽 네 단계 목차.\n\n클로드 또는 코덱스 중 하나의 유료 계정이 필수다. 힉스필드는 있으면 좋고 없으면 강사 시연을 본다. 앞서 제작한 세 도구 배지와 기존 준비물 디자인을 복원했다. 기존 네 단계와 본문은 유지한다.\n',encoding='utf-8')
for n,old,new in [(1,'3–11','4–12'),(2,'12쪽','13쪽'),(3,'13–14','14–15'),(4,'15–16','16–17')]:
 p=U/f'part-{n}.md';s=p.read_text(encoding='utf-8').replace('16장 v10','17장 v11').replace(old,new);p.write_text(s,encoding='utf-8')
p=U/'part-5.md';p.write_text(p.read_text(encoding='utf-8').replace('16장','17장').replace('v10','v11'),encoding='utf-8')
p=R/'AGENTS.md';p.write_text('## 최신 준비물 복원 — 2026-10-28\n\n현재 기준은 `output/webinar-knowledge-only/NotionTalk_모션그래픽_준비물복원_17장_v11.pptx`와 PDF다. 최신 사용자 요청으로 기존 준비물 장표를 표지 다음 2쪽에 복원했다. 클로드 또는 코덱스 중 하나의 유료 계정 필수, 힉스필드는 선택이며 없으면 시연을 본다는 기존 안내를 유지한다. 전체 흐름은 3쪽, 기본 지식은 4–12쪽, 이미지·영상 레퍼런스는 13쪽, storyline.md·스틸컷 두 장은 14–15쪽, 수정 후 제작은 16–17쪽이다. 기존 16장 디자인·삼인방·GIF·타이밍·기본 하네스·lesson.md·상속 G10 상태는 보존한다. 아래 이전 버전의 준비물 제외는 최신 복원 요청에 우선하지 않는다.\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
print('Prepared finalization, native export and current 17-slide documents.')
