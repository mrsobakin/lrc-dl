from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, Self
from pathlib import Path
import mutagen


@dataclass
class Song:
    title: str
    artist: str
    album: Optional[str] = None
    duration: Optional[int] = None

    @classmethod
    def from_file(cls, path: Path) -> Self:
        metadata = mutagen.File(path, easy=True)

        if (
            ("title" not in metadata) or
            ("artist" not in metadata and "albumartist" not in metadata)
        ):
            raise RuntimeError("Song is missing title or artist name")

        title = ", ".join(metadata.get("title"))

        if "albumartist" in metadata:
            artist = ", ".join(metadata.get("albumartist"))
        else:
            artist = ", ".join(metadata.get("artist"))

        album = metadata.get("album")
        if album:
            album = ", ".join(album)

        duration = metadata.info.length

        return cls(title=title, artist=artist, album=album, duration=duration)


class AbstractProvider(ABC):
    name: str = ""
    @abstractmethod
    def fetch_lyrics(self, song: Song) -> Optional[str]:
        pass
