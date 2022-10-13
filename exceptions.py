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
    def __init__(self, extension=None, *args):
        super().__init__(args)
        self.ext = extension
    
    def __str__(self) -> str:
        return f"{red}{self.ext}{end} {yellow}is not a valid extension. The data file must be a CSV.{end}"


class InvalidURL(Exception):
    def __init__(self, *args):
        super().__init__(args)