"""Local pre-publish checks; these do not claim to fact-check claims."""
import json
from pathlib import Path
from urllib.parse import urlparse

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
    if not title: issues.append("Metadata title is empty.")
    if len(title) > 100: issues.append("Title exceeds YouTube's 100-character limit.")
    if not description: issues.append("Metadata description is empty.")
    tags = data.get("tags", [])
    if not isinstance(tags, list): issues.append("Tags must be a list.")
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
    if video.is_file() and video.stat().st_size and video.suffix.lower() != ".mp4":
        issues.append("Video file extension is not .mp4.")
    if thumbnail.is_file() and thumbnail.stat().st_size:
        try:
            from PIL import Image
            with Image.open(thumbnail) as image: image.verify()
        except Exception:
            issues.append("Thumbnail is not a readable image.")
    return {"ok": not issues, "issues": issues, "warnings": warnings, "source_urls": sources,
            "human_review_required": True,
            "note": "Automated checks cannot verify factual accuracy, source relevance, copyright, or audience suitability."}
