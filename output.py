import csv

FIELDNAMES = ["input", "count", "normalized url", "domain", "subdomain", "host name", "normalized host name", "twitter user", "youtube channel name", "youtube channel id", "youtube channel link", "facebook group name", "facebook group id"]

class Output:
    def __init__(self, writer):
        self.writer = csv.DictWriter(writer, fieldnames=FIELDNAMES)

    def write_row(self, link):
        self.writer.writerow(
        {
            "input":link.input,
            "count":link.count,
            "normalized url":link.normalized_url,
            "domain":link.domain,
            "subdomain":link.subdomain,
            "host name":link.host,
            "normalized host name":link.normalized_host,
            "twitter user":link.twitter_user,
            "youtube channel name":link.youtube_channel_name,
            "youtube channel id":link.youtube_channel_id,
            "youtube channel link":link.youtube_channel_link,
            "facebook group name":link.facebook_group_name,
            "facebook group id":link.facebook_group_id
        }
        )
