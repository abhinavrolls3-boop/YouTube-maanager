"""Render lightweight animated motion graphics and a thumbnail."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
W, H = 720, 1280

def _font(size):
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"):
        try: return ImageFont.truetype(path, size)
        except OSError: pass
    return ImageFont.load_default()

def _wrap(draw, text, font, max_width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_width: line = test
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def make_frame(index, total, title, explanation):
    im = Image.new("RGB", (W, H), (8, 18, 42)); d = ImageDraw.Draw(im)
    phase = index / max(total, 1) * math.tau
    for r in (120, 175, 230): d.ellipse((W//2-r, 300-r, W//2+r, 300+r), outline=(35, 83, 135), width=3)
    x, y = W//2 + int(170*math.cos(phase)), 300 + int(170*math.sin(phase))
    d.ellipse((x-20, y-20, x+20, y+20), fill=(80, 210, 255))
    d.ellipse((W//2-56, 244, W//2+56, 356), fill=(42,125,220), outline=(170,225,255), width=4)
    d.text((36,48), "FACTVERSE", font=_font(34), fill=(105,220,255))
    d.rounded_rectangle((34,590,W-34,1125), radius=34, fill=(15,35,68), outline=(42,93,145), width=3)
    yy=650; tf=_font(44)
    for line in _wrap(d,title,tf,W-100)[:4]: d.text((58,yy),line,font=tf,fill=(255,255,255)); yy+=62
    yy=max(850,yy+22); bf=_font(28)
    for line in _wrap(d,explanation,bf,W-100)[:6]:
        if yy>1060: break
        d.text((58,yy),line,font=bf,fill=(195,216,240)); yy+=42
    d.text((36,1195),"Curiosity starts here  •  Follow for more",font=_font(22),fill=(105,220,255))
    return im

def render_video(title, explanation, output="output/factverse_sample.mp4", thumbnail="output/thumbnail.png", seconds=18, fps=12):
    if seconds < 5 or seconds > 60: raise ValueError("Duration must be between 5 and 60 seconds.")
    out, thumb = Path(output), Path(thumbnail); out.parent.mkdir(parents=True,exist_ok=True); thumb.parent.mkdir(parents=True,exist_ok=True)
    total=seconds*fps; make_frame(0,total,title,explanation).save(thumb)
    writer=imageio.get_writer(str(out),fps=fps,codec="libx264",macro_block_size=16,ffmpeg_log_level="error",quality=7)
    try:
        for i in range(total): writer.append_data(make_frame(i,total,title,explanation))
    finally: writer.close()
    return str(out), str(thumb)