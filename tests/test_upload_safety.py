import pytest
from factverse_manager.youtube_upload import upload_video

def test_upload_blocks_public_visibility_before_api_call(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video")
    monkeypatch.setenv("ENABLE_UPLOAD", "true")
    monkeypatch.setenv("UPLOAD_PRIVACY", "public")
    with pytest.raises(RuntimeError, match="never public"):
        upload_video(str(video), {"title":"Fact", "source_urls":["https://example.org"]})

def test_upload_blocks_missing_sources_before_api_call(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video")
    monkeypatch.setenv("ENABLE_UPLOAD", "true")
    monkeypatch.setenv("UPLOAD_PRIVACY", "unlisted")
    with pytest.raises(RuntimeError, match="source_urls"):
        upload_video(str(video), {"title":"Fact", "source_urls":[]})
