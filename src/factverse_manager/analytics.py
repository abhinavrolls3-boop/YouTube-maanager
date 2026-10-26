"""Summarize YouTube Studio CSV exports and suggest testable follow-up experiments."""
import csv
from pathlib import Path

ALIASES = {
    "views": ("views", "view"),
    "impressions": ("impressions",),
    "ctr": ("impressions click-through rate", "impressions ctr", "ctr"),
    "watch_time": ("watch time (hours)", "watch time", "watch_time_hours"),
    "avg_duration": ("average view duration", "average view duration (seconds)", "avg_view_duration"),
    "title": ("video title", "title", "content"),
    "likes": ("likes", "like"),
    "comments": ("comments", "comment"),
    "shares": ("shares", "share"),
    "subscribers": ("subscribers gained", "subscribers", "subscribers gained (net)"),
}

def _number(value):
    if value is None: return None
    cleaned = str(value).strip().replace(",", "").replace("%", "")
    if not cleaned or cleaned in {"-", "—", "N/A"}: return None
    try: return float(cleaned)
    except ValueError: return None

def _column(headers, aliases):
    lowered = {h.strip().lower(): h for h in headers}
    for alias in aliases:
        if alias in lowered: return lowered[alias]
    return None

def analyze_csv(path):
    """Return descriptive statistics; avoid pretending correlations prove causation."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames: raise ValueError("CSV must have a header row.")
        rows = list(reader)
        cols = {key: _column(reader.fieldnames, aliases) for key, aliases in ALIASES.items()}
    if not rows: raise ValueError("CSV contains no data rows.")
    result = {"rows": len(rows), "source": file_path.name, "metrics": {}, "top_videos_by_views": [], "experiments": [], "notes": []}
    for metric in ("views", "impressions", "ctr", "watch_time", "avg_duration", "likes", "comments", "shares", "subscribers"):
        col = cols[metric]
        if not col: continue
        values = [_number(row.get(col)) for row in rows]
        valid = [v for v in values if v is not None]
        if valid:
            result["metrics"][metric] = {"count": len(valid), "total": round(sum(valid), 2), "average": round(sum(valid)/len(valid), 2), "max": round(max(valid), 2)}
    ranked = []
    if cols["views"]:
        for row in rows:
            views = _number(row.get(cols["views"]))
            if views is not None:
                item = {"title": (row.get(cols["title"]) or "Untitled").strip(), "views": views}
                for metric in ("ctr", "avg_duration", "watch_time", "likes", "comments", "shares", "subscribers"):
                    col = cols[metric]
                    if col:
                        value = _number(row.get(col))
                        if value is not None: item[metric] = value
                ranked.append(item)
    result["top_videos_by_views"] = sorted(ranked, key=lambda item: item["views"], reverse=True)[:5]
    if "views" not in result["metrics"]:
        result["notes"].append("No recognized views column; export a YouTube Studio CSV with a Views column.")
    if "ctr" in result["metrics"]:
        result["notes"].append("CTR values are summarized as exported; check whether your CSV stores percentages or fractions.")
    if len(ranked) >= 3:
        by_views = sorted(ranked, key=lambda x: x["views"], reverse=True)
        result["experiments"].append({"observation": "Some videos have higher views than others in this export.",
            "test": "Compare the top and bottom videos' topic, opening hook, length, and audience retention in Studio; change one variable per next batch.",
            "caution": "Views alone do not identify the cause; account for impressions, age of video, and traffic sources."})
    if cols["ctr"] and cols["impressions"]:
        result["experiments"].append({"observation": "Impressions and click-through rate are available.",
            "test": "Review thumbnail/title clarity on videos with many impressions; test one title or thumbnail idea at a time where Studio supports it.",
            "caution": "Do not use misleading titles or thumbnails; CTR depends on audience and traffic source."})
    if cols["avg_duration"] or cols["watch_time"]:
        result["experiments"].append({"observation": "Watch-duration data is available.",
            "test": "Inspect retention graphs in YouTube Studio and compare the opening seconds with early drop-offs; improve the next script accordingly.",
            "caution": "CSV averages cannot replace the detailed retention graph."})
    result["notes"].append("Descriptive statistics and experiment ideas only; this CSV cannot prove why a video performed well.")
    return result
