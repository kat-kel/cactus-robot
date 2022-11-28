import csv

from minet import multithreaded_resolve
from tqdm.auto import tqdm
from ural import normalize_url

from analyze_url import LinkInspection


def normalize_urls(filepath, count, id_col, links_col, cache, log):

    aggregates = {}
    urls_to_resolve = []

    if count: reader = tqdm(generator(filepath), total=int(count), desc="Normalizing URLs")
    else: reader = generator(filepath)

    for row in reader:

        id = row.get(id_col)
        link = row.get(links_col)

        if not log.get(link) or not cache.get(link):

            inspection_result = LinkInspection(link)

            if inspection_result.message:
                log.update({link:{"raw link":link,"message":inspection_result.message}})

            if inspection_result.needs_resolved and not cache.get(link):
                urls_to_resolve.append({"url":link,"id":id, "raw link":link})

            elif inspection_result.normalized_url:
                cache.update({link:{"raw link":link,"normalization":inspection_result.normalized_url}})
                update_aggregate(aggregates, inspection_result.normalized_url, id, link)

        elif cache.get(link):
            update_aggregate(aggregates, cache[link]["normalization"], id, link)

    for result in tqdm(multithreaded_resolve(urls_to_resolve, key=lambda x: x['url']), total=len(urls_to_resolve), desc="Resolving URLs"):
        normalized_url = normalize_url(result.stack[-1].url)
        raw_link = result.item["raw link"]
        cache.update({raw_link:{"raw link":raw_link,"normalization":normalized_url}})
        update_aggregate(aggregates, normalized_url, result.item["id"], raw_link)

    return cache, log, aggregates


def update_aggregate(aggregates, normalized_url, id, link):
    if not aggregates.get(normalized_url):
        aggregates.update({normalized_url:{"normalized url":normalized_url, "first raw link":link, "ids":[id]}})
    else:
        aggregates[normalized_url]["ids"].append(id)


def generator(filepath):
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        yield from reader
