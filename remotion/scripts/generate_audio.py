#!/usr/bin/env python3
"""Create free narration and a simple original ambient music bed using system tools."""
import os, subprocess, wave, struct, math
from pathlib import Path
OUT = Path("out")
OUT.mkdir(exist_ok=True)
narration = (
    "As evening fell, the old bazaar glowed with a thousand little lights. "
    "Meera had come to buy sweets. But one quiet stall caught her eye. "
    "An elderly potter had made beautiful diyas, yet hardly anyone stopped. "
    "Meera had an idea. She arranged the little lamps in a shining trail and called out, "
    ' "Beautiful handmade diyas! Bring a little light into your home!" '
    "Curious shoppers gathered around. Soon, the potter's stall was full of smiling customers. "
    "The old potter thanked Meera. And as the whole market sparkled, Meera discovered something special: "
    "kindness is a light that grows brighter when you share it."
)
subprocess.run(["espeak-ng", "-v", "en+f3", "-s", "145", "-p", "62", "-w", str(OUT/"narration.wav"), narration], check=True)
# 60-second, gentle original tonal bed; generated locally, no external audio or paid API.
rate, duration = 22050, 60
with wave.open(str(OUT/"music.wav"), "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    chunk = []
    for i in range(rate * duration):
        t = i / rate
        fade = min(1, t/2, (duration-t)/3)
        # Soft, slow triad with gentle pulse; kept well below narration.
        val = (0.12*math.sin(2*math.pi*196*t) + 0.08*math.sin(2*math.pi*246.94*t) +
               0.07*math.sin(2*math.pi*293.66*t) + 0.025*math.sin(2*math.pi*392*t))
        sample = int(32767 * max(0, fade) * val)
        chunk.append(struct.pack("<h", sample))
        if len(chunk) >= 8192:
            w.writeframes(b"".join(chunk)); chunk=[]
    if chunk: w.writeframes(b"".join(chunk))
subprocess.run([
    "ffmpeg", "-y", "-i", str(OUT/"narration.wav"), "-i", str(OUT/"music.wav"),
    "-filter_complex",
    "[0:a]apad,atrim=0:60,volume=1.0,afade=t=in:st=0:d=1.5,afade=t=out:st=57:d=3[n];"
    "[1:a]volume=0.22,afade=t=in:st=0:d=2,afade=t=out:st=56:d=4[m];"
    "[n][m]amix=inputs=2:duration=longest:normalize=0[a]",
    "-map", "[a]", "-t", "60", "-c:a", "aac", "-b:a", "128k", str(OUT/"story-audio.m4a")
], check=True)
print("Created 60-second narration + original generated music bed.")
