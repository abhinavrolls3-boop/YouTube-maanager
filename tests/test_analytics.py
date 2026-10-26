import json
import pytest
from factverse_manager.analytics import analyze_csv

def test_csv_summary_sorts_videos_and_calculates_metrics(tmp_path):
    csv_file = tmp_path / "studio.csv"
    csv_file.write_text('Video title,Views,Impressions,Impressions click-through rate\nA,100,1000,5.0%\nB,250,2000,4.0%\n', encoding="utf-8")
    result = analyze_csv(csv_file)
    assert result["metrics"]["views"]["total"] == 350
    assert result["top_videos_by_views"][0]["title"] == "B"
    assert result["top_videos_by_views"][0]["views"] == 250
    assert result["top_videos_by_views"][0]["ctr"] == 4.0
    assert result["experiments"]
    json.dumps(result)

def test_empty_csv_rows_rejected(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("Views\n", encoding="utf-8")
    with pytest.raises(ValueError):
        analyze_csv(csv_file)

def test_analytics_handles_engagement_and_retention_fields(tmp_path):
    csv_file = tmp_path / "studio.csv"
    csv_file.write_text(
        "Title,Views,Likes,Comments,Average view duration (seconds)\n"
        "A,100,10,2,15\nB,50,7,1,20\nC,20,2,0,9\n",
        encoding="utf-8")
    result = analyze_csv(csv_file)
    assert result["metrics"]["likes"]["total"] == 19
    assert result["metrics"]["comments"]["total"] == 3
    assert result["top_videos_by_views"][0]["avg_duration"] == 15
    assert any("Watch-duration" in x.get("observation", "") for x in result["experiments"])
