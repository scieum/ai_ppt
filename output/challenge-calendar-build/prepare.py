from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parent.parent
s=(R/'output/tools-md-build/assemble.py').read_text(encoding='utf-8')
s=s.replace('tools-narration','challenge-calendar').replace('rIdToolsNarration','rIdChallengeCalendar').replace('tools-md-','challenge-calendar-').replace('if i not in (3,25)','if True')
s=s.replace("print('41 slides: replaced 3 and 25, added narration at 37; preserved 38 original slides and all media.')","print('Appended calendar as slide 41; all 40 original slides and media preserved.')")
(B/'assemble.py').write_text(s,encoding='utf-8')
old='NotionTalk_모션그래픽_표디자인정리_40장_v22';new='NotionTalk_모션그래픽_챌린지일정추가_41장_v24'
s=(R/'output/dark-tables-build/finalize.mjs').read_text(encoding='utf-8-sig').replace(old,new).replace('NotionTalk_모션그래픽_이미지설명강화_40장_v21',old).replace('explicitTotalSlideCount:40','explicitTotalSlideCount:41')
(B/'finalize.mjs').write_text(s,encoding='utf-8')
s=(R/'output/dark-tables-build/export.ps1').read_text(encoding='utf-8-sig').replace(old,new).replace('dark-tables-build','challenge-calendar-build').replace('dark-tables-20261029','challenge-calendar-20261029').replace('count=40','count=41')
(B/'export.ps1').write_text(s,encoding='utf-8-sig')
