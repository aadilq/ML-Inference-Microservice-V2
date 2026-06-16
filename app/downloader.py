import yt_dlp
import tempfile
import shutil

def download_video(video_url: str):
    temp_dir = tempfile.mkdtemp()
    print(f"Temporary directory created at: {temp_dir}")

    ydp_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": f"{temp_dir}/source.mp4",
        "merge_output_format": "mp4",
    }
    try:
        with yt_dlp.YoutubeDL(ydp_opts) as ydl:
            ydl.download([video_url])
        return f"{temp_dir}/source.mp4"
    except yt_dlp.utils.DownloadError as e:
        shutil.rmtree(temp_dir)
        raise RuntimeError(f"video cannot be downloaded: {e}")



