from pathlib import Path
import shutil,json,hashlib
R=Path.cwd();B=R/'output/reference-style-build';U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';A=U/'assets/reference-style-20261029'
history=U/'history/reference-style-20261029';history.mkdir(parents=True,exist_ok=True)
old='NotionTalk_모션그래픽_Part3_Part4확장_40장_v19';new='NotionTalk_모션그래픽_레퍼런스표현강화_40장_v20'
for name in ['plan.md','design.md','part-0.md','part-1.md','part-2.md','part-3.md','part-4.md']:
 f=U/name;shutil.copy2(f,history/name)
 if name!='design.md':
  s=f.read_text(encoding='utf-8-sig').replace(old,new).replace('40장 v19','40장 v20')
  if name in ['part-3.md','part-4.md']:
   s+='\n## 표현 강화 — 2026-10-29\n\n'+('24쪽은 문서 두 개와 설명하는 여성 포즈, 26쪽은 화면과 네 방향 주석, 27쪽은 큰 밝은 문서, 28~29쪽은 시간 흐름과 간격 도식, 30쪽은 어두운 문서와 밝은 확인 자료의 대조, 31쪽은 주황 폴더와 파일 목록을 사용한다.'if name=='part-3.md'else'34쪽은 대비가 명확한 수정 기준 표, 35쪽은 실제 제목 크기의 전후 비교, 36쪽은 스틸컷·구간·전체의 시각 비교, 37쪽은 검토 포즈와 체크 목록, 38쪽은 한 장면/전체 장면의 시간 비교, 39쪽은 문서와 같은 버전의 확인 자료 연결을 사용한다.')+' 기존 내용과 순서를 유지하며 설치·앱 조작·긴 프롬프트를 추가하지 않는다.\n'
  if name=='plan.md':s+='\n## 레퍼런스 표현 강화 — 2026-10-29\n\n새로 추가한 14장(24~31, 34~39)을 원본 PDF의 문서 확대·파일 에셋·좌우 대비·주석·체크리스트 표현에 맞춰 개정했다. 나머지 26장·원본 미디어·효과는 보존한다. 추가 이미지는 파일 묶음을 뜻하는 주황 폴더 한 개, 기존 캐릭터 시트의 여성 설명·남성 검토 포즈 각 한 번이다. 자료와 무관한 장식을 늘리지 않는다.\n'
  f.write_text(s,encoding='utf8')
