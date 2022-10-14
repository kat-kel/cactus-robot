from read_files import read_files
from config import LOG_FILE, OUTPUT_FILE
from parse_url import (
    Link,
    verify_link
)
from log import (
    LogInvalidURL,
)
from output import Output
from tqdm.auto import tqdm


def context_manager(filepath, count):

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

        # ------------------------------------ #
        # Adjust for a progress bar
        # ------------------------------------ #
        if count:
            reader = tqdm(read_files(filepath), total=int(count), desc="Progress Bar", dynamic_ncols=True)
        else:
            reader = read_files(filepath)

        # ------------------------------------ #
        # Parse each row of the data file
        # ------------------------------------ #
        for row in reader:
            url = row.get("links")

            # ------------------------------------ #
            # Log invalid URLs
            # ------------------------------------ #
            error = verify_link(url)
            if error:
                error_log.log_error(url, error.message)

            # ------------------------------------ #
            # Output URL data
            # ------------------------------------ #
            else:
                output.update(Link(url))
