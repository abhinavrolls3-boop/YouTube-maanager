# Daily automation

## What it does
The scheduled GitHub Actions workflow runs at 03:30 UTC (09:00 India time) when GitHub provides a runner. It runs tests, prepares one video package and review report, optionally attempts an AI-assisted draft, uploads run artifacts for seven days, and can send a completion webhook if configured. A manual run can prepare 1–3 topics.

## Optional AI drafting
To use the configured OpenAI-compatible OmniRoute route, add repository Actions secret "OMNIROUTE_API_KEY", repository variables "OMNIROUTE_BASE_URL" and "OMNIROUTE_MODEL", and set "ENABLE_AI_DRAFTS=true". The route may incur charges or have quotas; verify your route and budget first. If drafting fails, the job falls back to a curated offline fact. AI output is unverified and needs independent fact-checking. The current tool does not perform live source research or generate audio.

## Optional unattended unlisted upload
Uploads are disabled unless BOTH repository variables "ENABLE_YOUTUBE_UPLOAD=true" and "APPROVE_AUTOMATED_UNLISTED_UPLOAD=true" are set. You must also add a valid authorized-user OAuth JSON as Actions secret "YOUTUBE_TOKEN_JSON". The credential must belong to a channel you control and include a refresh token with YouTube upload scope. Never paste it into chat or commit it. See docs/YOUTUBE_SETUP.md.

If explicitly enabled, the workflow uploads generated packages as **unlisted**, not public. It never automatically changes videos to public. The upload history is cached on a best-effort basis; GitHub may evict caches, so this is not a durable database or a perfect cross-run duplicate guarantee. Inspect uploads in YouTube Studio before making them public.

## Optional notifications
Add a trusted webhook URL as repository Actions secret "NOTIFY_WEBHOOK_URL". Only operational counts are sent. If it is absent, the workflow continues without sending a notification.

## Hard limits
- GitHub Actions schedules are best-effort and free usage is subject to account/repository quotas. This is not a guaranteed always-on server.
- The current renderer produces silent motion graphics; it does not synthesize voice, licensed music, character animation, or motion-control video.
- The built-in facts are a starter library, not live research. A file check cannot verify factual accuracy, copyright, or audience suitability.
- The analytics command summarizes CSV files you provide; it does not connect to channel or competitor analytics on its own.
- No free AI quota, daily runtime, views, or earnings are guaranteed.
