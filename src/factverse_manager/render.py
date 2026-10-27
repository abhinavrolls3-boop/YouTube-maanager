"""Render lightweight topic-specific animated motion graphics and a thumbnail."""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio

W, H = 720, 1280


def _font(size):
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def _wrap(draw, text, font, max_width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def scene_for_topic(text):
    """Choose a simple illustrative scene from the curated topic title/text."""
    value = str(text).lower()
    if any(word in value for word in ("octopus", "squid", "tentacle", "hearts")):
        return "octopus"
    if "venus" in value:
        return "venus"
    if any(word in value for word in ("shark", "ocean predator")):
        return "shark"
    if any(word in value for word in ("honey", "bee", "hive", "honeycomb")):
        return "honey"
    if any(word in value for word in ("astronaut", "space", "orbit", "planet", "gravity", "microgravity", "moon", "jupiter")):
        return "space"
    return "science"


def _draw_scene(draw, scene, phase):
    cx, cy = W // 2, 300
    if scene == "space":
        for radius in (120, 175, 230):
            draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=(35, 83, 135), width=3)
        x, y = cx + int(170 * math.cos(phase)), cy + int(170 * math.sin(phase))
        draw.ellipse((x-20, y-20, x+20, y+20), fill=(80, 210, 255))
        draw.ellipse((cx-56, cy-56, cx+56, cy+56), fill=(42, 125, 220), outline=(170, 225, 255), width=4)
        draw.arc((cx-50, cy-25, cx+50, cy+28), 190, 350, fill=(100, 190, 255), width=5)
    elif scene == "octopus":
        body = (cx, cy-8)
        for arm in range(8):
            angle = math.tau * arm / 8
            sway = math.sin(phase + arm * 0.8) * 18
            p1 = (cx + int(70 * math.cos(angle)), cy + int(55 * math.sin(angle)))
            p2 = (cx + int(125 * math.cos(angle+0.16)) + int(sway), cy + int(110 * math.sin(angle+0.16)))
            p3 = (cx + int(170 * math.cos(angle+0.25)) + int(sway*1.4), cy + int(165 * math.sin(angle+0.25)))
            draw.line([body, p1, p2, p3], fill=(186, 111, 255), width=18, joint="curve")
            for dot in range(1, 4):
                px = int(p1[0] + (p3[0]-p1[0]) * dot / 4)
                py = int(p1[1] + (p3[1]-p1[1]) * dot / 4)
                draw.ellipse((px-4, py-4, px+4, py+4), fill=(255, 202, 235))
        draw.ellipse((cx-78, cy-82, cx+78, cy+76), fill=(151, 78, 220), outline=(230, 186, 255), width=5)
        draw.ellipse((cx-38, cy-18, cx-12, cy+10), fill="white")
        draw.ellipse((cx+12, cy-18, cx+38, cy+10), fill="white")
        draw.ellipse((cx-29, cy-12, cx-19, cy+3), fill=(20, 28, 55))
        draw.ellipse((cx+20, cy-12, cx+30, cy+3), fill=(20, 28, 55))
        draw.text((cx-34, cy+102), "3 HEARTS", font=_font(23), fill=(255, 205, 235))
    elif scene == "venus":
        for radius in (190, 225):
            draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=(72, 78, 127), width=2)
        r = 126
        draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(225, 125, 55), outline=(255, 211, 131), width=5)
        for offset in (-62, -18, 35, 76):
            draw.arc((cx-r+10, cy+offset-24, cx+r-10, cy+offset+24), 185, 355, fill=(255, 192, 105), width=9)
        angle = phase
        x, y = cx + int(205 * math.cos(angle)), cy + int(205 * math.sin(angle))
        draw.ellipse((x-12, y-12, x+12, y+12), fill=(255, 226, 159))
        draw.text((cx-53, cy-15), "VENUS", font=_font(26), fill=(255, 245, 214))
    elif scene == "shark":
        shift = int(30 * math.sin(phase))
        left, right = cx-185+shift, cx+175+shift
        mid = cy
        draw.polygon([(left, mid), (left+55, mid-55), (right-45, mid-35), (right+38, mid), (right-45, mid+35), (left+55, mid+55)],
                     fill=(102, 169, 205), outline=(194, 235, 250))
        draw.polygon([(cx-30+shift, mid-40), (cx+15+shift, mid-115), (cx+65+shift, mid-33)], fill=(102, 169, 205), outline=(194, 235, 250))
        draw.polygon([(left+12, mid-5), (left-50, mid-58), (left-30, mid+8)], fill=(102, 169, 205), outline=(194, 235, 250))
        draw.polygon([(cx+30+shift, mid+28), (cx+75+shift, mid+95), (cx+100+shift, mid+23)], fill=(102, 169, 205), outline=(194, 235, 250))
        draw.ellipse((cx-105+shift, mid-14, cx-89+shift, mid+2), fill=(8, 18, 42))
        for g in range(3):
            x = cx-75+shift+g*13
            draw.line((x, mid+5, x-3, mid+27), fill=(46, 101, 139), width=3)
        draw.arc((cx+70+shift, mid-8, cx+125+shift, mid+20), 5, 75, fill=(20, 52, 83), width=3)
    elif scene == "honey":
        size = 48
        for row in range(4):
            for col in range(6):
                x = 100 + col*104 + (row % 2)*52
                y = 125 + row*80
                points = [(x+int(size*math.cos(math.pi/3*k)), y+int(size*math.sin(math.pi/3*k))) for k in range(6)]
                draw.polygon(points, outline=(226, 164, 58), fill=(52, 44, 32))
        drop_y = cy + int(20*math.sin(phase))
        draw.ellipse((cx-45, drop_y-55, cx+45, drop_y+40), fill=(255, 184, 42), outline=(255, 226, 137), width=4)
        draw.polygon([(cx, drop_y-90), (cx-42, drop_y-20), (cx+42, drop_y-20)], fill=(255, 184, 42))
        draw.ellipse((cx-20, drop_y-28, cx-5, drop_y-10), fill=(255, 231, 166))
    else:
        for radius in (110, 160, 210):
            draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=(35, 83, 135), width=3)
        x, y = cx + int(150 * math.cos(phase)), cy + int(150 * math.sin(phase))
        draw.ellipse((x-18, y-18, x+18, y+18), fill=(80, 210, 255))
        draw.ellipse((cx-62, cy-62, cx+62, cy+62), fill=(42, 125, 220), outline=(170, 225, 255), width=4)
        draw.text((cx-16, cy-30), "?", font=_font(58), fill="white")


