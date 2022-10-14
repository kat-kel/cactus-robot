from ural import (
    is_url,
    normalize_url as ural_normalize_url,
    get_domain_name as ural_get_domain_name,
    get_hostname as ural_get_hostname,
    get_normalized_hostname as ural_get_normalized_hostname,
    should_resolve as ural_should_resolve,
)
from ural.twitter import(
    is_twitter_url,
    extract_screen_name_from_twitter_url,
    normalize_screen_name
)
from ural.youtube import(
    is_youtube_url,
    parse_youtube_url,
    YoutubeChannel
)
from ural.facebook import(
    is_facebook_url,
    parse_facebook_url,
    FacebookGroup,
)
from log import ErrorMessage
from urllib.parse import urlparse


# -----------------------------------
# Return an error message to log if the URL is invalid.
# -----------------------------------
def verify_link(url):

    # Check that the URL input is a URL
    if not is_url(url):
        return ErrorMessage("is not URL")
    
    # Check that the URL is not shortened
    elif ural_should_resolve(url):
        return ErrorMessage("not resolved")
    
    else:
        return None


# -----------------------------------
# Class to store data about a URL.
# -----------------------------------
class Link:
    def __init__(self, input_url):
        self.input = input_url
        self.normalized_url = ural_normalize_url(self.input)
        self.domain = ural_get_domain_name(self.input)
        self.subdomain = self.get_subdomain()
        self.host = ural_get_hostname(self.input)
        self.normalized_host = ural_get_normalized_hostname(self.input)
        self.twitter_user = None
        self.youtube_channel_name = None
        self.youtube_channel_id = None
        self.facebook_group_name = None
        self.facebook_group_id = None

        if is_twitter_url(self.input):
            screen_name = extract_screen_name_from_twitter_url(self.input)
            if screen_name:
                self.twitter_user = normalize_screen_name(screen_name)

        if is_youtube_url(self.input):
            parsed_url = parse_youtube_url(self.input)
            if parsed_url and isinstance(parsed_url, YoutubeChannel):
                self.youtube_channel_id = parsed_url.id
                self.youtube_channel_name = parsed_url.name
        
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
