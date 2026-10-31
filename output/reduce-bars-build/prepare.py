from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import json
B=Path(__file__).resolve().parent;R=B.parent.parent
old='NotionTalk_모션그래픽_효과음과움직임확장_48장_v33';new='NotionTalk_모션그래픽_텍스트바정리_48장_v34'
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
mapping=json.loads((R/'output/motion-audio-build/slide-map.json').read_text(encoding='utf8'))
changed=[m for m in mapping if m['page']in[15,16,19,20,25]]
with ZipFile(R/f'output/webinar-knowledge-only/{old}.pptx')as z:
 files={n:z.read(n)for n in z.namelist()}
 for m in changed:
  root=E.fromstring(files[m['part']]);tree=root.find('p:cSld/p:spTree',N);removed=[]
  for el in list(tree):
   nv=el.find('p:nvSpPr/p:cNvPr',N)
   if nv is not None and nv.get('name','').startswith('conclusion-bar-'):
    removed.append(nv.get('name'));tree.remove(el)
  assert len(removed)==5,(m['page'],removed)
  files[m['part']]=E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
 with ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED)as out:
  for n,d in files.items():out.writestr(n,d)
(B/'changes.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2),encoding='utf8')
finalize=(R/'output/motion-audio-build/finalize.mjs').read_text(encoding='utf8').replace('NotionTalk_모션그래픽_결론텍스트바_43장_v32',old).replace("path.join(B,'validated-final/"+old+".pptx')","path.join(R,'output/webinar-knowledge-only/"+new+".pptx')")
(B/'finalize.mjs').write_text(finalize,encoding='utf8')
export=(R/'output/motion-audio-build/export-final.ps1').read_text(encoding='utf-8-sig').replace('output/motion-audio-build','output/reduce-bars-build').replace(old,new).replace('renders/motion-audio-20261030','renders/reduce-bars-20261030')
(B/'export.ps1').write_text(export,encoding='utf-8-sig')
print('Removed only the 5 newly added conclusion bars; preserved all remaining package parts.')
