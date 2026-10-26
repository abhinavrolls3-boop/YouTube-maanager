# Daily automation

## What it does
The scheduled GitHub Actions workflow runs at 03:30 UTC (09:00 India time) when GitHub provides a runner. It runs tests, prepares one offline fact video, thumbnail, metadata and a machine-readable review report, then uploads them as an artifact for three days. A manual run can prepare 1–3 topics.

## Important limitations
- GitHub Actions schedule is best-effort, not a guaranteed always-on service. Free quotas and repository eligibility apply; scheduled workflows can be delayed or disabled by platform policy.
- The workflow does not publish to YouTube. It produces artifacts that must be reviewed. It cannot bypass YouTube OAuth or account permissions.
- The included library is a starter dataset, not live web research. Review claims and add credible source notes before publishing.
- Runner files are ephemeral. The local upload-history JSON does not persist between runs unless a private persistence mechanism is configured; do not assume cross-run duplicate prevention.
- Notifications are optional and require a webhook secret. Never paste secrets into source files or commit them.
- No guaranteed free AI quota, narration service, continuous background runtime, or earnings outcome.

## One-time activation
1. Confirm Actions are enabled in the repository.
2. Open the latest successful run and check its artifact.
3. If you want notifications, add a repository Actions secret named `NOTIFY_WEBHOOK_URL` for a trusted webhook endpoint; the current workflow does not send notifications unless explicitly configured.
4. To enable optional AI-assisted script drafts, set repository Actions secret `OMNIROUTE_API_KEY`, repository variables `OMNIROUTE_BASE_URL` (OpenAI-compatible API base URL) and `OMNIROUTE_MODEL`, then set `ENABLE_AI_DRAFTS` to `true`. The scheduled job will try a draft and fall back to the curated offline topic if the provider fails. These drafts are unverified and still require fact-checking. Provider quotas/costs depend on your OmniRoute account; do not enable this until you have confirmed the route is within your budget. Never commit keys.
