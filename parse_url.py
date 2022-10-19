from urllib.parse import urlparse

from ural import get_domain_name as ural_get_domain_name
from ural import get_hostname as ural_get_hostname
from ural import get_normalized_hostname as ural_get_normalized_hostname
from ural import is_url
from ural import normalize_url as ural_normalize_url
from ural import should_resolve as ural_should_resolve
from ural.facebook import (
    FacebookGroup,
    is_facebook_url,
    parse_facebook_url
)
from ural.twitter import (
    extract_screen_name_from_twitter_url,
    is_twitter_url,
    normalize_screen_name
)
from ural.youtube import (
    YoutubeChannel,
    is_youtube_url,
    parse_youtube_url
)
from log import Issue
from resolve_url import resolve
from youtube import (
    construct_channel_url,
    scrape_channel_id
)


# -----------------------------------
# Return an error message to log if the URL is invalid.
# -----------------------------------
def verify_link(url):
    issue = Issue()

    # Check that the URL input is a URL
    if not is_url(url): issue.error_message("is not URL")
    
    # Check if the URL needs resolved
    elif ural_should_resolve(url):

        # Log an error message that the URL will not be resolved
        if not is_youtube_url(url): issue.error_message("not resolved")
        
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
        self.domain = ural_get_domain_name(self.input)

        self.subdomain = self.get_subdomain()

        self.host = ural_get_hostname(self.input)

        self.normalized_host = ural_get_normalized_hostname(self.input)

        if is_twitter_url(self.input):
            screen_name = extract_screen_name_from_twitter_url(self.input)
            if screen_name:
                self.twitter_user = normalize_screen_name(screen_name)

        if is_youtube_url(self.input):
            parsed_url = parse_youtube_url(self.input)
            if parsed_url and isinstance(parsed_url, YoutubeChannel):
                self.youtube_channel_link = self.normalized_url
                self.youtube_channel_id = parsed_url.id
                self.youtube_channel_name = parsed_url.name
            else:
                self.youtube_channel_id = scrape_channel_id(self.input)
                self.youtube_channel_link = construct_channel_url(self.youtube_channel_id)
        
        if is_facebook_url(self.input):
            parsed_url = parse_facebook_url(self.input)
            if parsed_url and isinstance(parsed_url, FacebookGroup):
                self.facebook_group_id = parsed_url.id
                self.facebook_group_name = parsed_url.handle
    
    def get_subdomain(self):
        hostname = urlparse(self.input).hostname
        subdomain = hostname.split(".")[0]
        if subdomain and subdomain != "www" and subdomain != self.domain.split(".")[0]:
            return subdomain
