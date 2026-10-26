"""Deterministic sample content; no paid model API required."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Fact:
    title: str
    narration: str
    explanation: str
    tags: tuple[str, ...]
    sources: tuple[str, ...] = ()

SAMPLE_FACT = Fact(
    title="Why do astronauts look like they float?",
    narration="Astronauts look like they float because they and their spacecraft are falling around Earth together.",
    explanation="Gravity is still acting in orbit. The spacecraft moves forward fast enough that it keeps falling around Earth instead of hitting the ground. Astronauts experience this continuous free fall as weightlessness.",
    tags=("space", "science", "facts", "astronauts", "education"),
)

def validate_fact(fact: Fact) -> None:
    for value in (fact.title, fact.narration, fact.explanation):
        if not value or not value.strip():
            raise ValueError("Title, narration, and explanation must be non-empty.")
    if len(fact.title) > 100:
        raise ValueError("Title must be 100 characters or fewer.")
    if len(fact.explanation) > 1200:
        raise ValueError("Explanation is too long for the starter template.")

def make_metadata(fact: Fact) -> dict:
    validate_fact(fact)
    hashtags = " ".join("#" + re.sub(r"[^A-Za-z0-9]", "", tag.title()) for tag in fact.tags[:5])
    source_section = "\n\nSources to verify:\n" + "\n".join(fact.sources) if fact.sources else ""
    description = f"{fact.explanation}\n\nFollow FactVerse for more bite-sized facts.{source_section}\n\n{hashtags}"
    return {"title": fact.title, "description": description, "tags": list(fact.tags), "hashtags": hashtags, "categoryId": "27", "source_urls": list(fact.sources),
            "human_review_status": "needs_review", "originality_check_status": "needs_review"}