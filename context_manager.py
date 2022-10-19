from collections import Counter

from tqdm.auto import tqdm

from log import LogInvalidURL
from output import Output
from parse_data_file import parse_data_file
from parse_url import (
    Link,
    verify_link
)


def context_manager(filepath, count, output_path, log_path):
    internal_log = Counter({})

    with open(output_path, "w") as output_file, open(log_path, "w") as log_file:

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
            reader = tqdm(parse_data_file(filepath), total=int(count), desc="Progress Bar", dynamic_ncols=True)
        else:
            reader = parse_data_file(filepath)

        # ------------------------------------ #
        # Parse each row of the data file
        # ------------------------------------ #
        for row in reader:
            url = row.get("links")

            # ------------------------------------ #
            # Log invalid URLs
            # ------------------------------------ #
            issue = verify_link(url)

            if issue.message:
                error_log.log_error(url, issue.message)
                continue
            
            # ------------------------------------ #
            # Resolve URL if needed
            # ------------------------------------ #
            link = Link(url, issue.needs_resolved)

            if link.normalized_url:

            # ------------------------------------ #
            # Update the internal log
            # ------------------------------------ #
                internal_log.update([link.normalized_url])
                link.count = internal_log[link.normalized_url]

            # ------------------------------------ #
            # Update output only with new links
            # ------------------------------------ #
                if link.count == 1:
                    link.data()
                    output.update(link)
