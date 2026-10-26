# YouTube Manager — FactVerse

A zero-budget-first toolkit for preparing FactVerse videos and automating repeatable production steps.

## What is implemented
- Five curated offline science/nature topics.
- Vertical MP4 motion-graphics rendering, thumbnail, metadata and narration text.
- One-week content calendar and a bounded batch production runner.
- Package preflight checks and machine-readable reports that require human fact review.
- Offline YouTube Studio CSV analytics summaries.
- Optional OpenAI-compatible OmniRoute script drafts, disabled unless configured.
- Daily scheduled GitHub Actions workflow, artifacts, optional webhook notifications.
- Optional headless YouTube Data API upload, gated by two explicit opt-in repository variables and OAuth credentials; uploads are unlisted only.

## Commands
Run from the repository root:
- PYTHONPATH=src python -m factverse_manager.cli topics
- PYTHONPATH=src python -m factverse_manager.cli plan --days 7
- PYTHONPATH=src python -m factverse_manager.cli batch --days 1
- PYTHONPATH=src python -m factverse_manager.cli render octopus-hearts
- PYTHONPATH=src python -m factverse_manager.cli analytics path/to/youtube-studio-export.csv
- PYTHONPATH=src python -m factverse_manager.cli draft "ocean science"

## Daily automation
The scheduled workflow is set for 09:00 India time, subject to GitHub Actions availability and quotas. It creates a package and report automatically when a runner is provided. GitHub Actions is not a guaranteed always-on server.

Optional AI drafts require repository secret "OMNIROUTE_API_KEY", variables "OMNIROUTE_BASE_URL" and "OMNIROUTE_MODEL", and "ENABLE_AI_DRAFTS=true". AI output is unverified; the system does not currently perform live web research or generate narration audio.

Automated upload is disabled unless repository variables "ENABLE_YOUTUBE_UPLOAD=true" and "APPROVE_AUTOMATED_UNLISTED_UPLOAD=true" and secret "YOUTUBE_TOKEN_JSON" are configured. If enabled, the workflow uploads as **unlisted**, never public. Cross-run duplicate protection uses a best-effort Actions cache, not a durable database.

## Important limitations
- The built-in facts are starter copy, not live research. Review claims and sources before publishing.
- The renderer produces silent motion graphics; it does not synthesize voice, music, character animation or motion-control footage.
- Analytics requires a CSV exported by you; no competitor or channel account is connected automatically.
- Free API quotas, scheduled execution, views and earnings are not guaranteed.
- Never commit credentials or paste secrets into chat.

Read docs/AUTOMATION.md, docs/ROADMAP.md, docs/CONTENT_WORKFLOW.md, docs/ANALYTICS.md, docs/ARCHITECTURE.md, and docs/YOUTUBE_SETUP.md.
