"""Generate a simple SRT caption file from narration text without external services."""
import re
from pathlib import Path

def _stamp(seconds):
    milliseconds = int(round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def write_srt(text, path, duration=18, max_words=8):
    if not text or not text.strip():
        raise ValueError("Caption text cannot be empty.")
    if duration <= 0 or max_words < 1:
        raise ValueError("Duration and max_words must be positive.")
    words = re.findall(r"\S+", text.strip())
    chunks = [words[i:i+max_words] for i in range(0, len(words), max_words)]
    root = Path(path)
    root.parent.mkdir(parents=True, exist_ok=True)
    step = duration / max(1, len(chunks))
    entries = []
    for index, chunk in enumerate(chunks, start=1):
        start = (index - 1) * step
        end = duration if index == len(chunks) else index * step
        entries.append(f"{index}\n{_stamp(start)} --> {_stamp(end)}\n{' '.join(chunk)}")
    root.write_text("\n\n".join(entries) + "\n", encoding="utf-8")
    return str(root)
