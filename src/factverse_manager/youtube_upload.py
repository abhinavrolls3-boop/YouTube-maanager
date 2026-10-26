"""Optional YouTube Data API upload; disabled unless explicitly enabled."""
from pathlib import Path
import json
import os
from .state import file_sha256, has_uploaded_hash, record_upload

def _credentials(client_secret_file):
    token_json = os.getenv("YOUTUBE_TOKEN_JSON", "").strip()
    if token_json:
        from google.oauth2.credentials import Credentials
        info = json.loads(token_json)
        return Credentials.from_authorized_user_info(info, ["https://www.googleapis.com/auth/youtube.upload"])
    if not Path(client_secret_file).is_file():
        raise FileNotFoundError("Missing OAuth client JSON or YOUTUBE_TOKEN_JSON secret. Follow docs/YOUTUBE_SETUP.md; never commit credentials.")
    from google_auth_oauthlib.flow import InstalledAppFlow
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, ["https://www.googleapis.com/auth/youtube.upload"])
    return flow.run_local_server(port=0)

def upload_video(video_path: str, metadata: dict, client_secret_file: str = "client_secret.json") -> str:
    if os.getenv("ENABLE_UPLOAD", "false").lower() != "true":
        raise RuntimeError("Upload disabled. Set ENABLE_UPLOAD=true only after explicit channel authorization.")
    video = Path(video_path)
    if not video.is_file():
        raise FileNotFoundError(video_path)
    privacy = os.getenv("UPLOAD_PRIVACY", "unlisted").strip().lower()
    if privacy not in {"unlisted", "private"}:
        raise RuntimeError("Safety guard: this automation permits only unlisted or private uploads, never public uploads.")
    sources = metadata.get("source_urls", [])
    if not isinstance(sources, list) or not sources:
        raise RuntimeError("Upload blocked: metadata must include source_urls for human verification.")
    if metadata.get("human_review_status") != "approved":
        raise RuntimeError("Upload blocked: set human_review_status to approved only after checking factual accuracy, source relevance, originality, copyright, and audience suitability.")
    if metadata.get("originality_check_status") != "passed":
        raise RuntimeError("Upload blocked: originality_check_status must be passed after reviewing the video for reused or repetitive content.")
    digest = file_sha256(video)
    history_path = os.getenv("UPLOAD_HISTORY", "output/upload_history.json")
    if has_uploaded_hash(digest, history_path):
        raise RuntimeError("Duplicate upload blocked: this exact video file is already recorded in the local upload history.")
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    credentials = _credentials(client_secret_file)
    youtube = build("youtube", "v3", credentials=credentials)
    body = {
        "snippet": {
            "title": metadata["title"][:100],
            "description": metadata["description"][:5000],
            "tags": metadata.get("tags", [])[:500],
            "categoryId": metadata.get("categoryId", "27"),
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }
    response = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(str(video), mimetype="video/mp4", resumable=True),
    ).execute()
    video_id = response["id"]
    record_upload(digest, video_id, metadata.get("title", ""), history_path)
    return video_id
