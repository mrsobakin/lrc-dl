from typing import Optional, Dict
from contextlib import redirect_stdout
import subprocess
import io
import urllib
import unittest.mock

from yt_dlp import YoutubeDL

from lrc_dl.core import Song, AbstractProvider
from lrc_dl.registry import lyrics_provider
from lrc_dl import utils


@lyrics_provider
class Youtube(AbstractProvider):
    name = "youtube"

    def _craft_search_link(self, song: Song) -> str:
        query = f"{song.artist} - {song.title}"
        query = urllib.parse.quote(query)
        # sp=... means search only videos with subtitles
        url = f"https://www.youtube.com/results?search_query={query}&sp=EgIoAQ%253D%253D"
        return url

    def _download_subtitles(self, video_id: str) -> str:
        # buffer = io.BytesIO()
        buffer = io.StringIO()

        # A dirty monkey patch; youtube-dl does not
        # support "-" filename for subtitles, so we
        # just force it to use it here.
        with unittest.mock.patch("yt_dlp.YoutubeDL.subtitles_filename", new=lambda *_: "-"):
            with redirect_stdout(buffer):
                with YoutubeDL({"writesubtitles": True, "skip_download": True, "subtitlesformat": "srt/vtt/best", 'logtostderr': True}) as ydl:
                    ydl.download(video_id)

        return buffer.getvalue()

    def _subtitles_to_lyrics(self, subtitles: str) -> str:
        # "-fflags +bitexact" prevents ffmpeg from
        # writing metadata to .lrc file
        # TODO: use `with` statement
        process = subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i", "-", "-f", "lrc", "-fflags", "+bitexact", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        if not process.stdin or not process.stdout:
            return ""

        process.stdin.write(subtitles.encode())
        process.stdin.close()
        process.wait()
        return process.stdout.read().decode()[1:]

    def fetch_lyrics(self, song: Song) -> Optional[str]:
        search_link = self._craft_search_link(song)
        with YoutubeDL({"extract_flat": True, "playlistend": 10}) as ydl:
            videos = ydl.extract_info(search_link)["entries"]

        if song.duration:
            def match_duration(video: Dict) -> bool:
                return utils.threshold_equal(video["duration"], song.duration, 2)
            videos = filter(match_duration, videos)

        def match_title(video: Dict) -> bool:
            return True
        videos = filter(match_title, videos)

        video = utils.next_or_none(videos)

        if not video:
            return None

        subtitles = self._download_subtitles(video["id"])
        lyrics = self._subtitles_to_lyrics(subtitles)

        if lyrics != "":
            return lyrics

        return None
