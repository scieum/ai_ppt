from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,ssl,urllib.request,sys,datetime,hashlib
sys.stdout.reconfigure(encoding='utf8')
B=Path(__file__).resolve().parent;R=B.parents[1];P=R/'units/AI-001_모션그래픽수업영상_무료웨비나/research/youtube-top10-20261028';D=P/'captions';D.mkdir(exist_ok=True)
items=[json.loads(f.read_text(encoding='utf8'))for f in (P/'metadata').glob('*.json')];items.sort(key=lambda x:x.get('view_count')or 0,reverse=True);items=[j for j in items if j['id']in sys.argv[1:]]if len(sys.argv)>1 else items[:35]
def fetch(j):
 k=j['id'];f=D/(k+'.segments.json');record={'id':k,'title':j['title'],'views':j.get('view_count')}
 if f.exists():record.update({'segments':len(json.loads(f.read_text(encoding='utf8'))),'cached':True});return record
 try:
  tracks=None;lang=None;kind=None
  for category in ['subtitles','automatic_captions']:
   options=j.get(category,{})
   langs=['en-orig','ko-orig']+[key for key in options if key.endswith('-orig')]+['en','ko']
   for key in langs:
    choices=[t for t in options.get(key,[])if t.get('ext')=='json3']
    if choices:tracks=choices[0];lang=key;kind=category;break
   if tracks:break
  if not tracks:record['error']='No caption track';return record
  with urllib.request.urlopen(urllib.request.Request(tracks['url'],headers=j.get('http_headers',{})),context=ssl.create_default_context(),timeout=40)as response:raw=response.read()
  doc=json.loads(raw);segs=[]
  for e in doc.get('events',[]):
   t=''.join(s.get('utf8','')for s in e.get('segs',[])).strip()
   if t:segs.append({'start':round(e.get('tStartMs',0)/1000,3),'end':round((e.get('tStartMs',0)+e.get('dDurationMs',0))/1000,3),'text':t})
  if not segs:raise RuntimeError('Empty captions')
  (D/(k+'.json3')).write_bytes(raw);f.write_text(json.dumps(segs,ensure_ascii=False,indent=2),encoding='utf8')
  (D/(k+'.txt')).write_text('\n'.join(f"[{int(s['start']//60):02}:{int(s['start']%60):02}] {s['text']}"for s in segs),encoding='utf8')
  record.update({'language':lang,'kind':kind,'segments':len(segs),'last_caption_end':segs[-1]['end'],'sha256':hashlib.sha256(raw).hexdigest()})
 except Exception as err:record['error']=str(err)
 return record
results=[]
with ThreadPoolExecutor(max_workers=2)as pool:
 for future in as_completed([pool.submit(fetch,j)for j in items]):
  r=future.result();results.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
old=json.loads((P/'caption-index.json').read_text(encoding='utf8'))['items']if(P/'caption-index.json').exists()else[]
merged={j['id']:j for j in old}
for j in results:
 if j.get('cached')and j['id']in merged:continue
 merged[j['id']]=j
(P/'caption-index.json').write_text(json.dumps({'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'items':list(merged.values())},ensure_ascii=False,indent=2),encoding='utf8')
