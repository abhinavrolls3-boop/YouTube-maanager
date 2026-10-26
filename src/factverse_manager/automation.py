"""Run a bounded batch of offline production tasks; designed for scheduled CI."""
import json
import os
from pathlib import Path
from .planning import build_plan
from .quality import validate_package
from .library import get_topic
from .model_gateway import draft_fact

def run_batch(days=1, start_date=None, output_dir="output"):
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    plan = build_plan(start_date, days)
    results = []
    from .cli import render_topic
    from .cli import render_fact, render_topic
    for item in plan:
        slug = item["topic"]
        try:
            source = "offline_library"
            warnings = []
            if os.getenv("ENABLE_AI_DRAFTS", "false").lower() == "true":
                try:
                    fact = draft_fact(item["title"])
                    result = render_fact(fact, "draft-" + item["date"].replace("-", ""))
                    source = "model_draft_unverified"
                except Exception as model_error:
                    warnings.append("AI draft unavailable; used curated offline topic instead: " + str(model_error))
                    result = render_topic(slug)
            else:
                result = render_topic(slug)
            quality = validate_package(result["video"], result["thumbnail"], result["metadata"])
            results.append({"date": item["date"], "topic": slug, "source": source,
                            "status": "ready_for_review" if quality["ok"] else "needs_attention",
                            "warnings": warnings, "artifacts": result, "quality": quality})
        except Exception as exc:
            results.append({"date": item["date"], "topic": slug, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    report = {"items": results, "successful": sum(x["status"] == "ready_for_review" for x in results),
              "failed": sum(x["status"] == "failed" for x in results), "publishing_enabled": False,
              "note": "This batch does not publish videos. Review each claim and output before uploading."}
    report_path = root / "automation_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report, str(report_path)
