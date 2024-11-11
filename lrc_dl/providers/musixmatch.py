from typing import Optional
import httpx

from lrc_dl.core import Song, AbstractProvider
from lrc_dl.registry import lyrics_provider


@lyrics_provider
class Musixmatch(AbstractProvider):
    name = "musixmatch"

    def __init__(self, token: str) -> None:
        self.token = token

    def fetch_lyrics(self, song: Song) -> Optional[str]:
        response = httpx.get("https://apic-desktop.musixmatch.com/ws/1.1/macro.subtitles.get", params={
            "format": "json",
            "namespace": "lyrics_synched",
            "part": "lyrics_crowd,user,lyrics_verified_by",
            "user_language": "en",
            "f_subtitle_length_max_deviation": 1,
            "subtitle_format": "lrc",
            "app_id": "web-desktop-app-v1.0",
            "usertoken": self.token,

            "q_artist": song.artist,
            "q_track": song.title,
            "q_album": song.album,
        }, follow_redirects=True).json()

        response = response["message"]["body"]["macro_calls"]["track.subtitles.get"]["message"]["body"]

        if not response:
            return None

        return response["subtitle_list"][0]["subtitle"]["subtitle_body"]
