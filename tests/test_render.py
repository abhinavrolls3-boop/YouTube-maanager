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
    assert scene_for_topic("Is the Moon slowly moving away from Earth?") == "space"
    assert scene_for_topic("What is Jupiter’s Great Red Spot?") == "space"


def test_topic_scenes_are_visually_distinct():
    from factverse_manager.render import make_frame
    octopus = make_frame(0, 10, "How many hearts does an octopus have?", "An octopus has three hearts.")
    shark = make_frame(0, 10, "Were sharks around before trees?", "Sharks are an ancient group.")
    assert octopus.size == shark.size == (720, 1280)
    assert octopus.tobytes() != shark.tobytes()


def test_caption_text_is_burned_into_frame():
    from factverse_manager.render import make_frame

    without_caption = make_frame(0, 10, "Sample title", "Sample explanation")
    with_caption = make_frame(0, 10, "Sample title", "Sample explanation",
                              caption_text="Astronauts float in orbit.")
    assert without_caption.size == with_caption.size == (720, 1280)
    assert without_caption.tobytes() != with_caption.tobytes()



def test_render_caption_timing_uses_word_weighted_chunks(tmp_path, monkeypatch):
    import factverse_manager.render as render_module
    seen = []
    original = render_module.make_frame

    def capture(index, total, title, explanation, caption_text=None):
        if index in (0, 1, 2, 3, 4, 9):
            seen.append(caption_text)
        return original(index, total, title, explanation, caption_text)

    monkeypatch.setattr(render_module, "make_frame", capture)
    video = tmp_path / "weighted.mp4"
    thumb = tmp_path / "weighted.png"
    render_module.render_video(
        "Title", "Explanation", str(video), str(thumb),
        seconds=10, fps=1, narration="one two three four five six seven eight nine",
    )
    assert seen[0] == "one two three four five six seven eight"
    assert seen[-1] == "nine"
