# YouTube / YouTube Music Playlist to MP3 Downloader

Download entire playlists from **YouTube** or **YouTube Music** as high-quality **MP3 (320 kbps)** with automatic fallback and proper metadata.

This script uses **yt-dlp** and **ffmpeg** to extract the best available audio, convert it to MP3, embed cover art, and write metadata — with zero prompts or interruptions.

---

## Features

-  **MP3 only**, converted at **320 kbps**
-  Works with **YouTube** and **YouTube Music** playlists
-  Smart fallback: **m4a → opus → bestaudio → best**
-  Embeds thumbnail as cover art
-  Writes metadata (artist, album, track #, etc.)
-  Saves progress using `.archive.txt`
-  Organizes output by playlist and track index
-  Supports cookies (cookies.txt or browser profile)
-  Runs without any pauses or confirmations

---

## Requirements

### Install yt-dlp
```bash
pip install -U yt-dlp
```

### Install ffmpeg
**macOS**
```bash
brew install ffmpeg
```

---

## Usage

### Basic command
```bash
python3 d.py "PLAYLIST_URL"
```

### Example (your playlist)
```bash
python3 d.py "https://music.youtube.com/playlist?list="
```

**Output structure:**
```
downloads/
   Playlist Name/
      001 - Track Title [videoid].mp3
      002 - Track Title [videoid].mp3
   .archive.txt
```

---

## Custom Output Directory
```bash
python3 d.py "PLAYLIST_URL" -o mymusic
```

---

## Using Cookies (optional)

### Using cookies.txt
```bash
python3 d.py "PLAYLIST_URL" -c cookies.txt
```

### Auto-load browser cookies
```bash
python3 d.py "PLAYLIST_URL" -b chrome
```

Supports: `chrome`, `firefox`, `brave`, `edge`, `safari`.

---

## Script Behavior

- Downloads **audio only**
- Converts to **MP3 (320 kbps)**
- Embeds playlist thumbnail as cover art
- Writes metadata via FFmpeg
- Skips files already downloaded (via `.archive.txt`)
- Uses YouTube’s `android_music` → `android` client fallback

---

## Project Structure
```
d.py
README.md
downloads/
    ...
```

---

## Troubleshooting

### ffmpeg not found
Install ffmpeg and ensure it’s available in PATH.

### Age-restricted or region-locked tracks missing
Use:
```bash
-c cookies.txt
```
or:
```bash
-b chrome
```

### Playlist name contains unusual characters
yt-dlp automatically sanitizes filenames; rename manually if needed.

---

## License
Free to use. Modify as needed.
