import click
import os

from exceptions import (
    DataFileNotFound
)
from log import (
    recreate_log_file,
)
from context_manager import context_manager

@click.command
@click.argument("filepath")
def main(filepath):

    recreate_log_file()

    # ------------------------------------ #
    # Raise an error if the given filepath is invalid
    # ------------------------------------ #
    if not os.path.isfile(filepath):
        raise DataFileNotFound(filepath)

    # ------------------------------------ #
    # Manage the parsing, error logging, and output of links in the input file
    # ------------------------------------ #
    else:
        context_manager(filepath)


if __name__ == "__main__":
    main()
