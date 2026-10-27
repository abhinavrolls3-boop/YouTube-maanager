"""Free Wikimedia search for research leads; never treats search results as claim verification."""
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def discover_sources(query, limit=3, timeout=8):
    """Return Wikipedia article leads for a human to inspect, not verified citations."""
    query = str(query or "").strip()
    if not query:
        return {"query": query, "results": [], "status": "empty_query",
                "note": "Search leads must be opened and checked against each claim."}
    if not 1 <= int(limit) <= 10:
        raise ValueError("limit must be between 1 and 10")
    params = urlencode({
        "action": "query", "list": "search", "srsearch": query,
        "format": "json", "srlimit": int(limit), "utf8": 1,
    })
    url = "https://en.wikipedia.org/w/api.php?" + params
    request = Request(url, headers={"User-Agent": "FactVerseManager/1.0 (educational research lead lookup)"})
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        items = payload.get("query", {}).get("search", [])
        results = []
        for item in items[:int(limit)]:
            title = str(item.get("title", "")).strip()
            if not title:
                continue
            results.append({
                "title": title,
                "url": "https://en.wikipedia.org/wiki/" + title.replace(" ", "_"),
                "snippet": " ".join(str(item.get("snippet", "")).replace("<span class=\"searchmatch\">", "")
                                     .replace("</span>", "").split()),
                "source_type": "research_lead_only",
            })
        return {"query": query, "results": results,
                "status": "results" if results else "no_results",
                "note": "Search results are leads, not proof. Open the page and verify every claim against reliable primary or expert sources."}
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, KeyError, TypeError) as exc:
        return {"query": query, "results": [], "status": "unavailable",
                "error": type(exc).__name__,
                "note": "Live lookup failed. Use the curated source URLs and verify them manually."}
