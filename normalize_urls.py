from collections import Counter

from tqdm.auto import tqdm

from cache import Cache
from log import LogInvalidURL
from parse_data_file import parse_data_file
from parse_url import (
    Link,
    verify_link
)


def normalize_urls(filepath, cache_path, count, log_path):
    count_url_occurence = Counter({})
    count_urls_cached = Counter({})

    with open(log_path, "w") as log_file, open(cache_path, "w") as cache_file:

        # ------------------------------------ #
        # Create the error log CSV
        # ------------------------------------ #
        error_log = LogInvalidURL(log_file)
        error_log.writer.writeheader()

        # ------------------------------------ #
        # Create cache file
        # ------------------------------------ #
        cache = Cache(cache_file)
        cache.writer.writeheader()

        # ------------------------------------ #
        # Adjust for a progress bar
        # ------------------------------------ #
        if count:
            reader = tqdm(parse_data_file(filepath), total=int(count), desc="Normalizing URLs", dynamic_ncols=True)
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
            # Reset normalized URL to resolved URL if needed
            # ------------------------------------ #
            link = Link(url, issue.needs_resolved)

            if link.normalized_url:

            # ------------------------------------ #
            # Update the internal log
            # ------------------------------------ #
                count_url_occurence.update([link.normalized_url])
                link.count = count_url_occurence[link.normalized_url]

            # ------------------------------------ #
            # Cache the input URL, the normalized version, and its count
            # ------------------------------------ #
                if link.count == 1:
                    cache.new_entry(link)
                    count_urls_cached.update([link.normalized_url])
                else:
                    cache.update(link)
        cache.write()

    return count_urls_cached.total()