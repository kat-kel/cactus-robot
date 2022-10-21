yellow = "\033[1;33m"
green = "\033[0;32m"
red = "\033[0;31m"
end = "\033[0m"


class DataFileNotFound(Exception):
    def __init__(self, filepath=None, *args):
        super().__init__(args)
        self.fp = filepath

    def __str__(self) -> str:
        return f"{yellow}The data was not found at{end} {red}{self.fp}{end}{yellow}. Please enter the path to a CSV file.{end}"


class FileTypeError(Exception):
    def __init__(self, filepath=None, *args):
        super().__init__(args)
        self.fp = filepath
        self.ext = filepath.split(".")[-1]

    def __str__(self) -> str:
        return f"{yellow}The file {end}{red}{self.fp}{end}{yellow} is not a valid file type due to its extension {end}{red}{self.ext}{end}{yellow}. The data file must be a CSV or a CSV file zippped with gzip.{end}"


class InvalidURL(Exception):
    def __init__(self, url=None, *args):
        super().__init__(args)
        self.url = url

    def __str__(self) -> str:
        return f"{yellow}The URL is invalid: {end} {red}{self.url}{end}"