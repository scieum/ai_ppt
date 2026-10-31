"""Original, silent motion studies for the three agreed webinar examples.

These are locally authored examples, not claimed as app prompt execution captures.
Typography, information layouts and explanatory scientific diagrams are drawn as
content. No reference PDF pixels or third-party illustrations are copied.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, subprocess, json, hashlib
FFMPEG='C:/Users/User/AppData/Local/Programs/Python/Python312/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'

BUILD=Path(__file__).resolve().parent
UNIT=BUILD.parents[2]
ROOT=UNIT.parents[1]
OUT=ROOT/'output/webinar-three-cases-v2'
ASSETS=UNIT/'assets/three-cases-v2'
OUT.mkdir(parents=True,exist_ok=True)
ASSETS.mkdir(parents=True,exist_ok=True)
W,H,FPS=1280,720,24
ORANGE='#FF9228'; WHITE='#FFFFFF'; MUTED='#AAAAAA'
FONT='C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Bold.ttf'
REG='C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/Pretendard-Regular.ttf'
fonts={}
def f(size,bold=True):
    key=(size,bold)
    if key not in fonts: fonts[key]=ImageFont.truetype(FONT if bold else REG,size)
    return fonts[key]
def txt(d,xy,text,size=48,color=WHITE,bold=True,anchor=None):
    d.text(xy,text,font=f(size,bold),fill=color,anchor=anchor,spacing=12)
def ease(v):return 1-(1-max(0,min(1,v)))**3
def base(label):
    im=Image.new('RGB',(W,H),'#090909');d=ImageDraw.Draw(im)
    txt(d,(68,48),label,20,MUTED,False)
    txt(d,(1212,48),'NotionTalk',20,WHITE,True,'ra')
    return im,d
def typography(t):
    im,d=base('무료 웨비나 · 모션 그래픽으로 수업 영상 만들기')
    if t<4:
        txt(d,(640,245),'수업 자료가',76,WHITE,True,'ma')
        txt(d,(640,345+45*(1-ease(t/.65))),'영상이 되는 순간',94,ORANGE,True,'ma')
    elif t<8:
        txt(d,(640-100*(1-ease((t-4)/.65)),265),'글자는 흐르고',82,WHITE,True,'ma')
        txt(d,(640,375),'핵심은 커집니다',int(78+12*ease((t-4)/.8)),ORANGE,True,'ma')
    elif t<12:
        for j,(word,x) in enumerate([('텍스트',260),('링크',640),('지식',1020)]):
            q=ease((t-8-j*.22)/.6)
            txt(d,(x,300+70*(1-q)),word,72,ORANGE if j==1 else WHITE,True,'ma')
        txt(d,(640,440),'세 가지 출발점으로 직접 만들어 보세요',34,WHITE,False,'ma')
    elif t<16:
        txt(d,(640,210),'모션 그래픽으로',72,WHITE,True,'ma')
        txt(d,(640,315),'수업 영상 만들기',94,ORANGE,True,'ma')
        txt(d,(640,460),'노션톡 무료 웨비나',34,WHITE,False,'ma')
    else:
        txt(d,(640,210),'11월 1일 일요일',66,WHITE,True,'ma')
        txt(d,(640,305),'저녁 8시',110,ORANGE,True,'ma')
        txt(d,(640,465),'댓글에 ‘노션톡’을 남겨 주세요',38,WHITE,False,'ma')
    return im
def website(t):
    im,d=base('웹사이트 내용으로 만드는 소개 영상 · Notion 문서')
    if t<5:
        txt(d,(640,205),'메모가 쌓이면',76,WHITE,True,'ma')
        txt(d,(640,320),'문서로 정리하세요',88,ORANGE,True,'ma')
        txt(d,(640,470),'Notion 문서 소개',32,WHITE,False,'ma')
    elif t<13:
        txt(d,(80,150),'여러 콘텐츠를 한 문서에',56)
        rows=[('텍스트',260,ORANGE),('이미지·영상',360,WHITE),('코드',460,WHITE)]
        for j,(s,y,c) in enumerate(rows):
            q=ease((t-5-j*.25)/.65)
            x=90-int((1-q)*200)
            d.rounded_rectangle((x,y,x+int(1020*q),y+74),radius=12,fill='#252525')
            txt(d,(x+28,y+15),s,36,c)
    elif t<20:
        txt(d,(80,150),'긴 문서도 쉽게 찾도록',56)
        for j,s in enumerate(['수업 개요','활동 자료','정리와 과제']):
            q=ease((t-13-j*.3)/.6)
            x=95+j*355
            d.rounded_rectangle((x,300+60*(1-q),x+320,450+60*(1-q)),radius=16,fill=ORANGE if j==1 else '#252525')
            txt(d,(x+160,350+60*(1-q)),s,36,'#111111' if j==1 else WHITE,True,'ma')
        txt(d,(640,530),'목차에서 원하는 구간으로 이동',32,WHITE,False,'ma')
    elif t<26:
        txt(d,(80,150),'함께 쓰고 피드백하세요',56)
        d.rounded_rectangle((95,285,790,495),radius=18,fill='#252525')
        txt(d,(130,320),'수업 활동 문서',46)
        txt(d,(130,400),'공동 편집으로 내용을 채우고',30,MUTED,False)
        q=ease((t-20)/.7)
        d.rounded_rectangle((830,300+80*(1-q),1180,480+80*(1-q)),radius=18,fill=ORANGE)
        txt(d,(870,340+80*(1-q)),'댓글로 의견 남기기',28,'#111111')
    else:
        txt(d,(640,205),'담고 · 찾고 · 함께 쓰기',72,ORANGE,True,'ma')
        txt(d,(640,345),'Notion 문서',90,WHITE,True,'ma')
        txt(d,(640,490),'notion.com/ko/product/docs',26,MUTED,False,'ma')
    txt(d,(68,668),'내용 출처: Notion 공식 문서 소개 페이지 · 2026.10.27 확인',18,MUTED,False)
    return im
def atom(d,cx,cy,kind,t):
    if kind=='thomson':
        d.ellipse((cx-150,cy-150,cx+150,cy+150),fill='#49321C',outline=ORANGE,width=3)
        for x,y in [(-80,-55),(55,-85),(-40,80),(85,45)]:
            d.ellipse((cx+x-14,cy+y-14,cx+x+14,cy+y+14),fill=WHITE)
        for x,y in [(-30,-60),(65,5),(-65,15),(20,95)]:txt(d,(cx+x,cy+y),'+',28,ORANGE,True,'mm')
    else:
        radii=[95,155] if kind=='bohr' else [155]
        for r in radii:
            d.ellipse((cx-r,cy-r,cx+r,cy+r),outline='#666666',width=3)
        d.ellipse((cx-17,cy-17,cx+17,cy+17),fill=ORANGE)
        txt(d,(cx,cy+1),'+',23,'#101010',True,'mm')
        # One schematic electron, never a model of a literal observed orbit.
        r=radii[0];a=t*.8
        x,y=cx+r*math.cos(a),cy+r*math.sin(a)
        d.ellipse((x-10,y-10,x+10,y+10),fill=WHITE)
        if kind=='bohr':
            txt(d,(cx+165,cy-155),'n = 2',22,MUTED,False)
            txt(d,(cx+103,cy-95),'n = 1',22,MUTED,False)
def history(t):
    im,d=base('과학사 설명 영상 · 원자모형의 변화')
    if t<5:
        txt(d,(640,210),'보이지 않는 원자,',78,WHITE,True,'ma')
        txt(d,(640,325),'모형은 왜 바뀌었을까?',78,ORANGE,True,'ma')
    elif t<16:
        txt(d,(80,145),'톰슨 모형',60,ORANGE)
        txt(d,(80,255),'양전하가 퍼진 공간에',42)
        txt(d,(80,315),'전자가 들어 있는 그림',42)
        atom(d,950,360,'thomson',t)
        txt(d,(80,490),'원자의 내부 구조를 설명하려는 시도',28,MUTED,False)
    elif t<28:
        txt(d,(80,145),'1911 · 러더퍼드',60,ORANGE)
        txt(d,(80,255),'산란 결과를 설명하려면',42)
        txt(d,(80,315),'작고 집중된 중심이 필요',42)
        atom(d,950,360,'rutherford',t)
        txt(d,(80,490),'원자의 중심에 질량과 전하가 집중',28,MUTED,False)
    elif t<40:
        txt(d,(80,145),'1913 · 보어',60,ORANGE)
        txt(d,(80,255),'수소 원자의 에너지를',42)
        txt(d,(80,315),'정해진 상태로 설명',42)
        atom(d,950,360,'bohr',t)
        txt(d,(80,490),'전자의 에너지 상태를 구분하는 모형',28,MUTED,False)
    else:
        txt(d,(640,155),'새로운 증거와 설명이',62,WHITE,True,'ma')
        txt(d,(640,245),'모형을 바꿉니다',78,ORANGE,True,'ma')
        for j,kind in enumerate(['thomson','rutherford','bohr']):
            # The final row intentionally uses readable names rather than tiny diagrams.
            txt(d,(250+j*390,435),['톰슨','러더퍼드','보어'][j],46,WHITE,True,'ma')
        txt(d,(640,540),'보어 모형도 현대 원자모형으로 이어지는 한 단계',28,MUTED,False,'ma')
    txt(d,(68,650),'설명용 모식도 · 입자의 실제 크기 비율이나 전자의 관측 경로가 아님',18,MUTED,False)
    txt(d,(68,680),'근거: AIP 원자핵 발견사 / Manitoba Education, Models of Atomic Structure',18,MUTED,False)
    return im

records=[]
for stem,duration,draw,poster_time in [('01-typography',20,typography,2),('02-website',30,website,17),('03-atomic-history',45,history,32)]:
    target=OUT/(stem+'.mp4')
    error=BUILD/(stem+'.ffmpeg.log')
    with error.open('wb') as err:
        proc=subprocess.Popen([FFMPEG,'-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{W}x{H}','-pix_fmt','rgb24','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],stdin=subprocess.PIPE,stderr=err)
        for n in range(duration*FPS):
            im=draw(n/FPS)
            if n==int(poster_time*FPS):im.save(ASSETS/(stem+'.png'))
            if n in [int(duration*.2*FPS),int(duration*.5*FPS),int(duration*.85*FPS)]:im.save(ASSETS/(stem+f'-frame-{n:04}.png'))
            proc.stdin.write(im.tobytes())
        proc.stdin.close()
        if proc.wait():raise RuntimeError(error.read_text(errors='replace')[-2000:])
    # Full stream decode verifies all frames, not just header duration.
    result=subprocess.run([FFMPEG,'-v','error','-i',str(target),'-f','null','-'],capture_output=True)
    if result.returncode:raise RuntimeError(result.stderr.decode(errors='replace'))
    records.append(dict(file=str(target),duration=duration,fps=FPS,width=W,height=H,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),full_decode='passed',origin='locally-authored motion example; not an in-app prompt capture',audio=False))
    print('Created and decoded',target.name,flush=True)
(BUILD/'media-verification.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
