from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parent;P=R/'yt-dlp'
ids=['F7qQwYmIoxA','9uQVYIaYIeg','O0NR110DmLk','wOF1EDpWxQw','x08U8HJKV0E','_kc0riDpxOY']
out=[]
for vid in ids:
    f=P/(vid+'.ko.json3')
    if not f.exists() or not f.stat().st_size:continue
    try:data=json.loads(f.read_text(encoding='utf-8'))
    except Exception:continue
    rows=[]
    for e in data.get('events',[]):
        text=''.join(s.get('utf8','') for s in e.get('segs',[])).strip().replace('\n',' ')
        if not text:continue
        start=e.get('tStartMs',0)/1000;end=start+e.get('dDurationMs',0)/1000
        if rows and rows[-1]['text']==text:continue
        rows.append({'start':start,'end':end,'text':text})
    def stamp(t):
        t=int(t);return f'{t//3600:02}:{t%3600//60:02}:{t%60:02}'
    path=P/(vid+'.transcript.txt')
    path.write_text('\n'.join('['+stamp(x['start'])+'] '+x['text'] for x in rows)+'\n',encoding='utf-8')
    (P/(vid+'.segments.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    md=json.loads((R/(vid+'-metadata.json')).read_text(encoding='utf-8'))
    detail=md.get('video_details',{})
    out.append({'video_id':vid,'title':detail.get('title') or md.get('oembed',{}).get('title'),'channel':detail.get('author') or md.get('oembed',{}).get('author_name'),'duration_seconds':int(detail.get('lengthSeconds') or 0),'transcript_end_seconds':max([x['end'] for x in rows] or [0]),'segments':len(rows),'characters':sum(len(x['text']) for x in rows),'caption_file':f.name,'transcript_file':path.name,'caption_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'metadata_file':vid+'-metadata.json','transcript_kind':'YouTube Korean captions via verified yt-dlp; inspect caption track kind in metadata'})
(R/'source-index.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=True,indent=2))
