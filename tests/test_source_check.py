from urllib.error import HTTPError
from factverse_manager import source_check
from factverse_manager.source_check import check_sources


def test_invalid_source_url_is_flagged():
    result = check_sources(["file:///etc/passwd"])
    assert result["sources"][0]["status"] == "invalid_url"


def test_empty_sources_is_allowed():
    result = check_sources([])
    assert result["total"] == 0
    assert result["reachable"] == 0


def test_head_method_not_allowed_falls_back_to_get(monkeypatch):
    calls = []

    def fake_request(url, method, timeout):
        calls.append(method)
        if method == "HEAD":
            raise HTTPError(url, 405, "Method Not Allowed", {}, None)
        return {"reachable": True, "http_status": 206}

    monkeypatch.setattr(source_check, "_request", fake_request)
    result = check_sources(["https://example.com/source"])
    assert calls == ["HEAD", "GET"]
    assert result["reachable"] == 1
    assert result["sources"][0]["method"] == "GET_fallback"
    assert result["sources"][0]["http_status"] == 206


def test_unreachable_source_is_reported(monkeypatch):
    def fake_request(url, method, timeout):
        raise TimeoutError("timed out")

    monkeypatch.setattr(source_check, "_request", fake_request)
    result = check_sources(["https://example.com/source"])
    assert result["reachable"] == 0
    assert result["sources"][0]["status"] == "unreachable"


def test_head_method_not_allowed_falls_back_to_get(monkeypatch):
    from urllib.error import HTTPError
    import factverse_manager.source_check as source_check

    calls = []

    def fake_request(url, method, timeout):
        calls.append(method)
        if method == "HEAD":
            raise HTTPError(url, 405, "Method Not Allowed", {}, None)
        return {"reachable": True, "http_status": 206}

    monkeypatch.setattr(source_check, "_request", fake_request)
    result = check_sources(["https://example.com/source"])
    assert calls == ["HEAD", "GET"]
    assert result["reachable"] == 1
    assert result["sources"][0]["method"] == "GET_fallback"


def test_source_timeout_is_reported(monkeypatch):
    import factverse_manager.source_check as source_check

    def fake_request(url, method, timeout):
        raise TimeoutError("timed out")

    monkeypatch.setattr(source_check, "_request", fake_request)
    result = check_sources(["https://example.com/source"])
    assert result["reachable"] == 0
    assert result["sources"][0]["status"] == "unreachable"
