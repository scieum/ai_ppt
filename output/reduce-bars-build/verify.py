from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,hashlib,fitz,numpy as np
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
old='NotionTalk_모션그래픽_효과음과움직임확장_48장_v33';new='NotionTalk_모션그래픽_텍스트바정리_48장_v34'
src=R/f'output/webinar-knowledge-only/{old}.pptx';dst=R/f'output/webinar-knowledge-only/{new}.pptx'
changes=json.loads((B/'changes.json').read_text(encoding='utf8'));N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
with ZipFile(src)as a,ZipFile(dst)as b:
 assert set(a.namelist())==set(b.namelist())
 assert {n for n in a.namelist()if a.read(n)!=b.read(n)}=={m['part']for m in changes}
 for m in changes:
  root=E.fromstring(a.read(m['part']));tree=root.find('p:cSld/p:spTree',N)
  for el in list(tree):
   nv=el.find('p:nvSpPr/p:cNvPr',N)
   if nv is not None and nv.get('name','').startswith('conclusion-bar-'):tree.remove(el)
  assert E.tostring(root,method='c14n')==E.tostring(E.fromstring(b.read(m['part'])),method='c14n')
op=fitz.open(src.with_suffix('.pdf'));npdf=fitz.open(dst.with_suffix('.pdf'));assert len(op)==len(npdf)==48
for i in range(48):
 a=op[i].get_pixmap();b=npdf[i].get_pixmap();diff=np.any(np.frombuffer(a.samples,np.uint8).reshape(a.height,a.width,a.n)!=np.frombuffer(b.samples,np.uint8).reshape(b.height,b.width,b.n),axis=2)
 if i+1 in[15,16,19,20,25]:diff[478:512,110:851]=False
 assert not diff.any(),i+1
record={'slides':48,'removed_bars':[15,16,19,20,25],'remaining_bars':11,'other_43_slides_byte_and_pixel_identical':True,'other_objects_media_notes_timing_unchanged':True,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()}
d=U/'checks/reduce-bars-20261030';d.mkdir(parents=True,exist_ok=True);(d/'verification.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
head=f'''## 최신 정정 — 결론 바 절제 2026-10-30

현재 파일은 `output/webinar-knowledge-only/{new}.pptx`와 PDF다. 사용자 지적에 따라 직전에 추가한 15·16·19·20·25쪽의 결론 텍스트 바를 제거했다. 48장과 나머지 내용·디자인·GIF·영상·소리·발표자 노트는 그대로이며 기존에 확정한 결론 바 11개만 유지한다.

**결론 바는 모든 설명·예시 장표의 기본 요소가 아니다.** 새 장표마다 자동 삽입하지 않는다. 본문·제목을 되풀이하는 요약은 생략하며, 독립적인 핵심 결론을 강조해야 할 때만 제한적으로 사용한다. 기존 결론 바 디자인을 유지하라는 요청을 빈도 확대 지시로 해석하지 않는다. 검증은 단원 `checks/reduce-bars-20261030/verification.json`. 아래는 이전 이력이다.

'''
for f in[R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md']:
 text=f.read_text(encoding='utf8')
 if not text.startswith(head.split('\n')[0]):f.write_text(head+text,encoding='utf8')
print(json.dumps(record,ensure_ascii=False))
