# cactus-robot

Create/activate a virtual environment for python 3.10

1. Install the dependencies.
```
$ pip install -r requirements.txt
```

2. Call the program and declare a path to your CSV file of URLs, where the column containing the URLs is called "links".
```
$ python main.py DATAFILE
```
> Optionally, you can specify the path to the output file (`--output OUTPUT_CSV`) and the path to the error log (`--log LOG_CSV`). It is recommended that you also use the option to give the program a count of all the lines in your data file (`--count TOTAL`), so that a loading bar can be created to show the program's progress as it processes all the URLs in the data file.