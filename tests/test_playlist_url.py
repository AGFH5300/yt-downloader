"""CLI input tests with an in-memory yt_dlp; no network or media downloads."""

import contextlib
import importlib.util
import io
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch


DOWNLOADS = []


class FakeYoutubeDL:
    def __init__(self, _options):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def download(self, urls):
        DOWNLOADS.append(list(urls))
        return 0


fake_ydl = types.ModuleType("yt_dlp")
fake_ydl.YoutubeDL = FakeYoutubeDL
with patch.dict(sys.modules, {"yt_dlp": fake_ydl}):
    spec = importlib.util.spec_from_file_location("yt_cli_under_test", Path(__file__).parents[1] / "d.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def run_cli(url):
    DOWNLOADS.clear()
    with tempfile.TemporaryDirectory(prefix="yt-cli-test-") as directory:
        outdir = Path(directory) / "output"
        argv = ["d.py", url, "--outdir", str(outdir)]
        with patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                module.main()
                status = 0
            except SystemExit as exc:
                status = exc.code
        return status, list(DOWNLOADS), outdir.exists()


class PlaylistURLGuard(unittest.TestCase):
    def test_valid_youtube_playlist(self):
        url = "https://www.youtube.com/playlist?list=PLsafe_ABC-01"
        self.assertEqual(run_cli(url), (0, [[url]], True))

    def test_valid_music_playlist(self):
        url = "https://music.youtube.com/playlist?list=OLAK5uy_safe-1"
        self.assertEqual(run_cli(url), (0, [[url]], True))

    def test_valid_watch_link_with_playlist_id(self):
        url = "https://youtube.com/watch?v=example&list=PLsafe_ABC-01"
        self.assertEqual(run_cli(url), (0, [[url]], True))

    def test_untrusted_or_malformed_target_never_reaches_downloader_or_filesystem(self):
        invalid = [
            "http://127.0.0.1:8000/playlist?list=PLsafe_ABC-01",
            "http://169.254.169.254/latest/meta-data/?list=PLsafe_ABC-01",
            "file:///etc/passwd?list=PLsafe_ABC-01",
            "ftp://www.youtube.com/playlist?list=PLsafe_ABC-01",
            "http://www.youtube.com/playlist?list=PLsafe_ABC-01",
            "https://www.youtube.com.evil.invalid/playlist?list=PLsafe_ABC-01",
            "https://user:password@www.youtube.com/playlist?list=PLsafe_ABC-01",
            "https://www.youtube.com:444/playlist?list=PLsafe_ABC-01",
            "https://www.youtube.com/redirect?list=PLsafe_ABC-01",
            "https://www.youtube.com/playlist",
            "https://www.youtube.com/playlist?list=PLsafe_ABC-01&list=PLother_123",
            "https://www.youtube.com/playlist?list=%2Fetc%2Fpasswd",
            "https://www.youtube.com/playlist?list=PLsafe_ABC-01\nX-Evil: yes",
            "https://www.youtube.com/playlist?list=PLsafe_ABC-01#",
            "https://www.youtube.com/playlist?list=PLsafe_ABC-01#section",
            "https://www.youtube.com/playlist?list=PLsafe_ABC-01&" + "&".join(f"q{i}=1" for i in range(33)),
            "https://www.youtube.com/playlist?list=" + "A" * 2050,
        ]
        for url in invalid:
            with self.subTest(url=url):
                self.assertEqual(run_cli(url), (2, [], False))


if __name__ == "__main__":
    unittest.main()
