from pathlib import Path
import imageio_ffmpeg
from yt_dlp import YoutubeDL

UPLOAD_DIR =Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def download_youtube_video(url):
    
    ydl_opts = {
        "outtmpl": str(UPLOAD_DIR / "%(title)s.%(ext)s"),
        "format": "mp4",
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_path = ydl.prepare_filename(info)
        
    return video_path
