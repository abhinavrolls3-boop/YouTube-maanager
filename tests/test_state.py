import json
import pytest
from factverse_manager.state import file_sha256, has_uploaded_hash, record_upload

def test_upload_history_detects_duplicate_hash(tmp_path):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"sample-video-bytes")
    history = tmp_path / "history.json"
    digest = file_sha256(video)
    assert not has_uploaded_hash(digest, history)
    record_upload(digest, "abc123", "Sample title", history)
    assert has_uploaded_hash(digest, history)
    assert json.loads(history.read_text())["uploads"][0]["video_id"] == "abc123"

def test_upload_history_refuses_duplicate_record(tmp_path):
    history = tmp_path / "history.json"
    record_upload("same-hash", "abc123", "Title", history)
    with pytest.raises(ValueError):
        record_upload("same-hash", "def456", "Title", history)
