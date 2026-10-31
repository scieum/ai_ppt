from pathlib import Path
import json,shutil,hashlib
R=Path.cwd();B=R/'output/image-explain-build';U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';A=U/'assets/image-explain-20261029';H=U/'history/image-explain-20261029';H.mkdir(parents=True,exist_ok=True)
old='NotionTalk_모션그래픽_레퍼런스표현강화_40장_v20';new='NotionTalk_모션그래픽_이미지설명강화_40장_v21'
for name in ['plan.md','design.md','part-0.md','part-1.md','part-2.md','part-3.md','part-4.md']:
 f=U/name;shutil.copy2(f,H/name)
 if name!='design.md':
  s=f.read_text(encoding='utf-8-sig').replace(old,new).replace('40장 v20','40장 v21')
  s=s.replace('| 24 | 비슷한 톤을 다시 얻고 싶다면','| 24 | 같은 톤, 서로 다른 장면').replace('| 30 | 문서와 확인 자료를 함께 봅니다','| 30 | 스틸컷은 모습, 재생은 움직임')
  if name in ['plan.md','part-3.md','part-4.md']:
   s+='\n## 이미지 중심 설명 — 2026-10-29\n\n24쪽은 일관된 곰 캐릭터의 세 상황으로 같은 톤을 설명하고 design.md·motion.md 제작 추천을 유지한다. 30쪽은 한 컷과 연속 장면을 큰 이미지로 대조한다. 오른쪽 그림은 정지 예시임을 명시하고 실제 움직임은 구간 재생으로 확인한다. 38쪽은 한 장면만 색을 바꾸는 경우와 모든 장면의 기본색을 바꾸는 경우를 비교한다. 장면별 예외는 장면표, 공통 색은 design.md에 기록한다. 공통 시간 변경은 motion.md에 같은 방식으로 반영한다. 세 장의 긴 문구를 줄이고 상세 설명은 앞뒤 장표와 노트에서 이어 간다. 총 40장과 나머지 37장·기존 움직임은 보존한다.\n'
  f.write_text(s,encoding='utf8')
prefix=f'''# 현재 디자인 기준 — 이미지 중심 설명

2026-10-29 / 현재 40장 v21. 결과물은 output/webinar-knowledge-only/{new}.pptx와 PDF다.

텍스트가 연속되는 구간에서 24·30·38쪽을 큰 이미지, 짧은 제목과 한두 설명 문장으로 구성한다. 24쪽은 같은 캐릭터의 서로 다른 세 장면, 30쪽은 한 컷과 연속 장면, 38쪽은 일부 색 변경과 전체 색 변경이다. 문구·표 옆의 장식이 아니라 이미지 자체로 차이를 이해하게 한다. 이미지마다 설명하는 개념이 있어야 하며 같은 그림을 반복하지 않는다.

기존 주황·흑백·Pretendard·노션톡 원본 로고·저작권과 40장 순서를 유지한다. 나머지 37장과 모든 기존 미디어·효과는 보존한다. 새 이미지는 assets/image-explain-20261029/에 있고 내장 image_gen 프롬프트·참조·해시를 기록한다. 24쪽 새 곰 이미지는 사용자 캐릭터 외형을 참조했으며 기존 여성 설명 포즈는 그 장에서 제거했다. 나머지 본문 포즈와 표지는 유지한다.

38쪽 하늘색은 변경 범위를 보여 주는 교육용 사례이며 브랜드 변경이 아니다. 30쪽 오른쪽은 실제 재생 영상이 아닌 정지 연속 장면 그림이다. 움직임 확인은 구간을 재생해야 한다. 기존 33개 GIF, 6·11·20쪽 네이티브 타이밍, 22·25·33·34쪽 편집 가능한 표를 유지한다. 기본 하네스와 lesson.md, 영상 예시 문서, 상속 G10 상태는 변경하지 않는다.

## 이전 기준 기록

'''
(U/'design.md').write_text(prefix+(H/'design.md').read_text(encoding='utf-8-sig'),encoding='utf8')
short=f'''## 최신 이미지 중심 설명 — 2026-10-29

현재 강의는 output/webinar-knowledge-only/{new}.pptx와 PDF다. 사용자가 텍스트가 빽빽하다고 지적해 24·30·38쪽을 큰 설명 이미지 중심으로 바꿨다. 같은 톤의 다른 장면, 스틸컷과 연속 장면, 한 장면/공통 색 변경을 각각 시각화한다. 긴 문구는 줄이고 상세 내용은 앞뒤 장표와 노트에서 이어 간다. 총 40장과 나머지 37장·기존 미디어·효과·기본 디자인은 유지한다. 24쪽 여성 설명 포즈는 새 곰의 일관된 세 장면으로 대체했다. 단원 plan.md·design.md·part 문서가 현재 기준이며 아래 내용은 이전 이력이다.

'''
for name in ['AGENTS.md','design.md']:
 f=R/name;f.write_text(short+f.read_text(encoding='utf-8-sig'),encoding='utf8')
prompts=json.loads((A/'prompts.json').read_text(encoding='utf8'));manifest={'tool':'built-in image_gen','date':'2026-10-29','assets':[]}
for d,n in zip(prompts,[24,30,38]):
 file=d['key']+'.png';manifest['assets'].append({**d,'file':file,'page':n,'sha256':hashlib.sha256((A/file).read_bytes()).hexdigest()})
(A/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
readme='# 이미지로 이해하는 장표 에셋\n\n2026-10-29 / 내장 image_gen으로 생성. 원본 PNG 바이트 그대로 저장했으며 한 자산을 한 장표에만 쓴다. 모든 프롬프트와 참조·SHA-256은 [manifest.json](manifest.json)에 있다.\n\n'
for d in manifest['assets']:readme+=f"## {d['page']}쪽\n\n[{d['file']}]({d['file']})\n\n{d['prompt']}\n\n"
readme+='30쪽은 정지 연속 장면 그림이며 실제 영상이나 실제 속도 검증 결과가 아니다. 38쪽 파란색은 변경 범위 예시다. 상속 자산의 권리 상태는 별도로 유지한다.\n';(A/'README.md').write_text(readme,encoding='utf8')
print('Documents and asset provenance updated')
