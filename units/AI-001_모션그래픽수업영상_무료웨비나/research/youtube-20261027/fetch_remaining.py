from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,urllib.request,ssl,datetime
R=Path(__file__).resolve().parent; P=R/'yt-dlp'
EXE=R/'toolchain/yt-dlp-2026.10.26/yt-dlp.exe'
def fetch(vid):
    args=[str(EXE),'--ignore-config','--compat-options','no-certifi,prefer-legacy-http-handler','--skip-download','--dump-single-json','--js-runtimes','node:C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe','https://www.youtube.com/watch?v='+vid]
    result=subprocess.run(args,capture_output=True,timeout=210)
    (P/(vid+'-metadata-fetch.log')).write_bytes(result.stderr)
    if result.returncode: return {'id':vid,'status':'metadata_failed'}
    data=json.loads(result.stdout);(P/(vid+'.info.json')).write_bytes(result.stdout)
    tracks=data.get('subtitles',{}).get('ko') or data.get('automatic_captions',{}).get('ko') or []
    track=next(t for t in tracks if t['ext']=='json3')
    req=urllib.request.Request(track['url'],headers=data.get('http_headers',{}))
    with urllib.request.urlopen(req,context=ssl.create_default_context(),timeout=60) as response:
        raw=response.read()
    parsed=json.loads(raw)
    if not parsed.get('events'):raise ValueError('No caption events')
    (P/(vid+'.ko.json3')).write_bytes(raw)
    return {'id':vid,'bytes':len(raw),'events':len(parsed['events']),'transport':'urllib with default verified TLS trust','at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
def safe(vid):
    try:r=fetch(vid)
    except Exception as e:r={'id':vid,'error':str(e)}
    print(json.dumps(r,ensure_ascii=True),flush=True)
    return r
with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(safe,['wOF1EDpWxQw','x08U8HJKV0E']))
(R/'remaining-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
