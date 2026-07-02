from yt_dlp import YoutubeDL


def yt_dlp_downloader(url):
    ydl_opts = {
    "outtmpl": "temp/%(id)s.%(ext)s",
    "format": "mp4/best",
    "cookiesfrombrowser": ("firefox",),
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    video_id = url.split("/")[-2]
    return f"temp/{video_id}.mp4"