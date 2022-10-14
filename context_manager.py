from read_files import read_files
from config import LOG_FILE, OUTPUT_FILE
from parse_url import (
    Link,
    verify_link
)
from log import (
    LogInvalidURL,
    ErrorMessage
)
from output import Output


def context_manager(filepath):

    with open(OUTPUT_FILE, "w") as output_file, open(LOG_FILE, "w") as log_file:

        # ------------------------------------ #
        # Create the error log CSV
        # ------------------------------------ #
        error_log = LogInvalidURL(log_file)
        error_log.writer.writeheader()

        # ------------------------------------ #
        # Create the output CSV
        # ------------------------------------ #
        output = Output(output_file)
        output.writer.writeheader()

        for row in read_files(filepath):

            url = row.get("links")

            # ------------------------------------ #
            # Log invalid URLs
            # ------------------------------------ #
            error = verify_link(url)
            if isinstance(error, ErrorMessage):
                    error_log.log_error(url, error.message)
            elif isinstance(error, str):
                url = error

            # ------------------------------------ #
            # Output URL data
            # ------------------------------------ #
            else:
                output.update(Link(url))
