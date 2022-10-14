from ural import (
    is_shortened_url, 
    is_url,
    normalize_url
)


# -----------------------------------
# Return an error message to log if the URL is invalid.
# -----------------------------------
def verify_link(url):

    if not is_url(url):
        return "not url"
    
    elif is_shortened_url(url):
        return "shortened url"
    
    else:
        return None


# -----------------------------------
# Class to store data about a URL.
# -----------------------------------
class Link:
    def __init__(self, input_url):
        self.input = input_url
        self.normalized_url = normalize_url(input_url)
