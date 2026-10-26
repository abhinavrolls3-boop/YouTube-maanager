# YouTube Manager — FactVerse

A phone-manageable, zero-budget-first workflow for the FactVerse channel. The first milestone is a lightweight template-based 2D animated facts video, thumbnail, metadata, and an optional authorized YouTube upload.

## Non-negotiable constraints
- Target budget: ₹0; no paid API, GPU rental, server, or subscription assumed.
- Manage setup from an Android browser; rendering requires a remote runner.
- No 24/7 compute. Jobs should run on a schedule and stop when finished.
- Free runners and quotas can change. GitHub Actions scheduling is best-effort, not guaranteed always-on.
- The initial renderer is lightweight 2D motion graphics, not a full character animation or motion-control engine.
- YouTube uploads require your own Google Cloud project, YouTube Data API, and OAuth. Never commit credentials.
- Hashtags cannot guarantee virality; growth recommendations must be based on observed analytics.

## Included so far
- Python pipeline for a sample animated fact video, thumbnail, title/description/tags.
- Unit tests for content and rendering.
- Optional official YouTube upload adapter, disabled unless explicitly enabled.
- Manual GitHub Actions workflow to test rendering and download artifacts.
- Architecture, research, roadmap, and OAuth setup docs.

## First proof
1. Open Actions and run **Build FactVerse sample** manually.
2. Download the `factverse-sample` artifact and inspect the MP4, thumbnail, and metadata.
3. Configure Google OAuth only after reading `docs/YOUTUBE_SETUP.md`.
4. Test an unlisted upload and verify it in YouTube Studio.
5. Enable a daily schedule only after repeated successful runs and confirming current runner limits.

## Milestones
1. Foundation and safety checks.
2. Render one sample and validate artifacts.
3. Verify OAuth upload.
4. Test scheduled reliability over several days.
5. Enable one post/day; consider two only after stable tests.
6. Add analytics-based recommendations and a separate advanced motion-control engine.

See `docs/ROADMAP.md`, `docs/ARCHITECTURE.md`, `docs/RESEARCH.md`, and `docs/YOUTUBE_SETUP.md`.

**Status:** source files have been committed, but runtime tests and an actual YouTube upload have not yet been verified. Do not treat the system as production-ready until those gates pass.