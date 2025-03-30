import time
import traceback
from pathlib import Path
from typing import Optional

# Initialize classes from lrc_dl/providers
import lrc_dl.providers as _
from lrc_dl.core import Song
from lrc_dl.registry import Registry
from lrc_dl.config import LyricsDlConfig
from lrc_dl.logger import DefaultLogger, AbstractLogger


class LyricsDl:
    logger: AbstractLogger

    def __init__(self, config: LyricsDlConfig = LyricsDlConfig(), logger: AbstractLogger = DefaultLogger()):
        self.config = config
        self.logger = logger

        providers_classes = Registry.get_synced_providers()

        self.providers = []

        for name in config.order:
            Provider = providers_classes.get(name)

            if not Provider:
                continue

            provider_config = config.providers_configs.get(name, {})

            try:
                provider = Provider(**provider_config)
            except TypeError as e:
                self.logger.error(f"[lrc-dl] {e}")
                continue

            self.providers.append(provider)

    def fetch_lyrics(self, song: Song) -> Optional[str]:
        self.logger.info(f"[lrc-dl] Fetching lyrics for \"{song.artist} - {song.title}\"")
        for provider in self.providers:
            self.logger.info(f"[{provider.name}] Fetching lyrics...")

            try:
                lyrics = provider.fetch_lyrics(song)
            except Exception as e:
                lyrics = None
                self.logger.error(f"[{provider.name}] Got exception while fetching lyrics! ({type(e).__name__}: {e})")
                self.logger.debug(f"[{provider.name}] {traceback.format_exc()}")

            if lyrics:
                self.logger.info(f"[{provider.name}] Found lyrics!")

                if self.config.prepend_header:
                    lyrics = f"[re:lrc-dl:{provider.name}]\n\n{lyrics}"

                return lyrics

            self.logger.info(f"[{provider.name}] No lyrics were found!")

        return None

    def process_file(self, path: Path, force: bool = False) -> bool:
        lyrics_path = path.with_suffix(".lrc")

        if lyrics_path.exists() and not force:
            self.logger.error("[lrc-dl] Lyrics file already exists!")
            return False

        # TODO handle errors
        try:
            song = Song.from_file(path)
        except Exception as e:
            self.logger.error(f"[lrc-dl] {path}: {e}")
            return False

        lyrics = self.fetch_lyrics(song)

        if not lyrics:
            self.logger.error("[lrc-dl] No lyrics were found!")
            return True

        with open(lyrics_path, "w") as f:
            f.write(lyrics)

        return True

    def process_directory(self, path: Path, extensions: list[str], force: bool = False) -> None:
        delay_next = False

        for file_path in path.rglob("*"):
            if delay_next and self.config.delay is not None:
                self.logger.info(f"[lrc-dl] Sleeping for {self.config.delay:.2f}s...")
                time.sleep(self.config.delay)

            if file_path.suffix[1:] not in extensions:
                continue

            delay_next = self.process_file(file_path, force)
