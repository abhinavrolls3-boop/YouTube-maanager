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

def test_upload_requires_evidence_approval_before_api_call(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video")
    monkeypatch.setenv("ENABLE_UPLOAD", "true")
    monkeypatch.setenv("UPLOAD_PRIVACY", "unlisted")
    metadata = {"title":"Fact", "description":"desc", "source_urls":["https://example.org"],
                "human_review_status":"approved", "originality_check_status":"passed"}
    with pytest.raises(RuntimeError, match="per-claim evidence review"):
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
    monkeypatch.setenv("YOUTUBE_MADE_FOR_KIDS", "false")
    monkeypatch.setenv("UPLOAD_HISTORY", str(history))
    monkeypatch.setenv("MAX_UPLOADS_PER_DAY", "1")
    metadata = {"title":"Fact", "description":"desc", "source_urls":["https://example.org"],
                "human_review_status":"approved", "originality_check_status":"passed", "evidence_review_status":"human_reviewed_supported"}
    with pytest.raises(RuntimeError, match="Daily upload safety limit"):
        upload_video(str(video), metadata)

def _fully_reviewed_metadata(**overrides):
    metadata = {
        "title": "A reviewed science fact",
        "description": "A short explanation with sources.",
        "source_urls": ["https://example.org/fact"],
        "human_review_status": "approved",
        "originality_check_status": "passed",
        "evidence_review_status": "human_reviewed_supported",
    }
    metadata.update(overrides)
    return metadata


def test_upload_rejects_invalid_source_urls(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video")
    monkeypatch.setenv("ENABLE_UPLOAD", "true")
    monkeypatch.setenv("UPLOAD_PRIVACY", "unlisted")
    monkeypatch.setenv("YOUTUBE_MADE_FOR_KIDS", "false")
    with pytest.raises(RuntimeError, match="valid HTTP"):
        upload_video(str(video), _fully_reviewed_metadata(source_urls=["javascript:alert(1)"]))


def test_upload_requires_explicit_made_for_kids_setting(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video")
    monkeypatch.setenv("ENABLE_UPLOAD", "true")
    monkeypatch.setenv("UPLOAD_PRIVACY", "unlisted")
    monkeypatch.delenv("YOUTUBE_MADE_FOR_KIDS", raising=False)
    with pytest.raises(RuntimeError, match="YOUTUBE_MADE_FOR_KIDS"):
        upload_video(str(video), _fully_reviewed_metadata())


def test_upload_rejects_missing_title_and_empty_video_before_api_call(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video")
    monkeypatch.setenv("ENABLE_UPLOAD", "true")
    monkeypatch.setenv("UPLOAD_PRIVACY", "unlisted")
    monkeypatch.setenv("YOUTUBE_MADE_FOR_KIDS", "false")
    with pytest.raises(RuntimeError, match="title must"):
        upload_video(str(video), _fully_reviewed_metadata(title=" "))


def test_upload_rejects_non_mp4_file(tmp_path, monkeypatch):
    video = tmp_path / "video.txt"
    video.write_text("not a video")
    monkeypatch.setenv("ENABLE_UPLOAD", "true")
    monkeypatch.setenv("UPLOAD_PRIVACY", "unlisted")
    monkeypatch.setenv("YOUTUBE_MADE_FOR_KIDS", "false")
    with pytest.raises(RuntimeError, match="non-empty .mp4"):
        upload_video(str(video), _fully_reviewed_metadata())
