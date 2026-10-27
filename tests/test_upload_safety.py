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

def test_upload_requires_human_review_before_api_call(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video")
    monkeypatch.setenv("ENABLE_UPLOAD", "true")
    monkeypatch.setenv("UPLOAD_PRIVACY", "unlisted")
    metadata = {"title":"Fact", "description":"desc", "source_urls":["https://example.org"],
                "human_review_status":"needs_review", "originality_check_status":"passed"}
    with pytest.raises(RuntimeError, match="human_review_status"):
        upload_video(str(video), metadata)

def test_upload_requires_originality_approval_before_api_call(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video")
    monkeypatch.setenv("ENABLE_UPLOAD", "true")
    monkeypatch.setenv("UPLOAD_PRIVACY", "unlisted")
    metadata = {"title":"Fact", "description":"desc", "source_urls":["https://example.org"],
                "human_review_status":"approved", "originality_check_status":"needs_review", "evidence_review_status":"human_reviewed_supported"}
    with pytest.raises(RuntimeError, match="originality_check_status"):
        upload_video(str(video), metadata)

def test_upload_daily_cap_blocks_before_api_call(tmp_path, monkeypatch):
    import json
    from datetime import datetime, timezone
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video")
    history = tmp_path / "history.json"
    history.write_text(json.dumps({"uploads":[{"sha256":"other","video_id":"x","title":"old",
        "uploaded_at":datetime.now(timezone.utc).isoformat()}]}))
    monkeypatch.setenv("ENABLE_UPLOAD", "true")
    monkeypatch.setenv("UPLOAD_PRIVACY", "unlisted")
    monkeypatch.setenv("UPLOAD_HISTORY", str(history))
    monkeypatch.setenv("MAX_UPLOADS_PER_DAY", "1")
    metadata = {"title":"Fact", "description":"desc", "source_urls":["https://example.org"],
                "human_review_status":"approved", "originality_check_status":"passed", "evidence_review_status":"human_reviewed_supported"}
    with pytest.raises(RuntimeError, match="Daily upload safety limit"):
        upload_video(str(video), metadata)
