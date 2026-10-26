"""Lightweight source URL validation; reachability does not prove factual support."""
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse

def check_sources(urls, timeout=8):
    results=[]
    for raw in urls or []:
        url=str(raw).strip()
        parsed=urlparse(url)
        if parsed.scheme not in ("http","https") or not parsed.netloc:
            results.append({"url":url,"status":"invalid_url","reachable":False})
            continue
        request=Request(url, headers={"User-Agent":"FactVerseSourceChecker/1.0"}, method="HEAD")
        try:
            with urlopen(request, timeout=timeout) as response:
                results.append({"url":url,"status":"reachable","reachable":200 <= response.status < 400,"http_status":response.status})
        except HTTPError as exc:
            results.append({"url":url,"status":"http_error","reachable":False,"http_status":exc.code})
        except (URLError, TimeoutError, OSError) as exc:
            results.append({"url":url,"status":"unreachable","reachable":False,"error":type(exc).__name__})
    return {"total":len(results),"reachable":sum(1 for item in results if item["reachable"]),"sources":results,
            "note":"URL reachability is not evidence that the page supports the claim; review the source content."}
