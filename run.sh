#!/bin/bash

# ---------------------------------------------
#                  COLOR
# ---------------------------------------------
# Color codes for console messages
bold='\033[1m'
reset='\033[0m'
inverted="\033[7m"
red="\033[31m"
green="\033[32m"
yellow="\033[33m"

# ---------------------------------------------
#                  HELP
# ---------------------------------------------
Help()
{
    echo
    echo "This program parses collections of URLs in the format of Twitter API's export"
    echo "and/or Gazouilloire, a collecting tool from Science Po's médialab. It extracts"
    echo "URLs from the collection and yields a CSV file with metadata about valid links."
    echo
    echo "Twitter and Gazouilloire store URLs in the column 'links' and this program will"
    echo "search that column by default. But if you want to execute the analysis on a dataset"
    echo "with URLs stored under a different column, you can declare it with the option -s."
    echo
    echo "Syntax: run.sh [-f|-s|-o|-l|-h]"
    echo
    echo
    echo "options:"
    echo "f     path to the data file or directory"
    echo "s     name of the column with the URLs to be analyzed"
    echo "o     path to the file in which the results will be sent"
    echo "l     path to file in which any errors will be logged"
    echo "h     print this help"
    echo
    exit
}

# ---------------------------------------------
#         PRE-PROCESS & COUNT DATA
# ---------------------------------------------

TEMPFILE1="temp/temp_links-only.csv"
TEMPFILE2="temp/temp_exploded-links.csv"

XSV_SELECT="xsv select"
XSV_EXPLODE="xsv explode"
XSV_SEARCH="xsv search"

GetBasename() # parameter: file path
{
    if [[ $1 == *.csv ]]
        then
        BASENAME=$(basename $1 .csv)
    elif [[ $1 == *.csv.gz ]]
        then
        BASENAME=$(basename $1 .csv.gz)
    fi
}

Decompresser()
{
    if [[ $(uname -s) == "Darwin" ]]
        then
            DECOMPRESS="gzcat"
            COMPRESS="gzip"
        else
            DECOMPRESS="zcat"
            COMPRESS="gzip"
    fi
}

PreProcess() # parameter: file path
{
    DATAFILE=$1
    TEMPFILE3="temp/${BASENAME}_links.csv"

    if [[ $1 == *.gz ]]
        then
            echo -e "${green}XSV is extracting 'links' column in $1.${reset}"
            $DECOMPRESS $DATAFILE | $XSV_SELECT $COLUMN | $COMPRESS > "${TEMPFILE1}.gz"

            echo -e "${green}XSV is separating ('exploding') URLs in $TEMPFILE1.${reset}"
            $DECOMPRESS $TEMPFILE1 | $XSV_EXPLODE $COLUMN "|" | $COMPRESS > "${TEMPFILE2}.gz"

            echo -e "${green}XSV is removing empty rows in $TEMPFILE2.${reset}"
            $DECOMPRESS $TEMPFILE2 | $XSV_SEARCH -s $COLUMN "." | $COMPRESS > "${TEMPFILE3}.gz"

            COUNT_RESULT=$($DECOMPRESS ${TEMPFILE3}.gz | xsv count)
            COUNT=" --count $COUNT_RESULT"

            return

    else
        echo -e "${green}XSV is extracting 'links' column in $1.${reset}"
        $XSV_SELECT -o $TEMPFILE1 $COLUMN $DATAFILE

        echo -e "${green}XSV is separating URLs in $TEMPFILE1.${reset}"
        $XSV_EXPLODE -o $TEMPFILE2 $COLUMN "|" $TEMPFILE1

        echo -e "${green}XSV is removing empty rows in $TEMPFILE2.${reset}"
        $XSV_SEARCH -s $COLUMN -o $TEMPFILE3 "." $TEMPFILE2

        COUNT_RESULT=$(xsv count $TEMPFILE3)
        COUNT=" --count $COUNT_RESULT"

        return
    fi
}

# ---------------------------------------------
#                MAIN SCRIPT
# ---------------------------------------------

mkdir -p data
mkdir -p temp

# ---------------------------------------------
#   PARSING OPTIONS
COLUMN="links"
while [ $# -gt 0 ]
do
    case "$1" in
        -f) options="$options $1"
            DATA="$2"
            shift
            ;;
        -h) options="$options $1"
            Help
            ;;
        --help) options="$options $1"
            Help
            ;;
        -s) options="$options $1"
            COLUMN="$2"
            shift
            ;;
        -o) options="$options $1"
            OUTPUT=" --output $2"
            shift
            ;;
        -l) options="$options $1"
            LOG=" --log $2"
            shift
            ;;
    esac
    shift
done

if [[ -z "$DATA" ]]
    then
    echo -e "${yellow}Error: A directory or a file must be the first argument positioned after the command.${reset}"
    exit
fi

Decompresser
# ---------------------------------------------
#   EXECUTING SCRIPT ON FILES IN DIRECTORY
if [ -d $DATA ]
    then
        for FILE in $DATA*.csv.gz; do
            GetBasename $FILE
            PreProcess $FILE
            echo "running python with options:${COUNT}${OUTPUT}${LOG}"
            python main.py ${FILE}${COUNT}${OUTPUT}${LOG}
        done

# ---------------------------------------------
#       EXECUTING SCRIPT ON SINGLE FILE
elif [ -f $DATA ] && [[ $DATA == *.csv ]] || [[ $DATA == *.csv.gz ]]
    then
        GetBasename $DATA
        PreProcess $DATA
        echo "running python with options:${COUNT}${OUTPUT}${LOG}"
        python main.py ${DATA}${COUNT}${OUTPUT}${LOG}

# ---------------------------------------------
#                  ERROR
else
    echo -e "${yellow}Error: The first argument must be either a directory or a CSV file. Only the '.gz' extension is permitted for compressed CSV files.${reset}"
    exit
fi
