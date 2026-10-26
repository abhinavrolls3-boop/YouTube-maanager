import pytest
from factverse_manager.content import Fact, SAMPLE_FACT, make_metadata, validate_fact

def test_sample_fact_validates(): validate_fact(SAMPLE_FACT)
def test_metadata_has_title_and_hashtags():
    m=make_metadata(SAMPLE_FACT); assert m["title"]==SAMPLE_FACT.title and "#" in m["hashtags"] and m["tags"]
def test_empty_title_rejected():
    with pytest.raises(ValueError): validate_fact(Fact("", "narration", "explanation", ("facts",)))
def test_curated_topic_metadata_includes_source_urls():
    from factverse_manager.library import get_topic
    fact = get_topic("venus-day").fact
    metadata = make_metadata(fact)
    assert metadata["source_urls"]
    assert metadata["source_urls"][0].startswith("https://")
