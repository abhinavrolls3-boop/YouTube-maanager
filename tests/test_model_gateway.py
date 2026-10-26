import json
import pytest
from factverse_manager.model_gateway import draft_fact

def test_model_adapter_requires_explicit_configuration(monkeypatch):
    for key in ("OMNIROUTE_API_KEY", "OMNIROUTE_BASE_URL", "OMNIROUTE_MODEL"):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(RuntimeError, match="needs OMNIROUTE"):
        draft_fact("space")

def test_model_response_parser(monkeypatch):
    import factverse_manager.model_gateway as gateway
    class FakeResponse:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self):
            return json.dumps({"choices":[{"message":{"content":json.dumps({
                "title":"A science fact", "narration":"A short narration.",
                "explanation":"A cautious explanation for review.",
                "tags":["science","facts","learning"]})}}]}).encode()
    monkeypatch.setenv("OMNIROUTE_API_KEY","test-key")
    monkeypatch.setenv("OMNIROUTE_BASE_URL","https://example.invalid/v1")
    monkeypatch.setenv("OMNIROUTE_MODEL","test-model")
    monkeypatch.setattr(gateway, "urlopen", lambda *args, **kwargs: FakeResponse())
    fact = draft_fact("space")
    assert fact.title == "A science fact"
    assert len(fact.tags) == 3
