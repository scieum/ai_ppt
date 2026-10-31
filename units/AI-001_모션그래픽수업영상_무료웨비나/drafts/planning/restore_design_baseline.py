"""Restore the previous representative deck as the working visual baseline.

Do not modify slide binaries or invent a rights/design gate approval.
"""
from pathlib import Path
import hashlib,json,shutil

unit=Path(__file__).resolve().parents[2]
root=unit.parents[1]
deck=root/'output/webinar-samples/NotionTalk_모션그래픽_주황포인트_자체사례_v5.pptx'
pdf=deck.with_suffix('.pdf')
assert deck.is_file() and pdf.is_file()
history=unit/'history/before-baseline-restoration-20261027'
history.mkdir(parents=True,exist_ok=True)
for p in [unit/'design.md',unit/'plan.md',unit/'part-1.md',root/'AGENTS.md',root/'design.md']:
    target=history/((('root-' if p.parent==root else 'unit-'))+p.name)
    if not target.exists():shutil.copy2(p,target)

record={
 'user_feedback':'아까 만들었던 대표 5장이 진짜 괜찮았는데 왜 니맘대로 햇가지고 또 고이게 하니',
 'working_baseline':str(deck.relative_to(root)).replace('\\','/'),
 'baseline_identification':'기존 대표본 중 주황 표지·세 캐릭터·자체 사례가 반영된 가장 최근 v5를 작업 기준으로 복원. 사용자는 정확한 파일명을 명시하지 않았으며, 이를 정식 버전별 게이트 승인으로 기록하지 않는다.',
 'sha256':hashlib.sha256(deck.read_bytes()).hexdigest(),
 'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
 'rejected_replacement':'output/webinar-three-cases-v2/NotionTalk_Part1_예제와실제시연_v4.pptx',
 'preserve':['기존 대표 5장 자체','주황 그라데이션 표지','세 캐릭터','상단 안내와 제목 체계','회색 카드·문서 표·흰 프롬프트 박스','로고·푸터·서체·간격'],
 'change_scope':'사용자가 요청한 강의 내용·세 예제·실제 캡처만 기존 형식 안에서 반영. 전체 대표본 재설계로 확대하지 않는다.',
 'formal_design_gate_approval_created':False,'G10_clearance_created':False,
}
(unit/'checks/design-baseline.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')

