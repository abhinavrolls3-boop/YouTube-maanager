import pytest
from factverse_manager.render import make_frame, render_video

def test_frame_is_vertical_video_size():
    frame=make_frame(0,10,"Sample title","Sample explanation")
    assert frame.size==(720,1280)

def test_duration_out_of_range_rejected(tmp_path):
    with pytest.raises(ValueError): render_video("title","text",str(tmp_path/"a.mp4"),str(tmp_path/"a.png"),seconds=2)