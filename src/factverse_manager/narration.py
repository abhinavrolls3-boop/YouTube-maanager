"""Optional local text-to-speech. Uses system espeak-ng; no API key or paid service."""
import shutil
import subprocess
import tempfile
from pathlib import Path
import imageio_ffmpeg

def add_narration(video_path, text, voice="en-us", speed=155, timeout=45):
    video = Path(video_path)
    if not video.is_file():
        raise FileNotFoundError(str(video))
    if not text or not text.strip():
        raise ValueError("Narration text cannot be empty.")
    espeak = shutil.which("espeak-ng") or shutil.which("espeak")
    if not espeak:
        raise RuntimeError("Local speech engine is not installed. Install espeak-ng or disable ENABLE_NARRATION.")
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    with tempfile.TemporaryDirectory(prefix="factverse-tts-") as tmp:
        wav = Path(tmp) / "narration.wav"
        muxed = Path(tmp) / "narrated.mp4"
        subprocess.run([espeak, "-v", voice, "-s", str(speed), "-w", str(wav), text],
                       check=True, capture_output=True, timeout=timeout)
        subprocess.run([ffmpeg, "-y", "-i", str(video), "-i", str(wav),
                        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "96k", "-af", "apad", "-shortest",
                        str(muxed)], check=True, capture_output=True, timeout=timeout)
        if not muxed.is_file() or muxed.stat().st_size == 0:
            raise RuntimeError("FFmpeg did not produce a narrated video.")
        video.write_bytes(muxed.read_bytes())
    return str(video)