def make_frame(index, total, title, explanation):
    im = Image.new("RGB", (W, H), (8, 18, 42))
    d = ImageDraw.Draw(im)
    phase = index / max(total, 1) * math.tau
    scene = scene_for_topic(str(title) + " " + str(explanation))
    _draw_scene(d, scene, phase)
    d.text((36, 48), "FACTVERSE", font=_font(34), fill=(105, 220, 255))
    d.rounded_rectangle((34, 590, W-34, 1125), radius=34, fill=(15, 35, 68), outline=(42, 93, 145), width=3)
    yy = 650
    tf = _font(44)
    for line in _wrap(d, title, tf, W-100)[:4]:
        d.text((58, yy), line, font=tf, fill=(255, 255, 255))
        yy += 62
    yy = max(850, yy+22)
    bf = _font(28)
    for line in _wrap(d, explanation, bf, W-100)[:6]:
        if yy > 1060:
            break
        d.text((58, yy), line, font=bf, fill=(195, 216, 240))
        yy += 42
    d.text((36, 1195), "Curiosity starts here  •  Follow for more", font=_font(22), fill=(105, 220, 255))
    return im


def render_video(title, explanation, output="output/factverse_sample.mp4", thumbnail="output/thumbnail.png", seconds=18, fps=12):
    if seconds < 5 or seconds > 60:
        raise ValueError("Duration must be between 5 and 60 seconds.")
    out, thumb = Path(output), Path(thumbnail)
    out.parent.mkdir(parents=True, exist_ok=True)
    thumb.parent.mkdir(parents=True, exist_ok=True)
    total = seconds * fps
    make_frame(0, total, title, explanation).save(thumb)
    writer = imageio.get_writer(str(out), fps=fps, codec="libx264", macro_block_size=16, ffmpeg_log_level="error", quality=7)
    try:
        for i in range(total):
            writer.append_data(np.asarray(make_frame(i, total, title, explanation)))
    finally:
        writer.close()
    return str(out), str(thumb)
