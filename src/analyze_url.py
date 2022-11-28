from urllib.parse import urlparse

from minet.youtube.scrapers import scrape_channel_id
from ural import (get_domain_name, get_normalized_hostname, is_url,
                  normalize_url, should_resolve)
from ural.facebook import FacebookGroup, is_facebook_url, parse_facebook_url
from ural.twitter import (extract_screen_name_from_twitter_url, is_twitter_url,
                          normalize_screen_name)
from ural.youtube import (YoutubeChannel, YoutubeVideo, is_youtube_url,
                          parse_youtube_url)


# -----------------------------------
# Return an error message to log if the URL is invalid.
# -----------------------------------
class LinkInspection:
    def __init__(self, url):
        self.url = url
        self.message = None
        self.needs_resolved = False
        self.normalized_url = None

        if not is_url(url): self.message = "not URL"

        elif should_resolve(url):
            if is_youtube_url(url):
                self.needs_resolved = True
            else: self.message = "not resolved"

        else:
            self.normalized_url = normalize_url(url)

# -----------------------------------
# Class to store data about a URL.
# -----------------------------------
class LinkData:
    def __init__(self, raw_url:str, normalized_url:str, ids:str):
        self.raw_url = raw_url
        self.normalized_url = normalized_url
        self.ids = ids
        self.count = len(self.ids)
        self.domain = None
        self.subdomain = None
        self.hostname = None
        self.twitter_user = None
        self.youtube_channel_name = None
        self.youtube_channel_id = None
        self.youtube_channel_link = None
        self.facebook_group_name = None
        self.facebook_group_id = None

        # rewrite ids with | separator
        self.ids = "|".join(self.ids)

        # Use URAL to get domain name
        self.domain = get_domain_name(self.normalized_url)

        # Parse subdomain name and concatenate with domain name
        self.subdomain = self.get_subdomain()

        # Use URAL to get normalized version of hostname
        self.hostaname = get_normalized_hostname(self.normalized_url)

        # Twitter data fields
        if is_twitter_url(self.normalized_url):
            screen_name = extract_screen_name_from_twitter_url(self.normalized_url)
            if screen_name:
                self.twitter_user = normalize_screen_name(screen_name)

        # Youtube data fields
        if is_youtube_url(self.normalized_url):
            parsed_url = parse_youtube_url(self.normalized_url)
            if parsed_url:
                if isinstance(parsed_url, YoutubeChannel):
                    self.youtube_channel_id = parsed_url.id
                    self.youtube_channel_name = parsed_url.name
                if isinstance(parsed_url, YoutubeVideo):
                    url = "https://"+self.normalized_url
                    try:
                        self.youtube_channel_id = scrape_channel_id(url)
                    except:
                        pass
            if self.youtube_channel_id:
                channel_url = f"https://youtube.com/channel/{self.youtube_channel_id}"
                if is_youtube_url(channel_url):
                    parsed_url = parse_youtube_url(channel_url)
                    if parsed_url and isinstance(parsed_url, YoutubeChannel):
                     self.youtube_channel_link = channel_url

        
        # Facebook data fields
        if is_facebook_url(self.normalized_url):
            parsed_url = parse_facebook_url(self.normalized_url)
            if parsed_url and isinstance(parsed_url, FacebookGroup):
                self.facebook_group_id = parsed_url.id
                self.facebook_group_name = parsed_url.handle
        

    def get_subdomain(self):
        url = "https://"+self.normalized_url
        hostname = urlparse(url).hostname
        subdomain = hostname.split(".")[0]
        if self.domain:
            if subdomain and subdomain != "www" and subdomain != self.domain.split(".")[0]:
                return subdomain+self.domain
