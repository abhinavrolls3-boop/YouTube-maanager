"""Generate a transparent, deterministic Shorts brief; never invent new factual claims."""
import re


def build_short_brief(title, narration, explanation, tags=()):
    title = " ".join(str(title or "").split()).strip()
    narration = " ".join(str(narration or "").split()).strip()
    explanation = " ".join(str(explanation or "").split()).strip()
    words = re.findall(r"[A-Za-z0-9’'-]+", narration)
    # Reuse the actual narration rather than inventing a sensational claim.
    hook = narration if len(words) <= 12 else " ".join(words[:12]).rstrip(".,;:!?") + "…"
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", explanation) if part.strip()]
    beats = [
        {"time": "0–2s", "purpose": "Curiosity hook", "on_screen": hook},
        {"time": "2–8s", "purpose": "Set up the question", "on_screen": title},
    ]
    if sentences:
        beats.append({"time": "8–16s", "purpose": "Explain the core idea", "on_screen": sentences[0]})
    if len(sentences) > 1:
        beats.append({"time": "final seconds", "purpose": "Clarify / memorable takeaway", "on_screen": sentences[-1]})
    clean_tags = [str(tag).strip() for tag in tags if str(tag).strip()]
    return {
        "format": "vertical_short",
        "opening_hook": hook,
        "core_question": title,
        "shot_plan": beats,
        "editing_notes": [
            "Show the main subject immediately; avoid a logo intro.",
            "Use large, high-contrast captions and keep text away from interface edges.",
            "Change visual emphasis when the narration moves to a new idea.",
            "Use only visuals and audio with appropriate rights; avoid repetitive stock-like loops.",
            "End on the answer, not an unsupported cliffhanger."
        ],
        "cta": "Follow FactVerse for more verified bite-sized facts.",
        "topic_tags": clean_tags[:8],
        "human_review_required": True,
        "note": "Timing is a rough storyboard, not word-level audio alignment. Confirm against the rendered video and narration."
    }
