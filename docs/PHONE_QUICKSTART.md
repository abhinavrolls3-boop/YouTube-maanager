# Phone-only quick start

This repository can prepare draft video packages on GitHub-hosted runners. You do not need Termux, a laptop, or the ChatGPT app left open.

## Automatic schedule
- The scheduled workflow targets 09:00 India time daily.
- GitHub schedule timing and free runner availability are best-effort, not guaranteed.
- Automatic YouTube uploading is intentionally disabled. Generated videos are drafts for review.

## Check a run from your phone
1. Open the [FactVerse daily workflow](https://github.com/abhinavrolls3-boop/YouTube-maanager/actions/workflows/daily-automation.yml).
2. Open the latest run and read its **Summary** first.
3. Under **Artifacts**, open `factverse-daily-<run-id>` to retrieve the generated files. Start with `index.html` for a phone-friendly per-topic dashboard; it links to the video, thumbnail, captions, metadata, source report, and review files. The artifact expires after 7 days.
4. If a topic says `needs_attention`, read its warning and source-check report before considering the video.

## Run it manually
1. Open the same workflow link.
2. Tap **Run workflow**.
3. Choose 1, 2, or 3 topics, then start the workflow.
4. Wait for the run to finish and inspect the Summary and Artifacts sections.

If **Run workflow** is unavailable, check that you are signed in to GitHub and have permission to run Actions for this repository.

## What is not automatic yet
- No automatic public upload or publishing.
- No guaranteed push notification unless a trusted `NOTIFY_WEBHOOK_URL` secret is configured.
- The source checker verifies URL reachability only; it cannot prove the source supports the claim.
- Human claim review, originality/rights review, and audience-suitability checks are required before an upload.
- The free workflow is not a permanent always-on server; quotas or runner delays may apply.
