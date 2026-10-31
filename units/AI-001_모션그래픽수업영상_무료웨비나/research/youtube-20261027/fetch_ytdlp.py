from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import subprocess,json,datetime
R=Path(__file__).resolve().parent;OUT=R/'yt-dlp';OUT.mkdir(exist_ok=True)
EXE=R/'toolchain/yt-dlp-2026.10.26/yt-dlp.exe'
IDS=['F7qQwYmIoxA','9uQVYIaYIeg','O0NR110DmLk','wOF1EDpWxQw','x08U8HJKV0E','_kc0riDpxOY']
def fetch(vid):
    if (OUT/(vid+'.ko.json3')).exists() and (OUT/(vid+'.info.json')).exists():
        return {'video_id':vid,'exit_code':0,'status':'previously_fetched'}
    args=[str(EXE),'--ignore-config','--compat-options','no-certifi,prefer-legacy-http-handler','--no-playlist','--skip-download','--write-subs','--write-auto-subs','--sub-langs','ko','--sub-format','json3','--write-info-json','--write-description','--js-runtimes','node:C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe','--retries','2','--extractor-retries','2','--sleep-requests','1','--paths',str(OUT),'--output','%(id)s.%(ext)s','https://www.youtube.com/watch?v='+vid]
    with (OUT/(vid+'-system-ca-urllib-fetch.log')).open('w',encoding='utf-8') as log:
        try:
            result=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,timeout=210,encoding='utf-8',errors='replace')
            code=result.returncode
        except subprocess.TimeoutExpired:code='timeout'
    files=[{'name':p.name,'bytes':p.stat().st_size} for p in OUT.glob(vid+'*') if p.suffix!='.log']
    row={'video_id':vid,'exit_code':code,'files':files,'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    print(json.dumps(row,ensure_ascii=True),flush=True)
    return row
with ThreadPoolExecutor(max_workers=2) as pool:
    rows=[future.result() for future in as_completed([pool.submit(fetch,x) for x in IDS])]
(OUT/'fetch-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
