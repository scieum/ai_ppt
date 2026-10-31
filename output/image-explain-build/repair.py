from pathlib import Path
B=Path('output/image-explain-build');p=B/'author.mjs';s=p.read_text(encoding='utf-8-sig').replace('190+i*330,601','255+i*265,601');p.write_text(s,encoding='utf8')
(B/'publish-final').mkdir(exist_ok=True);s=(B/'finalize.mjs').read_text(encoding='utf8').replace("finalPath:path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_이미지설명강화_40장_v21.pptx')","finalPath:path.join(B,'publish-final/NotionTalk_모션그래픽_이미지설명강화_40장_v21.pptx')").replace('final-validation.json','final-validation-complete.json');(B/'finalize-repair.mjs').write_text(s,encoding='utf8')
