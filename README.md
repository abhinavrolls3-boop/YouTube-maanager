# YouTube Manager — FactVerse

A zero-budget-first toolkit for preparing FactVerse videos and automating repeatable production steps.

## Implemented
- Seven curated offline science/nature topics with source URLs in metadata.
- Vertical MP4 videos with topic-specific 2D scenes for space, octopuses, Venus, sharks, and honey, plus two additional space topics; thumbnail, metadata, narration text, and timed SRT subtitles.
- Optional free local English TTS in the daily workflow using espeak-ng; failure is recorded and may leave a silent video.
- One-week calendar, bounded batch production, package preflight checks, JSON review report, and SHA-256 artifact integrity manifest.
- Package preflight now decodes the generated MP4, checks that it is readable and vertical, and validates thumbnail readability; corrupt/non-video files are rejected.
- If metadata points to an SRT file, package preflight checks cue numbering, timestamp syntax, overlaps, and missing captions; it does not claim captions are synchronized to spoken audio.
- Missing source URLs are flagged. Scheduled batches also check source URL reachability and include a per-topic report; this cannot verify factual support.
- Each batch now creates a per-claim evidence register; every claim starts unverified and needs human evidence review.
- Offline YouTube Studio CSV analytics summaries, including average view-duration parsing from common M:SS and H:MM:SS exports.
- Optional OmniRoute model drafts, disabled unless configured.
- Scheduled GitHub Actions workflow, artifacts, a phone-friendly run summary with per-topic status, and optional webhook notifications.
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
- `PYTHONPATH=src python -m factverse_manager.cli evidence output/astronauts-float_metadata.json`
- Edit the generated `output/astronauts-float_evidence.json`: add a supporting `evidence_url`, quote/location, and set each reviewed claim assessment to `supported` only if the source actually supports it.
- After checking every claim and source, fill in each claim's evidence URL, supporting quote/location, and set its assessment to `supported`; then run `PYTHONPATH=src python -m factverse_manager.cli evidence-approve output/astronauts-float_evidence.json --confirm-each-claim --confirm-sources`. This also records the evidence-review status in the linked metadata.
- Only after evidence approval and a separate originality/asset-rights review: `PYTHONPATH=src python -m factverse_manager.cli approve output/astronauts-float_metadata.json --confirm-human-review --confirm-originality`. The uploader blocks packages without the evidence-review status.
- `PYTHONPATH=src python -m factverse_manager.cli draft "ocean science"`

## Daily automation
Scheduled for 09:00 India time when GitHub provides a runner; this is not guaranteed always-on compute. AI drafts need secret `OMNIROUTE_API_KEY`, variables `OMNIROUTE_BASE_URL` and `OMNIROUTE_MODEL`, plus `ENABLE_AI_DRAFTS=true`. Provider costs/quotas may apply. The system does not yet conduct live source research.

The scheduled workflow runs in GitHub's cloud; you do not need to keep ChatGPT or the phone app open. After each run, the workflow summary reports ready/failed counts and points to the temporary artifact. To receive a notification without checking GitHub, configure `NOTIFY_WEBHOOK_URL`. The scheduled workflow does not upload videos. Manual upload requires YouTube OAuth and explicit per-video approval metadata. The uploader permits only private/unlisted visibility and defaults to one upload per UTC day. Approval flags are meaningful only after you actually review the video and its sources; they are not a way to bypass review.

## Not finished
- Live source discovery and evidence checking, robust character animation, licensed music, advanced motion control, permanent database, guaranteed 24/7 runtime, full channel analytics, or guaranteed earnings.
- Narration is basic robotic TTS, not studio-quality voice acting.
- AI drafts are not automatically treated as verified or upload-ready.

Never commit credentials or paste secrets into chat. See docs/AUTOMATION.md and docs/YOUTUBE_SETUP.md.


## Safety and review

Generated videos are drafts, not auto-published content. The scheduled workflow prepares artifacts only. Uploading requires source links, per-video human approval and an originality review; the uploader rejects public visibility and defaults to one upload per UTC day. No automated process can guarantee that YouTube will never restrict or remove a channel.