design='''# 현재 디자인 기준 — 레퍼런스 표현 강화

2026-10-29 / 현재 40장 v20. 결과물은 output/webinar-knowledge-only/NotionTalk_모션그래픽_레퍼런스표현강화_40장_v20.pptx와 PDF다.

## 유지할 기준

검정 바탕, 흰 제목, 주황 #FF9228, Pretendard, 우측 위 NotionTalk 원본 로고와 저작권을 유지한다. 40장 순서와 파트 전환·목차·준비물·기본 지식은 그대로다. 새로 추가했던 14장의 시각 표현을 개정하고 나머지 26장의 슬라이드 XML과 모든 기존 미디어를 보존한다.

## 레퍼런스를 사용하는 방식

R01·R03 PDF의 중앙 제목, 넓은 여백, 큰 문서 패널, 어두운 질문과 밝은 답변의 대비, 파일 묶음, 주석, 전후 비교와 체크 목록을 따른다. 참고 문구·원본 화면·펭귄을 복제하지 않고 노션톡 예시와 자체 자산으로 구성한다. 신규 표는 파일·기준·결과의 행 관계를 비교할 때만 유지한다. 설명을 전부 같은 카드나 표로 바꾸지 않는다.

| 쪽 | 표현 |
|---:|---|
| 24 | 밝은 design.md·어두운 motion.md 사이의 여성 설명 포즈 |
| 25 | 어두운 분류 열과 밝은 설명 영역의 네이티브 표 |
| 26 | 중앙 영상 화면에 색·글자·구도·자산 주석 |
| 27 | 크게 확대한 밝은 design.md 문서 |
| 28 | 등장·순차 등장·유지·전환의 시간 흐름 |
| 29 | 어두운 motion.md 문서와 시작 간격 도식 |
| 30 | 문서와 확인 자료를 어두운/밝은 행으로 대조 |
| 31 | 주황 3D 폴더, 파일 목록, 역할 연결 |
| 34 | 수정 대상·문서·검토 결과의 네이티브 표 |
| 35 | 제목 크기의 전후 화면을 직접 비교 |
| 36 | 스틸컷·3초 구간·15초 전체의 검토 범위 |
| 37 | 빈 체크 목록과 남성 검토 포즈 |
| 38 | 한 장면만 0.6초 / 세 장면 모두 0.6초의 대비 |
| 39 | 문서와 같은 버전의 실제 자산·확인 자료 묶음 |

## 이미지와 움직임

표지 삼인방은 보존한다. 본문 포즈는 기존 6·18·20·40쪽에 24쪽 여성 설명, 37쪽 남성 검토를 더한 서로 다른 여섯 포즈다. 기존 시트 원본과 PPT의 자르기를 사용하고 얼굴·의상·비율은 바꾸지 않는다. 주황 폴더는 31쪽 한 번만 사용한다. assets/reference-style-20261029/README.md와 manifest.json에 생성 도구·원문 프롬프트·해시를 보관한다.

네이티브 타이밍은 6·11·20쪽, 네이티브 표는 22·25·33·34쪽이다. 기존 33개 GIF와 모든 미디어 바이트를 보존한다. 문서·표·주석·시간 도식은 편집 가능한 요소다. 박자 예시는 무음 도식이고 PDF는 정지 보기다.

## 검토

참고 페이지와 적용 목록은 checks/reference-style-20261029/verification.json에 기록한다. 기존 자산의 상속 G10 상태는 변경하지 않는다. 이번 개정은 사용자의 디자인 수정 요청이며 별도 법률 판단이나 권리 승인으로 기록하지 않는다. 영상 예시 design.md·motion.md는 output/webinar-style-docs-examples/에 있으며 이 문서는 계속 PPT 하네스의 디자인 기준이다.

## 이전 기준 기록

'''
(U/'design.md').write_text(design+(history/'design.md').read_text(encoding='utf-8-sig'),encoding='utf8')
prefix=f'''## 최신 레퍼런스 표현 강화 — 2026-10-29

현재 강의는 output/webinar-knowledge-only/{new}.pptx와 PDF다. 새 14장(24~31, 34~39)의 문서·파일·주석·전후 비교·체크 목록 표현을 R01/R03 레퍼런스에 맞춰 강화했다. 26장과 모든 기존 미디어·움직임은 보존한다. 기존 시트에서 24쪽 여성 설명, 37쪽 남성 검토 포즈를 각 한 번 더 쓰며, 자체 생성 주황 폴더는 31쪽 한 번만 쓴다. 같은 컷 반복 장식과 무관한 이미지를 늘리지 않는다. 40장 순서, 주황·흑백, 노션톡 브랜드, lesson.md, 예시 문서, 기본 하네스와 상속 G10 상태를 유지한다. 단원 plan.md·design.md·part-3.md·part-4.md가 현재 기준이다. 아래 버전은 이력이다.

'''
for name in ['AGENTS.md','design.md']:
 f=R/name;f.write_text(prefix+f.read_text(encoding='utf-8-sig'),encoding='utf8')
manifest=json.loads((B/'asset-manifest.json').read_text(encoding='utf8'));manifest['sha256']=hashlib.sha256((A/'orange-folder-v1.png').read_bytes()).hexdigest();manifest['used_on_page']=31;manifest['character_poses']={'24':'woman-explain','37':'man-review'};manifest['references']=json.loads((B/'additions.json').read_text(encoding='utf8'));(A/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
(A/'README.md').write_text('''# 노션톡 레퍼런스 표현 에셋

2026-10-29. 내장 image_gen으로 주황 폴더 자산 하나를 생성하고 원본 PNG를 그대로 보관했다. [주황 폴더](orange-folder-v1.png)는 40장 v20의 31쪽에 사용한다. 투명 배경을 유지한다. [manifest.json](manifest.json)에 원문 프롬프트·SHA-256·페이지별 참고 목록을 기록했다.

캐릭터는 기존 character-sheets-20261028/의 여성 설명 포즈(24쪽)와 남성 검토 포즈(37쪽)를 PPT에서 자른다. 원본 시트를 수정하거나 같은 컷을 반복하지 않는다. 문서·비교·주석·체크 목록은 PPT에서 편집 가능하다.

## 생성 프롬프트

'''+manifest['prompt']+'\n',encoding='utf8')
print('Current docs and asset provenance updated')
