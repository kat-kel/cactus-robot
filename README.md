# Analyze Links in Twitter

This program parses URLS in datasets conforming to Twitter API's export and/or [Gazouilloire](https://github.com/medialab/gazouilloire), a collection tool from Science Po's médialab. From a dataset, the program extracts the tweets' IDs and linked URLs. It then yields a CSV file with metadata about valid, active URLS. The program can either (a) accept a zipped or open CSV file directly or (b) a directory containing open or zipped CSV files.

Twitter and Gazouilloire store tweet IDs in the column 'id' and media links in the column 'links'. By default, the program will search these two columns. If you want to work with a CSV file with different column headers for the ID and URL, use the option -s followed by 2 arguments: the ID header name, the URL column name.

```shell
$ ./run.sh -f datafile.csv -s my_ids my_links
```

# Requirements
The program requires Python 3.10 (and some libraries) as well as a tool coded in Rust named `xsv`, which is called during the bash script and used to parse the incoming CSV file(s). To install `xsv`, follow the instructions for [the forked version maintained by Sciences Po's médialab](https://github.com/medialab/xsv).

# How to use

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
$ bash run.sh -f FILE.CSV
```

## Iterate through CSV files in a directory

Analyze links in a batch of Twitter or Gazouilloire exports stored inside a directory. The program will only process files in the directory with either `.csv` or `.csv.gz` as the extension. The incoming files are never modified, only read.

```shell
$ bash run.sh -f DIRECTORY/
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
