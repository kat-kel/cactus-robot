import click
import csv

from configure_data import (
    verify_data_file,
    verify_link,
    Link
)


@click.command
@click.argument("filepath")
def main(filepath):

    data = verify_data_file(filepath)

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)

        results = []

        for row in reader:
            url = row.get("links")
            if verify_link(url):
                link = Link(url)
                results.append(link.normalized_url)
        
        print(results[:10])


if __name__ == "__main__":
    main()