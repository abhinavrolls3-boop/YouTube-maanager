from factverse_manager.creative import build_short_brief


def test_brief_reuses_narration_and_explanation_without_new_claims():
    brief = build_short_brief(
        "Why do astronauts float?",
        "Astronauts float because they and their spacecraft fall around Earth together.",
        "Gravity still acts in orbit. The spacecraft and astronauts are in continuous free fall.",
        ["space", "science"],
    )
    assert brief["opening_hook"].startswith("Astronauts float because")
    assert brief["core_question"] == "Why do astronauts float?"
    assert brief["shot_plan"][0]["time"] == "0–2s"
    assert "Gravity still acts in orbit." in [x["on_screen"] for x in brief["shot_plan"]]
    assert brief["human_review_required"] is True
    assert brief["topic_tags"] == ["space", "science"]


def test_brief_handles_empty_fields():
    brief = build_short_brief("", "", "", [])
    assert brief["opening_hook"] == ""
    assert brief["shot_plan"][0]["purpose"] == "Curiosity hook"
