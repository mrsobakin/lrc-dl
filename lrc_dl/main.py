import argparse
from pathlib import Path

from lrc_dl.config import LyricsDlConfig
from lrc_dl.logger import DefaultLogger
from lrc_dl import LyricsDl


DEFAULT_EXTENSIONS = ["flac", "alac", "mp3", "m4a", "mp4", "aac", "wav", "opus", "ogg"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="Path to the song file or directory")
    parser.add_argument("-c", "--config", type=Path, help="Config file for lrc-dl")
    parser.add_argument("-e", "--extensions", type=str, help="Music files extensions, separated by a comma. For example: wav,flac,mp3")
    parser.add_argument("-f", "--force-override", action="store_true", help="Force override .lrc file, if it already exists")
    return parser.parse_args()


def main():
    args = parse_args()
    logger = DefaultLogger()

    if args.config:
        config = LyricsDlConfig.from_file(args.config)
    else:
        config = LyricsDlConfig.default()

    lrc_dl = LyricsDl(config=config, logger=logger)

    if args.path.is_dir():
        if not args.extensions:
            extensions = DEFAULT_EXTENSIONS
        else:
            extensions = args.extensions.split(",")

        lrc_dl.process_directory(args.path, extensions, args.force_override)
    else:
        lrc_dl.process_file(args.path, args.force_override)
