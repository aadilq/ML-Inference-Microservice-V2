import yt_dlp
import tempfile

def download_video(video_url: str):
    temp_dir = tempfile.mkdtemp()
    print(f"Temporary directory created at: {temp_dir}")

    ydp_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": f"{temp_dir}/source.mp4",
        "merge_output_format": "mp4",
    }

    with yt_dlp.YoutubeDL(ydp_opts) as ydl:
        ydl.download([video_url])
    return f"{temp_dir}/source.mp4"

