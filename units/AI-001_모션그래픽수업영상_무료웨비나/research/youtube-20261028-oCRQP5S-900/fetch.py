from pathlib import Path
import json,subprocess,hashlib,urllib.request,ssl
P=Path(__file__).resolve().parent;U=P.parents[1];OLD=U/'research/youtube-20261027/toolchain/yt-dlp-2026.10.26';EXE=OLD/'yt-dlp.exe';V='oCRQP5S-900'
verified=json.loads((OLD/'verification.json').read_text(encoding='utf8'))
assert hashlib.sha256(EXE.read_bytes()).hexdigest().lower()==verified['checks'][0]['expected'].lower()
result=subprocess.run([str(EXE),'--ignore-config','--compat-options','no-certifi,prefer-legacy-http-handler','--skip-download','--dump-single-json','--js-runtimes','node:C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe','https://www.youtube.com/watch?v='+V],capture_output=True,timeout=180)
(P/'metadata-fetch.log').write_bytes(result.stderr)
if result.returncode:raise RuntimeError('Metadata collection failed. See metadata-fetch.log')
data=json.loads(result.stdout);(P/(V+'.info.json')).write_bytes(result.stdout)
choices=data.get('subtitles',{}).get('ko')or data.get('automatic_captions',{}).get('ko-orig')or data.get('automatic_captions',{}).get('ko')or[]
track=next(t for t in choices if t['ext']=='json3')
req=urllib.request.Request(track['url'],headers=data.get('http_headers',{}))
with urllib.request.urlopen(req,context=ssl.create_default_context(),timeout=45)as response:raw=response.read()
j=json.loads(raw);assert j.get('events');(P/(V+'.ko.json3')).write_bytes(raw)
segments=[]
for ev in j['events']:
 text=''.join(s.get('utf8','')for s in ev.get('segs',[])).strip()
 if text:segments.append({'start':round(ev.get('tStartMs',0)/1000,3),'end':round((ev.get('tStartMs',0)+ev.get('dDurationMs',0))/1000,3),'text':text})
(P/'segments.json').write_text(json.dumps(segments,ensure_ascii=False,indent=2),encoding='utf8')
(P/'transcript.txt').write_text('\n'.join(f"[{int(s['start']//60):02}:{int(s['start']%60):02}] {s['text']}"for s in segments),encoding='utf8')
report={'id':V,'title':data.get('title'),'channel':data.get('channel'),'duration':data.get('duration'),'segments':len(segments),'last_caption_end':max(s['end']for s in segments),'captions_sha256':hashlib.sha256(raw).hexdigest(),'tool_sha256_matches_previous_verified_release':True,'analysis_basis':'metadata, description and Korean captions; no source video media reused'}
(P/'source-index.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False))

