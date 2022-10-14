import csv

from config import LOG_FILE
FIELDNAMES = ["url", "error"]

def recreate_log_file():
    with open(LOG_FILE, "w") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows([])


class LogInvalidURL:
    def __init__(self, writer):
        self.writer = csv.DictWriter(writer, fieldnames=FIELDNAMES)
    
    def log_error(self, url:str, error:str):
        self.writer.writerow({FIELDNAMES[0]:url, FIELDNAMES[1]:error})
        

class ErrorMessage:
    def __init__(self, message):
        self.message = message