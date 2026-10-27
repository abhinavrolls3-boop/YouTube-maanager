import json
from factverse_manager.growth import growth_report


def test_growth_report_adds_experiments_and_per_view_rates(tmp_path):
    path = tmp_path / "studio.csv"
    path.write_text(
        "Video title,Views,Impressions,Impressions click-through rate,Average view duration,Likes,Comments,Shares,Subscribers gained\n"
        "A,100,1000,5%,0:12,10,2,1,2\n"
        "B,50,700,3%,0:08,4,1,0,0\n"
        "C,25,300,2%,0:05,1,0,0,0\n",
        encoding="utf-8",
    )
    result = growth_report(path)
    assert result["rows_analyzed"] == 3
    assert result["top_videos"][0]["title"] == "A"
    assert result["top_videos"][0]["interactions_per_100_views"] == 13.0
    assert result["top_videos"][0]["subscribers_per_1000_views"] == 20.0
    assert len(result["experiments"]) >= 2
    assert result["limitations"]
    json.dumps(result)


def test_growth_report_handles_missing_diagnostic_metrics(tmp_path):
    path = tmp_path / "minimal.csv"
    path.write_text("Title,Views\nA,10\nB,5\n", encoding="utf-8")
    result = growth_report(path)
    assert result["experiments"][0]["priority"] == 1
    assert "export" in result["experiments"][0]["action"].lower()
