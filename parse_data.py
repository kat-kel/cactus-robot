from configure_data import (
    verify_link,
    Link
)

def parse_data_file(reader):
    links = []
    # -----------------------------------
    # Parse every row in the data file
    # -----------------------------------
    for row in reader:
        url = row.get("links")
        if verify_link(url):
            link = Link(url)
            links.append(link.normalized_url)

    return links