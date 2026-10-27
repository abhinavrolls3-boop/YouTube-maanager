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


def test_scene_selection_matches_curated_fact_topics():
    from factverse_manager.render import scene_for_topic
    assert scene_for_topic("How many hearts does an octopus have?") == "octopus"
    assert scene_for_topic("Is a day on Venus longer than its year?") == "venus"
    assert scene_for_topic("Were sharks around before trees?") == "shark"
    assert scene_for_topic("Why can honey last a very long time?") == "honey"
    assert scene_for_topic("Why do astronauts look like they float?") == "space"


def test_topic_scenes_are_visually_distinct():
    from factverse_manager.render import make_frame
    octopus = make_frame(0, 10, "How many hearts does an octopus have?", "An octopus has three hearts.")
    shark = make_frame(0, 10, "Were sharks around before trees?", "Sharks are an ancient group.")
    assert octopus.size == shark.size == (720, 1280)
    assert octopus.tobytes() != shark.tobytes()
