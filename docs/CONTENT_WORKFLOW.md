# Offline content workflow

## Included now
- A small curated library of five science/nature facts that can be rendered without an AI API.
- A CLI topic selector, script/metadata export, MP4 render, thumbnail, and JSON sidecar.
- A CSV analytics summary for YouTube Studio exports.
- Explicit upload opt-in; no automatic public publishing is enabled by these features.

## Render a topic
```bash
PYTHONPATH=src python -m factverse_manager.cli topics
PYTHONPATH=src python -m factverse_manager.cli render octopus-hearts
```

## Quality gate before publishing
- Check the claim and source it independently; sample facts are starter copy, not a substitute for research.
- Review the script, spelling, pacing, and visual legibility.
- Watch the full MP4 and check the thumbnail.
- Use an unlisted upload first after OAuth is configured.
- Keep publishing manual until repeated runs and duplicate prevention have been tested.

The renderer creates simple topic-specific 2D motion graphics for the five built-in topics (space/orbit, octopus, Venus, shark, and honeycomb). The scheduled workflow attempts basic local English narration with espeak-ng; narration can fail and leave a silent video, so check the recorded narration status and listen to the full output. It does not provide licensed music, advanced character animation, or motion-control footage. No model or service can be assumed to have a permanent free quota.
