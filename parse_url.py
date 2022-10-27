from urllib.parse import urlparse

from ural import get_domain_name as ural_get_domain_name
from ural import get_hostname as ural_get_hostname
from ural import get_normalized_hostname as ural_get_normalized_hostname
from ural import is_url as ural_is_url
from ural import normalize_url as ural_normalize_url
from ural import should_resolve as ural_should_resolve
from ural.facebook import (
    FacebookGroup,
    is_facebook_url as ural_is_facebook_url,
    parse_facebook_url as ural_parse_facebook_url
)
from ural.twitter import (
    extract_screen_name_from_twitter_url as ural_extract_screen_name_from_twitter_url,
    is_twitter_url as ural_is_twitter_url,
    normalize_screen_name as ural_normalize_screen_name
)
from ural.youtube import (
    YoutubeChannel,
    YoutubeVideo,
    is_youtube_url as ural_is_youtube_url,
    parse_youtube_url as ural_parse_youtube_url
)
from log import Issue
from resolve_url import resolve
from youtube import construct_channel_url, catch_bad_channel_path
from minet.youtube.scrapers import scrape_channel_id as minet_scrape_channel_id
from facebook import contains_id


# -----------------------------------
# Return an error message to log if the URL is invalid.
# -----------------------------------
def verify_link(url):
    issue = Issue()

    # Check that the URL input is a URL
    if not ural_is_url(url): issue.error_message("is not URL")

    # Check if the URL needs resolved
    elif ural_should_resolve(url):

        # Log an error message that the URL will not be resolved
        if not ural_is_youtube_url(url): issue.error_message("not resolved")

        # If the URL is from Youtube, note that it should be resolved
        else: issue.unresolved()

    # If there is no error or further resolution to do, return an empty issue
    return issue


# -----------------------------------
# Class to store data about a URL.
# -----------------------------------
class Link:
    def __init__(self, input_url:str, needs_resolution:bool):
        self.input = input_url
        self.needs_resolution = needs_resolution
        self.normalized_url = None
        self.count = 0
        self.domain = None
        self.subdomain = None
        self.complete_subdomain = None
        self.host = None
        self.normalized_host = None
        self.twitter_user = None
        self.youtube_channel_name = None
        self.youtube_channel_id = None
        self.youtube_channel_link = None
        self.facebook_group_name = None
        self.facebook_group_id = None

        if needs_resolution:
            resolved_url = resolve(self.input)
            self.normalized_url = ural_normalize_url(resolved_url)
        else:
            self.normalized_url = ural_normalize_url(self.input)

    def data(self):
        self.domain = ural_get_domain_name(self.normalized_url)

        self.subdomain = self.get_subdomain()

        self.complete_subdomain = self.clean_subdomain()

        self.host = ural_get_hostname(self.normalized_url)

        self.normalized_host = ural_get_normalized_hostname(self.normalized_url)

        if ural_is_twitter_url(self.normalized_url):
            screen_name = ural_extract_screen_name_from_twitter_url(self.normalized_url)
            if screen_name:
                self.twitter_user = ural_normalize_screen_name(screen_name)

        if ural_is_youtube_url(self.normalized_url):
            if not catch_bad_channel_path(self.normalized_url):
                parsed_url = ural_parse_youtube_url(self.normalized_url)
                if parsed_url:
                    if isinstance(parsed_url, YoutubeChannel):
                        self.youtube_channel_id = parsed_url.id
                        self.youtube_channel_name = parsed_url.name
                    if isinstance(parsed_url, YoutubeVideo):
                        url = "https://"+self.normalized_url
                        try:
                            self.youtube_channel_id = minet_scrape_channel_id(url)
                        except:
                            pass
                if self.youtube_channel_id:
                    self.youtube_channel_link = construct_channel_url(self.youtube_channel_id)
                
        if ural_is_facebook_url(self.normalized_url):
            # contains_id() is a little fix for the moment, should be repaired later with an update to Minet.
            # It responds to a problem with constructing the class FacebookPost when the parsed url doesn't give a parent ID.
            # The function parse_facebook_url() will try to return an instance of the class FacebookPost if it determines the URL to be from a post.
            if contains_id(self.normalized_url):
                parsed_url = ural_parse_facebook_url(self.normalized_url)
                if parsed_url and isinstance(parsed_url, FacebookGroup):
                    self.facebook_group_id = parsed_url.id
                    self.facebook_group_name = parsed_url.handle

    def get_subdomain(self):
        url = "https://"+self.normalized_url
        hostname = urlparse(url).hostname
        subdomain = hostname.split(".")[0]
        if self.domain:
            if subdomain and subdomain != "www" and subdomain != self.domain.split(".")[0]:
                return subdomain

    def clean_subdomain(self):
        if self.subdomain:
            return self.subdomain+self.domain
        elif self.domain:
            return self.domain
