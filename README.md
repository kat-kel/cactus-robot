# Analyze Links in Twitter

This program parses collections of URLs in the format of Twitter API's export 
and/or Gazouilloire, a collecting tool from Science Po's médialab. It extracts
URLs from the collection and yields a CSV file with metadata about valid links.

Twitter and Gazouilloire store URLs in the column 'links' and this program will
search that column by default. But if you want to execute the analysis on a dataset
with URLs stored under a different column, you can declare it with the option -s.


1. Create and activate a virtual environment for python (version 3.10)

2. Install dependencies.
```shell
$ pip install -r requirements.txt
```

3. Call command.

    1. Analyze links in multiple Twitter/Gazouilloire exports, contained in a directory

    ```shell
    $ bash run.sh -f DIR -o PATH/TO/OUTFILE.csv -l PATH/TO/LOG.csv
    ```

    2. Analyze links in one Twitter/Gazouilloire export.

    ```shell
    $ bash run.sh -f FILE -o PATH/TO/OUTFILE.csv -l PATH/TO/LOG.csv
    ```

Help:
```
Syntax: run.sh [-f|-s|-o|-l|-h]


options:
f     path to the data file or directory
s     name of the column with the URLs to be analyzed
o     path to the file in which the results will be sent
l     path to file in which any errors will be logged
h     print this help
```