import csv

FIELDNAMES = ["input", "normalized_url", "domain_name", "host_name", "normalized_host"]

class Output:
    def __init__(self, writer):
        self.writer = csv.DictWriter(writer, fieldnames=FIELDNAMES)
    
    def update(self, url_data):
        self.writer.writerow({"normalized_url":url_data.normalized_url})
        