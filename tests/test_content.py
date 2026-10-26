import pytest
from factverse_manager.content import Fact, SAMPLE_FACT, make_metadata, validate_fact

def test_sample_fact_validates(): validate_fact(SAMPLE_FACT)
def test_metadata_has_title_and_hashtags():
    m=make_metadata(SAMPLE_FACT); assert m["title"]==SAMPLE_FACT.title and "#" in m["hashtags"] and m["tags"]
def test_empty_title_rejected():
    with pytest.raises(ValueError): validate_fact(Fact("", "narration", "explanation", ("facts",)))