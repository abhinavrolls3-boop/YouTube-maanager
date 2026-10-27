import json
from factverse_manager import research


def test_discover_sources_returns_human_review_leads(monkeypatch):
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self):
            return json.dumps({"query": {"search": [
                {"title": "Venus", "snippet": "The <span class=\"searchmatch\">planet</span> Venus"}
            ]}}).encode()

    monkeypatch.setattr(research, "urlopen", lambda request, timeout: Response())
    result = research.discover_sources("Venus facts")
    assert result["status"] == "results"
    assert result["results"][0]["url"] == "https://en.wikipedia.org/wiki/Venus"
    assert result["results"][0]["source_type"] == "research_lead_only"
    assert "not proof" in result["note"]


def test_discover_sources_reports_network_failure(monkeypatch):
    def fail(request, timeout):
        raise TimeoutError("timeout")

    monkeypatch.setattr(research, "urlopen", fail)
    result = research.discover_sources("ocean science")
    assert result["status"] == "unavailable"
    assert result["results"] == []


def test_discover_sources_rejects_bad_limit():
    import pytest
    with pytest.raises(ValueError):
        research.discover_sources("science", limit=11)
