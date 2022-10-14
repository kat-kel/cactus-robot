import csv
from zipfile import (
    ZipFile,
    is_zipfile
)
from io import TextIOWrapper

from exceptions import FileTypeError


def read_files(filepath):
    """
    Generate a CSV DictReader of the data file being processed.
    """
    # ------------------------------------ #
    # Read CSV file zipped in filepath
    # ------------------------------------ #
    if is_zipfile(filepath):
        with ZipFile(filepath) as zf:
            with zf.open(ZipFile.infolist(zf)[0].filename, "r") as f:
                try:
                    reader = csv.DictReader(TextIOWrapper(f, "utf-8"))
                    yield from reader
                except:
                    raise FileTypeError(filepath)

    # ------------------------------------ #
    # Read one CSV file given in filepath
    # ------------------------------------ #
    else:
        with open(filepath, "r") as f:
            try:
                reader = csv.DictReader(f)
                yield from reader
            except:
                raise FileTypeError(filepath)
