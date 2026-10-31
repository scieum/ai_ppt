from pathlib import Path
from zipfile import ZipFile
import fitz,numpy as np,json,hashlib,shutil
B=Path(__file__).resolve().parent;R=B.parent.parent;U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
src=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_헤더확대_글라스로고_43장_v27.pptx'
out=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_로고색복원_43장_v28.pptx'
with ZipFile(src) as a,ZipFile(out) as b:
 assert set(a.namelist())==set(b.namelist())
 changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
 assert set(changed)=={'ppt/media/header-glass-claude.png','ppt/media/header-glass-higgsfield.png'},changed
old=fitz.open(src.with_suffix('.pdf'));new=fitz.open(out.with_suffix('.pdf'));assert len(old)==len(new)==43
for i in range(43):
 a=old[i].get_pixmap();b=new[i].get_pixmap()
 x=np.frombuffer(a.samples,np.uint8).reshape(a.height,a.width,a.n);y=np.frombuffer(b.samples,np.uint8).reshape(b.height,b.width,b.n)
 d=np.any(x!=y,axis=2)
 if i==2:
  # Only the Claude and Higgsfield image rectangles, in PDF point coordinates.
  d[248:367,182:302]=False;d[248:367,652:772]=False
 assert not d.any(),i+1
record={'output':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'slides':43,'only_changed_parts':changed,'all_slide_xml_unchanged':True,'all_42_other_pages_pixel_identical':True,'prep_changes_confined_to_two_logo_frames':True,'font_increase_and_text_container_preserved':True}
dest=U/'checks/logo-color-20261030';dest.mkdir(parents=True,exist_ok=True);(dest/'verification.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
prefix='''## 최신 로고 색 복원 — 2026-10-30

현재 강의는 `output/webinar-knowledge-only/NotionTalk_모션그래픽_로고색복원_43장_v28.pptx`와 PDF다. 사용자 정정 ‘색은 있어야지’에 따라 준비물 3쪽의 클로드는 코랄색, 힉스필드는 라임색으로 복원했다. 코덱스는 원래의 흰색이다. 주황 테두리·모서리 장식 제거와 중성 유리 질감은 유지한다. 로고 색까지 모두 흰색으로 만드는 v27 해석은 취소한다.

자산과 ImageGen 프롬프트는 `assets/tool-logos/glass-color-v4/`에 있다. 다른 42장·상단 +2pt·필수 계정 배경 박스·모든 텍스트·GIF·애니메이션은 유지한다. 검증은 단원 `checks/logo-color-20261030/verification.json`이다. 아래는 이전 이력이다.

'''
for p in [R/'AGENTS.md',R/'design.md',U/'plan.md',U/'design.md',U/'part-0.md']:
 backup=U/'history/logo-color-20261030'/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(p,backup)
 s=p.read_text(encoding='utf-8-sig')
 if not s.startswith('## 최신 로고 색 복원'):p.write_text(prefix+s,encoding='utf-8')
print('Verified: two image payloads only; all 43 slide XML and 42 other rendered pages unchanged.')
