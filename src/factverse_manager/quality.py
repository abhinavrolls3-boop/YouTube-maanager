"""Local pre-publish checks. These checks do not claim to fact-check claims."""
import json
from pathlib import Path

def validate_package(video_path, thumbnail_path, metadata_path):
    issues = []
    video, thumbnail, metadata = Path(video_path), Path(thumbnail_path), Path(metadata_path)
    for label, path in (("video", video), ("thumbnail", thumbnail), ("metadata", metadata)):
        if not path.is_file() or path.stat().st_size == 0:
            issues.append(f"Missing or empty {label} file: {path}")
    data = {}
    if metadata.is_file():
        try:
            data = json.loads(metadata.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            issues.append("Metadata is not valid JSON.")
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
    if video.is_file() and video.stat().st_size:
        if video.suffix.lower() != ".mp4":
            issues.append("Video file extension is not .mp4.")
    if thumbnail.is_file() and thumbnail.stat().st_size:
        try:
            from PIL import Image
            with Image.open(thumbnail) as image:
                image.verify()
        except Exception:
            issues.append("Thumbnail is not a readable image.")
    return {"ok": not issues, "issues": issues, "human_review_required": True,
            "note": "Automated checks cannot verify factual accuracy, copyright, or audience suitability."}
