# Analyze Links in Twitter Data

This program parses URLS in datasets conforming to Twitter API's export and/or [Gazouilloire](https://github.com/medialab/gazouilloire), a long-term tweet collection tool from Science Po's médialab. From a dataset, the program extracts tweets' IDs and linked URLs. It then yields a CSV file with enriched metadata about valid, active URLS. The enrichments includes (1) agregated counts about the URL in the dataset, (2) metadata about the URL itself, and (3) metadata about certain social media sites if the URL is from one of the studied sources.

## Raw Tweet Data
The incoming data file must have an ID for each tweet and a column containing the URLs linked to the tweet. If a tweet contains multiple URLs (i.e. tweet `1565043914381434881`), they must be separated by a pipe `|`. Twitter's API returns data already in this format, as does Gazouilloire.

|id|...|links|
|-|-|-|
|1564138363136909312|...||
|1565043914381434881|...|https://twitter.com/franceinter/status/1556286125270093825\|https://www.radiofrance.fr/franceinter/les-milliardaires-et-les-stars-irrites-par-le-suivi-en-ligne-de-leurs-trajets-aeriens-4327256|
|1564626931353616386|...|https://l.franceculture.fr/qhT|
1555931971188150272|..|https://www.radiofrance.fr/franceinter/les-milliardaires-et-les-stars-irrites-par-le-suivi-en-ligne-de-leurs-trajets-aeriens-4327256\|

## Preprocessing

Using the Rust tool `xsv`, the program preprocesses the data. First, it removes everything but the ID and links columns. Second, it creates a unique row for every link, "exploding" links that might have been concatenated and separated by a pipe (i.e. tweet `1565043914381434881`). Finally, it removes any tweets which do not contain links (i.e. tweet `1564138363136909312`), yielding a cleaned dataset that can be accessed later in the directory `preprocessing/`.

|id|links|
|-|-|
|1565043914381434881|https://twitter.com/franceinter/status/1556286125270093825|
|1565043914381434881|https://www.radiofrance.fr/franceinter/les-milliardaires-et-les-stars-irrites-par-le-suivi-en-ligne-de-leurs-trajets-aeriens-4327256|
|1564626931353616386|https://l.franceculture.fr/qhT|
1555931971188150272|https://www.radiofrance.fr/franceinter/les-milliardaires-et-les-stars-irrites-par-le-suivi-en-ligne-de-leurs-trajets-aeriens-4327256\|

## Enriched Links Data

Using its Python scripts, the program then analyzes all the links in the preprocessed dataset and yields an enriched CSV with the following fields:

1. **raw_url** : raw version of the link*

    |raw_url|
    |-|
    |https://www.radiofrance.fr/franceinter/les-milliardaires-et-les-stars-irrites-par-le-suivi-en-ligne-de-leurs-trajets-aeriens-4327256|

\* If multiple tweets contain links that normalize to the same URL but are composed differently, the field `input` only contains the first raw version of the link that the program encountered. Subsequent versions are not recorded, though their presence in the dataset is recorded in the `count` and `tweet_ids` fields.

---

2. **normalized_url** : normalized version of the link

    |normalized_url|
    |-|
    |radiofrance.fr/franceinter/les-milliardaires-et-les-stars-irrites-par-le-suivi-en-ligne-de-leurs-trajets-aeriens-4327256|
---

3. **count** : number of times the link (according to its normalized version) appeared in the dataset

    |count|
    |-|
    |2|
---

4. **tweet_ids** : IDs of the tweets that contained the link

    |tweet_ids|
    |-|
    |1565043914381434881\|1555931971188150272|
---

5. **domain** : domain name of the normalized URL

    |domain|
    |-|
    |radiofrance.fr|
---

6. **subdomain** : concatenation of the subdomain and domain name of the normalized URL

    |subdomain|
    |-|
    |radiofrance.fr|
---

7. **hostname** : normalized hostname of the normalized URL

    |hostname|
    |-|
    |radiofrance.fr|
---

8. **twitter_user** : if the link is from Twitter\.com, the Twitter user's handle


9. **youtube_channel_name** : if the link is from Youtube\.com, the name of the channel / the video's channel


10. **youtube_channel_id** : if the link is from Youtube\.com, the ID of the channel / the video's channel


11. **youtube_channel_link** : if the link is from Youtube\.com, a link to the channel / the video's channel


12. **facebook_group_id** : if the link is from Facebook\.com and a public Facebook group, the group's ID


# Program Requirements
The program requires Python 3.10 (and some libraries) as well as a tool coded in Rust named `xsv`, which is called during the bash script and used to parse the incoming CSV file(s). To install `xsv`, follow the instructions for [the forked version maintained by Sciences Po's médialab](https://github.com/medialab/xsv).

# How-To

1. Clone this repository and change to that directory.
```shell
$ git clone https://github.com/kat-kel/cactus-robot
$ cd cactus-robot
```

2. Create and activate a new virtual environment for Python (version 3.10).

3. In that virtual Python environment, install the Python dependencies listed in the `requirements.txt` file.

4. While still in the directory `cactus-robot/`, launch the program by calling the bash script with the necessary options.

# File Systems

## Directly work with one CSV file
Analyze links in one Twitter or Gazouilloire export. This file can either be open with the extension `.csv` or it can be compressed with the extension `.csv.gz`. The incoming file is never modified, only read.

```shell
$ ./run.sh-f FILE.CSV
```

## Iterate through CSV files in a directory

Analyze links in a batch of Twitter or Gazouilloire exports stored inside a directory. The program will only process files in the directory with either `.csv` or `.csv.gz` as the extension. The incoming files are never modified, only read.

```shell
$ ./run.sh -f DIRECTORY/
```

# Options

## Data file \[**Required**\] `-f`

The only required option is `-f` which precedes either the data file on which you want to work or the directory over which you want to iterate.

```shell
$ ./run.sh -f incomingfile.csv
```

## Columns \[*Optional*\] `-s`

By default, in accordance with Twitter's and Gazouilloire's naming system, the program searches for tweet's IDs and the URLs of their linked media in the columns "id" and "links", respectively. The option `-s` allows you to select different columns in your CSV file(s) which contain the same information.

```shell
$ ./run.sh -f incomingfile.csv -s custom_id_col custom_links_col
```

## Output \[*Optional*\] `-o`

By default, the program outputs the enriched CSV file to the directory `data/` with the concatenation of the input CSV file's basename plus `_output.csv` (ex. `data/incomingfile_output.csv`). The option `-o` allows you to specify your own name for the enriched CSV file.

> This option is automatically ignored if the program is iterating over a directory. Otherwise, the output file would be rewritten to the same file path every time a new CSV file is processed.

```shell
$ ./run.sh -f incomingfile.csv -o /path/to/customOutput.csv
```

## Log \[*Optional*\] `-l`

The program logs all URLs from the incoming CSV file that were not able to be enriched. This can occur if, for example, the URL is not recognized as a URL according to conditions defined in [URAL](https://github.com/medialab/ural). By default, the program logs unprocessed URLs in the directory `data/` with the concatenation of the input CSV file's basename plus `_log.csv` (ex. `data/incomingfile_log.csv`). The option `-l` changes this default path to whatever argument is entered after the option.

> This option is automatically ignored if the program is iterating over a directory. Otherwise, the log file would be rewritten to the same file path every time a new CSV file is processed.

```shell
$ ./run.sh -f incomingfile.csv -o /path/to/customLog.csv
```

## Help \[*Optional*\] `-h`, `--help`

Displays a help message.
