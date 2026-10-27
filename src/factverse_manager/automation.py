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
from .source_check import check_sources
from .research import discover_sources


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
                research_path = None
                if os.getenv("ENABLE_LIVE_RESEARCH", "false").lower() == "true":
                    try:
                        query = metadata.get("title", slug)
                        tags = metadata.get("tags", [])
                        if isinstance(tags, list):
                            query += " " + " ".join(str(tag) for tag in tags[:3])
                        research_report = discover_sources(query, limit=3, timeout=6)
                        research_path = str(root / (slug + "_research_leads.json"))
                        Path(research_path).write_text(json.dumps(research_report, indent=2, ensure_ascii=False), encoding="utf-8")
                        result["research_leads"] = research_path
                        if research_report["status"] != "results":
                            warnings.append("Live research lookup returned no leads; inspect the curated sources manually.")
                    except Exception as research_error:
                        warnings.append("Live research lookup failed: " + type(research_error).__name__)
                source_report_path = None
                if os.getenv("ENABLE_SOURCE_CHECKS", "false").lower() == "true":
                    source_report = check_sources(metadata.get("source_urls", []), timeout=4)
                    source_report_path = str(root / (slug + "_source_check.json"))
                    Path(source_report_path).write_text(json.dumps(source_report, indent=2, ensure_ascii=False), encoding="utf-8")
                    result["source_check"] = source_report_path
                    if source_report["total"] and source_report["reachable"] != source_report["total"]:
                        warnings.append("One or more source URLs could not be reached; inspect the source-check report.")
                if os.getenv("ENABLE_NARRATION", "false").lower() == "true" and metadata.get("narration_status", "").startswith("unavailable"):
                    warnings.append("Voice narration could not be generated; output may be silent.")
                status = "ready_for_review" if quality["ok"] else "needs_attention"
                if source_report_path and source_report["total"] and source_report["reachable"] != source_report["total"]:
                    status = "needs_attention"
                results.append({"date": item["date"], "topic": slug, "source": source,
                                "status": status, "warnings": warnings + quality.get("warnings", []),
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
        for key in ("video", "thumbnail", "metadata", "subtitles", "review_checklist", "evidence_register", "source_check", "research_leads"):
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

    # A small, self-contained dashboard makes the artifact easier to inspect on a phone.
    def _relative_link(value):
        if not value:
            return ""
        target = Path(value)
        try:
            rel = target.resolve().relative_to(root)
        except ValueError:
            return ""
        return rel.as_posix()

    rows = []
    for item in results:
        artifacts = item.get("artifacts", {})
        links = []
        for key, label in (("video", "Video"), ("thumbnail", "Thumbnail"),
                           ("metadata", "Metadata"), ("subtitles", "Captions"),
                           ("source_check", "Source check"), ("evidence_register", "Evidence review"),
                           ("review_checklist", "Review checklist"), ("research_leads", "Research leads"),
                           ("creative_brief", "Shorts creative brief")):
            rel = _relative_link(artifacts.get(key))
            if rel:
                links.append(f'<a href="{rel}">{label}</a>')
        note = "; ".join(item.get("warnings", [])) or item.get("error", "")
        note = note.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        rows.append("<tr><td>" + str(item.get("topic", "unknown")) + "</td><td>" +
                    str(item.get("status", "unknown")) + "</td><td>" + " · ".join(links) +
                    "</td><td>" + note + "</td></tr>")
    dashboard = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FactVerse production report</title><style>
body{font:16px system-ui,sans-serif;max-width:1100px;margin:24px auto;padding:0 14px;color:#172033}
.notice{padding:12px;border:1px solid #d99;background:#fff8e8;border-radius:10px}
table{border-collapse:collapse;width:100%;margin-top:18px}th,td{text-align:left;padding:10px;border-bottom:1px solid #ddd;vertical-align:top}
a{margin-right:8px;white-space:nowrap}small{color:#555}
</style></head><body><h1>FactVerse production report</h1>
<p class="notice"><strong>Drafts only — nothing has been uploaded to YouTube.</strong> Review every factual claim, source, asset right, and originality before publishing.</p>
<p>Attempted: """ + str(report["attempted"]) + """ · Ready for review: """ + str(ready) + """ · Needs attention: """ + str(attention) + """ · Failed: """ + str(failed) + """</p>
<table><thead><tr><th>Topic</th><th>Status</th><th>Files</th><th>Warnings / errors</th></tr></thead><tbody>""" + "".join(rows) + """</tbody></table>
<p><small>Source reachability does not prove factual support. This dashboard is generated locally inside the workflow artifact.</small></p>
</body></html>"""
    (root / "index.html").write_text(dashboard, encoding="utf-8")
    return report, str(report_path)
