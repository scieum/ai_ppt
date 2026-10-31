from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parent.parent
old='NotionTalk_모션그래픽_챌린지11월2일시작_41장_v25';new='NotionTalk_모션그래픽_사이클활동안내_43장_v26'
s=(R/'output/challenge-calendar-build/assemble.py').read_text(encoding='utf-8')
s=s.replace('NotionTalk_모션그래픽_표디자인정리_40장_v22',old)
s=s.replace("'ppt/slides/challenge-calendar.xml'","f'ppt/slides/challenge-activity-{d[\"key\"]}.xml'")
s=s.replace("'ppt/notesSlides/challenge-calendar.xml'","f'ppt/notesSlides/challenge-activity-{d[\"key\"]}.xml'")
s=s.replace("rid='rIdChallengeCalendar'","rid='rIdChallengeActivity'+d['key']")
s=s.replace(".text='41'",".text='43'").replace("'count':41","'count':43")
s=s.replace("print('Appended calendar as slide 41; all 40 original slides and media preserved.')","print('Appended cycle guides at 42 and 43; all 41 originals preserved.')")
(B/'assemble.py').write_text(s,encoding='utf-8')
s=(R/'output/challenge-date-fix-build/finalize.mjs').read_text(encoding='utf-8').replace(old,new).replace('NotionTalk_모션그래픽_챌린지일정추가_41장_v24',old).replace('explicitTotalSlideCount:41','explicitTotalSlideCount:43')
(B/'finalize.mjs').write_text(s,encoding='utf-8')
s=(R/'output/challenge-date-fix-build/export.ps1').read_text(encoding='utf-8-sig').replace(old,new).replace('challenge-date-fix-build','challenge-activities-build').replace('challenge-date-fix-20261030','challenge-activities-20261030').replace('count=41','count=43')
(B/'export.ps1').write_text(s,encoding='utf-8-sig')
