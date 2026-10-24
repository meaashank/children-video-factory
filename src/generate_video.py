#!/usr/bin/env python3
"""Render a short, frame-animated storybook short with Pillow, espeak-ng and FFmpeg."""
from __future__ import annotations
import math, os, re, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/"build"; OUTPUT=ROOT/"output"
W,H,FPS=720,1280,24
SCENES=[
 {"voice":"In a quiet moonlit forest lived Milo, a curious little fox who loved finding tiny wonders.",
  "caption":"Milo loved finding tiny wonders.","action":"intro","sky":(27,43,81)},
 {"voice":"One night, a soft blue glow flickered beneath a fern. Milo padded closer to investigate.",
  "caption":"A mysterious blue light!","action":"discover","sky":(30,48,91)},
 {"voice":"There, he found a little flower glowing all by itself. Milo leaned in, amazed.",
  "caption":"A flower that glowed!","action":"look","sky":(34,53,99)},
 {"voice":"His shy friend Pip peeked from behind a tree. Milo waved and invited Pip to come closer.",
  "caption":"Come and see, Pip!","action":"meet","sky":(38,58,105)},
 {"voice":"Together, they placed bright little stones around the flower. Its gentle light spread across the forest.",
  "caption":"Together, they made it shine.","action":"team","sky":(46,68,113)},
 {"voice":"The friends smiled as the path lit up. Milo learned that kindness shines brightest when it is shared.",
  "caption":"Kindness shines brighter when shared.","action":"ending","sky":(66,81,126)},
]
def font(size,bold=False):
 p="/usr/share/fonts/truetype/dejavu/DejaVuSans"+("-Bold" if bold else "")+".ttf"
 return ImageFont.truetype(p,size) if Path(p).exists() else ImageFont.load_default()
def run(cmd): subprocess.run(cmd,check=True)
def wrap(draw,text,f,maxw):
 out=[]; cur=""
 for word in text.split():
  test=(cur+" "+word).strip()
  if draw.textbbox((0,0),test,font=f)[2]<=maxw: cur=test
  else:
   if cur: out.append(cur)
   cur=word
 if cur: out.append(cur)
 return out
