import pytest
from PIL import Image
from factverse_manager.render import make_frame, render_video

def test_frame_is_vertical_video_size():
    frame=make_frame(0,10,"Sample title","Sample explanation")
    assert frame.size==(720,1280)

def test_duration_out_of_range_rejected(tmp_path):
    with pytest.raises(ValueError):
        render_video("title","text",str(tmp_path/"a.mp4"),str(tmp_path/"a.png"),seconds=2)

def test_render_creates_nonempty_mp4_and_readable_thumbnail(tmp_path):
    video=tmp_path/"sample.mp4"
    thumbnail=tmp_path/"sample.png"
    render_video("A tiny test title","A short test explanation.",str(video),str(thumbnail),seconds=5,fps=2)
    assert video.is_file() and video.stat().st_size > 1000
    assert thumbnail.is_file() and thumbnail.stat().st_size > 100
    with Image.open(thumbnail) as image:
        assert image.size == (720,1280)
