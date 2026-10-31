from pathlib import Path
B=Path(__file__).resolve().parent
R=B.parent.parent
old='NotionTalk_모션그래픽_이미지설명강화_40장_v21'
new='NotionTalk_모션그래픽_표디자인정리_40장_v22'
s=(R/'output/image-explain-build/finalize.mjs').read_text(encoding='utf-8-sig')
s=s.replace(old,new).replace('NotionTalk_모션그래픽_레퍼런스표현강화_40장_v20',old)
(B/'finalize.mjs').write_text(s,encoding='utf-8')
s=(R/'output/image-explain-build/export.ps1').read_text(encoding='utf-8-sig')
s=s.replace(old,new).replace('image-explain-build','dark-tables-build').replace('image-explain-20261029','dark-tables-20261029')
(B/'export.ps1').write_text(s,encoding='utf-8-sig')
