"""Local upload ledger. Keep it private; it contains video hashes and YouTube IDs."""
import hashlib
import json
from pathlib import Path

def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def load_history(path="output/upload_history.json"):
    file_path = Path(path)
    if not file_path.exists():
        return {"uploads": []}
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("Upload history is unreadable; refusing to upload until it is repaired or backed up.") from exc
    if not isinstance(data, dict) or not isinstance(data.get("uploads"), list):
        raise ValueError("Upload history has an invalid format; refusing to upload.")
    return data

def has_uploaded_hash(video_hash, path="output/upload_history.json"):
    return any(item.get("sha256") == video_hash for item in load_history(path)["uploads"])

def record_upload(video_hash, video_id, title, path="output/upload_history.json"):
    history_path = Path(path)
    history = load_history(history_path)
    if any(item.get("sha256") == video_hash for item in history["uploads"]):
        raise ValueError("This exact video file is already recorded as uploaded.")
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history["uploads"].append({"sha256": video_hash, "video_id": video_id, "title": title})
    history_path.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
