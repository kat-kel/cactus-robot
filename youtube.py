from bs4 import BeautifulSoup
import requests
from ural.youtube import (
    is_youtube_url,
    parse_youtube_url,
    YoutubeChannel
)


def scrape_channel_id(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    target = soup.find(itemprop="channelId")
    if target:
        id = target.get("content")
        if id:
            return id

def construct_channel_url(id):
    if id:
        channel_url = f"https://youtube.com/channel/{id}"
        if is_youtube_url(channel_url):
            parsed_url = parse_youtube_url(channel_url)
            if parsed_url and isinstance(parsed_url, YoutubeChannel):
                return channel_url
