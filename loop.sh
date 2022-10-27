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
#                  MAIN SCRIPT
# ---------------------------------------------

# Parse first positional argument (the directory of files)
if [ $# -gt 0 ] && [ -d $1 ]
    then
        DIR=$1
        shift
    else
        echo -e "${red}Error: Please enter a valid directory containing the data.${reset}"
        echo
        exit
fi

for FILE in $DIR*.gz; do
    # Get the last part of the file name
    IFS="/"
    long_array=($FILE)
    unset IFS;
    FULL_FILENAME=${long_array[1]}

    IFS="."
    short_array=($FULL_FILENAME)
    unset IFS;
    FILENAME=${short_array[0]}

    # Set the names of the output files
    OUTPUT="${FILENAME}_output.csv"
    LOG="${FILENAME}_log.csv"

    ./run.sh $FILE -o $OUTPUT -l $LOG

done
