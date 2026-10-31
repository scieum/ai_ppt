import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {chromium} from 'playwright';
const B=path.dirname(fileURLToPath(import.meta.url)), R=path.resolve(B,'../..');
const A=path.join(R,'units/AI-001_모션그래픽수업영상_무료웨비나/assets/motion-audio-20261030');
await fs.mkdir(A,{recursive:true});
function ff(args){const r=spawnSync('ffmpeg',['-hide_banner','-loglevel','error','-y',...args],{encoding:'utf8'});if(r.status!==0)throw Error(r.stderr||r.error);}
const browser=await chromium.launch({headless:true});
const page=await browser.newPage();
const font=(await fs.readFile('C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf')).toString('base64');
await page.setContent(`<style>@font-face{font-family:Pretendard;src:url(data:font/ttf;base64,${font})}</style><canvas id="c" width="840" height="300"></canvas>`);
await page.evaluate(async()=>{await document.fonts.load('bold 56px Pretendard');});
// These frames demonstrate the requested motion properties, not decorative illustrations.
const draw=({kind,t,poster=false})=>{
 const c=document.querySelector('canvas'),g=c.getContext('2d'),W=840,H=300;
 g.setTransform(1,0,0,1,0,0);g.filter='none';g.globalAlpha=1;g.fillStyle='#202020';g.fillRect(0,0,W,H);
 const clamp=x=>Math.max(0,Math.min(1,x)),ease=x=>1-Math.pow(1-clamp(x),3);
 const outback=x=>{x=clamp(x)-1;return 1+2.70158*x*x*x+1.70158*x*x;};
 const txt=(text,x,y,size=70,color='#FF9228')=>{g.fillStyle=color;g.font=`bold ${size}px Pretendard`;g.textAlign='center';g.textBaseline='middle';g.fillText(text,x,y);};
 const round=(x,y,w,h,r,col)=>{g.fillStyle=col;g.beginPath();g.roundRect(x,y,w,h,r);g.fill();};
 const clock=poster?1.8:t;
 if(kind==='snap'){
  const p=outback((clock-.25)/1.1);txt('노션톡',420+(1-p)*460,139,86);txt('웨비나 챌린지',420,222,37,'#AAAAAA');
 }else if(kind==='blur'){
  const chars=[...'새로운 시작'];chars.forEach((ch,i)=>{let p=ease((clock-.2-i*.07)/.85);g.save();g.translate(236+i*62,150);g.rotate((1-p)*-.65);g.scale(1+(1-p)*1.6,1+(1-p)*1.6);g.globalAlpha=p;g.filter=`blur(${(1-p)*13}px)`;txt(ch,0,0,66,'#73D3F4');g.restore();});
 }else if(kind==='counter'){
  const p=ease((clock-.3)/1.7),val=Math.round(p*100);txt(val+'%',420,138,112);round(190,226,460,8,4,'#414141');if(p>0)round(190,226,460*p,8,4,'#FF9228');
 }else if(kind==='squash'){
  let y=90,sx=1,sy=1;
  if(clock<.95){let p=clamp((clock-.2)/.75);sy=1+.25*p;sx=1/sy;y=85+(250-45*sy-85)*p*p;}
  else if(clock<1.18){let p=(clock-.95)/.23;sx=1+.58*Math.sin(Math.PI*p);sy=1/sx;y=250-45*sy;}
  else if(clock<1.9){let p=(clock-1.18)/.72;y=205-115*Math.sin(p*Math.PI/2);sy=1+.3*Math.sin(p*Math.PI);sx=1/sy;}
  else{y=90;}
  g.strokeStyle='#555555';g.lineWidth=2;g.beginPath();g.moveTo(210,251);g.lineTo(630,251);g.stroke();g.fillStyle='#FF9228';g.beginPath();g.ellipse(420,y,45*sx,45*sy,0,0,Math.PI*2);g.fill();
 }else if(kind==='flip'){
  const p=ease((clock-.5)/1.2),ang=p*Math.PI,scale=Math.max(.015,Math.abs(Math.cos(ang)));g.save();g.translate(420,150);g.scale(scale,1);round(-155,-95,310,190,22,p<.5?'#FF9228':'#73D3F4');txt(p<.5?'질문':'답',0,0,80,'#151515');g.restore();
 }else if(kind==='sound'){
  const tt=poster?2.4:t;
  txt('노션톡',420,75,37,'#AAAAAA');
  const p=outback((tt-.3)/.55);g.save();g.globalAlpha=clamp((tt-.3)/.2);txt('웨비나 챌린지',420+(1-p)*250,145,74);g.restore();
  const q=ease((tt-1.45)/.32);g.save();g.globalAlpha=q;round(260,211+(1-q)*35,320,55,14,'#303030');txt(tt<2.8?'함께 시작해요':'준비 완료',420,240+(1-q)*35,32,tt<2.8?'#FFFFFF':'#73D3F4');g.restore();
 }
 return c.toDataURL('image/png').split(',')[1];
};
for(const kind of ['snap','blur','counter','squash','flip','sound']){
 const dir=path.join(B,'frames',kind);await fs.mkdir(dir,{recursive:true});
 const frames=80;
 for(let i=0;i<frames;i++){
  const b64=await page.evaluate(draw,{kind,t:i/20});
  await fs.writeFile(path.join(dir,`${String(i).padStart(3,'0')}.png`),Buffer.from(b64,'base64'));
 }
 const poster=Buffer.from(await page.evaluate(draw,{kind,t:0,poster:true}),'base64');await fs.writeFile(path.join(A,kind+'-poster.png'),poster);
 if(kind!=='sound'){
  ff(['-framerate','20','-i',path.join(dir,'%03d.png'),'-filter_complex','[0:v]split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',path.join(A,kind+'.gif')]);
  for(const [i,n] of [[10,'start'],[21,'middle'],[42,'end']])await fs.copyFile(path.join(dir,`${String(i).padStart(3,'0')}.png`),path.join(A,kind+'-'+n+'.png'));
 }else{
  ff(['-framerate','20','-i',path.join(dir,'%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',path.join(A,'silent.mp4')]);
 }
 console.log('Generated',kind);
}
await browser.close();
// Original synthetic teaching sounds: pop, short filtered noise, gentle chime.
const sr=48000,count=sr*4,pcm=Buffer.alloc(count*2);let seed=3907,filtered=0;
for(let i=0;i<count;i++){
 const t=i/sr;let v=0;
 for(const [at,freq,decay,amp] of [[.85,580,.045,.19],[2.8,880,.13,.12],[2.8,1320,.08,.05]]){const d=t-at;if(d>=0&&d<.5)v+=Math.sin(2*Math.PI*freq*d)*Math.exp(-d/decay)*Math.min(1,d/.006)*amp;}
 seed=(1664525*seed+1013904223)>>>0;filtered=.74*filtered+.26*(seed/2147483648-1);let d=t-1.45;if(d>=0&&d<.23)v+=filtered*Math.sin(Math.PI*d/.23)*.25;
 pcm.writeInt16LE(Math.max(-32767,Math.min(32767,Math.round(v*32767))),i*2);
}
await fs.writeFile(path.join(B,'sound.pcm'),pcm);
ff(['-f','s16le','-ar',String(sr),'-ac','1','-i',path.join(B,'sound.pcm'),path.join(A,'original-effects.wav')]);
ff(['-i',path.join(A,'silent.mp4'),'-i',path.join(A,'original-effects.wav'),'-c:v','copy','-c:a','aac','-b:a','128k','-shortest',path.join(A,'with-sound.mp4')]);
await fs.writeFile(path.join(A,'manifest.json'),JSON.stringify({created:'2026-10-30',fps:20,duration_seconds:4,source:'Original educational motion demonstrations',effects:['snap','blur','counter','squash','flip'],sound:'Original deterministic synthetic pop, noise swipe and chime. Not output from Real SFX or earshot.',reference:'User-provided @mynameisjaemin screenshot, movement concepts only'},null,2));
console.log(A);
