import csv
import gzip

from exceptions import FileTypeError


def read_files(filepath):
    """
    Generate a CSV DictReader of the data file being processed.
    """
    # ------------------------------------ #
    # Read CSV file zipped in filepath
    # ------------------------------------ #
    if filepath.split(".")[-1] == "gz":
        with gzip.open(filepath, mode="rt") as zf:
            try:
                reader = csv.DictReader(zf)
                yield from reader
            except:
                raise FileTypeError(filepath)

    # ------------------------------------ #
    # Read one CSV file given in filepath
    # ------------------------------------ #
    elif filepath.split(".")[-1] == "csv":
        with open(filepath, "r") as f:
            try:
                reader = csv.DictReader(f)
                yield from reader
            except:
                raise FileTypeError(filepath)
    
    else:
        raise FileTypeError(filepath)