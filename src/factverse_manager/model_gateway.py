"""Optional OpenAI-compatible chat adapter. Never sends requests unless explicitly called."""
import json
import os
from urllib.request import Request, urlopen
from .content import Fact, validate_fact

def draft_fact(topic_hint, timeout=30):
    api_key = os.getenv("OMNIROUTE_API_KEY", "").strip()
    base_url = os.getenv("OMNIROUTE_BASE_URL", "").strip().rstrip("/")
    model = os.getenv("OMNIROUTE_MODEL", "").strip()
    if not api_key or not base_url or not model:
        raise RuntimeError("AI drafting needs OMNIROUTE_API_KEY secret plus OMNIROUTE_BASE_URL and OMNIROUTE_MODEL repository variables.")
    endpoint = base_url if base_url.endswith("/chat/completions") else base_url + "/chat/completions"
    prompt = (
        "Create one short educational fact video script in JSON only with keys title, narration, explanation, tags. "
        "Use a cautious, verifiable claim, avoid fabricated citations or unsupported exact statistics, "
        "keep title under 100 characters, narration 1-2 sentences, explanation under 1200 characters, "
        "and tags as an array of 3-6 short strings. This is an unverified draft requiring human fact-checking. "
        f"Topic hint: {topic_hint}"
    )
    payload = {"model": model, "temperature": 0.4, "messages": [
        {"role": "system", "content": "You draft concise educational scripts. Return valid JSON only."},
        {"role": "user", "content": prompt},
    ]}
    request = Request(endpoint, data=json.dumps(payload).encode("utf-8"),
                      headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
                      method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
        content = result["choices"][0]["message"]["content"]
        if isinstance(content, list):
            content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
        data = json.loads(content)
        tags = data.get("tags", [])
        if not isinstance(tags, list):
            raise ValueError("Model response tags must be a JSON array.")
        fact = Fact(str(data.get("title", "")).strip(), str(data.get("narration", "")).strip(),
                    str(data.get("explanation", "")).strip(), tuple(str(t).strip() for t in tags if str(t).strip()))
        validate_fact(fact)
        if len(fact.tags) < 3:
            raise ValueError("Model draft must include at least three tags.")
        return fact
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("Model returned an invalid response; no draft was accepted.") from exc
