# YouTube upload setup

Uploads are disabled by default and require a channel you control.

1. In Google Cloud Console, create/select a project and enable YouTube Data API v3.
2. Configure the OAuth consent screen and create an OAuth client for testing.
3. Keep the downloaded client JSON private. Do not commit it or paste it into chat.
4. For a manual test, place it in the runtime as client_secret.json; the starter's local OAuth flow requires a browser-capable environment.
5. CI upload requires a carefully configured encrypted refresh-token flow; do not store tokens in source or plain repository variables.
6. First upload as unlisted and verify it in YouTube Studio.

YouTube quota and policy restrictions apply. The current starter does not authorize your account or upload anything automatically.