"""Run a bounded batch of offline production tasks; designed for scheduled CI."""
import json
from pathlib import Path
from .planning import build_plan
from .quality import validate_package

def run_batch(days=1, start_date=None, output_dir="output"):
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    plan = build_plan(start_date, days)
    results = []
    from .cli import render_topic
    for item in plan:
        slug = item["topic"]
        try:
            result = render_topic(slug)
            # render_topic writes under output/; keep its paths as returned.
            quality = validate_package(result["video"], result["thumbnail"], result["metadata"])
            results.append({"date": item["date"], "topic": slug, "status": "ready_for_review" if quality["ok"] else "needs_attention",
                            "artifacts": result, "quality": quality})
        except Exception as exc:
            results.append({"date": item["date"], "topic": slug, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    report = {"items": results, "successful": sum(x["status"] == "ready_for_review" for x in results),
              "failed": sum(x["status"] == "failed" for x in results), "publishing_enabled": False,
              "note": "This batch does not publish videos. Review each claim and output before uploading."}
    report_path = root / "automation_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report, str(report_path)
