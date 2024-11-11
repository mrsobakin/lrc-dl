from typing import Optional, Iterable
from base64 import b64decode
import zlib
import re
from itertools import filterfalse, islice
from datetime import datetime

import httpx

from lrc_dl.core import Song, AbstractProvider
from lrc_dl.registry import lyrics_provider


KRC_ENCODE_KEY = [64, 71, 97, 119, 94, 50, 116, 71, 81, 54, 49, 45, 206, 210, 110, 105]

RE_KRC_JUNK = re.compile(r"^\[((id|ar|ti|by|hash|al|sign|qq|total|language):|offset:0\]|.*\](<.*>)?(Written by：|Lyrics by：|Composed by：|Producer：|作曲 :|作词 :)).*$")
RE_WORD_TIMING = re.compile(r"<-?\d+,-?\d+,-?\d+>")


def decode_krc(content: bytes) -> str:
    content = b64decode(content)

    buf = bytearray(len(content) - 4)
    for i in range(4, len(content)):
        buf[i - 4] = content[i] ^ KRC_ENCODE_KEY[(i - 4) % 16]

    return zlib.decompress(buf).decode('utf-8-sig')


def reformat_timings(lines: Iterable[str]) -> Iterable[str]:
    for line in lines:
        if not line.startswith("["):
            yield line
            continue

        raw_timings, text = line.split("]", 1)
        beginning, _ = map(int, raw_timings[1:].split(","))

        timing = datetime.fromtimestamp(beginning / 1000).strftime("%M:%S.%f")[:8]

        yield f"[{timing}]{text}"


@lyrics_provider
class Kugou(AbstractProvider):
    name = "kugou"

    def fetch_lyrics(self: AbstractProvider, song: Song) -> Optional[str]:
        keyword = f"{song.artist} - {song.title}"

        response = httpx.get("https://krcs.kugou.com/search", params={
            "ver": 1,
            "man": "yes",
            "client": "mobi",
            "keyword": keyword
        }).json()

        candidates = response["candidates"]

        if not candidates:
            return None

        id_, accesskey = candidates[0]["id"], candidates[0]["accesskey"]

        r = httpx.get("https://krcs.kugou.com/download", params={
            "ver": 1,
            "man": "yes",
            "client": "mobi",
            "format": "lrc",
            "id": id_,
            "accesskey": accesskey
        }).json()

        krc = decode_krc(r["content"])

        krc = RE_WORD_TIMING.sub("", krc)
        lines = reformat_timings(islice(filterfalse(RE_KRC_JUNK.match, krc.splitlines()), 1, None))

        return "\n".join(lines)
