import pytest
from factverse_manager.narration import add_narration

def test_narration_rejects_empty_text(tmp_path):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video")
    with pytest.raises(ValueError, match="cannot be empty"):
        add_narration(video, " ")

def test_narration_reports_missing_local_engine(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video")
    import factverse_manager.narration as narration
    monkeypatch.setattr(narration.shutil, "which", lambda name: None)
    with pytest.raises(RuntimeError, match="not installed"):
        narration.add_narration(video, "Hello world")
