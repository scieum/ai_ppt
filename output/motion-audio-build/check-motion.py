from pathlib import Path
from PIL import Image, ImageDraw
import subprocess,json,io,numpy as np
B=Path(__file__).resolve().parent;R=B.parent.parent;A=R/'units/AI-001_모션그래픽수업영상_무료웨비나/assets/motion-audio-20261030'
report={}
for kind in ['snap','blur','counter','squash','flip']:
 im=Image.open(A/(kind+'.gif')); hashes=set();duration=0
 for i in range(im.n_frames):
  im.seek(i);hashes.add(im.convert('RGB').tobytes());duration+=im.info.get('duration',0)
 report[kind]={'frames':im.n_frames,'unique_frames':len(hashes),'duration_ms':duration}
 assert im.n_frames==92 and len(hashes)>12
def frame(t):
 result=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i',str(B/'playback-check.mp4'),'-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True,check=True)
 return Image.open(io.BytesIO(result.stdout)).convert('RGB')
# Contact sheet of actual PowerPoint-rendered playback, for private visual QA.
times=[.7,1.2,1.7,6.2,6.8,7.4,11.8,12.4,13,18.7,19.4,20.4]
canvas=Image.new('RGB',(1280,4*260),'#151515');draw=ImageDraw.Draw(canvas)
for i,t in enumerate(times):
 im=frame(t);im.crop((130,330,1150,620)).resize((410,210)).save(B/f'play-{i:02}.png')
 tile=Image.open(B/f'play-{i:02}.png');x=i%3*425;y=i//3*260;canvas.paste(tile,(x,y+27));draw.text((x+8,y+6),f'PowerPoint export: {t}s',fill='white')
canvas.save(B/'motion-playback-contact.png')
for key in ['silent','with-sound']:
 r=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,duration','-of','json',str(A/(key+'.mp4'))],capture_output=True,text=True,check=True);report[key]=json.loads(r.stdout)
assert not any(s['codec_type']=='audio'for s in report['silent']['streams'])
assert any(s['codec_type']=='audio'for s in report['with-sound']['streams'])
audio=subprocess.run(['ffmpeg','-v','error','-i',str(B/'playback-check.mp4'),'-f','f32le','-ac','1','-ar','12000','-'],capture_output=True,check=True).stdout
v=np.frombuffer(audio,np.float32);report['powerpoint_export_audio']={'peak':float(np.max(np.abs(v))),'nonzero_samples':int(np.sum(np.abs(v)>.001))}
assert report['powerpoint_export_audio']['peak']>.05
(B/'motion-check.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))
