import json
import pytest
from factverse_manager.analytics import analyze_csv

def test_csv_summary_sorts_videos_and_calculates_metrics(tmp_path):
    csv_file = tmp_path / "studio.csv"
    csv_file.write_text('Video title,Views,Impressions,Impressions click-through rate\nA,100,1000,5.0%\nB,250,2000,4.0%\n', encoding="utf-8")
    result = analyze_csv(csv_file)
    assert result["metrics"]["views"]["total"] == 350
    assert result["top_videos_by_views"][0] == {"title": "B", "views": 250}
    json.dumps(result)

def test_empty_csv_rows_rejected(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("Views\n", encoding="utf-8")
    with pytest.raises(ValueError):
        analyze_csv(csv_file)
