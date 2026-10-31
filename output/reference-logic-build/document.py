from pathlib import Path
import shutil,json,hashlib
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';A=R/'assets/layout-library-20261028/logic-patterns-20261030'
assert (U/'checks/reference-logic-20261030/verification.json').exists()
refs=['56485ada-1a9a-45a1-a8b3-29f0f8b74109','bce621b6-e672-4e1c-b2e7-b352cea22029','64c144b1-1847-4621-9ffe-66cd0ac1c5b5','e0d2ea86-4978-454e-8831-18171cf16341','f637c771-1843-480a-aaf7-2221c2088c91','6000ed83-4096-43be-86f7-c7aee164e2c0','035c9349-87d2-4185-ba81-88321f2b2269','68d93889-922e-4674-b502-80fa7f347f57'];manifest=[]
(A/'references').mkdir(exist_ok=True)
for i,ref in enumerate(refs,1):
 src=Path('C:/Users/User/AppData/Local/Temp')/f'codex-clipboard-{ref}.png';dst=A/'references'/f'reference-{i:02d}.png';shutil.copy2(src,dst)
 manifest.append({'attachment':i,'source':str(src),'internal_reference_copy':str(dst.relative_to(R)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'used_as_slide_image':False})
(A/'manifest.json').write_text(json.dumps({'references':manifest,'mapping':json.loads((B/'spec.json').read_text(encoding='utf8'))},ensure_ascii=False,indent=2),encoding='utf8')
prefix='''## 최신 논리 구조 에셋 반영 — 2026-10-30

현재 강의는 `output/webinar-knowledge-only/NotionTalk_모션그래픽_논리구조에셋반영_43장_v31.pptx`와 PDF다. 사용자 제공 캡처의 비교·분기·단계·확인 지점·결론 띠를 기존 웨비나 내용에 맞춰 5개 장표에 적용했다. 총 43장과 순서, 공통 상단·제목·부제·푸터, 준비물 3쪽 박스·간격, 기존 이미지와 움직임을 유지한다. 나머지 38장은 XML과 PDF 픽셀 모두 v30 그대로다.

- 20쪽: 한 질문에서 이미지의 디자인 기준과 영상의 모션 기준으로 갈라지는 분기. 기존 여성 캐릭터와 모션 강조 효과 유지.
- 36쪽: 스틸컷→짧은 구간→전체 영상의 세 단계 카드. 기존 스틸컷 예시와 4–7초/15초 예시 유지.
- 37쪽: 점검 기준·질문·함께 볼 자료를 연결하는 탭과 4행 비교. 네이티브 표로 편집 가능하며 기존 남성 검토 캐릭터 유지.
- 39쪽: 섞인 문서·분리된 자산·오래된 장면표와 확인한 자료 묶음을 좌우로 대비. 다음 주제의 storyline.md와 확정 design.md·motion.md를 함께 전달하는 의미 유지.
- 40쪽: 기준 확인→스틸컷 수정→전체 제작의 단계와 결과물을 연결하고 제작 전 확인 지점을 표시. 기존 승인 포즈 캐릭터 유지.

주황·검정·어두운 회색을 기본으로 하며 대조와 확인 자료에는 보조 파랑을 제한적으로 사용한다. 원본의 흰 표 셀·핑크 포인트·펭귄·로고·주제 문구는 가져오지 않는다. 관련 없는 장표에 에셋을 억지로 추가하지 않는다. 이미 적합한 기존 25·33·34쪽 어두운 표는 유지한다.

재사용 에셋·출처 매핑은 `assets/layout-library-20261028/logic-patterns-20261030/`에 있다. 검증은 단원 `checks/reference-logic-20261030/verification.json`, 렌더는 `renders/reference-logic-20261030/`다. 기존 G10 상태는 유지하며 법적 권리 승인으로 간주하지 않는다. 아래는 이전 이력이다.

'''
for p in [R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md',U/'part-2.md',U/'part-4.md']:
 backup=U/'history/reference-logic-20261030'/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(p,backup)
 s=p.read_text(encoding='utf-8-sig')
 if not s.startswith('## 最新 논리 구조 에셋 반영') and not s.startswith('## 최신 논리 구조 에셋 반영'):p.write_text(prefix+s,encoding='utf8')
print('Recorded five slide mappings, reusable patterns, sources and current version.')
