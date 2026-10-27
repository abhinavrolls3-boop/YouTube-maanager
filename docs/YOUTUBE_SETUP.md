# YouTube upload setup

Uploads are optional and disabled by default. Use a channel you control.

1. In Google Cloud Console, create/select a project and enable YouTube Data API v3.
2. Configure the OAuth consent screen and create an OAuth client.
3. Keep the downloaded client JSON private. Never commit it or paste it into chat.
4. Complete OAuth authorization locally using the upload scope and keep the authorized-user credentials private.
5. The scheduled GitHub Actions workflow only prepares videos and review artifacts. It does not upload or publish videos.
6. Before any upload, open the actual video, verify every claim against relevant sources, check originality and asset rights, review title/thumbnail/description, and consider whether altered/synthetic-content disclosure is required.
7. Generate a per-claim evidence register with `PYTHONPATH=src python -m factverse_manager.cli evidence output/<topic>_metadata.json`. For every claim, fill in an evidence URL, a supporting quote/location, and mark `assessment` as `supported` only after checking the source. Then run `PYTHONPATH=src python -m factverse_manager.cli evidence-approve output/<topic>_evidence.json --confirm-each-claim --confirm-sources`. This records evidence approval in the metadata.
8. Generate the separate review checklist with `PYTHONPATH=src python -m factverse_manager.cli review output/<topic>_metadata.json`. After inspecting the actual video, originality, asset rights, metadata, and audience suitability, record approval with `PYTHONPATH=src python -m factverse_manager.cli approve output/<topic>_metadata.json --confirm-human-review --confirm-originality`.
9. Only then use the upload CLI with valid OAuth credentials. The uploader allows only private or unlisted visibility, requires source URLs, evidence approval, both review flags, blocks matching video hashes in the local history, and defaults to one upload per UTC day.

The upload history is local/best-effort and can be lost, so it is not a permanent duplicate-proof database. YouTube API quota, OAuth verification restrictions, channel permissions, monetization policies, and community guidelines still apply. These checks cannot guarantee that YouTube will never restrict a video or channel.

10. Set `YOUTUBE_MADE_FOR_KIDS=true` or `YOUTUBE_MADE_FOR_KIDS=false` in the upload environment only after choosing the correct audience setting for the specific content/channel. Upload is blocked if this declaration is missing or invalid. The uploader also rejects empty/non-MP4 files, invalid source URLs, empty descriptions, and titles outside 1–100 characters.
