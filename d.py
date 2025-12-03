#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("yt-dlp is not installed. Install with: pip install -U yt-dlp")
    sys.exit(1)

def build_ydl_opts(playlist_url: str, outdir: Path, browser: str, cookies_file: str | None):
    outdir.mkdir(parents=True, exist_ok=True)
    outtmpl = str(outdir / "%(playlist_title)s/%(playlist_index)03d - %(title)s [%(id)s].%(ext)s")
    archive_path = str(outdir / ".archive.txt")

    format_selector = (
        "bestaudio[ext=m4a]/"
        "bestaudio[ext=opus]/"
        "bestaudio/"
        "best"
    )

    opts = {
        "format": format_selector,
        "outtmpl": {"default": outtmpl},
        "download_archive": archive_path,
        "ignoreerrors": "only_download",
        "continuedl": True,
        "retries": 10,
        "fragment_retries": 10,
        "concurrent_fragments": 5,
        "sleep_requests": 0,
        "retry_sleep": 0,
        "noprogress": False,
        "progress_with_newline": True,
        "geo_bypass": True,
        "writethumbnail": True,
        "writesubtitles": False,
        "writeautomaticsub": False,
        "embedsubtitles": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320"
            },
            {"key": "FFmpegMetadata"},
            {"key": "EmbedThumbnail"},
        ],
        "extractor_args": {
            "youtube": {
                "player_client": ["android_music", "android"]
            }
        },
    }

    if cookies_file:
        opts["cookiefile"] = cookies_file
    else:
        browser = (browser or "none").strip().lower()
        if browser in {"chrome", "firefox"}:
            opts["cookiesfrombrowser"] = (browser,)

    return opts

def main():
    parser = argparse.ArgumentParser(description="Download YouTube/YouTube Music playlist as MP3 (320kbps).")
    parser.add_argument("playlist_url", help="YouTube / YouTube Music playlist URL")
    parser.add_argument("-o", "--outdir", default="downloads", help="Output directory")
    parser.add_argument("-b", "--browser", choices=["none", "safari", "chrome", "firefox", "brave", "edge"], default="none")
    parser.add_argument("-c", "--cookies", default=None)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    ydl_opts = build_ydl_opts(args.playlist_url, outdir, args.browser, args.cookies)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ret = ydl.download([args.playlist_url])
        if ret != 0:
            sys.exit(ret)

    print("Done.")

if __name__ == "__main__":
    main()
