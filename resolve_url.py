from minet.web import resolve as minet_resolve

def resolve(url):
    error, stack = minet_resolve(url)
    resolution = stack.pop()
    return resolution.url
    