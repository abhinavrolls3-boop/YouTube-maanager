"""Run a bounded batch of offline production tasks; designed for scheduled CI."""
import json
import os
from pathlib import Path
from .planning import build_plan
from .quality import validate_package
from .model_gateway import draft_fact
from .manifest import create_manifest
from .review import create_review_checklist
from .evidence import create_evidence_register


def run_batch(days=1, start_date=None, output_dir="output"):
    root = Path(output_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    plan = build_plan(start_date, days)
    results = []
    from .cli import render_fact, render_topic
    previous_output_dir = os.environ.get("FACTVERSE_OUTPUT_DIR")
    os.environ["FACTVERSE_OUTPUT_DIR"] = str(root)
    try:
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
                metadata = json.loads(Path(result["metadata"]).read_text(encoding="utf-8"))
                if os.getenv("ENABLE_NARRATION", "false").lower() == "true" and metadata.get("narration_status", "").startswith("unavailable"):
                    warnings.append("Voice narration could not be generated; output may be silent.")
                results.append({"date": item["date"], "topic": slug, "source": source,
                                "status": "ready_for_review" if quality["ok"] else "needs_attention",
                                "warnings": warnings + quality.get("warnings", []),
                                "quality": quality, "artifacts": result})
            except Exception as exc:
                results.append({"date": item["date"], "topic": slug, "status": "failed",
                                "error": f"{type(exc).__name__}: {exc}"})
    finally:
        if previous_output_dir is None:
            os.environ.pop("FACTVERSE_OUTPUT_DIR", None)
        else:
            os.environ["FACTVERSE_OUTPUT_DIR"] = previous_output_dir

    artifact_paths = []
    for item in results:
        metadata_path = item.get("artifacts", {}).get("metadata")
        if metadata_path and item.get("status") != "failed":
            try:
                _, checklist_path = create_review_checklist(metadata_path)
                item.setdefault("artifacts", {})["review_checklist"] = checklist_path
                _, evidence_path = create_evidence_register(metadata_path)
                item.setdefault("artifacts", {})["evidence_register"] = evidence_path
            except Exception as exc:
                item.setdefault("warnings", []).append("Could not create review/evidence checklist: " + str(exc))
                item["status"] = "needs_attention"
        for key in ("video", "thumbnail", "metadata", "subtitles", "review_checklist", "evidence_register"):
            path = item.get("artifacts", {}).get(key)
            if path:
                artifact_paths.append(path)
    manifest_path = create_manifest(artifact_paths, root / "artifact_manifest.json")
    ready = sum(x["status"] == "ready_for_review" for x in results)
    attention = sum(x["status"] == "needs_attention" for x in results)
    failed = sum(x["status"] == "failed" for x in results)
    report = {
        "items": results,
        "attempted": len(results),
        "successful": ready,
        "ready_for_review": ready,
        "needs_attention": attention,
        "failed": failed,
        "publishing_enabled": False,
        "artifact_manifest": manifest_path,
        "note": "This batch does not publish videos. Review every claim, source, and output before uploading.",
    }
    report_path = root / "automation_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report, str(report_path)
