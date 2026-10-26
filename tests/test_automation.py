import json
from factverse_manager.automation import run_batch

def test_batch_generates_review_report_without_publishing(tmp_path, monkeypatch):
    # Redirect render_topic output paths by running in a temporary working directory.
    monkeypatch.chdir(tmp_path)
    report, path = run_batch(days=1, start_date="2026-10-26")
    assert report["publishing_enabled"] is False
    assert len(report["items"]) == 1
    assert report["items"][0]["status"] == "ready_for_review"
    assert json.loads(open(path, encoding="utf-8").read())["successful"] == 1
