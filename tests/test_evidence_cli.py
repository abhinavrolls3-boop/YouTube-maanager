import json
import sys

from factverse_manager.cli import main


def test_evidence_command_creates_register(tmp_path, monkeypatch, capsys):
    metadata = tmp_path / "clip_metadata.json"
    metadata.write_text(json.dumps({
        "narration": "Octopuses have three hearts.",
        "explanation": "Two hearts pump blood to the gills.",
        "source_urls": ["https://example.org/octopus"],
    }), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["factverse-manager", "evidence", str(metadata)])
    main()
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "needs_human_review"
    assert result["claims"] >= 1
    assert (tmp_path / "clip_evidence.json").is_file()


def test_evidence_approve_command_dispatches_gate(tmp_path, monkeypatch, capsys):
    register = tmp_path / "evidence.json"
    register.write_text(json.dumps({
        "status": "needs_human_review",
        "source_urls": ["https://example.org/source"],
        "claims": [{
            "claim_id": "C01",
            "text": "A claim long enough to review.",
            "assessment": "supported",
            "evidence_url": "https://example.org/source",
            "evidence_quote_or_location": "Paragraph 2",
        }],
    }), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", [
        "factverse-manager", "evidence-approve", str(register),
        "--confirm-each-claim", "--confirm-sources",
    ])
    main()
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "human_reviewed_supported"
    saved = json.loads(register.read_text(encoding="utf-8"))
    assert saved["status"] == "human_reviewed_supported"
