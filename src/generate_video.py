#!/usr/bin/env python3
"""Generate a short illustrated children's story using Pillow, espeak-ng and FFmpeg."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "build"
OUTPUT = ROOT / "output"
WIDTH, HEIGHT = 720, 1280
FPS = 24

STORY = [
    {
        "narration": "At the edge of a quiet forest lived Milo, a little fox who collected things that glowed.",
        "caption": "Milo loved all things that glowed.",
        "sky": (35, 52, 93), "ground": (38, 83, 74), "moon": True,
        "fox": (360, 770), "flower": (500, 820), "stars": True,
    },
    {
        "narration": "One evening, Milo found a tiny blue flower hiding beneath a fern. Its petals shimmered like the stars.",
        "caption": "A tiny blue flower shimmered.",
        "sky": (39, 58, 105), "ground": (35, 91, 72), "moon": True,
        "fox": (280, 790), "flower": (470, 830), "stars": True,
    },
    {
        "narration": "The flower whispered, I can shine brighter when someone shares their light with a friend.",
        "caption": "Sharing makes a little light grow.",
        "sky": (45, 63, 110), "ground": (36, 93, 72), "moon": True,
        "fox": (260, 790), "flower": (450, 820), "stars": True,
    },
    {
        "narration": "Milo called his shy friend Pip the hedgehog. Together, they placed little glowing stones around the flower.",
        "caption": "Milo invited his friend Pip.",
        "sky": (47, 67, 116), "ground": (39, 98, 75), "moon": True,
        "fox": (250, 790), "flower": (450, 820), "stars": True,
    },
    {
        "narration": "With every kind act, the flower grew brighter, lighting the path for every animal in the forest.",
        "caption": "Kindness lit the whole forest.",
        "sky": (56, 76, 127), "ground": (44, 105, 78), "moon": True,
        "fox": (300, 790), "flower": (450, 790), "stars": True,
    },
    {
        "narration": "That night, Milo learned that the loveliest light is the one we help others find. And the forest glowed until morning.",
        "caption": "The best light is shared.",
        "sky": (73, 91, 140), "ground": (50, 112, 81), "moon": True,
        "fox": (330, 790), "flower": (470, 800), "stars": True,
    },
]


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, chosen_font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=chosen_font)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_tree(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
    trunk = int(26 * scale)
    draw.rounded_rectangle((x - trunk // 2, y - 90 * scale, x + trunk // 2, y + 65 * scale),
                           radius=8, fill=(92, 66, 53))
    for dx, dy, r, color in [
        (-35, -105, 55, (29, 79, 66)),
        (25, -135, 62, (34, 94, 72)),
        (0, -175, 52, (40, 105, 78)),
    ]:
        cx, cy, radius = int(x + dx * scale), int(y + dy * scale), int(r * scale)
        draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), fill=color)


def draw_fox(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    # Tail
    draw.ellipse((x-88, y+5, x-5, y+68), fill=(232, 126, 58))
    draw.ellipse((x-86, y+24, x-52, y+61), fill=(255, 232, 202))
    # Body and head
    draw.ellipse((x-62, y-12, x+70, y+96), fill=(231, 123, 54))
    draw.ellipse((x-38, y+38, x+48, y+88), fill=(255, 225, 188))
    draw.ellipse((x-42, y-92, x+48, y+5), fill=(240, 143, 66))
    # Ears
    draw.polygon([(x-35,y-62),(x-42,y-119),(x-4,y-83)], fill=(240,143,66))
    draw.polygon([(x+8,y-82),(x+42,y-120),(x+37,y-55)], fill=(240,143,66))
    draw.polygon([(x-31,y-76),(x-34,y-105),(x-15,y-82)], fill=(91,53,47))
    draw.polygon([(x+18,y-82),(x+35,y-105),(x+31,y-72)], fill=(91,53,47))
    # Face, muzzle and eyes
    draw.ellipse((x-24,y-55,x-14,y-43), fill=(35,35,43))
    draw.ellipse((x+15,y-55,x+25,y-43), fill=(35,35,43))
    draw.ellipse((x-12,y-31,x+22,y-9), fill=(255,231,201))
    draw.ellipse((x+1,y-31,x+14,y-19), fill=(48,39,43))
    # Feet
    draw.ellipse((x-43,y+74,x-6,y+99), fill=(112,62,45))
    draw.ellipse((x+25,y+74,x+59,y+99), fill=(112,62,45))


def draw_flower(draw: ImageDraw.ImageDraw, x: int, y: int, glow: int = 1) -> None:
    # A soft halo is built from translucent concentric circles.
    halo = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    for radius, alpha in [(100, 12), (75, 18), (48, 24)]:
        hd.ellipse((x-radius,y-radius,x+radius,y+radius), fill=(111, 196, 255, alpha * glow))
    draw._image.alpha_composite(halo) if hasattr(draw, "_image") else None
    draw.line((x, y+20, x, y+112), fill=(90, 203, 139), width=10)
    draw.ellipse((x-48,y+58,x-4,y+83), fill=(70,177,113))
    draw.ellipse((x+2,y+76,x+45,y+101), fill=(70,177,113))
    for dx, dy in [(-28,-10),(0,-34),(28,-10),(-18,20),(18,20)]:
        draw.ellipse((x+dx-19,y+dy-19,x+dx+19,y+dy+19), fill=(101,180,255))
    draw.ellipse((x-19,y-19,x+19,y+19), fill=(255,226,131))


def make_scene(scene: dict, index: int, title: str) -> Path:
    image = Image.new("RGBA", (WIDTH, HEIGHT), scene["sky"] + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    # Stars
    if scene["stars"]:
        for x, y, r in [(90,140,4),(210,205,3),(570,155,4),(625,270,3),
                        (120,340,3),(510,370,3),(335,115,3),(650,450,2)]:
            draw.ellipse((x-r,y-r,x+r,y+r), fill=(255,248,211,220))
    # Moon
    draw.ellipse((500, 115, 610, 225), fill=(255, 231, 164))
    draw.ellipse((530, 98, 620, 195), fill=scene["sky"])
    # Distant hills
    draw.ellipse((-150, 570, 430, 930), fill=(42, 88, 79))
    draw.ellipse((280, 530, 900, 940), fill=(35, 77, 72))
    # Forest floor
    draw.rectangle((0, 850, WIDTH, HEIGHT), fill=scene["ground"])
    # Trees frame the scene
    draw_tree(draw, 75, 770, 1.0)
    draw_tree(draw, 650, 780, 1.15)
    draw_tree(draw, 155, 940, 0.72)
    # Little glowing motes
    for x, y in [(130,700),(565,670),(205,610),(590,920),(95,1030)]:
        draw.ellipse((x-5,y-5,x+5,y+5), fill=(255,227,139,220))
    # Flower glow must be composited on the image before drawing foreground.
    x, y = scene["flower"]
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((x-105,y-105,x+105,y+105), fill=(91,166,255,35))
    gd.ellipse((x-65,y-65,x+65,y+65), fill=(91,166,255,30))
    image = Image.alpha_composite(image, glow)
    draw = ImageDraw.Draw(image, "RGBA")
    draw_flower(draw, x, y)
    fx, fy = scene["fox"]
    draw_fox(draw, fx, fy)

    # Title chip and scene number
    draw.rounded_rectangle((42, 36, WIDTH-42, 112), radius=24, fill=(13,24,45,180))
    title_font = font(25, True)
    shown_title = title if len(title) <= 34 else title[:31].rstrip() + "..."
    draw.text((WIDTH//2, 74), shown_title, font=title_font, fill=(255,248,224),
              anchor="mm", stroke_width=0)
    draw.text((WIDTH-48, 137), f"{index+1}/{len(STORY)}", font=font(20, True),
              fill=(235,242,255), anchor="ra")

    # Captions with a dark backing for readability.
    caption_font = font(30, True)
    lines = wrap_text(draw, scene["caption"], caption_font, WIDTH-112)
    line_h = 42
    box_h = len(lines) * line_h + 42
    top = HEIGHT - box_h - 78
    draw.rounded_rectangle((38, top, WIDTH-38, top+box_h), radius=24, fill=(12,20,35,220))
    for i, line in enumerate(lines):
        draw.text((WIDTH//2, top+22+i*line_h), line, font=caption_font,
                  fill=(255,255,255), anchor="ma")
    return save_image(image, WORK / f"scene_{index:02d}.png")


def save_image(image: Image.Image, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, quality=92)
    return path


def main() -> None:
    for tool in ("ffmpeg", "espeak-ng"):
        if shutil.which(tool) is None:
            raise SystemExit(f"Required program not found: {tool}")

    title = os.environ.get("STORY_TITLE", "Milo and the Moonflower").strip()
    title = re.sub(r"[^\w\s'!?,.-]", "", title)[:70] or "Milo and the Moonflower"
    shutil.rmtree(WORK, ignore_errors=True)
    shutil.rmtree(OUTPUT, ignore_errors=True)
    WORK.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    clips: list[Path] = []
    for index, scene in enumerate(STORY):
        image_path = make_scene(scene, index, title)
        audio_path = WORK / f"voice_{index:02d}.wav"
        clip_path = WORK / f"clip_{index:02d}.mp4"
        run(["espeak-ng", "-v", "en-us", "-s", "142", "-p", "57",
             "-w", str(audio_path), scene["narration"]])
        # A gentle zoom keeps the illustrations from feeling completely static.
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-loop", "1", "-framerate", str(FPS), "-i", str(image_path),
            "-i", str(audio_path),
            "-vf", f"zoompan=z='min(zoom+0.0007,1.045)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS},format=yuv420p",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "25",
            "-c:a", "aac", "-b:a", "96k", "-af", "apad",
            "-shortest", "-movflags", "+faststart", str(clip_path),
        ])
        clips.append(clip_path)

    concat_file = WORK / "concat.txt"
    concat_file.write_text("".join(f"file '{p.resolve()}'\n" for p in clips), encoding="utf-8")
    output_path = OUTPUT / "mil o-and-the-moonflower.mp4"
    # Avoid spaces in the final artifact filename.
    output_path = OUTPUT / "childrens_story.mp4"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c", "copy", "-movflags", "+faststart", str(output_path),
    ])
    run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
         "-of", "default=noprint_wrappers=1", str(output_path)])
    print(f"Video ready: {output_path}")


if __name__ == "__main__":
    main()
