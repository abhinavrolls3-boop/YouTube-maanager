# YouTube upload setup

Uploads are optional and disabled by default. Use a channel you control.

1. In Google Cloud Console, create/select a project and enable YouTube Data API v3.
2. Configure the OAuth consent screen and create an OAuth client.
3. Keep the downloaded client JSON private. Never commit it or paste it into chat.
4. Complete OAuth authorization locally using the upload scope and keep the authorized-user credentials private.
5. The scheduled GitHub Actions workflow only prepares videos and review artifacts. It does not upload or publish videos.
6. Before any upload, open the actual video, verify every claim against relevant sources, check originality and asset rights, review title/thumbnail/description, and consider whether altered/synthetic-content disclosure is required.
7. Generate a checklist with `PYTHONPATH=src python -m factverse_manager.cli review output/<topic>_metadata.json`. After completing the checks yourself, explicitly record approval with `PYTHONPATH=src python -m factverse_manager.cli approve output/<topic>_metadata.json --confirm-human-review --confirm-originality`.
8. Only then use the upload CLI with valid OAuth credentials. The uploader allows only private or unlisted visibility, requires source URLs and both approval flags, blocks matching video hashes in the local history, and defaults to one upload per UTC day.

The upload history is local/best-effort and can be lost, so it is not a permanent duplicate-proof database. YouTube API quota, OAuth verification restrictions, channel permissions, monetization policies, and community guidelines still apply. These checks cannot guarantee that YouTube will never restrict a video or channel.
