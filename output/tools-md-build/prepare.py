from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parent.parent
prev='NotionTalk_모션그래픽_표디자인정리_40장_v22'
new='NotionTalk_모션그래픽_준비물_문서_내레이션_41장_v23'
s=(R/'output/dark-tables-build/finalize.mjs').read_text(encoding='utf-8-sig').replace(prev,new).replace('NotionTalk_모션그래픽_이미지설명강화_40장_v21',prev).replace('[22,25,33,34]','[22,33,34]').replace('explicitTotalSlideCount:40','explicitTotalSlideCount:41')
(B/'finalize.mjs').write_text(s,encoding='utf-8')
s=(R/'output/dark-tables-build/export.ps1').read_text(encoding='utf-8-sig').replace(prev,new).replace('dark-tables-build','tools-md-build').replace('dark-tables-20261029','tools-md-20261029').replace('count=40','count=41')
(B/'export.ps1').write_text(s,encoding='utf-8-sig')
