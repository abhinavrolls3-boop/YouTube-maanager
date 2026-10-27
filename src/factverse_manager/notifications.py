"""Optional generic webhook notifications; disabled when URL is not configured."""
import json
import os
from urllib.request import Request, urlopen


def notify_report(report, timeout=10):
    url = os.getenv("NOTIFY_WEBHOOK_URL", "").strip()
    if not url:
        return {"sent": False, "reason": "NOTIFY_WEBHOOK_URL is not configured."}
    # Avoid accidentally posting secrets or full scripts; send only operational counts.
    payload = {"text": "FactVerse automation report: "
               f"{report.get('ready_for_review', report.get('successful', 0))} ready for review, "
               f"{report.get('needs_attention', 0)} need attention, "
               f"{report.get('failed', 0)} failed. Publishing remains disabled."}
    request = Request(url, data=json.dumps(payload).encode("utf-8"),
                      headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=timeout) as response:
        return {"sent": 200 <= response.status < 300, "status": response.status}
