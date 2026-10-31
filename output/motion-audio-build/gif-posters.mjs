import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';import{spawnSync}from'node:child_process';
const B=path.dirname(fileURLToPath(import.meta.url)),A=path.resolve(B,'../../units/AI-001_모션그래픽수업영상_무료웨비나/assets/motion-audio-20261030');
for(const kind of['snap','blur','counter','squash','flip']){
 const d=path.join(B,'frames',kind+'-presentation');await fs.mkdir(d,{recursive:true});
 for(let i=0;i<92;i++)await fs.copyFile(i<12?path.join(A,kind+'-poster.png'):path.join(B,'frames',kind,String(i-12).padStart(3,'0')+'.png'),path.join(d,String(i).padStart(3,'0')+'.png'));
 const r=spawnSync('ffmpeg',['-hide_banner','-loglevel','error','-y','-framerate','20','-i',path.join(d,'%03d.png'),'-filter_complex','[0:v]split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',path.join(A,kind+'.gif')],{encoding:'utf8'});if(r.status)throw Error(r.stderr);
}
const manifest=JSON.parse(await fs.readFile(path.join(A,'manifest.json'),'utf8'));manifest.gif_duration_seconds=4.6;manifest.gif_frames=92;manifest.poster_hold_seconds=.6;await fs.writeFile(path.join(A,'manifest.json'),JSON.stringify(manifest,null,2));console.log('GIF poster frames retained for static PDF previews.');
