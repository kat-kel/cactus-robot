from tqdm.auto import tqdm

from output import Output
from parse_data_file import generator
from parse_url import Link


def analyze_urls(cache_path, output_path, cache_length):
    with open(output_path, "w") as output_file:

        # ------------------------------------ #
        # Create output CSV
        # ------------------------------------ #
        output = Output(output_file)
        output.writer.writeheader()

        # ------------------------------------ #
        # Generate the cache file
        # ------------------------------------ #
        reader = tqdm(generator(cache_path), total=int(cache_length), desc="Analyzing URLs", dynamic_ncols=True)

        # ------------------------------------ #
        # Analyze each URL in the cache file
        # ------------------------------------ #
        for row in reader:
            link = Link(row["input"], False)
            link.count = row["count"]
            link.normalized_url = row["normalized url"]

            link.data()

            # ------------------------------------ #
            # Update the output file with analyzed data
            # ------------------------------------ #

            output.write_row(link)
