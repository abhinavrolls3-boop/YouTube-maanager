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



def test_relative_subtitle_path_resolves_from_metadata_directory(tmp_path):
    video = tmp_path / "clip.mp4"
    make_video(video)
    thumb = tmp_path / "thumb.png"
    Image.new("RGB", (720, 1280)).save(thumb)
    subtitle = tmp_path / "clip.srt"
    subtitle.write_text("""1
00:00:00,000 --> 00:00:05,000
A short caption
""", encoding="utf-8")
    metadata = tmp_path / "metadata.json"
    make_metadata(metadata, subtitle_path="clip.srt")
    result = validate_package(video, thumb, metadata)
    assert result["ok"], result["issues"]
    assert result["subtitle_report"]["ok"]


def test_subtitle_cues_cannot_extend_past_video_duration(tmp_path):
    video = tmp_path / "clip.mp4"
    make_video(video)
    thumb = tmp_path / "thumb.png"
    Image.new("RGB", (720, 1280)).save(thumb)
    subtitle = tmp_path / "clip.srt"
    subtitle.write_text("""1
00:00:04,000 --> 00:00:06,000
Caption extends past the end
""", encoding="utf-8")
    metadata = tmp_path / "metadata.json"
    make_metadata(metadata, subtitle_path="clip.srt")
    result = validate_package(video, thumb, metadata)
    assert not result["ok"]
    assert any("after video duration" in issue for issue in result["issues"])


def test_evidence_review_and_caption_presence_are_explicit_warnings(tmp_path):
    video = tmp_path / "clip.mp4"
    make_video(video)
    thumb = tmp_path / "thumb.png"
    Image.new("RGB", (720, 1280)).save(thumb)
    metadata = tmp_path / "metadata.json"
    make_metadata(metadata)
    result = validate_package(video, thumb, metadata)
    assert result["ok"]
    assert any("Claim-by-claim evidence review" in warning for warning in result["warnings"])
    assert any("No subtitle_path" in warning for warning in result["warnings"])
