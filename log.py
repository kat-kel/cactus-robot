import csv

FIELDNAMES = ["url", "error"]

def recreate_log_file(log):
    with open(log, "w") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows([])


class LogInvalidURL:
    def __init__(self, writer):
        self.writer = csv.DictWriter(writer, fieldnames=FIELDNAMES)

    def log_error(self, url:str, error:str):
        self.writer.writerow({FIELDNAMES[0]:url, FIELDNAMES[1]:error})


class Issue:
    def __init__(self):
        self.message = None
        self.needs_resolved = False

    def error_message(self, message):
        self.message = message

    def unresolved(self):
        self.needs_resolved = True
