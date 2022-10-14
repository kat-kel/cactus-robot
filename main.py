import click
import os

from exceptions import (
    DataFileNotFound
)
from read_files import read_files


@click.command
@click.argument("filepath")
def main(filepath):
    # ------------------------------------ #
    # Raise an error if the given filepath is invalid
    # ------------------------------------ #
    if not os.path.isfile(filepath):
        raise DataFileNotFound(filepath)

    # ------------------------------------ #
    # Otherwise, read the files and extract a list of links of type Link() from configure_data.py
    # ------------------------------------ #
    else:
        links = read_files(filepath)


if __name__ == "__main__":
    main()