from pathlib import Path
B=Path('output/reference-style-build');(B/'publish-final').mkdir(exist_ok=True);s=(B/'finalize.mjs').read_text(encoding='utf8').replace("path.join(R,'output/webinar-knowledge-only/NotionTalk_모션그래픽_레퍼런스표현강화_40장_v20.pptx')","path.join(B,'publish-final/NotionTalk_모션그래픽_레퍼런스표현강화_40장_v20.pptx')");(B/'finalize-repair.mjs').write_text(s,encoding='utf8')
