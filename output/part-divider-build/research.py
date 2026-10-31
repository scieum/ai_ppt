from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import subprocess,json,hashlib,datetime,time
B=Path(__file__).resolve().parent;R=B.parents[1]
U=R/'units/AI-001_모션그래픽수업영상_무료웨비나'
P=U/'research/youtube-top10-20261028';P.mkdir(parents=True,exist_ok=True)
T=U/'research/youtube-20261027/toolchain/yt-dlp-2026.10.26'
EXE=T/'yt-dlp.exe';verify=json.loads((T/'verification.json').read_text(encoding='utf8'))
assert hashlib.sha256(EXE.read_bytes()).hexdigest().lower()==verify['checks'][0]['expected'].lower()
BASE=[str(EXE),'--ignore-config','--compat-options','no-certifi,prefer-legacy-http-handler','--skip-download','--js-runtimes','node:C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe']
queries=['Claude Code motion graphics','Claude Code Remotion','Claude Code animation','클로드 코드 모션그래픽','클로드 리모션']
def search(i,q):
 f=P/f'search-{i+1}.json'
 if f.exists():return json.loads(f.read_text(encoding='utf8'))
 p=subprocess.run(BASE+['--flat-playlist','--dump-single-json',f'ytsearch30:{q}'],capture_output=True,timeout=180)
 (P/f'search-{i+1}.log').write_bytes(p.stderr)
 if p.returncode:return {'query':q,'error':p.stderr.decode('utf8','replace')[-500:]}
 j=json.loads(p.stdout);f.write_bytes(p.stdout);return j
allitems={};searches=[]
with ThreadPoolExecutor(max_workers=3)as pool:
 for future in as_completed([pool.submit(search,i,q)for i,q in enumerate(queries)]):
  j=future.result();searches.append({'title':j.get('title'),'count':len(j.get('entries',[])),'error':j.get('error')})
  for e in j.get('entries',[]):
   if e and e.get('id'):
    k=e['id'];row={x:e.get(x)for x in ['id','title','channel','view_count','duration','url','description']}
    if k in allitems:allitems[k]['queries'].append(j.get('title'))
    else:row['queries']=[j.get('title')];allitems[k]=row
  print('Search done',j.get('title'),len(j.get('entries',[])),flush=True)
out={'collected_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'queries':queries,'tool_sha256_verified':True,'searches':searches,'candidates':sorted(allitems.values(),key=lambda x:x.get('view_count')or 0,reverse=True)}
(P/'candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print('Unique candidates',len(allitems),flush=True)
for e in out['candidates']:print(json.dumps({k:e[k]for k in ['id','title','channel','view_count','duration']},ensure_ascii=False),flush=True)
