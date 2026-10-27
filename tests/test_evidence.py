import json
import pytest
from factverse_manager.evidence import create_evidence_register, approve_evidence_register

def test_register_starts_unverified_and_splits_script_into_review_units(tmp_path):
    metadata = tmp_path / "sample_metadata.json"
    metadata.write_text(json.dumps({
        "narration": "Octopuses have three hearts. They are fascinating animals.",
        "explanation": "Two hearts pump blood to the gills. One heart pumps blood to the body.",
        "source_urls": ["https://example.org"]
    }), encoding="utf-8")
    register, path = create_evidence_register(metadata)
    assert register["status"] == "needs_human_review"
    assert len(register["claims"]) >= 3
    assert all(c["assessment"] == "unverified" for c in register["claims"])
    assert path.endswith("_evidence.json")

def test_approval_requires_explicit_confirmation_and_supported_evidence(tmp_path):
    metadata = tmp_path / "metadata.json"
    metadata.write_text(json.dumps({
        "narration": "Octopuses have three hearts.",
        "explanation": "They have a closed circulatory system.",
        "source_urls": ["https://example.org"]
    }), encoding="utf-8")
    _, path = create_evidence_register(metadata)
    with pytest.raises(ValueError):
        approve_evidence_register(path, True, True)
    data = json.loads(open(path, encoding="utf-8").read())
    for claim in data["claims"]:
        claim["assessment"] = "supported"
        claim["evidence_url"] = "https://example.org"
        claim["evidence_quote_or_location"] = "Section 2, paragraph 1"
    open(path, "w", encoding="utf-8").write(json.dumps(data))
    with pytest.raises(ValueError):
        approve_evidence_register(path, False, True)
    result = approve_evidence_register(path, True, True)
    assert result["status"] == "human_reviewed_supported"
    assert result["reviewed_at_utc"]
    updated_metadata = json.loads(metadata.read_text(encoding="utf-8"))
    assert updated_metadata["evidence_review_status"] == "human_reviewed_supported"
    assert updated_metadata["evidence_reviewed_at_utc"]

def test_approval_rejects_non_http_evidence_urls(tmp_path):
    metadata = tmp_path / "metadata.json"
    metadata.write_text(json.dumps({"narration":"A factual sentence here.", "source_urls":["https://example.org"]}), encoding="utf-8")
    _, path = create_evidence_register(metadata)
    data = json.loads(open(path, encoding="utf-8").read())
    for claim in data["claims"]:
        claim.update({"assessment":"supported", "evidence_url":"javascript:alert(1)", "evidence_quote_or_location":"quote"})
    open(path, "w", encoding="utf-8").write(json.dumps(data))
    with pytest.raises(ValueError):
        approve_evidence_register(path, True, True)
