"""Summarize a YouTube Studio CSV export without sending it anywhere."""
import csv
from pathlib import Path

ALIASES = {
    "views": ("views", "view"),
    "impressions": ("impressions",),
    "ctr": ("impressions click-through rate", "impressions ctr", "ctr"),
    "watch_time": ("watch time (hours)", "watch time", "watch_time_hours"),
    "avg_duration": ("average view duration", "average view duration (seconds)", "avg_view_duration"),
    "title": ("video title", "title", "content"),
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
    """Return transparent, descriptive stats from an exported CSV; no invented benchmarks."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV must have a header row.")
        rows = list(reader)
        cols = {key: _column(reader.fieldnames, aliases) for key, aliases in ALIASES.items()}
    if not rows: raise ValueError("CSV contains no data rows.")
    result = {"rows": len(rows), "source": file_path.name, "metrics": {}, "top_videos_by_views": [], "notes": []}
    for metric in ("views", "impressions", "ctr", "watch_time", "avg_duration"):
        col = cols[metric]
        if not col: continue
        values = [_number(row.get(col)) for row in rows]
        valid = [v for v in values if v is not None]
        if valid:
            result["metrics"][metric] = {"count": len(valid), "total": round(sum(valid), 2), "average": round(sum(valid)/len(valid), 2), "max": round(max(valid), 2)}
    if cols["views"]:
        ranked = []
        for row in rows:
            views = _number(row.get(cols["views"]))
            if views is not None:
                ranked.append({"title": (row.get(cols["title"]) or "Untitled").strip(), "views": views})
        result["top_videos_by_views"] = sorted(ranked, key=lambda item: item["views"], reverse=True)[:5]
    if "views" not in result["metrics"]:
        result["notes"].append("No recognized views column; export a YouTube Studio CSV with a Views column.")
    if "ctr" in result["metrics"]:
        result["notes"].append("CTR values are summarized as exported; check whether your CSV stores percentages or fractions.")
    result["notes"].append("Descriptive statistics only; this CSV alone cannot prove why a video performed well.")
    return result