rule='''## 최신 정정 — 기존 대표 5장을 디자인 기준으로 유지

사용자는 기존 대표 5장이 좋았다고 했고 직전의 임의 재구성을 거부했다. 작업 기준은 `output/webinar-samples/NotionTalk_모션그래픽_주황포인트_자체사례_v5.pptx`다. 주황 그라데이션 표지·세 캐릭터·상단 안내·중앙 제목·카드·문서 표·흰 프롬프트 박스·로고·푸터·서체·간격을 보존한다. 기존 파일을 덮어쓰거나 새 다섯 장으로 교체하지 않는다.

사용자가 선택한 세 예제와 Part 0 등 최신 내용은 유지한다. 새 예제·실제 앱 캡처는 기존 대표본의 해당 유형을 확장하고 내용 슬롯만 바꾼다. 캡처 개선 요청을 대표본 전체 재설계 허가로 해석하지 않는다. 직전 `webinar-three-cases-v2`의 새 5장은 비채택 검토 이력이며 후속 디자인 기준이 아니다.

기준 파일 식별·해시는 단원 `checks/design-baseline.json`에 기록했다. 사용자의 기존 대표본에 대한 긍정 평가와 정확한 파일명을 명시한 정식 게이트 승인을 구분한다. 기존 G10 검토 상태를 변경하지 않는다.

'''
design='''# 이번 웨비나의 장표·캡처 디자인 기준

2026-10-27 · 기존 대표 5장의 형식을 보존하는 사용자 정정 반영.

'''+rule+'''## 추가 장표 제작

먼저 기준 대표본에서 해당 유형을 고른다. 전체 흐름·영상 유형 소개는 카드, 모션 지식 설명은 같은 카드 체계, Markdown 설명은 기존 문서 표, 예제 요청은 기존 흰 프롬프트 박스 형식에 새 내용을 넣는다. 실제 앱 캡처도 기존의 제목·여백·상단 안내를 유지하며 자료 영역에 배치한다. 원본 PDF 좌표를 새로 고르며 이미 좋다고 한 대표본의 디자인을 다시 바꾸지 않는다.

단원 plan.md·part-1.md의 세 예제 조합과 Part 0 준비물은 유지한다. 기존 대표본의 오래된 질문 사례를 최신 내용으로 확정한 것으로 처리하지 않는다. 영상·실행 원본과 출처·권리 기록은 보존한다.

## 브랜드

노션톡 원본 로고와 `© 2026. NotionTalk. All rights reserved.`를 유지한다. 표지의 주황 그라데이션과 세 캐릭터를 교체하지 않는다.
'''
(unit/'design.md').write_text(design,encoding='utf-8')
agents=root/'AGENTS.md'
a=agents.read_text(encoding='utf-8')
needle='## 현재 작업 범위 — AI 사용법 연수 하네스 (2026-10-27)\n'
a=a.replace(needle,needle+'\n- 최신 디자인 정정: 사용자는 이전 대표 5장이 좋았다고 했으며 임의로 바꾼 직전 5장을 거부했다. 기존 주황 표지·세 캐릭터·자체 사례 대표본 v5(`output/webinar-samples/NotionTalk_모션그래픽_주황포인트_자체사례_v5.pptx`)를 작업 기준으로 유지한다. 원본 파일은 보존하며 새 예제·실제 캡처와 요청한 문구만 그 형식 안에서 바꾼다. 대표본 전체 재설계 금지. `webinar-three-cases-v2`의 새 5장을 기준으로 이어 만들지 않는다. 자세한 범위는 단원 design.md와 checks/design-baseline.json.\n',1)
agents.write_text(a,encoding='utf-8')
rd=root/'design.md'
r=rd.read_text(encoding='utf-8')
idx=r.find('## 0.')
r=r[:idx]+rule+r[idx:]
rd.write_text(r,encoding='utf-8')
plan=unit/'plan.md'
p=plan.read_text(encoding='utf-8')
i=p.find('## ')
p=p[:i]+rule+p[i:]
plan.write_text(p,encoding='utf-8')
part=unit/'part-1.md'
t=part.read_text(encoding='utf-8')
i=t.find('## ')
t=t[:i]+rule+t[i:]
part.write_text(t,encoding='utf-8')

# Prevent the prior planning regeneration helper from restoring the rejected
# layout direction. Its content updates can still regenerate the three topics.
helper=unit/'drafts/planning/agreed_examples_v2.py'
h=helper.read_text(encoding='utf-8')
h=h.replace("    plan.write_text(head+'```harness-plan\\n'", "    baseline_note='## 디자인 기준 유지\\n\\n기존 주황 표지·세 캐릭터 대표 5장 v5를 보존하고 최신 내용만 그 형식 안에서 반영한다. 직전 새 5장은 대체 기준이 아니다. 상세 기준은 design.md와 checks/design-baseline.json을 따른다.\\n\\n'\n    head=head.replace('## 최신 예제 선택과 대표 시안 수정', baseline_note+'## 최신 예제 선택과 대표 시안 수정',1)\n    plan.write_text(head+'```harness-plan\\n'")
h=h.replace('## 장표와 캡처 구성\n\n','## 장표와 캡처 구성\n\n최신 디자인 정정: 기존 주황 표지·세 캐릭터 대표 5장 v5를 유지한다. 아래의 직전 제작 방식과 결과는 검토 이력이며 새 기준으로 사용하지 않는다. 후속 장표는 design.md의 기존 대표본 유형에 최신 내용만 반영한다.\n\n',1)
helper.write_text(h,encoding='utf-8')
assert hashlib.sha256(deck.read_bytes()).hexdigest()==record['sha256']
print('Previous representative deck preserved; working design baseline restored. No slide binaries changed.')
