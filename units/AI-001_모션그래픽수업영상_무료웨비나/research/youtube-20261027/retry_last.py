from pathlib import Path
import json,urllib.request,urllib.parse,ssl,datetime
R=Path(__file__).resolve().parent;P=R/'yt-dlp';v='x08U8HJKV0E'
d=json.loads((P/(v+'.info.json')).read_text(encoding='utf-8'))
tracks=d['automatic_captions']['ko-orig']
for ext in ['json3','vtt']:
    t=next(t for t in tracks if t['ext']==ext)
    try:
        with urllib.request.urlopen(urllib.request.Request(t['url'],headers=d.get('http_headers',{})),context=ssl.create_default_context(),timeout=60) as r:raw=r.read()
        if not raw:raise ValueError('Empty response')
        if ext=='json3':assert json.loads(raw).get('events')
        (P/(v+'.ko.'+ext)).write_bytes(raw)
        print(json.dumps({'id':v,'ext':ext,'bytes':len(raw),'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}));break
    except Exception as e:print(json.dumps({'ext':ext,'error':str(e)}),flush=True)
