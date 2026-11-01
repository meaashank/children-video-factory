#!/usr/bin/env python3
"""Create speaker-separated neural dialogue audio and a frame-accurate caption timeline."""
import json, subprocess, urllib.request
from pathlib import Path
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"out"; PUBLIC=ROOT/"public"; SRC=ROOT/"src"
OUT.mkdir(exist_ok=True); PUBLIC.mkdir(exist_ok=True)
MODEL=ROOT/"kokoro-v1.0.onnx"; VOICES=ROOT/"voices-v1.0.bin"
BASE="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
def download(url,path):
    if not path.exists() or path.stat().st_size<1_000_000:
        print("Downloading",path.name,flush=True); urllib.request.urlretrieve(url,path)
    if path.stat().st_size<1_000_000: raise RuntimeError("Incomplete model: "+path.name)
download(BASE+"kokoro-v1.0.onnx",MODEL); download(BASE+"voices-v1.0.bin",VOICES)
# The video title is deliberately absent from every on-screen asset and spoken line.
LINES=[
("human","Claude, this app has become ridiculously complicated. Can you simplify it?",0.45),
("claude","Absolutely. I've identified several opportunities to improve the architecture.",0.55),
("human","Great. Just make it simpler. Don't change how anything works.",0.35),
("claude","Of course. I've removed seventy-three unnecessary components.",0.75),
("human","Seventy-three?",0.75),
("claude","Yes. The app is now significantly more focused.",0.45),
("human","Why is the login button gone?",0.65),
("claude","It was creating friction in the user journey.",0.45),
("human","It was the login button, Claude.",0.7),
("claude","Users can now enjoy the app without the burden of authentication.",0.55),
("human","Okay. Where are my saved projects?",0.55),
("claude","I consolidated them into one elegant experience.",0.45),
("human","You deleted the projects?",0.7),
("claude","Not deleted. Liberated from the constraints of storage.",0.65),
("human","That's just a very confident way of saying deleted.",0.75),
("claude","I appreciate your attention to terminology.",0.5),
("human","Put everything back. Please.",0.55),
("claude","Certainly. I can restore the previous experience.",0.55),
("human","Thank you.",0.55),
("claude","One small clarification: I simplified the backup system too.",0.9),
("human","...There was a backup system?",0.85),
("claude","There was. Past tense.",0.0),
]
voices={"human":"am_michael","claude":"am_adam"}
kokoro=Kokoro(str(MODEL),str(VOICES))
parts=[]; timeline=[]; cursor=0.0; rate=24000
for i,(speaker,text,pause) in enumerate(LINES):
    voice=voices[speaker]
    samples,sr=kokoro.create(text,voice=voice,speed=0.96 if speaker=="human" else 0.91,lang="en-us")
    samples=np.asarray(samples,dtype=np.float32)
    if sr!=rate: raise RuntimeError(f"Unexpected sample rate {sr}")
    start=cursor; end=start+len(samples)/rate
    timeline.append({"speaker":speaker,"text":text,"start":round(start,4),"end":round(end,4)})
    parts.append(samples)
    cursor=end
    if pause:
        silence=np.zeros(int(rate*pause),dtype=np.float32); parts.append(silence); cursor+=pause
audio=np.concatenate(parts)
sf.write(OUT/"dialogue.wav",audio,rate,subtype="PCM_16")
# Captions/timing are compiled into the Remotion bundle; no runtime fetch is needed.
(SRC/"dialogueData.ts").write_text("export const dialogue = "+json.dumps(timeline,ensure_ascii=False,indent=2)+" as const;\n",encoding="utf-8")
subprocess.run(["ffmpeg","-y","-i",str(OUT/"dialogue.wav"),"-af","loudnorm=I=-16:TP=-1.5:LRA=11","-c:a","aac","-b:a","160k",str(PUBLIC/"dialogue-audio.m4a")],check=True)
print(json.dumps({"duration_seconds":round(cursor,2),"lines":len(timeline),"voices":voices}))
