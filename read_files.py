import csv
from zipfile import (
    ZipFile,
    is_zipfile
)
from io import TextIOWrapper

from exceptions import FileTypeError
from parse_data import parse_data_file


def read_files(filepath):
    # ------------------------------------ #
    # Read all CSV file(s) zipped in filepath
    # ------------------------------------ #
    if is_zipfile(filepath):
        with ZipFile(filepath) as zf:
            for i in ZipFile.infolist(zf):
                with zf.open(i.filename, "r") as f:
                    try:
                        reader = csv.DictReader(TextIOWrapper(f, "utf-8"))
                        return parse_data_file(reader)
                    # ------------------------------------ #
                    # If the read file is not a CSV, raise an error
                    # ------------------------------------ #
                    except:
                        raise FileTypeError(filepath)

    # ------------------------------------ #
    # Read one CSV file given in filepath
    # ------------------------------------ #
    else:
        with open(filepath, "r") as f:
            try:
                reader = csv.DictReader(f)
                return parse_data_file(reader)
            # ------------------------------------ #
            # If the read file is not a CSV, raise an error
            # ------------------------------------ #
            except:
                raise FileTypeError(filepath)
