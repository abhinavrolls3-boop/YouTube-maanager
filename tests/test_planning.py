from factverse_manager.planning import build_plan

def test_plan_has_sequential_dates_and_rotates_topics():
    plan = build_plan("2026-10-26", 7)
    assert len(plan) == 7
    assert plan[0]["date"] == "2026-10-26"
    assert plan[1]["date"] == "2026-10-27"
    assert plan[0]["topic"] != plan[1]["topic"]
    assert all(item["review_required"] for item in plan)

def test_plan_length_is_bounded():
    try:
        build_plan("2026-10-26", 32)
    except ValueError:
        pass
    else:
        raise AssertionError("Overlong plan should be rejected")

def test_single_day_topic_changes_with_date():
    first = build_plan("2026-10-26", 1)[0]["topic"]
    second = build_plan("2026-10-27", 1)[0]["topic"]
    assert first != second
