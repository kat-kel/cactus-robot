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
    # Display help
    echo
    echo "This program will download a CSV file of tweets gathered with gazouilloire, "
    echo "clean and analyze links published in those tweets, and output the results of"
    echo "that analysis in a CSV file."
    echo
    echo "Syntax: run.sh f [-h|-o|-l]"
    echo
    echo "positional argument:"
    echo "f     path to the data file"
    echo
    echo "options:"
    echo "h     print this help"
    echo "o     path to the file in which the results will be sent"
    echo "l     path to file in which any errors will be logged"
    echo
    exit
}


# ---------------------------------------------
#                  VARIABLES
# ---------------------------------------------

mkdir -p data

# Set variables
DATA=""
OUTPUT=""
LOG=""
LENGTH="0"

# Temp files
TEMPFILE1="data/tempfile1.csv.gz"
TEMPFILE2="data/tempfile2.csv.gz"
TEMPFILE3="data/tempfile3.csv.gz"

# XSV commands
SELECT_COLUMN="xsv select"
EXPLODE_COLUMN="xsv explode"
SEARCH_COLUMN="xsv search -s"


# ---------------------------------------------
#                  PREPARE DATA
# ---------------------------------------------
OperatingSystem()
{
    if [[ $(uname -s) == "Darwin" ]];
        then
            DECOMPRESS="gzcat"
            COMPRESS="gzip"
        else
            DECOMPRESS="zcat"
            COMPRESS="gzip" # not sure if this works
    fi
}

Count()
{
    if [[ "$DATA" == *.gz ]]; then

        echo
        echo -e "${yellow}(step 1/3) Extracting 'links' column from zipped file --> ${TEMPFILE1}${reset}"
        $DECOMPRESS $DATA | $SELECT_COLUMN "links" | $COMPRESS > $TEMPFILE1
        echo -e "${green}    Finished.${reset}"

        echo
        echo -e "${yellow}(step 2/3) Exploding into separate rows the links that are listed together in one row --> ${TEMPFILE2}${reset}"
        $DECOMPRESS $TEMPFILE1 | $EXPLODE_COLUMN "links" "|" | $COMPRESS > $TEMPFILE2
        rm $TEMPFILE1
        echo -e "${green}    Finished.${reset}"

        echo
        echo -e "${yellow}(step 3/3) Filtering out empty rows --> ${TEMPFILE3}${reset}"
        $DECOMPRESS $TEMPFILE2 | $SEARCH_COLUMN "links" "." | $COMPRESS > $TEMPFILE3
        rm $TEMPFILE2
        echo -e "${green}    Finished.${reset}"

        LENGTH=$($DECOMPRESS $TEMPFILE3 | xsv count)

        return

    elif [[ "$DATA" == *.csv ]]
    then
        TEMPFILE3=$DATA
        LENGTH=$(xsv count $TEMPFILE3)

        return

    else
        echo
        echo -e "${red}File not valid.${reset}"
        exit

    fi
}

# ---------------------------------------------
#                  MAIN SCRIPT
# ---------------------------------------------

# Parse first positional argument (the data file)
if [ $# -gt 0 ] && [ -e $1 ]
    then
        DATA=$1
        shift
    else
        echo -e "${red}Error: A valid data file is required as the first argument positioned after run.sh${reset}"
        echo
        exit

fi

# Parse optional arguments (the output file, the log file)
while [ $# -gt 0 ]
do
    case "$1" in
        -h) options="$options $1"
            Help
            ;;
        --help) options="$options $1"
            Help
            ;;
        -o) options="$options $1"
            OUTPUT="$2"
            shift
            ;;
        -l) options="$options $1"
            LOG="$2"
            shift
            ;;
    esac
    shift
done

# Prepare arguments to be passed to command line
if ! [ -z "$OUTPUT" ]
then
    OUTPUT_OPTION=" --output data/${OUTPUT}"
else
    OUTPUT_OPTION=""
fi

if ! [ -z "$LOG" ]
then
    LOG_OPTION=" --log data/${LOG}"
else
    LOG_OPTION=""
fi

# Prepare data for processing
echo
echo "------- Preparing Gazoulloire data set for processing -------"
OperatingSystem
Count

# Launch the Python script with command-line arguments
echo
echo "------- Processing data -------"
echo
python main.py $TEMPFILE3 --count ${LENGTH}${OUTPUT_OPTION}${LOG_OPTION}

# Clean up
if [ "$?" -eq 0 ]; then rm $TEMPFILE3
fi
echo
echo -e "${green}Program finished processing data file ${DATA}.\nTemporary files successfully deleted.${reset}"
echo
