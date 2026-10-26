from factverse_manager.notifications import notify_report

def test_webhook_disabled_without_configuration(monkeypatch):
    monkeypatch.delenv("NOTIFY_WEBHOOK_URL", raising=False)
    assert notify_report({"successful": 1, "failed": 0})["sent"] is False
