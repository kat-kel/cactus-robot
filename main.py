import click
import os

from exceptions import (
    DataFileNotFound
)
from log import (
    recreate_log_file,
)
from context_manager import context_manager

DEFAULT_OUTPUT = os.path.join(".","output.csv")
DEFAULT_LOG = os.path.join(".", "log.csv")

@click.command
@click.argument("filepath")
@click.option("--count", default=None)
@click.option("--output", default=DEFAULT_OUTPUT)
@click.option("--log", default=DEFAULT_LOG)
def main(filepath, count, output, log):

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
        context_manager(filepath, count, output, log)


if __name__ == "__main__":
    main()
