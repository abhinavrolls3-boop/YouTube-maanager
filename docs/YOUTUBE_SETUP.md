# YouTube upload setup

Uploads are disabled by default and require a channel you control.

1. In Google Cloud Console, create/select a project and enable YouTube Data API v3.
2. Configure the OAuth consent screen and create an OAuth client.
3. Keep the downloaded client JSON private. Do not commit it or paste it into chat.
4. A local browser-capable OAuth flow can produce authorized-user credentials with a refresh token. Ensure the credentials include the YouTube upload scope. Do not share the token publicly.
5. For unattended GitHub Actions uploads, store the complete authorized-user credential JSON as the encrypted repository Actions secret "YOUTUBE_TOKEN_JSON". Do not put it in a repository variable or source file.
6. Only after confirming the secret belongs to the correct channel, set repository variables "ENABLE_YOUTUBE_UPLOAD=true" and "APPROVE_AUTOMATED_UNLISTED_UPLOAD=true".
7. The daily workflow will upload videos as **unlisted**. It does not make videos public. Verify the result in YouTube Studio before changing visibility.

The workflow uses a best-effort Actions cache for upload hashes; cache eviction can remove this history. Do not rely on it as a permanent duplicate-proof database. YouTube quota, API policies, OAuth verification restrictions, and account permissions still apply. No upload is made unless the opt-in variables and credentials are configured.
