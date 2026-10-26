# YouTube Manager — FactVerse

A zero-budget-first toolkit for preparing FactVerse videos and automating repeatable production steps.

## Implemented
- Five curated offline science/nature topics with source URLs in metadata.
- Vertical MP4 motion graphics, thumbnail, metadata, narration text and timed SRT subtitles.
- Optional free local English TTS in the daily workflow using espeak-ng; failure is recorded and may leave a silent video.
- One-week calendar, bounded batch production, package preflight checks, JSON review report, and SHA-256 artifact integrity manifest.
- Missing source URLs are flagged. A separate command checks URL reachability but cannot verify claims.
- Offline YouTube Studio CSV analytics summaries.
- Optional OmniRoute model drafts, disabled unless configured.
- Scheduled GitHub Actions workflow, artifacts, optional webhook notifications.
- Manual YouTube API upload is protected by source, explicit human-review, originality-review, duplicate-file and daily-limit gates; public uploads are rejected.

## Commands
- `PYTHONPATH=src python -m factverse_manager.cli topics`
- `PYTHONPATH=src python -m factverse_manager.cli plan --days 7`
- `PYTHONPATH=src python -m factverse_manager.cli batch --days 1`
- `PYTHONPATH=src python -m factverse_manager.cli render octopus-hearts`
- `PYTHONPATH=src python -m factverse_manager.cli sources output/octopus-hearts_metadata.json`
- `PYTHONPATH=src python -m factverse_manager.cli verify-manifest output/artifact_manifest.json`
- `PYTHONPATH=src python -m factverse_manager.cli analytics path/to/youtube-studio-export.csv`
- `PYTHONPATH=src python -m factverse_manager.cli review output/astronauts-float_metadata.json`
- After personally reviewing the actual video and its sources: `PYTHONPATH=src python -m factverse_manager.cli approve output/astronauts-float_metadata.json --confirm-human-review --confirm-originality`
- `PYTHONPATH=src python -m factverse_manager.cli draft "ocean science"`

## Daily automation
Scheduled for 09:00 India time when GitHub provides a runner; this is not guaranteed always-on compute. AI drafts need secret `OMNIROUTE_API_KEY`, variables `OMNIROUTE_BASE_URL` and `OMNIROUTE_MODEL`, plus `ENABLE_AI_DRAFTS=true`. Provider costs/quotas may apply. The system does not yet conduct live source research.

The scheduled workflow does not upload videos. Manual upload requires YouTube OAuth and explicit per-video approval metadata. The uploader permits only private/unlisted visibility and defaults to one upload per UTC day. Approval flags are meaningful only after you actually review the video and its sources; they are not a way to bypass review.

## Not finished
- Live source discovery and evidence checking, robust character animation, licensed music, advanced motion control, permanent database, guaranteed 24/7 runtime, full channel analytics, or guaranteed earnings.
- Narration is basic robotic TTS, not studio-quality voice acting.
- AI drafts are not automatically treated as verified or upload-ready.

Never commit credentials or paste secrets into chat. See docs/AUTOMATION.md and docs/YOUTUBE_SETUP.md.


## Safety and review

Generated videos are drafts, not auto-published content. The scheduled workflow prepares artifacts only. Uploading requires source links, per-video human approval and an originality review; the uploader rejects public visibility and defaults to one upload per UTC day. No automated process can guarantee that YouTube will never restrict or remove a channel.
