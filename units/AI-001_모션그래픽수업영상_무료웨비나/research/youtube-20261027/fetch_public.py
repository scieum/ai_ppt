"""Read public video metadata and caption-track inventory; do not download video."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import urllib.request,urllib.parse,json,re,datetime

OUT=Path(__file__).resolve().parent
IDS=['F7qQwYmIoxA','9uQVYIaYIeg','O0NR110DmLk','wOF1EDpWxQw','x08U8HJKV0E','_kc0riDpxOY']
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept-Language':'ko-KR,ko;q=0.9,en;q=0.7'})
    with urllib.request.urlopen(req,timeout=20) as r:return r.read().decode('utf-8')
def fetch(vid):
    record={'video_id':vid,'url':'https://www.youtube.com/watch?v='+vid,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        record['oembed']=json.loads(get('https://www.youtube.com/oembed?format=json&url='+urllib.parse.quote(record['url'],safe='')))
    except Exception as e:record['oembed_error']=str(e)
    try:
        html=get(record['url'])
        decoder=json.JSONDecoder()
        hit=re.search(r'(?:var\s+)?ytInitialPlayerResponse\s*=\s*',html)
        if hit:
            player=decoder.raw_decode(html[hit.end():])[0]
            record['video_details']=player.get('videoDetails',{})
            record['playability']=player.get('playabilityStatus',{})
            record['microformat']=player.get('microformat',{})
            captions=player.get('captions',{}).get('playerCaptionsTracklistRenderer',{})
            record['caption_tracks']=captions.get('captionTracks',[])
            for index,track in enumerate(record['caption_tracks']):
                if track.get('languageCode') in ['ko','en']:
                    try:
                        raw=get(track['baseUrl']+'&fmt=json3')
                        (OUT/(vid+'-captions-'+str(index)+'.json')).write_text(raw,encoding='utf-8')
                        record.setdefault('caption_files',[]).append(vid+'-captions-'+str(index)+'.json')
                    except Exception as e:record.setdefault('caption_errors',[]).append(str(e))
        else:record['player_error']='No player response in public watch HTML'
    except Exception as e:record['watch_error']=str(e)
    (OUT/(vid+'-metadata.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    title=record.get('video_details',{}).get('title') or record.get('oembed',{}).get('title')
    print(json.dumps({'id':vid,'title':title,'tracks':[x.get('languageCode') for x in record.get('caption_tracks',[])],'caption_files':record.get('caption_files',[]),'errors':{k:v for k,v in record.items() if k.endswith('_error')}},ensure_ascii=True),flush=True)
    return record
with ThreadPoolExecutor(max_workers=6) as pool:
    records=[r.result() for r in as_completed([pool.submit(fetch,v) for v in IDS])]
(OUT/'metadata-index.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
