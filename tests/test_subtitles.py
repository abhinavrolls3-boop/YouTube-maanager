from factverse_manager.subtitles import validate_srt, write_srt


def test_write_srt_creates_timed_captions(tmp_path):
    path = tmp_path / "captions.srt"
    result = write_srt("One two three four five six seven eight nine ten", path, duration=18, max_words=5)
    text = path.read_text(encoding="utf-8")
    assert result == str(path)
    assert "00:00:00,000 -->" in text
    assert "One two three four five" in text
    assert "nine ten" in text
    assert validate_srt(path, duration_seconds=18)["ok"]


def test_write_srt_rejects_empty_text(tmp_path):
    import pytest
    with pytest.raises(ValueError):
        write_srt(" ", tmp_path / "empty.srt")


def test_validate_srt_rejects_cue_after_video_end(tmp_path):
    path = tmp_path / "late.srt"
    path.write_text("1\n00:00:04,000 --> 00:00:06,000\nToo late\n", encoding="utf-8")
    result = validate_srt(path, duration_seconds=5)
    assert not result["ok"]
    assert any("after video duration" in issue for issue in result["issues"])


def test_validate_srt_rejects_overlapping_cues(tmp_path):
    path = tmp_path / "overlap.srt"
    path.write_text(
        "1\n00:00:00,000 --> 00:00:03,000\nFirst cue\n\n"
        "2\n00:00:02,000 --> 00:00:04,000\nSecond cue\n",
        encoding="utf-8",
    )
    result = validate_srt(path)
    assert not result["ok"]
    assert any("overlaps" in issue for issue in result["issues"])
