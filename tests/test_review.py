import json
import pytest
from factverse_manager.review import create_review_checklist, approve_metadata

def test_review_checklist_starts_unapproved(tmp_path):
    metadata = tmp_path / "clip_metadata.json"
    metadata.write_text(json.dumps({"title":"A science fact","source_urls":["https://example.org"]}))
    checklist, path = create_review_checklist(metadata)
    assert checklist["human_review_status"] == "needs_review"
    assert checklist["originality_check_status"] == "needs_review"
    assert len(checklist["checks"]) >= 6
    assert (tmp_path / "clip_metadata_review.json").is_file()

def test_approval_requires_both_explicit_confirmations(tmp_path):
    metadata = tmp_path / "clip_metadata.json"
    metadata.write_text(json.dumps({"title":"A science fact","source_urls":["https://example.org"]}))
    with pytest.raises(ValueError, match="both explicit"):
        approve_metadata(metadata, human_review=True, originality=False)

def test_approval_requires_sources(tmp_path):
    metadata = tmp_path / "clip_metadata.json"
    metadata.write_text(json.dumps({"title":"A science fact","source_urls":[]}))
    with pytest.raises(ValueError, match="source URLs"):
        approve_metadata(metadata, human_review=True, originality=True)

def test_approval_requires_evidence_review(tmp_path):
    metadata = tmp_path / "clip_metadata.json"
    metadata.write_text(json.dumps({"title":"A science fact","source_urls":["https://example.org"]}))
    with pytest.raises(ValueError, match="evidence register first"):
        approve_metadata(metadata, human_review=True, originality=True)

def test_approval_records_review_timestamp(tmp_path):
    metadata = tmp_path / "clip_metadata.json"
    metadata.write_text(json.dumps({"title":"A science fact","source_urls":["https://example.org"], "evidence_review_status":"human_reviewed_supported"}))
    result = approve_metadata(metadata, human_review=True, originality=True)
    assert result["human_review_status"] == "approved"
    assert result["originality_check_status"] == "passed"
    assert result["reviewed_at_utc"]
