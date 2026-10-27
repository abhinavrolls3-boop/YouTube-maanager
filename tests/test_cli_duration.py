from pathlib import Path

from factverse_manager.content import Fact
from factverse_manager import cli


def test_duration_estimate_scales_with_narration_and_is_bounded():
    assert cli.estimate_video_duration("one two three") == 18
    long_text = " ".join(["word"] * 100)
    assert cli.estimate_video_duration(long_text) == 46
    very_long = " ".join(["word"] * 1000)
    assert cli.estimate_video_duration(very_long) == 60


def test_render_fact_uses_same_duration_for_video_and_subtitles(tmp_path, monkeypatch):
    observed = {}

    def fake_render_video(title, explanation, video_path, thumbnail_path, seconds=18, fps=12):
        observed["video_seconds"] = seconds
        Path(video_path).write_bytes(b"video-placeholder")
        Path(thumbnail_path).write_bytes(b"thumbnail-placeholder")
        return video_path, thumbnail_path

    def fake_write_srt(text, path, duration=18, max_words=8):
        observed["subtitle_seconds"] = duration
        Path(path).write_text("placeholder", encoding="utf-8")
        return str(path)

    monkeypatch.setenv("FACTVERSE_OUTPUT_DIR", str(tmp_path))
    monkeypatch.setenv("ENABLE_NARRATION", "false")
    monkeypatch.setattr(cli, "render_video", fake_render_video)
    monkeypatch.setattr(cli, "write_srt", fake_write_srt)
    fact = Fact(
        title="A longer fact",
        narration=" ".join(["word"] * 100),
        explanation="A sample explanation.",
        tags=("science",),
        sources=("https://example.com/source",),
    )

    result = cli.render_fact(fact, "duration-test")

    assert observed["video_seconds"] == 46
    assert observed["subtitle_seconds"] == 46
    assert Path(result["metadata"]).is_file()
    assert Path(result["subtitles"]).is_file()
