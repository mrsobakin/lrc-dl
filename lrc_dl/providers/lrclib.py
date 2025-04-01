from typing import Optional
import httpx

from lrc_dl.core import Song, AbstractProvider
from lrc_dl.registry import lyrics_provider

@lyrics_provider
class LrcLib(AbstractProvider):
    name = "lrclib"

    def fetch_lyrics(self, song: Song, with_album = True) -> Optional[str]:
        r = httpx.get("https://lrclib.net/api/get", params={
            'track_name': song.title,
            'artist_name': song.artist,
            'album_name': song.album if with_album else None,
        }).json()

        return r.get('syncedLyrics') or r.get('plainLyrics') or (self.fetch_lyrics(song, False) if with_album else None)
