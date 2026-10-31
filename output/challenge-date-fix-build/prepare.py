from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parent.parent;prev=R/'output/challenge-calendar-build'
old='NotionTalk_모션그래픽_챌린지일정추가_41장_v24';new='NotionTalk_모션그래픽_챌린지11월2일시작_41장_v25'
s=(prev/'author.mjs').read_text(encoding='utf-8')
for a,b in [
 ('2026.11.1.(일) ~ 11.14.(토)','2026.11.2.(월) ~ 11.15.(일)'),
 ("['일','월','화','수','목','금','토']","['월','화','수','목','금','토','일']"),
 ('11/1 ~ 11/7','11/2 ~ 11/8'),('11/8 ~ 11/14','11/9 ~ 11/15'),
 ('row*7+col+1','row*7+col+2'),('day===1','day===2'),("?'11/1'","?'11/2'"),
 ('2026년 11월 1일부터','2026년 11월 2일부터'),
 ('11월 1일 일요일~11월 7일 토요일','11월 2일 월요일~11월 8일 일요일'),
 ('11월 8일 일요일~11월 14일 토요일','11월 9일 월요일~11월 15일 일요일'),
 ('replace:null,before:41','replace:41,before:null')]:s=s.replace(a,b)
(B/'author.mjs').write_text(s,encoding='utf-8')
s=(prev/'assemble.py').read_text(encoding='utf-8').replace('NotionTalk_모션그래픽_표디자인정리_40장_v22',old).replace('if True','if i != 41')
s=s.replace("print('Appended calendar as slide 41; all 40 original slides and media preserved.')","print('Corrected calendar 41 only; previous 40 slides preserved.')")
(B/'assemble.py').write_text(s,encoding='utf-8')
s=(prev/'finalize.mjs').read_text(encoding='utf-8').replace(old,new).replace('NotionTalk_모션그래픽_표디자인정리_40장_v22',old)
(B/'finalize.mjs').write_text(s,encoding='utf-8')
s=(prev/'export.ps1').read_text(encoding='utf-8-sig').replace(old,new).replace('challenge-calendar-build','challenge-date-fix-build').replace('challenge-calendar-20261029','challenge-date-fix-20261030')
(B/'export.ps1').write_text(s,encoding='utf-8-sig')
