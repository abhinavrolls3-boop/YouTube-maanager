"""Create cautious, actionable growth experiments from a YouTube Studio CSV."""
from .analytics import analyze_csv


def growth_report(csv_path):
    """Summarize observable signals and propose one-variable tests, not guarantees."""
    summary = analyze_csv(csv_path)
    videos = summary.get("top_videos_by_views", [])
    enriched = []
    for item in videos:
        row = dict(item)
        views = float(row.get("views") or 0)
        if views > 0:
            interactions = sum(float(row.get(k) or 0) for k in ("likes", "comments", "shares"))
            if any(k in row for k in ("likes", "comments", "shares")):
                row["interactions_per_100_views"] = round(interactions / views * 100, 2)
            if "subscribers" in row:
                row["subscribers_per_1000_views"] = round(float(row["subscribers"]) / views * 1000, 2)
        enriched.append(row)

    experiments = []
    metrics = summary.get("metrics", {})
    if "impressions" in metrics and "ctr" in metrics:
        experiments.append({
            "priority": 1,
            "hypothesis": "Packaging may be limiting clicks on videos receiving impressions.",
            "action": "Compare title and thumbnail clarity on videos with similar audience and age; test one change at a time.",
            "measure": "Impressions click-through rate alongside views and traffic source.",
            "guardrail": "Never promise a result or use a misleading thumbnail/title; CSV CTR units need checking."
        })
    if "avg_duration" in metrics or "watch_time" in metrics:
        experiments.append({
            "priority": 2,
            "hypothesis": "The opening or pacing may be losing viewers early.",
            "action": "Inspect each video's audience-retention graph; make the first 1–2 seconds state the specific curiosity, then remove slow setup.",
            "measure": "Early retention and average view duration for comparable Shorts.",
            "guardrail": "Use Studio retention graphs; average duration alone cannot locate drop-offs."
        })
    if "subscribers" in metrics:
        experiments.append({
            "priority": 3,
            "hypothesis": "Some topics may attract viewers who are more likely to return.",
            "action": "Compare subscriber gains per 1,000 views by topic and make a follow-up to the strongest topic.",
            "measure": "Subscribers gained per 1,000 views and returning viewers, where available.",
            "guardrail": "Small samples fluctuate; do not infer causation from a single upload."
        })
    if not experiments:
        experiments.append({
            "priority": 1,
            "hypothesis": "The export does not yet contain enough recognized diagnostic metrics.",
            "action": "Export video-level views, impressions, impressions click-through rate, average view duration, likes, comments, shares and subscribers gained from YouTube Studio.",
            "measure": "A consistent date range and comparable video age.",
            "guardrail": "Do not compare a new Short with an older Short without noting age and traffic source."
        })
    return {
        "source": summary.get("source"),
        "rows_analyzed": summary.get("rows", 0),
        "top_videos": enriched,
        "experiments": sorted(experiments, key=lambda x: x["priority"]),
        "next_upload_checklist": [
            "Make the opening deliver the promised fact quickly.",
            "Keep each Short to one clear claim and a readable visual sequence.",
            "Check the claim against the linked source before publishing.",
            "Review thumbnail/title on a phone-sized screen.",
            "Compare results only after recording upload date and a consistent measurement window."
        ],
        "limitations": [
            "This report is descriptive; it cannot guarantee growth or prove why a video performed well.",
            "A CSV cannot replace YouTube Studio retention graphs, traffic-source breakdowns or returning-viewer data.",
            "Review every claim, source, and final video manually before upload."
        ]
    }
