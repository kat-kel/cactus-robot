import click
import os

from analyze_urls import analyze_urls
from config import (
    DEFAULT_LOG_FILE,
    DEFAULT_OUTPUT_FILE,
    CACHE_FILE
)
from exceptions import (
    DataFileNotFound
)
from log import (
    recreate_log_file,
)
from normalize_urls import normalize_urls

@click.command
@click.argument("filepath")
@click.option("--count", default=None)
@click.option("--output", default=DEFAULT_OUTPUT_FILE)
@click.option("--log", default=DEFAULT_LOG_FILE)
def main(filepath, count, output, log):

    recreate_log_file(log)

    # ------------------------------------ #
    # Raise an error if the given filepath is invalid
    # ------------------------------------ #
    if not os.path.isfile(filepath):
        raise DataFileNotFound(filepath)

    # ------------------------------------ #
    # Manage the parsing, error logging, and output of links in the input file
    # ------------------------------------ #
    else:
        cache_length = normalize_urls(filepath, CACHE_FILE, count, log)
        analyze_urls(CACHE_FILE, output, cache_length)
        

if __name__ == "__main__":
    main()
