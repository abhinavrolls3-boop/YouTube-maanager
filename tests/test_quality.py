import json
from PIL import Image
from factverse_manager.quality import validate_package
from factverse_manager.render import render_video


def make_video(path):
    render_video("Test", "A short test explanation.", str(path),
                 str(path.with_suffix(".png")), seconds=5, fps=2)


def make_metadata(path, **overrides):
    data = {"title": "Fact", "description": "A fact.", "tags": ["science"],
            "source_urls": ["https://example.org/fact"]}
    data.update(overrides)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_valid_package_checks_real_video_and_thumbnail(tmp_path):
    video = tmp_path / "clip.mp4"
    make_video(video)
    thumb = tmp_path / "thumb.png"
    Image.new("RGB", (720, 1280)).save(thumb)
    metadata = tmp_path / "metadata.json"
    make_metadata(metadata)
    result = validate_package(video, thumb, metadata)
    assert result["ok"], result["issues"]
    assert result["human_review_required"]
    assert result["video_probe"]["readable"]
    assert result["video_probe"]["width"] == 720
    assert result["video_probe"]["height"] == 1280


def test_empty_title_fails(tmp_path):
    video = tmp_path / "clip.mp4"
    make_video(video)
    thumb = tmp_path / "thumb.png"
    Image.new("RGB", (10, 10)).save(thumb)
    metadata = tmp_path / "metadata.json"
    make_metadata(metadata, title=" ")
    result = validate_package(video, thumb, metadata)
    assert not result["ok"]
    assert any("title" in issue.lower() for issue in result["issues"])


def test_invalid_source_url_fails_package_check(tmp_path):
    video = tmp_path / "clip.mp4"
    make_video(video)
    thumb = tmp_path / "thumb.png"
    Image.new("RGB", (10, 10)).save(thumb)
    metadata = tmp_path / "metadata.json"
    make_metadata(metadata, source_urls=["javascript:alert(1)"])
    result = validate_package(video, thumb, metadata)
    assert not result["ok"]
    assert any("Invalid source URL" in issue for issue in result["issues"])


def test_review_needed_is_warning_not_fake_approval(tmp_path):
    video = tmp_path / "clip.mp4"
    make_video(video)
    thumb = tmp_path / "thumb.png"
    Image.new("RGB", (10, 10)).save(thumb)
    metadata = tmp_path / "metadata.json"
    make_metadata(metadata)
    result = validate_package(video, thumb, metadata)
    assert result["ok"]
    assert result["warnings"]
    assert result["human_review_required"]


def test_corrupt_mp4_is_rejected(tmp_path):
    video = tmp_path / "broken.mp4"
    video.write_bytes(b"not a video")
    thumb = tmp_path / "thumb.png"
    Image.new("RGB", (10, 10)).save(thumb)
    metadata = tmp_path / "metadata.json"
    make_metadata(metadata)
    result = validate_package(video, thumb, metadata)
    assert not result["ok"]
    assert any("cannot be decoded" in issue.lower() for issue in result["issues"])
