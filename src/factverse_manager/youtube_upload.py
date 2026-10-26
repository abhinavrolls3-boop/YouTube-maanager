"""Optional YouTube Data API upload; disabled unless explicitly enabled."""
from pathlib import Path
import os

def upload_video(video_path: str, metadata: dict, client_secret_file: str = "client_secret.json") -> str:
    if os.getenv("ENABLE_UPLOAD", "false").lower() != "true":
        raise RuntimeError("Upload disabled. Enable only after OAuth setup and review.")
    if not Path(video_path).is_file(): raise FileNotFoundError(video_path)
    if not Path(client_secret_file).is_file():
        raise FileNotFoundError("Missing OAuth client JSON. Follow docs/YOUTUBE_SETUP.md; never commit credentials.")
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    flow=InstalledAppFlow.from_client_secrets_file(client_secret_file,["https://www.googleapis.com/auth/youtube.upload"])
    credentials=flow.run_local_server(port=0)
    youtube=build("youtube","v3",credentials=credentials)
    body={"snippet":{"title":metadata["title"][:100],"description":metadata["description"][:5000],"tags":metadata.get("tags",[])[:500],"categoryId":metadata.get("categoryId","27")},"status":{"privacyStatus":os.getenv("UPLOAD_PRIVACY","unlisted"),"selfDeclaredMadeForKids":False}}
    response=youtube.videos().insert(part="snippet,status",body=body,media_body=MediaFileUpload(video_path,mimetype="video/mp4",resumable=True)).execute()
    return response["id"]