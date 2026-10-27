# Daily automation

## What it does
The scheduled GitHub Actions workflow is configured for 03:30 UTC (09:00 India time), subject to GitHub providing a runner. At the end of a run it writes a phone-friendly GitHub Actions summary with per-topic status and the artifact name, including when earlier steps fail. It installs the free local espeak-ng speech engine, runs tests, prepares a video package with attempted English voice narration and a review report, optionally attempts an AI-assisted draft, uploads run artifacts for seven days, and can send a completion webhook if configured. It does not publish videos automatically. A manual run can prepare 1–3 topics.

## Source and fact review
Curated topics include source URLs in metadata. Scheduled batches now check whether those URLs respond and save a per-topic `*_source_check.json` report included in the SHA-256 artifact manifest. The check uses a small GET fallback for sites that reject HEAD requests. You can also run `PYTHONPATH=src python -m factverse_manager.cli sources output/<topic>_metadata.json` manually. Network reachability is not proof that a source supports a claim; a human must open each source and verify its content. The package checker flags missing source URLs, and every batch writes a SHA-256 artifact manifest. The workflow verifies these hashes before optional upload. A human must open the sources and verify each claim. AI-generated drafts currently do not include independently researched citations and should not be automatically published.

## Optional AI drafting
To use the configured OpenAI-compatible OmniRoute route, add repository Actions secret `OMNIROUTE_API_KEY`, repository variables `OMNIROUTE_BASE_URL` and `OMNIROUTE_MODEL`, and set `ENABLE_AI_DRAFTS=true`. The route may incur charges or have quotas; verify your route and budget first. If drafting fails, the job falls back to a curated offline fact. AI output is unverified and needs independent fact-checking. The current tool does not perform live source research.

## Upload safety (manual approval required)

Unattended publishing is intentionally disabled. Every generated metadata file starts with `human_review_status: needs_review` and `originality_check_status: needs_review`. Before uploading, a person must inspect the actual video, confirm each factual claim against relevant sources, check that narration/visuals are original or properly licensed, and verify audience suitability. Only then may the metadata be manually changed to `human_review_status: approved` and `originality_check_status: passed`. These fields are an explicit human checklist, not an automated proof of originality.

The uploader accepts only `private` or `unlisted` visibility, requires source URLs and both approval fields, blocks exact video-file duplicates recorded in its local history, and defaults to at most **one upload per UTC day** (`MAX_UPLOADS_PER_DAY`). The history is local/best-effort, not a durable global database, so it cannot guarantee cross-run duplicate prevention if history is lost. Review the final video in YouTube Studio before any public release.

## Running without opening the app

The workflow runs on GitHub-hosted runners, so the ChatGPT app and your phone do not need to remain open. It produces drafts on schedule, then stores an artifact temporarily for seven days. GitHub does not guarantee exact start times or every scheduled run. Without a configured webhook, there is no separate push notification; the run summary is visible on GitHub Actions. This workflow does not publish to YouTube automatically, and a person must still review the video and evidence before uploading.

## Optional notifications
Add a trusted webhook URL as Actions secret `NOTIFY_WEBHOOK_URL`. Only operational counts are sent. If it is absent, the workflow continues without sending a notification.

## Hard limits
- GitHub Actions schedules are best-effort and free usage is subject to account/repository quotas. This is not a guaranteed always-on server.
- The renderer creates simple motion graphics with optional local robotic English narration; it does not provide licensed music, character animation, or motion-control video.
- The built-in facts are a starter library, not live research. A URL check cannot verify factual accuracy or source relevance.
- Analytics requires a CSV exported by you; it does not connect to channel or competitor analytics on its own.
- No free AI quota, daily runtime, views, or earnings are guaranteed.


## Review workflow

Every batch creates a `*_review.json` checklist beside the metadata and includes it in the artifact manifest. The checklist starts with every item unchecked. Review factual support, originality, asset rights, metadata accuracy, audience suitability, and whether synthetic-content disclosure is required. After you personally complete the review, run `PYTHONPATH=src python -m factverse_manager.cli approve output/<topic>_metadata.json --confirm-human-review --confirm-originality`. This records an approval timestamp. Do not run the command unless you have actually performed both reviews.
