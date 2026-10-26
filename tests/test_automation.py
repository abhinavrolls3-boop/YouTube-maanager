import json
from pathlib import Path
from factverse_manager.automation import run_batch

def test_batch_generates_review_report_without_publishing(tmp_path, monkeypatch):
    # Redirect render_topic output paths by running in a temporary working directory.
    monkeypatch.chdir(tmp_path)
    report, path = run_batch(days=1, start_date="2026-10-26")
    assert report["publishing_enabled"] is False
    assert len(report["items"]) == 1
    assert report["items"][0]["status"] == "ready_for_review"
    assert json.loads(open(path, encoding="utf-8").read())["successful"] == 1
    assert (tmp_path / "output" / "artifact_manifest.json").is_file()
    checklist = report["items"][0]["artifacts"]["review_checklist"]
    assert (tmp_path / checklist).is_file() if not Path(checklist).is_absolute() else Path(checklist).is_file()

def test_batch_respects_custom_output_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    destination = tmp_path / "custom-artifacts"
    report, report_path = run_batch(days=1, start_date="2026-10-26", output_dir=str(destination))
    assert report["successful"] == 1
    assert (destination / "automation_report.json").is_file()
    assert (destination / "artifact_manifest.json").is_file()
    assert (destination / (report["items"][0]["artifacts"]["topic"] + ".mp4")).is_file()
    assert Path(report["items"][0]["artifacts"]["review_checklist"]).is_file()
