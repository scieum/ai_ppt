from pathlib import Path
import zipfile,re,json
B=Path(__file__).resolve().parent;U=B.parents[2];R=U.parents[1]
old='../../output/webinar-fundamentals/NotionTalk_모션그래픽_개념부터실습까지_21장_v2'
new='../../output/webinar-flipbook/NotionTalk_플립북설명추가_22장_v1'
intro='''## 플립북 설명 추가 — 2026-10-28

최신 반영본은 플립북을 추가한 22장이다. ‘01 모션 그래픽 이해하기’의 5쪽에 물리적 플립북 삽화·미세하게 달라지는 여섯 프레임·PPT 내부에 포함한 GIF를 넣었다. 모션 그래픽도 시간에 따라 상태가 조금씩 달라지는 장면을 이어 보여 주지만, 모든 프레임을 손으로 그려야 한다는 뜻은 아니다.

기존 정의 설명 1.5분 안에서 약 40초를 배분하므로 전체 90분·Part 1 26분 제안은 유지한다. 최신 묶음 대응은 01 이해하기 4~6쪽, 02 움직임과 효과 7~11쪽, 03 제작 예제 12~18쪽, 04 적용 19쪽이다. 기존 대표 5장 대응은 1·2·20·21·22쪽이다. 원본 21장과 번호 묶음·디자인·기존 애니메이션은 보존했다.

에셋·원본 파일·생성 프롬프트는 [플립북 에셋 README](../../assets/flipbook/20261028/README.md)에 있다. 삽화는 생성 이미지이고 프레임·GIF는 별도의 자체 다이어그램이다. PDF에는 GIF의 정지 프레임을 표시한다. G10 승인을 생성하지 않는다.

'''
ranges={'4~5쪽':'4~6쪽','6~10쪽':'7~11쪽','11~17쪽':'12~18쪽','4~10쪽':'4~11쪽','11~18쪽':'12~19쪽'}
for filename in ['plan.md','part-1.md']:
 p=U/filename;s=p.read_text(encoding='utf-8');s=s.replace(old,new).replace('21장','22장');s=re.sub('|'.join(map(re.escape,ranges)),lambda m:ranges[m[0]],s)
 pos=s.index('\n\n');s=s[:pos+2]+intro+s[pos+2:]
 s=s.replace('| 04 | 내 수업에 적용하기 | 18쪽 |','| 04 | 내 수업에 적용하기 | 19쪽 |')
 p.write_text(s,encoding='utf-8')
p=U/'plan.md';s=p.read_text(encoding='utf-8');m=re.search(r'```harness-plan\s*\n(.*?)\n```',s,re.S);j=json.loads(m[1]);action='정지 디자인과 움직임을 비교하고 플립북의 미세한 여섯 그림과 반복 재생을 설명한다';j['slides'][4]['instructor_action']=action;s=s[:m.start(1)]+json.dumps(j,ensure_ascii=False,indent=2)+s[m.end(1):];rows=s.splitlines()
for i,row in enumerate(rows):
 if row.startswith('| 5 | '):
  cols=row.split('|');cols[4]=' '+action+' ';rows[i]='|'.join(cols)
p.write_text('\n'.join(rows)+'\n',encoding='utf-8')
qa=(U/'drafts/foundations-20261028/build/qa-video.ps1').read_text(encoding='utf-8');source=str(R/'output/webinar-flipbook/NotionTalk_플립북설명추가_22장_v1.pptx').replace('\\','/');qa=qa.replace("(Join-Path $build 'native-animation.pptx')","'"+source+"'").replace('@(4,6,7,8,9)','@(5)').replace('effect-playback-check.mp4','flipbook-playback-check.mp4').replace('five animated demonstration slides','flipbook demonstration slide');(B/'qa-video.ps1').write_text(qa,encoding='utf-8')
with zipfile.ZipFile(R/'output/webinar-flipbook/NotionTalk_플립북_에셋.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in (R/'assets/flipbook/20261028').iterdir():
  if p.is_file():z.write(p,'flipbook/'+p.name)
print('Synchronized planning notes and created the asset ZIP.')
