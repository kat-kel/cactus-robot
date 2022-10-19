import csv

FIELDNAMES = ["input", "count", "normalized url", "domain", "subdomain", "host name", "normalized host name", "twitter user", "youtube channel name", "youtube channel id", "youtube channel link", "facebook group name", "facebook group id"]

class Output:
    def __init__(self, writer):
        self.writer = csv.DictWriter(writer, fieldnames=FIELDNAMES)
        self.data = {}
    
    def new_entry(self, url):
        self.data[url.normalized_url] = \
        {
            "input":url.input,
            "count":url.count,
            "normalized url":url.normalized_url,
            "domain":url.domain,
            "subdomain":url.subdomain,
            "host name":url.host,
            "normalized host name":url.normalized_host,
            "twitter user":url.twitter_user,
            "youtube channel name":url.youtube_channel_name,
            "youtube channel id":url.youtube_channel_id,
            "youtube channel link":url.youtube_channel_link,
            "facebook group name":url.facebook_group_name,
            "facebook group id":url.facebook_group_id
        }
    
    def update(self, url):
        self.data[url.normalized_url]["count"] = url.count
    
    def write(self):
        self.writer.writerows([link[1] for link in self.data.items()])
        