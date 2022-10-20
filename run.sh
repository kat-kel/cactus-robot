#!/bin/bash

# ---------------------------------------------
#                  COLOR
# ---------------------------------------------
# Color codes for console messages.
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
#                  ARGUMENTS
# ---------------------------------------------

# Set variables
DATA=""
OUTPUT=""
LOG=""
LENGTH="0"

# ---------------------------------------------
#                  COUNT CSV
# ---------------------------------------------
Count()
{
    if [[ $DATA == *.gz ]]
    then
        if [[ $(uname -s) == "Darwin" ]];
        then 
            LENGTH=`gzcat $DATA | xsv count`
        else
            LENGTH=`zcat $DATA | xsv count`
        fi

    elif [[ $DATA == *.csv ]]
    then
        LENGTH=`xsv count $DATA`

    fi
}

# ---------------------------------------------
#                  MAIN SCRIPT
# ---------------------------------------------

if [ $# -gt 0 ] && [ -e $1 ]
    then
        DATA=$1
        Count
        shift
    else
        echo -e "${red}Error: A valid data file is required as the first argument positioned after run.sh${reset}"
        echo
        exit

fi

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


if [ $OUTPUT ]
then
    OUTPUT_OPTION="--output $OUTPUT"
else
    OUTPUT_OPTION=""
fi

if [ "$LOG" ]
then
    LOG_OPTION="--log $LOG"
else
    LOG_OPTION=""
fi

`python main.py $DATA --count $LENGTH $OUTPUT_OPTION $LOG_OPTION`