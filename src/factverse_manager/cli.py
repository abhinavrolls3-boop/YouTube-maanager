"""Command-line interface for offline FactVerse planning and rendering."""
import argparse
import json
from pathlib import Path
from .analytics import analyze_csv
from .automation import run_batch
from .quality import validate_package
from .content import SAMPLE_FACT, make_metadata
from .library import all_topics, get_topic
from .model_gateway import draft_fact
from .planning import build_plan
from .render import render_video
from .narration import add_narration
from .source_check import check_sources
from .youtube_upload import upload_video

def _write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)

def render_fact(fact, safe_slug):
    import os
    output_dir = Path(os.getenv("FACTVERSE_OUTPUT_DIR", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    video_path = str(output_dir / f"{safe_slug}.mp4")
    thumbnail_path = str(output_dir / f"{safe_slug}_thumbnail.png")
    video, thumbnail = render_video(fact.title, fact.explanation, video_path, thumbnail_path)
    narration_status = "disabled"
    if __import__("os").getenv("ENABLE_NARRATION", "false").lower() == "true":
        try:
            add_narration(video, fact.narration)
            narration_status = "generated_local_tts"
        except Exception as exc:
            narration_status = "unavailable: " + str(exc)
    metadata = make_metadata(fact)
    metadata["narration"] = fact.narration
    metadata["topic_slug"] = safe_slug
    metadata["human_fact_check_required"] = True
    metadata["narration_status"] = narration_status
    metadata_path = _write_json(str(output_dir / f"{safe_slug}_metadata.json"), metadata)
    return {"topic": safe_slug, "video": video, "thumbnail": thumbnail, "metadata": metadata_path}

def render_topic(slug=None):
    topic = get_topic(slug) if slug else None
    fact = topic.fact if topic else SAMPLE_FACT
    safe_slug = topic.slug if topic else "factverse_sample"
    result = render_fact(fact, safe_slug)
    print(json.dumps(result, indent=2))
    return result

def main():
    parser = argparse.ArgumentParser(description="Offline-first FactVerse content helper")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("topics", help="list built-in offline topics")
    render_parser = sub.add_parser("render", help="render one built-in topic")
    render_parser.add_argument("topic", help="topic slug shown by the topics command")
    plan_parser = sub.add_parser("plan", help="create an offline content calendar")
    plan_parser.add_argument("--start", help="start date in YYYY-MM-DD format")
    plan_parser.add_argument("--days", type=int, default=7, help="number of days (1-31)")
    batch_parser = sub.add_parser("batch", help="render a bounded batch and produce a review report")
    batch_parser.add_argument("--start", help="start date in YYYY-MM-DD format")
    batch_parser.add_argument("--days", type=int, default=1, help="number of topics to render (1-31)")
    upload_parser = sub.add_parser("upload", help="upload one reviewed video using YouTube OAuth")
    upload_parser.add_argument("video")
    upload_parser.add_argument("metadata")
    draft_parser = sub.add_parser("draft", help="generate an optional model-assisted script draft")
    draft_parser.add_argument("topic_hint", help="topic hint for the draft")
    check_parser = sub.add_parser("check", help="check a video, thumbnail and metadata package")
    check_parser.add_argument("video")
    check_parser.add_argument("thumbnail")
    check_parser.add_argument("metadata")
    sources_parser = sub.add_parser("sources", help="check whether source URLs are reachable")
    sources_parser.add_argument("metadata", help="metadata JSON containing source_urls")
    analytics_parser = sub.add_parser("analytics", help="summarize a YouTube Studio CSV export")
    analytics_parser.add_argument("csv_path", help="path to CSV file")
    args = parser.parse_args()
    if args.command == "topics":
        print(json.dumps([{"slug": t.slug, "title": t.fact.title} for t in all_topics()], indent=2, ensure_ascii=False))
    elif args.command == "render":
        render_topic(args.topic)
    elif args.command == "plan":
        plan = build_plan(args.start, args.days)
        path = _write_json("output/content_plan.json", plan)
        print(json.dumps({"plan": path, "items": plan}, indent=2, ensure_ascii=False))
    elif args.command == "batch":
        report, path = run_batch(args.days, args.start)
        print(json.dumps({"report": path, "summary": report}, indent=2, ensure_ascii=False))
    elif args.command == "upload":
        metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
        video_id = upload_video(args.video, metadata)
        print(json.dumps({"video_id": video_id, "privacy": __import__("os").getenv("UPLOAD_PRIVACY", "unlisted")}, indent=2))
    elif args.command == "draft":
        fact = draft_fact(args.topic_hint)
        data = make_metadata(fact)
        data.update({"narration": fact.narration, "explanation": fact.explanation, "human_fact_check_required": True})
        path = _write_json("output/model_draft.json", data)
        print(json.dumps({"draft": path, "title": fact.title, "human_fact_check_required": True}, indent=2, ensure_ascii=False))
    elif args.command == "check":
        result = validate_package(args.video, args.thumbnail, args.metadata)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not result["ok"]:
            raise SystemExit(1)
    elif args.command == "sources":
        metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
        result = check_sources(metadata.get("source_urls", []))
        path = _write_json("output/source_check.json", result)
        print(json.dumps({"report": path, "summary": result}, indent=2, ensure_ascii=False))
        if result["total"] and result["reachable"] != result["total"]:
            raise SystemExit(1)
    elif args.command == "analytics":
        result = analyze_csv(args.csv_path)
        path = _write_json("output/analytics.json", result)
        print(json.dumps({"report": path, "summary": result}, indent=2, ensure_ascii=False))
    else:
        render_topic()

if __name__ == "__main__":
    main()
