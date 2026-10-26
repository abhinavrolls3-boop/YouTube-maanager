# Roadmap and acceptance gates

## Day 1: render proof
- Run the manual workflow on a real runner.
- Generate one short 2D motion-graphics MP4, thumbnail, and metadata.
- Inspect logs and play the video.

## Day 2: upload and reliability proof
- Configure Google OAuth from your own Google Cloud project.
- Upload one unlisted test video and verify it in YouTube Studio.
- Test reruns and duplicate prevention; confirm runner access and limits.

Two days is a target for a proof-of-concept, not a guarantee of a finished autonomous manager. Afterward, run a daily schedule for several days before public publishing. Start with one video/day; consider two only after quality checks.

## Acceptance gates
- Workflow log confirms success.
- MP4 plays with expected dimensions/duration.
- Thumbnail and metadata exist.
- Test upload is visible in YouTube Studio.
- Repeated runs do not publish duplicates.

## Stop conditions
If the runner is unavailable, asks for payment, or fails before starting, report that honestly. Phone-only dependable scheduled rendering at ₹0 is not feasible without a usable free remote runner.