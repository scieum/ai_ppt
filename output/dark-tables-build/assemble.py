from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import posixpath,json
B=Path(__file__).resolve().parent
R=B.parent.parent
source=R/'output/webinar-knowledge-only/NotionTalk_모션그래픽_이미지설명강화_40장_v21.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
def ordered(z):
 rels={r.get('Id'):r.get('Target') for r in E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
 ids=E.fromstring(z.read('ppt/presentation.xml')).find('{http://schemas.openxmlformats.org/presentationml/2006/main}sldIdLst')
 return [posixpath.normpath('ppt/'+rels[s.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]) if not rels[s.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')].startswith('/') else rels[s.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')].lstrip('/') for s in ids]
with ZipFile(source) as original, ZipFile(B/'restyled.pptx') as edited, ZipFile(B/'candidate.pptx','w',ZIP_DEFLATED) as dest:
 oldparts,newparts=ordered(original),ordered(edited)
 changes={oldparts[n-1]:newparts[n-1] for n in (25,34)}
 (B/'slide-map.json').write_text(json.dumps({'ordered_parts':oldparts,'changed':changes},indent=2),encoding='utf-8')
 for name in original.namelist():
  data=original.read(name)
  if name in changes:
   old=E.fromstring(data);new=E.fromstring(edited.read(changes[name]))
   table=old.find('.//a:tbl',ns);newtable=new.find('.//a:tbl',ns)
   assert table is not None and newtable is not None
   assert table.xpath('.//a:t/text()',namespaces=ns)==newtable.xpath('.//a:t/text()',namespaces=ns)
   table.getparent().replace(table,newtable)
   data=E.tostring(old,xml_declaration=True,encoding='UTF-8',standalone=True)
  dest.writestr(name,data)
print('Preserved every package part except two table nodes.')
