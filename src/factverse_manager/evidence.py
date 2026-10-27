"""Human-in-the-loop claim/evidence register. No automatic truth claims."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

def create_evidence_register(metadata_path, output_path=None):
    source = Path(metadata_path)
    metadata = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a JSON object.")
    text = str(metadata.get("narration", "")) + " " + str(metadata.get("explanation", ""))
    claims = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if len(part.strip()) >= 12]
    register = {
        "schema_version": 1,
        "metadata_path": str(source),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "needs_human_review",
        "warning": "Sentence splitting only suggests review units; it does not detect every factual claim or verify truth.",
        "source_urls": metadata.get("source_urls", []) if isinstance(metadata.get("source_urls", []), list) else [],
        "claims": [{"claim_id": f"C{i+1:02d}", "text": claim, "evidence_url": "",
                    "evidence_quote_or_location": "", "assessment": "unverified",
                    "reviewer_note": ""} for i, claim in enumerate(claims)],
        "reviewed_at_utc": None
    }
    destination = Path(output_path) if output_path else source.with_name(source.stem.replace("_metadata", "") + "_evidence.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(register, indent=2, ensure_ascii=False), encoding="utf-8")
    return register, str(destination)

def approve_evidence_register(register_path, confirm_each_claim=False, confirm_sources=False):
    path = Path(register_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        raise ValueError("Evidence register is malformed.")
    if not confirm_each_claim or not confirm_sources:
        raise ValueError("Explicitly confirm each claim and source review.")
    if not data["claims"]:
        raise ValueError("No claims found; review the script manually.")
    for claim in data["claims"]:
        if not isinstance(claim, dict) or not claim.get("text", "").strip():
            raise ValueError("Every claim must have text.")
        if claim.get("assessment") != "supported":
            raise ValueError(f"{claim.get('claim_id', 'Unknown claim')} is not marked supported.")
        url = str(claim.get("evidence_url", "")).strip()
        if not url.startswith(("https://", "http://")) or not claim.get("evidence_quote_or_location", "").strip():
            raise ValueError(f"{claim.get('claim_id', 'Unknown claim')} needs an evidence URL and quote/location.")
    if not data.get("source_urls"):
        raise ValueError("Add and review source URLs before approval.")
    reviewed_at = datetime.now(timezone.utc).isoformat()
    data["status"] = "human_reviewed_supported"
    data["reviewed_at_utc"] = reviewed_at
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    # Link the evidence approval to its metadata so the upload gate can require it.
    metadata_path = Path(data.get("metadata_path", ""))
    if not metadata_path.is_absolute() and not metadata_path.is_file():
        metadata_path = path.parent / metadata_path
    if not metadata_path.is_file():
        raise ValueError(f"Linked metadata file does not exist: {metadata_path}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise ValueError("Linked metadata must be a JSON object.")
    metadata["evidence_review_status"] = "human_reviewed_supported"
    metadata["evidence_reviewed_at_utc"] = reviewed_at
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    return data
