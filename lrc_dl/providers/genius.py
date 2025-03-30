# https://github.com/jeffvli/feishin/blob/development/src/main/features/core/lyrics/genius.ts
import re
from typing import Optional
import httpx
import bs4

from lrc_dl.core import Song, AbstractProvider
from lrc_dl.registry import lyrics_provider


def _format_div(div: bs4.Tag):
    for br in div.find_all('br'):
        br.replace_with('\n') # type: ignore
    text = div.get_text().strip()
    text = re.sub(r"\[.*\]\n", '', text).strip()

    # remove extra newlines
    return '\n\n'.join(['\n'.join(x.split('\n')) for x in text.split('\n\n')])


@lyrics_provider
class Genius(AbstractProvider):
    name = "genius"

    def fetch_lyrics(self, song: Song) -> Optional[str]:
        r = httpx.get('https://genius.com/api/search/song', params={
            'per_page': 1,
            'q': f'{song.artist} {song.title}'
        })

        if r.status_code != 200 or 'application/json' not in r.headers.get('content-type', ''):
            return

        hits = r.json().get('response', {}).get('sections', [{}])[0].get('hits')

        if not hits:
            return

        url: str = hits[0].get('result', {}).get('url')

        if not url:
            return

        r = httpx.get(url, headers={
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'
        })

        if r.status_code != 200:
            return

        soup = bs4.BeautifulSoup(r.text, features='html.parser')
        div = soup.select_one('div.lyrics')

        if div:
            return _format_div(div)

        div = soup.select_one('div[class^=Lyrics__Container]')

        if not div:
            return

        return _format_div(div)
