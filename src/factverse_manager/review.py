"""Human review checklist helpers. These functions never infer that content is safe."""
import json
from pathlib import Path
from datetime import datetime, timezone

CHECKS = [
    ("claims_verified", "I checked every factual claim against the linked sources."),
    ("sources_relevant", "The sources directly support the claims and are reputable."),
    ("original_value", "This video adds meaningful original explanation, not just template repetition."),
    ("rights_checked", "Visuals, audio, footage, and text are original or properly licensed."),
    ("metadata_accurate", "Title, thumbnail, description, tags, and hashtags are accurate and not misleading."),
    ("audience_suitable", "The video is suitable for the intended audience and follows current platform rules."),
    ("synthetic_disclosure_checked", "I checked whether altered/synthetic-content disclosure is required and will disclose if needed."),
]

def create_review_checklist(metadata_path, output_path=None):
    path = Path(metadata_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    checklist_path = Path(output_path) if output_path else path.with_name(path.stem + "_review.json")
    checklist = {
        "metadata_path": str(path),
        "title": data.get("title", ""),
        "source_urls": data.get("source_urls", []),
        "human_review_status": "needs_review",
        "originality_check_status": "needs_review",
        "checks": [{"id": key, "instruction": label, "checked": False} for key, label in CHECKS],
        "note": "Read the video and sources yourself. A reachable URL is not proof of factual support.",
    }
    checklist_path.write_text(json.dumps(checklist, indent=2, ensure_ascii=False), encoding="utf-8")
    return checklist, str(checklist_path)

def approve_metadata(metadata_path, human_review=False, originality=False):
    if not human_review or not originality:
        raise ValueError("Approval requires both explicit human-review and originality confirmations.")
    path = Path(metadata_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    sources = data.get("source_urls", [])
    if not isinstance(sources, list) or not sources:
        raise ValueError("Cannot approve metadata without source URLs.")
    if data.get("evidence_review_status") != "human_reviewed_supported":
        raise ValueError("Approve the per-claim evidence register first with evidence-approve.")
    data["human_review_status"] = "approved"
    data["originality_check_status"] = "passed"
    data["reviewed_at_utc"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data
