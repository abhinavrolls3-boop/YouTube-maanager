"""Simple repeat-avoiding content plan from the curated offline library."""
from datetime import date, timedelta
from .library import all_topics

def build_plan(start_date=None, days=7):
    if not 1 <= days <= 31:
        raise ValueError("Plan length must be between 1 and 31 days.")
    start = date.fromisoformat(start_date) if start_date else date.today()
    topics = all_topics()
    plan = []
    for offset in range(days):
        topic = topics[(start.toordinal() + offset) % len(topics)]
        plan.append({"date": (start + timedelta(days=offset)).isoformat(),
                     "topic": topic.slug, "title": topic.fact.title,
                     "review_required": True})
    return plan
