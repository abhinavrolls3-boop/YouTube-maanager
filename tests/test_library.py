from factverse_manager.library import all_topics, get_topic

def test_topic_library_has_multiple_valid_facts():
    topics = all_topics()
    assert len(topics) >= 5
    assert len({topic.slug for topic in topics}) == len(topics)

def test_topic_lookup_returns_fact():
    assert get_topic("octopus-hearts").fact.title.startswith("How many hearts")

def test_unknown_topic_lists_available_topics():
    try:
        get_topic("not-a-real-topic")
    except ValueError as exc:
        assert "astronauts-float" in str(exc)
    else:
        raise AssertionError("Unknown topic should fail clearly")
