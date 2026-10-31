#!/usr/bin/env python3
"""Generate natural-sounding narration with the free Kokoro neural TTS model."""
import math
import subprocess
import urllib.request
import wave
import struct
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

OUT = Path("out")
OUT.mkdir(exist_ok=True)
MODEL = Path("kokoro-v1.0.onnx")
VOICES = Path("voices-v1.0.bin")

def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 1_000_000:
        return
    print(f"Downloading {path.name} ...", flush=True)
    urllib.request.urlretrieve(url, path)
    if path.stat().st_size < 1_000_000:
        raise RuntimeError(f"Model download appears incomplete: {path}")

BASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
download(BASE + "kokoro-v1.0.onnx", MODEL)
download(BASE + "voices-v1.0.bin", VOICES)

story_parts = [
    "As evening settled over the old bazaar, a thousand little lights began to glow. "
    "The market was alive with colour, music, and the happy chatter of families.",

    "Meera had come to buy sweets for Diwali. As she wandered past the bright stalls, "
    "she noticed an elderly potter sitting quietly beside a table of beautiful handmade diyas.",

    "The potter had worked for many days, but hardly anyone had stopped to look. "
    "Meera felt that his little lamps deserved to shine. She thought for a moment, then smiled.",

    "She carefully arranged the diyas in a glowing trail along the front of his stall. "
    "Then she called out, with excitement: Beautiful handmade diyas! Take a little light home tonight!",

    "People turned around. One family came closer, then another. Soon, a cheerful crowd gathered "
    "around the potter's stall. The old man looked at Meera with grateful eyes.",

    "Thank you, child, he said. You have made this Diwali brighter for me. "
    "Meera smiled as the whole street shimmered with tiny flames. "
    "And she discovered that kindness is a light that grows brighter when you share it."
]

kokoro = Kokoro(str(MODEL), str(VOICES))
voice = "af_sarah"  # Warm, expressive American English voice.
audio_parts = []
sample_rate = 24000
for index, text in enumerate(story_parts, start=1):
    print(f"Synthesizing narration segment {index}/{len(story_parts)} ...", flush=True)
    samples, sample_rate = kokoro.create(text, voice=voice, speed=0.94, lang="en-us")
    audio_parts.append(np.asarray(samples, dtype=np.float32))
    audio_parts.append(np.zeros(int(sample_rate * 0.28), dtype=np.float32))

narration = np.concatenate(audio_parts)
sf.write(OUT / "narration.wav", narration, sample_rate)

# Keep the original generated instrumental bed, mixed quietly under the voice.
rate, duration = 22050, 60
with wave.open(str(OUT / "music.wav"), "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(rate)
    chunk = []
    for i in range(rate * duration):
        t = i / rate
        fade = min(1, t / 2, (duration - t) / 3)
        val = (0.12 * math.sin(2 * math.pi * 196 * t) +
               0.08 * math.sin(2 * math.pi * 246.94 * t) +
               0.07 * math.sin(2 * math.pi * 293.66 * t) +
               0.025 * math.sin(2 * math.pi * 392 * t))
        chunk.append(struct.pack("<h", int(32767 * max(0, fade) * val)))
        if len(chunk) >= 8192:
            w.writeframes(b"".join(chunk))
            chunk = []
    if chunk:
        w.writeframes(b"".join(chunk))

subprocess.run([
    "ffmpeg", "-y", "-i", str(OUT / "narration.wav"), "-i", str(OUT / "music.wav"),
    "-filter_complex",
    "[0:a]apad,atrim=0:60,volume=1.0,afade=t=in:st=0:d=1.2,afade=t=out:st=57:d=3[n];"
    "[1:a]volume=0.12,afade=t=in:st=0:d=2,afade=t=out:st=56:d=4[m];"
    "[n][m]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]",
    "-map", "[a]", "-t", "60", "-c:a", "aac", "-b:a", "160k",
    str(OUT / "story-audio.m4a")
], check=True)
print(f"Created natural neural narration ({voice}) and mixed audio.")
