from exceptions import (
    InvalidURL
)

from ural import (
    ensure_protocol, 
    is_shortened_url, 
    is_url,
    normalize_url
)


# -----------------------------------
# Parse row in data file
# -----------------------------------
def verify_link(url):

    try:
        is_url(url) and not is_shortened_url(url)
        return ensure_protocol(url, protocol="https")
        
    except InvalidURL as e:
        pass


class Link:
    def __init__(self, input_url):
        self.input = input_url
        self.normalized_url = normalize_url(input_url)
