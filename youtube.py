from ural.youtube import (
    is_youtube_url,
    parse_youtube_url,
    YoutubeChannel
)
from ural.utils import urlsplit, urlpathsplit


def construct_channel_url(id):
    if id:
        channel_url = f"https://youtube.com/channel/{id}"
        if is_youtube_url(channel_url):
            parsed_url = parse_youtube_url(channel_url)
            if parsed_url and isinstance(parsed_url, YoutubeChannel):
                return channel_url


def catch_bad_channel_path(url):
    parsed = urlsplit(url)
    if parsed.path.startswith('/channel/'):
        split = urlpathsplit(parsed.path)
        if len(split) < 2:
            return True
