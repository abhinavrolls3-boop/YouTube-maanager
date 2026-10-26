from factverse_manager.source_check import check_sources

def test_invalid_source_url_is_flagged():
    result=check_sources(["file:///etc/passwd"])
    assert result["sources"][0]["status"] == "invalid_url"

def test_empty_sources_is_allowed():
    result=check_sources([])
    assert result["total"] == 0
    assert result["reachable"] == 0
