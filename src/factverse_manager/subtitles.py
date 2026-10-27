"""Generate and validate simple SRT captions without external services."""
import re
from pathlib import Path

_TIME = re.compile(r"^(\d{2,}):(\d{2}):(\d{2}),(\d{3})$")


def _stamp(seconds):
    milliseconds = int(round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def _parse_stamp(value):
    match = _TIME.match(value)
    if not match:
        raise ValueError(f"invalid SRT timestamp: {value!r}")
    hours, minutes, seconds, millis = map(int, match.groups())
    if minutes >= 60 or seconds >= 60:
        raise ValueError(f"timestamp component out of range: {value!r}")
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def validate_srt(path, duration_seconds=None):
    """Return a validation report for SRT structure and cue timing."""
    file_path = Path(path)
    issues = []
    if not file_path.is_file() or file_path.stat().st_size == 0:
        return {"ok": False, "issues": ["Subtitle file is missing or empty."], "cues": 0}
    raw = file_path.read_text(encoding="utf-8-sig")
    blocks = [block.strip() for block in re.split(r"\n\s*\n", raw.strip()) if block.strip()]
    previous_end = 0.0
    for expected_index, block in enumerate(blocks, start=1):
        lines = block.splitlines()
        if len(lines) < 3 or lines[0].strip() != str(expected_index):
            issues.append(f"Cue {expected_index} has invalid numbering or missing text.")
            continue
        times = lines[1].split(" --> ")
        if len(times) != 2:
            issues.append(f"Cue {expected_index} has invalid timing line.")
            continue
        try:
            start, end = (_parse_stamp(item.strip()) for item in times)
        except ValueError as exc:
            issues.append(f"Cue {expected_index}: {exc}")
            continue
        if end <= start:
            issues.append(f"Cue {expected_index} ends before or at its start.")
        if start < previous_end:
            issues.append(f"Cue {expected_index} overlaps the previous cue.")
        if not any(line.strip() for line in lines[2:]):
            issues.append(f"Cue {expected_index} has no caption text.")
        if duration_seconds is not None and end > duration_seconds + 0.05:
            issues.append(f"Cue {expected_index} ends after video duration.")
        previous_end = end
    if not blocks:
        issues.append("Subtitle file contains no cues.")
    return {"ok": not issues, "issues": issues, "cues": len(blocks)}


def write_srt(text, path, duration=18, max_words=8):
    if not text or not text.strip():
        raise ValueError("Caption text cannot be empty.")
    if duration <= 0 or max_words < 1:
        raise ValueError("Duration and max_words must be positive.")
    words = re.findall(r"\S+", text.strip())
    chunks = [words[i:i + max_words] for i in range(0, len(words), max_words)]
    root = Path(path)
    root.parent.mkdir(parents=True, exist_ok=True)
    # Allocate time by spoken word count rather than giving a short final cue
    # the same duration as a much longer cue. This is still an estimate, not
    # forced alignment against actual TTS audio.
    total_words = max(1, len(words))
    elapsed_words = 0
    entries = []
    for index, chunk in enumerate(chunks, start=1):
        start = duration * elapsed_words / total_words
        elapsed_words += len(chunk)
        end = duration if index == len(chunks) else duration * elapsed_words / total_words
        entries.append(f"{index}\n{_stamp(start)} --> {_stamp(end)}\n{' '.join(chunk)}")
    root.write_text("\n\n".join(entries) + "\n", encoding="utf-8")
    return str(root)
