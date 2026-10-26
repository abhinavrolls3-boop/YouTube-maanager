# YouTube Manager — FactVerse

A phone-manageable, zero-budget-first toolkit for preparing FactVerse videos. The repo supports offline topic selection, lightweight silent 2D motion-graphics rendering, thumbnail/metadata generation, and summaries of YouTube Studio CSV exports.

## Zero-budget and safety rules
- No paid API, GPU rental, server, or subscription is assumed.
- GitHub Actions is a remote runner, but free access/quotas are not guaranteed and schedules are best-effort.
- This is not an always-on service. Work runs only when a supported runner is available.
- The starter renderer makes silent motion graphics, not full character animation or motion-control footage.
- YouTube uploads remain disabled by default and require OAuth for a channel you control.
- Never commit OAuth files, tokens, or private audience reports.
- Do not automatically publish unreviewed claims or use fake engagement.

## What is implemented
- Five curated offline science/nature topics (no model API required).
- One-week content calendar generation with review-required flags.
- Local SHA-256 upload history that blocks repeat uploads of the exact same video file.
- MP4, vertical thumbnail, title/description/tags/hashtags and narration text metadata.
- Tests for content validation, topic selection, CSV analytics and real render artifact creation.
- YouTube Studio CSV analytics summary with top videos and descriptive metrics.
- Optional official YouTube Data API upload adapter, opt-in only.
- Manual GitHub Actions build workflow that uploads a short-lived artifact.

## Commands
Run from the repository root:
- PYTHONPATH=src python -m factverse_manager.cli topics
- PYTHONPATH=src python -m factverse_manager.cli plan --days 7 --start 2026-10-26
- PYTHONPATH=src python -m factverse_manager.cli render octopus-hearts
- PYTHONPATH=src python -m factverse_manager.cli analytics path/to/youtube-studio-export.csv

Without a subcommand, the CLI renders the original sample fact.

## Current known limits
- Videos have no generated narration or music; narration text is included as metadata for review/recording.
- Content is a starter library, not live research. Fact-check each script before publishing.
- Analytics requires a CSV export supplied by you; no channel or competitor account is connected automatically.
- No unattended upload or automatic public publishing is enabled. The OAuth adapter currently uses an interactive local browser flow, so it is not suitable for headless CI as-is.
- No guaranteed daily schedule, 24/7 compute, free AI quota, or earnings outcome.

## Next acceptance gates
1. Run the workflow on the latest commit and confirm every test passes.
2. Download the artifact and play the MP4; inspect the thumbnail and metadata.
3. Verify the new topic render command on a runner.
4. Test an unlisted upload only after completing the OAuth setup guide.
5. Enable any scheduled workflow only after repeatability, quota limits, duplicate prevention, and notifications are verified.

Read the documentation in docs/ROADMAP.md, docs/CONTENT_WORKFLOW.md, docs/ANALYTICS.md, docs/ARCHITECTURE.md, and docs/YOUTUBE_SETUP.md.
