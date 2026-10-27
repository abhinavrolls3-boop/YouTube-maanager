"""Local pre-publish checks; these do not claim to fact-check claims."""
import json
from pathlib import Path
from urllib.parse import urlparse
from .subtitles import validate_srt


def _inspect_video(path):
    """Read a real frame and probe container metadata, not just file size."""
    import imageio.v2 as imageio

    reader = imageio.get_reader(str(path), format="ffmpeg")
    try:
        meta = reader.get_meta_data()
        frame = reader.get_data(0)
        height, width = frame.shape[:2]
        fps = float(meta.get("fps") or 0)
        duration = float(meta.get("duration") or 0)
        if width < 360 or height < 640:
            raise ValueError(f"video resolution too small: {width}x{height}")
        if height <= width:
            raise ValueError(f"video must be vertical, got {width}x{height}")
        if fps <= 0:
            raise ValueError("video FPS metadata is missing or invalid")
        if duration <= 0:
            # Some ffmpeg builds omit duration; a readable first frame still
            # establishes basic decodability, but report duration as unknown.
            duration = None
        return {"readable": True, "width": width, "height": height,
                "fps": fps, "duration_seconds": duration}
    finally:
        reader.close()


def validate_package(video_path, thumbnail_path, metadata_path):
    issues = []
    warnings = []
    video, thumbnail, metadata = Path(video_path), Path(thumbnail_path), Path(metadata_path)
    for label, path in (("video", video), ("thumbnail", thumbnail), ("metadata", metadata)):
        if not path.is_file() or path.stat().st_size == 0:
            issues.append(f"Missing or empty {label} file: {path}")
    data = {}
    if metadata.is_file():
        try:
            data = json.loads(metadata.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("metadata root must be an object")
        except (OSError, json.JSONDecodeError, ValueError):
            issues.append("Metadata is not a valid JSON object.")
            data = {}
    title = str(data.get("title", "")).strip()
    description = str(data.get("description", "")).strip()
    if not title:
        issues.append("Metadata title is empty.")
    if len(title) > 100:
        issues.append("Title exceeds YouTube's 100-character limit.")
    if not description:
        issues.append("Metadata description is empty.")
    tags = data.get("tags", [])
    if not isinstance(tags, list):
        issues.append("Tags must be a list.")
    elif any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        issues.append("Tags must contain only non-empty strings.")
    sources = data.get("source_urls", [])
    if not isinstance(sources, list):
        issues.append("source_urls must be a list.")
        sources = []
    if not sources:
        issues.append("No source URLs supplied; a human should add and verify sources before publishing.")
    for source in sources:
        parsed = urlparse(source) if isinstance(source, str) else None
        if not parsed or parsed.scheme not in {"http", "https"} or not parsed.netloc:
            issues.append(f"Invalid source URL: {source!r}")
    if data.get("human_review_status") != "approved":
        warnings.append("Human factual/source review is still required.")
    if data.get("originality_check_status") != "passed":
        warnings.append("Originality and asset-rights review is still required.")
    subtitle_path = data.get("subtitle_path")
    subtitle_report = None
    video_probe = None
    if video.is_file() and video.stat().st_size:
        if video.suffix.lower() != ".mp4":
            issues.append("Video file extension is not .mp4.")
        else:
            try:
                video_probe = _inspect_video(video)
            except Exception as exc:
                issues.append(f"Video cannot be decoded or fails vertical-video checks: {exc}")
    if subtitle_path:
        try:
            subtitle_file = Path(subtitle_path)
            if not subtitle_file.is_absolute():
                subtitle_file = metadata.parent / subtitle_file
            duration = video_probe.get("duration_seconds") if video_probe else None
            subtitle_report = validate_srt(subtitle_file, duration_seconds=duration)
            if not subtitle_report["ok"]:
                issues.extend("Subtitle check: " + issue for issue in subtitle_report["issues"])
        except (OSError, UnicodeError, ValueError) as exc:
            issues.append(f"Subtitle file could not be checked: {exc}")
    if thumbnail.is_file() and thumbnail.stat().st_size:
        try:
            from PIL import Image
            with Image.open(thumbnail) as image:
                image.verify()
        except Exception:
            issues.append("Thumbnail is not a readable image.")
    return {
        "ok": not issues, "issues": issues, "warnings": warnings,
        "source_urls": sources, "video_probe": video_probe, "subtitle_report": subtitle_report,
        "human_review_required": True,
        "note": "Automated checks cannot verify factual accuracy, source relevance, copyright, or audience suitability.",
    }
