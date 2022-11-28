import csv
import json
import os

import click
from tqdm.auto import tqdm
from normalize_urls import normalize_urls, generator
from analyze_url import LinkData

CACHEDIR = os.path.join(".", "cache")
AGGDIR = os.path.join(CACHEDIR, "link_aggregates")
OUTPUTDIR = os.path.join(".","output")
CACHEPATH = os.path.join(CACHEDIR,"normalizationCache.json")
LOGPATH = os.path.join(CACHEDIR, "notNormalizedLog.json")
FIELDNAMES = ["raw_url", "normalized_url", "count", "ids", "domain", "subdomain", "hostname", "twitter user", "youtube channel name", "youtube channel id", "youtube channel link", "facebook group name", "facebook group id"]

@click.command
@click.argument("filepath")
@click.option("--id", default="id")
@click.option("--links", default="links")
@click.option("--count", default=None)
@click.option("--output", default=None)
def main(filepath, id, links, count, output):

    # Set up file paths
    if not os.path.isdir(CACHEDIR):
        os.mkdir(CACHEDIR)
    if not os.path.isdir(AGGDIR):
        os.mkdir(AGGDIR)
    if not os.path.isdir(OUTPUTDIR):
        os.mkdir(OUTPUTDIR)
    basename = os.path.basename(filepath).split(".")[0]
    if not output:
        output = os.path.join(OUTPUTDIR,f"{basename}_enriched.csv")
    temp_aggreg_file = os.path.join(AGGDIR, f"{basename}.json")

    # Get cache of normalized URLs
    if os.path.isfile(CACHEPATH):
        with open(CACHEPATH, "r") as open_cache_file:
            cache = json.load(open_cache_file)
    if not os.path.isfile(CACHEPATH) or not cache:
        cache = {}

    # Get log of not normalized links
    if os.path.isfile(LOGPATH):
        with open(LOGPATH, "r") as open_log_file:
            log = json.load(open_log_file)
    if not os.path.isfile(LOGPATH) or not log:
        log = {}

    # Cache normalized URLs or log problematic URLs
    cache, log, aggregates = normalize_urls(filepath, count, id, links, cache, log)
    with open(CACHEPATH, "w") as open_cache_file, open(LOGPATH, "w") as open_log_file, open(temp_aggreg_file, "w") as open_aggreg_file:
        json.dump(cache, open_cache_file, indent=4)
        json.dump(log, open_log_file, indent=4)
        json.dump(aggregates, open_aggreg_file, indent=4)
       
    # Analyze URLs
    with open(output, "w") as open_outfile:
        outfile_writer = csv.DictWriter(open_outfile, fieldnames=FIELDNAMES)
        outfile_writer.writeheader()
        for i in tqdm(aggregates.values(), total=len(aggregates), desc="Enriching URLs"):
            link = LinkData(i["first raw link"], i["normalized url"], i["ids"])
            outfile_writer.writerow({"raw_url":link.raw_url, "normalized_url":link.normalized_url, "count":link.count, "ids":link.ids, "domain":link.domain, "subdomain":link.subdomain, "hostname":link.hostaname,
                "twitter user":link.twitter_user, "youtube channel name":link.youtube_channel_name, "youtube channel id":link.youtube_channel_id, "youtube channel link":link.youtube_channel_link, "facebook group name":link.facebook_group_name, "facebook group id":link.facebook_group_id})

if __name__ == "__main__":
    main()
