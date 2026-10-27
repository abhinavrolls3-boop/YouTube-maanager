"""Lightweight source URL validation; reachability does not prove factual support."""
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse


def _request(url, method, timeout):
    headers = {"User-Agent": "FactVerseSourceChecker/1.1"}
    if method == "GET":
        # Only fetch a tiny byte range when servers reject HEAD requests.
        headers["Range"] = "bytes=0-0"
    request = Request(url, headers=headers, method=method)
    with urlopen(request, timeout=timeout) as response:
        status = getattr(response, "status", 200)
        return {"reachable": 200 <= status < 400, "http_status": status}


def check_sources(urls, timeout=8):
    """Check HTTP availability, falling back to a tiny GET when HEAD is unsupported."""
    results = []
    for raw in urls or []:
        url = str(raw).strip()
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            results.append({"url": url, "status": "invalid_url", "reachable": False})
            continue
        try:
            result = _request(url, "HEAD", timeout)
            # Some legitimate sites reject HEAD but allow ordinary GET requests.
            if not result["reachable"] and result["http_status"] in {403, 405, 501}:
                result = _request(url, "GET", timeout)
                result["method"] = "GET_fallback"
            else:
                result["method"] = "HEAD"
            result["url"] = url
            result["status"] = "reachable" if result["reachable"] else "http_error"
            results.append(result)
        except HTTPError as exc:
            if exc.code in {403, 405, 501}:
                try:
                    result = _request(url, "GET", timeout)
                    result.update({"url": url, "status": "reachable" if result["reachable"] else "http_error",
                                   "method": "GET_fallback"})
                    results.append(result)
                    continue
                except HTTPError as get_exc:
                    results.append({"url": url, "status": "http_error", "reachable": False,
                                    "http_status": get_exc.code, "method": "GET_fallback"})
                    continue
                except (URLError, TimeoutError, OSError) as get_exc:
                    results.append({"url": url, "status": "unreachable", "reachable": False,
                                    "error": type(get_exc).__name__, "method": "GET_fallback"})
                    continue
            results.append({"url": url, "status": "http_error", "reachable": False, "http_status": exc.code})
        except (URLError, TimeoutError, OSError) as exc:
            results.append({"url": url, "status": "unreachable", "reachable": False, "error": type(exc).__name__})
    return {
        "total": len(results),
        "reachable": sum(1 for item in results if item["reachable"]),
        "sources": results,
        "note": "URL reachability is not evidence that the page supports the claim; review the source content.",
    }
