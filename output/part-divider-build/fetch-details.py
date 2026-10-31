from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,subprocess,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parent;R=B.parents[1];U=R/'units/AI-001_모션그래픽수업영상_무료웨비나';P=U/'research/youtube-top10-20261028';M=P/'metadata';M.mkdir(exist_ok=True)
T=U/'research/youtube-20261027/toolchain/yt-dlp-2026.10.26';EXE=T/'yt-dlp.exe';verify=json.loads((T/'verification.json').read_text(encoding='utf8'));assert hashlib.sha256(EXE.read_bytes()).hexdigest().lower()==verify['checks'][0]['expected'].lower()
BASE=[str(EXE),'--ignore-config','--compat-options','no-certifi,prefer-legacy-http-handler','--skip-download','--dump-single-json','--js-runtimes','node:C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe']
items=json.loads((P/'candidates.json').read_text(encoding='utf8'))['candidates']
def fetch(e):
 k=e['id'];f=M/(k+'.json')
 if f.exists():j=json.loads(f.read_text(encoding='utf8'))
 else:
  try:p=subprocess.run(BASE+['https://www.youtube.com/watch?v='+k],capture_output=True,timeout=120)
  except Exception as err:return {'id':k,'error':str(err)}
  (M/(k+'.log')).write_bytes(p.stderr)
  if p.returncode:return {'id':k,'error':p.stderr.decode('utf8','replace')[-300:]}
  j=json.loads(p.stdout);f.write_bytes(p.stdout)
 return {x:j.get(x)for x in ['id','title','channel','view_count','duration','upload_date','description','chapters','language','webpage_url']}
results=[]
with ThreadPoolExecutor(max_workers=4)as pool:
 for future in as_completed([pool.submit(fetch,e)for e in items]):
  results.append(future.result())
  if len(results)%10==0:print('Metadata',len(results),'/',len(items),flush=True)
results.sort(key=lambda x:x.get('view_count')or 0,reverse=True)
(P/'details-index.json').write_text(json.dumps({'collected_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'items':results},ensure_ascii=False,indent=2),encoding='utf8')
for j in results[:45]:
 print(json.dumps({'id':j['id'],'views':j.get('view_count'),'title':j.get('title'),'channel':j.get('channel'),'code_mention':'claude code'in(j.get('description')or'').lower(),'description':(j.get('description')or'')[:1600],'chapters':j.get('chapters')},ensure_ascii=False),flush=True)
