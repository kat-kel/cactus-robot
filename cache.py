import csv

FIELDNAMES = ["input", "count", "normalized url"]

class Cache:
    def __init__(self, writer):
        self.writer = csv.DictWriter(writer, fieldnames=FIELDNAMES)
        self.data = {}
    
    def new_entry(self, url):
        self.data[url.normalized_url] = \
        {
            "input":url.input,
            "count":url.count,
            "normalized url":url.normalized_url
        }
    
    def update(self, url):
        self.data[url.normalized_url]["count"] = url.count
    
    def write(self):
        self.writer.writerows([link[1] for link in self.data.items()])
        