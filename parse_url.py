from ural import (
    is_url,
    normalize_url as ural_normalize_url,
    get_domain_name as ural_get_domain_name,
    get_hostname as ural_get_hostname,
    get_normalized_hostname as ural_get_normalized_hostname,
    should_resolve as ural_should_resolve
)
from log import ErrorMessage

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
    # fieldnames = "input", "normalized url", "domain", "subdomain", "host name", "normalized host name", "twitter user", "youtube channel", "facebook group"
    def __init__(self, input_url):
        self.input = input_url
        self.normalized_url = ural_normalize_url(self.input)
        self.domain = ural_get_domain_name(self.input)
        self.subdomain = None
        self.host = ural_get_hostname(self.input)
        self.normalized_host = ural_get_normalized_hostname(self.input)
        self.twitter_user = None
        self.youtube_channel = None
        self.facebook_group = None
