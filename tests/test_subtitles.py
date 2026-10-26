from factverse_manager.subtitles import write_srt

def test_write_srt_creates_timed_captions(tmp_path):
    path = tmp_path / "captions.srt"
    result = write_srt("One two three four five six seven eight nine ten", path, duration=18, max_words=5)
    text = path.read_text(encoding="utf-8")
    assert result == str(path)
    assert "00:00:00,000 -->" in text
    assert "One two three four five" in text
    assert "nine ten" in text

def test_write_srt_rejects_empty_text(tmp_path):
    import pytest
    with pytest.raises(ValueError):
        write_srt(" ", tmp_path / "empty.srt")
