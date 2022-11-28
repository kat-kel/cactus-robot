# Analyze Links in Twitter Data

This program parses URLs in datasets conforming to Twitter API's export and/or [Gazouilloire](https://github.com/medialab/gazouilloire), a long-term tweet collection tool from Science Po's médialab, and yields an enriched CSV file containing information about each unique URL.

Example:
|raw_url|normalized_url|count|ids|domain|subdomain|hostname|twitter_user|youtube_channel_name|youtube_channel_id|youtube_channel_link|facebook_group_name|facebook_group_id|
|--|--|--|--|--|--|--|--|--|--|--|--|--|
|https://www.youtube.com/watch?v=4acSVmN3XT4|youtube.com/watch?v=4acSVmN3XT4|2|1565043914381434881\|1564626931353616386|youtube.com|youtube.com|youtube.com|[none]|[none]|UCLq9OzDa0HBnj_sNyEkdZJg|https://youtube.com/channel/UCLq9OzDa0HBnj_sNyEkdZJg|[none]|[none]|

[--> more detailed description](description.md)

---

## Requirements
The program requires Python 3.10 (and some libraries) as well as a tool coded in Rust named `xsv`, which is called during the bash script and used to parse the incoming CSV file(s). To install `xsv`, follow the instructions for [the forked version maintained by Sciences Po's médialab](https://github.com/medialab/xsv).

## Steps

1. Clone this repository and change to that directory.
```shell
$ git clone https://github.com/kat-kel/cactus-robot
$ cd cactus-robot
```

2. Create and activate a new virtual environment for Python (version 3.10).

3. In that virtual Python environment, install the Python dependencies listed in the `requirements.txt` file.

4. While still in the directory `cactus-robot/`, launch the program by calling the bash script with the necessary options. ([--> description of options](https://github.com/kat-kel/cactus-robot/blob/main/description.md#options))
```shell
$ ./run.sh -f data/sampleData.csv
```
