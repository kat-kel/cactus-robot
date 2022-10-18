from minet.web import resolve as minet_resolve
from ural import normalize_url as ural_normalize_url

def resolve(url):
    error, stack = minet_resolve(url)
    resolution = stack.pop()
    return ural_normalize_url(resolution.url)