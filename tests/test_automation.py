import json
from pathlib import Path
from factverse_manager.automation import run_batch


def test_batch_generates_review_report_without_publishing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    report, path = run_batch(days=1, start_date="2026-10-26")
    assert report["publishing_enabled"] is False
    assert len(report["items"]) == 1
    assert report["items"][0]["status"] == "ready_for_review"
    saved = json.loads(Path(path).read_text(encoding="utf-8"))
    assert saved["successful"] == 1
    assert saved["ready_for_review"] == 1
    assert saved["needs_attention"] == 0
    assert saved["failed"] == 0
    assert saved["attempted"] == 1
    assert (tmp_path / "output" / "artifact_manifest.json").is_file()
    checklist = report["items"][0]["artifacts"]["review_checklist"]
    assert Path(checklist).is_file()
    evidence = report["items"][0]["artifacts"]["evidence_register"]
    assert Path(evidence).is_file()
    assert json.loads(Path(evidence).read_text(encoding="utf-8"))["status"] == "needs_human_review"


def test_batch_respects_custom_output_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    destination = tmp_path / "custom-artifacts"
    report, _ = run_batch(days=1, start_date="2026-10-26", output_dir=str(destination))
    assert report["successful"] == 1
    assert (destination / "automation_report.json").is_file()
    assert (destination / "artifact_manifest.json").is_file()
    assert (destination / (report["items"][0]["artifacts"]["topic"] + ".mp4")).is_file()
    assert Path(report["items"][0]["artifacts"]["review_checklist"]).is_file()
    assert Path(report["items"][0]["artifacts"]["evidence_register"]).is_file()


def test_batch_restores_output_environment_after_completion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("FACTVERSE_OUTPUT_DIR", "previous-value")
    run_batch(days=1, start_date="2026-10-26", output_dir=str(tmp_path / "custom"))
    assert __import__("os").environ["FACTVERSE_OUTPUT_DIR"] == "previous-value"