def background(scene, title, idx):
 im=Image.new("RGB",(W,H),scene["sky"]); d=ImageDraw.Draw(im)
 # stars and moon
 for x,y,r in [(70,150,3),(185,230,4),(320,120,3),(570,180,4),(650,330,3),(455,275,2),(120,380,3)]:
  d.ellipse((x-r,y-r,x+r,y+r),fill=(255,246,207))
 d.ellipse((510,105,615,210),fill=(255,232,174))
 d.ellipse((535,90,625,190),fill=scene["sky"])
 # layered hills and floor
 d.ellipse((-170,570,440,1030),fill=(34,78,72)); d.ellipse((250,560,900,1000),fill=(30,68,68))
 d.rectangle((0,850,W,H),fill=(35,86,69))
 # tree trunks and leafy crowns
 for x,y,s in [(62,790,1.1),(660,780,1.15),(155,900,.7),(585,920,.75)]:
  d.rectangle((int(x-12*s),int(y-120*s),int(x+12*s),int(y+70*s)),fill=(83,59,52))
  for ox,oy,r,c in [(-25,-135,52,(25,77,64)),(24,-165,60,(31,91,69)),(0,-205,50,(38,101,74))]:
   rr=int(r*s); cx=int(x+ox*s); cy=int(y+oy*s)
   d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill=c)
 # title
 d.rounded_rectangle((34,32,W-34,105),radius=22,fill=(13,23,43))
 shown=title if len(title)<32 else title[:29]+"..."
 d.text((W//2,68),shown,font=font(24,True),fill=(255,247,222),anchor="mm")
 d.text((W-42,128),f"{idx+1}/{len(SCENES)}",font=font(19,True),fill=(239,243,255),anchor="ra")
 return im
def fox(d,x,y,scale=1, wave=False):
 # tail, body, belly, head, ears
 d.ellipse((x-78*scale,y+12*scale,x+2*scale,y+65*scale),fill=(235,126,57))
 d.ellipse((x-78*scale,y+26*scale,x-43*scale,y+58*scale),fill=(255,229,198))
 d.ellipse((x-50*scale,y-4*scale,x+58*scale,y+83*scale),fill=(229,119,53))
 d.ellipse((x-27*scale,y+34*scale,x+35*scale,y+74*scale),fill=(255,225,188))
 d.ellipse((x-35*scale,y-78*scale,x+42*scale,y+5*scale),fill=(242,143,65))
 d.polygon([(x-29*scale,y-48*scale),(x-38*scale,y-105*scale),(x-1*scale,y-72*scale)],fill=(242,143,65))
 d.polygon([(x+8*scale,y-71*scale),(x+40*scale,y-105*scale),(x+35*scale,y-43*scale)],fill=(242,143,65))
 d.polygon([(x-26*scale,y-64*scale),(x-30*scale,y-92*scale),(x-12*scale,y-68*scale)],fill=(105,54,48))
 d.polygon([(x+15*scale,y-69*scale),(x+32*scale,y-92*scale),(x+29*scale,y-58*scale)],fill=(105,54,48))
 d.ellipse((x-20*scale,y-48*scale,x-12*scale,y-38*scale),fill=(31,30,37))
 d.ellipse((x+13*scale,y-48*scale,x+21*scale,y-38*scale),fill=(31,30,37))
 d.ellipse((x-7*scale,y-28*scale,x+21*scale,y-8*scale),fill=(255,231,202))
 d.ellipse((x+3*scale,y-27*scale,x+14*scale,y-17*scale),fill=(42,34,37))
 d.ellipse((x-35*scale,y+67*scale,x-5*scale,y+91*scale),fill=(113,63,45))
 d.ellipse((x+19*scale,y+67*scale,x+49*scale,y+91*scale),fill=(113,63,45))
 if wave:
  d.line((x+35*scale,y+18*scale,x+52*scale,y-8*scale),fill=(229,119,53),width=max(4,int(10*scale)))
  d.ellipse((x+43*scale,y-19*scale,x+61*scale,y-1*scale),fill=(255,222,184))
def hedgehog(d,x,y,scale=1):
 # soft spines and body
 for i in range(9):
  px=x-42*scale+i*10*scale
  d.polygon([(px,y+18*scale),(px-6*scale,y-14*scale),(px+10*scale,y+5*scale)],fill=(117,87,73))
 d.ellipse((x-44*scale,y-2*scale,x+43*scale,y+47*scale),fill=(180,137,102))
 d.ellipse((x+15*scale,y+8*scale,x+50*scale,y+35*scale),fill=(226,184,143))
 d.ellipse((x+28*scale,y+17*scale,x+35*scale,y+24*scale),fill=(36,31,30))
 d.ellipse((x-20*scale,y+10*scale,x-13*scale,y+17*scale),fill=(36,31,30))
 d.ellipse((x-25*scale,y+39*scale,x-7*scale,y+52*scale),fill=(90,63,49))
 d.ellipse((x+17*scale,y+39*scale,x+35*scale,y+52*scale),fill=(90,63,49))
def flower(d,x,y,pulse=0):
 r=int(46+6*math.sin(pulse))
 # glow rings
 for rr,col in [(r+45,(83,153,255,22)),(r+25,(83,153,255,35))]:
  d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=col)
 d.line((x,y+24,x,y+115),fill=(83,192,126),width=9)
 d.ellipse((x-42,y+57,x-2,y+81),fill=(66,163,103))
 d.ellipse((x+1,y+75,x+39,y+98),fill=(66,163,103))
 for dx,dy in [(-25,-6),(0,-31),(25,-6),(-16,19),(16,19)]:
  d.ellipse((x+dx-18,y+dy-18,x+dx+18,y+dy+18),fill=(100,177,255))
 d.ellipse((x-17,y-17,x+17,y+17),fill=(255,226,134))
def make_frame(scene,idx,frame,title):
 t=frame/FPS
 im=background(scene,title,idx).convert("RGBA")
 # Animated transparent light layer so glow can actually blend with background.
 glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
 action=scene["action"]
 fx=220+int(120*min(1,t/2)) if action in ("intro","discover","look") else 275
 if action=="intro": fx=180+int(55*math.sin(t*2))
 if action=="discover": fx=175+int(85*min(1,t/2))
 if action=="look": fx=260+int(8*math.sin(t*3))
 if action in ("meet","team","ending"): fx=245+int(8*math.sin(t*2))
 fy=820+int(5*math.sin(t*4))
 flower_x=500 if action in ("intro","discover","look") else 420
 flower_y=845
 # Flower light grows during team/ending.
 strength=(0.5+0.5*math.sin(t*4)) if action in ("team","ending") else (0.25+0.15*math.sin(t*3))
 radius=int(80+strength*75)
 gd.ellipse((flower_x-radius,flower_y-radius,flower_x+radius,flower_y+radius),fill=(90,160,255,int(20+strength*28)))
 im=Image.alpha_composite(im,glow)
 d=ImageDraw.Draw(im)
 # Milo walks in from the left in the opening and discovery shots.
 fox(d,fx,fy,1.0,wave=action in ("meet","ending"))
 flower(d,flower_x,flower_y,t*2)
 # Pip appears and stays in the last three scenes; little bobbing motion.
 if action in ("meet","team","ending"):
  hx=560-int(18*min(1,t/1.2))
  hedgehog(d,hx,875+int(4*math.sin(t*4)),0.92)
 # Sparkles animate around the flower in the final two scenes.
 if action in ("team","ending"):
  for j in range(7):
   a=t*1.4+j*math.tau/7
   sx=flower_x+int((82+8*math.sin(t*3))*math.cos(a))
   sy=flower_y+int((76+8*math.sin(t*3))*math.sin(a))
   rr=3+(j%2)
   d.ellipse((sx-rr,sy-rr,sx+rr,sy+rr),fill=(255,239,158))
 # Captions remain in a stable lower safe area.
 lines=wrap(d,scene["caption"],font(29,True),W-100)
 lh=40; bh=len(lines)*lh+34; top=H-bh-68
 d.rounded_rectangle((34,top,W-34,top+bh),radius=22,fill=(10,19,34,230))
 for j,line in enumerate(lines):
  d.text((W//2,top+17+j*lh),line,font=font(29,True),fill=(255,255,255),anchor="ma")
 return im.convert("RGB")
def main():
 for tool in ("ffmpeg","ffprobe","espeak-ng"):
  if not shutil.which(tool): raise SystemExit("Missing required program: "+tool)
 title=re.sub(r"[^\w\s'!?,.-]","",os.environ.get("STORY_TITLE","Milo and the Moonflower").strip())[:60] or "Milo and the Moonflower"
 shutil.rmtree(WORK,ignore_errors=True); shutil.rmtree(OUTPUT,ignore_errors=True)
 WORK.mkdir(parents=True); OUTPUT.mkdir(parents=True)
 clips=[]
 for i,scene in enumerate(SCENES):
  scene_dir=WORK/f"scene_{i:02d}"; scene_dir.mkdir()
  audio=WORK/f"voice_{i:02d}.wav"; clip=WORK/f"clip_{i:02d}.mp4"
  run(["espeak-ng","-v","en-us","-s","145","-p","56","-w",str(audio),scene["voice"]])
  # A fixed 5.5-second scene gives each action time to read; audio is padded gently.
  total_frames=int(5.5*FPS)
  for n in range(total_frames):
   make_frame(scene,i,n,title).save(scene_dir/f"frame_{n:04d}.png",compress_level=1)
  run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate",str(FPS),
       "-i",str(scene_dir/"frame_%04d.png"),"-i",str(audio),
       "-vf","format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","24",
       "-c:a","aac","-b:a","96k","-af","apad=pad_dur=0.8","-t","5.5",
       "-movflags","+faststart",str(clip)])
  clips.append(clip)
 concat=WORK/"concat.txt"
 concat.write_text("".join(f"file '{p.resolve()}'\n" for p in clips),encoding="utf-8")
 out=OUTPUT/"childrens_story.mp4"
 run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),
      "-c","copy","-movflags","+faststart",str(out)])
 run(["ffprobe","-v","error","-show_entries","format=duration,size","-of","default=noprint_wrappers=1",str(out)])
 print(f"Rendered animated story: {out}")
if __name__=="__main__": main()
