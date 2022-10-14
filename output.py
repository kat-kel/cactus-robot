import csv

FIELDNAMES = ["input", "normalized url", "domain", "subdomain", "host name", "normalized host name", "twitter user", "youtube channel", "facebook group"]

class Output:
    def __init__(self, writer):
        self.writer = csv.DictWriter(writer, fieldnames=FIELDNAMES)
    
    def update(self, url):
        self.writer.writerow({
            "normalized url":url.normalized_url,
            "domain":url.domain,
            "subdomain":url.subdomain,
            "host name":url.host,
            "normalized host name":url.normalized_host,
            "twitter user":url.twitter_user,
            "youtube channel":url.youtube_channel,
            "facebook group":url.facebook_group
            })