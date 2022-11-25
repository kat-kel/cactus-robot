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
    echo "This program parses URLS in datasets conforming to Twitter API's export and/or"
    echo "Gazouilloire, a collection tool from Science Po's médialab. It extracts URLs"
    echo "from the collection and yields a CSV file with metadata about valid, active URLs."
    echo "The program can either (a) accept a zipped or open CSV file directly or (b) a "
    echo "a directory containing zipped files. (Zipped files must have extension '.gz')"
    echo
    echo "Twitter and Gazouilloire store tweet IDs in the column 'id' and media links in the"
    echo "column 'links'. By default, the program will search these two columns. If you want"
    echo "to work with a CSV file with different column headers for the ID and URL, use the"
    echo "option -s followed by 2 arguments: the ID header name, the URL column name."
    echo
    echo "Example"
    echo "./run.sh -f datafile.csv -s my_ids my_links"
    echo
    echo "Syntax: run.sh [-f|-s|-o|-l|-h]"
    echo
    echo
    echo "options:"
    echo "f     path to the data file or directory [required]"
    echo "s     name of the ID column and URL column"
    echo "o     path to the file in which the results will be sent"
    echo "l     path to file in which any errors will be logged"
    echo "h     print this help"
    echo
    echo
    exit
}

# ---------------------------------------------
#         PRE-PROCESS & COUNT DATA
# ---------------------------------------------

TEMPFILE1="preprocessing/temp_links-only.csv"
TEMPFILE2="preprocessing/temp_exploded-links.csv"

XSV_SELECT="xsv select"
XSV_EXPLODE="xsv explode"
XSV_SEARCH="xsv search"

GetBasename() # parameter: file path
{
    if [[ $1 == *.csv ]]; then
        BASENAME=$(basename $1 .csv)
    elif [[ $1 == *.csv.gz ]]; then
        BASENAME=$(basename $1 .csv.gz)
    fi
}

Decompresser()
{
    if [[ $(uname -s) == "Darwin" ]]; then
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
    TEMPFILE3="preprocessing/${BASENAME}_id-links.csv"

    if [[ ${DATAFILE} == *.gz ]]; then
        echo -e "${bold}XSV is extracting the columns '${IDCOL}' and '${LINKCOL}' in $DATAFILE.${reset}"
        $DECOMPRESS $DATAFILE | $XSV_SELECT ${IDCOL},${LINKCOL} | $COMPRESS > "${TEMPFILE1}.gz"
        XSVErrorEscape

        echo -e "${bold}XSV is separating ('exploding') URLs in $TEMPFILE1.${reset}"
        $DECOMPRESS $TEMPFILE1 | $XSV_EXPLODE $LINKCOL "|" | $COMPRESS > "${TEMPFILE2}.gz"
        XSVErrorEscape

        echo -e "${bold}XSV is removing empty rows in $TEMPFILE2.${reset}"
        $DECOMPRESS $TEMPFILE2 | $XSV_SEARCH -s $LINKCOL "." | $COMPRESS > "${TEMPFILE3}.gz"
        XSVErrorEscape

        echo -e "${bold}XSV is counting the number of rows in $TEMPFILE3.${reset}"
        COUNT_RESULT=$($DECOMPRESS ${TEMPFILE3}.gz | xsv count)
        XSVErrorEscape
        COUNT=" --count $COUNT_RESULT"

        # Clean up
        rm "${TEMPFILE1}.gz" "${TEMPFILE2}.gz"

        return

    else
        echo -e "${bold}XSV is extracting the columns '${IDCOL}' and '${LINKCOL}' in $1.${reset}"
        $XSV_SELECT -o $TEMPFILE1 ${IDCOL},${LINKCOL} $DATAFILE
        XSVErrorEscape

        echo -e "${bold}XSV is separating URLs in $TEMPFILE1.${reset}"
        $XSV_EXPLODE -o $TEMPFILE2 $LINKCOL "|" $TEMPFILE1
        XSVErrorEscape

        echo -e "${bold}XSV is removing empty rows in $TEMPFILE2.${reset}"
        $XSV_SEARCH -s $LINKCOL -o $TEMPFILE3 "." $TEMPFILE2
        XSVErrorEscape

        echo -e "${bold}XSV is counting the number of rows in $TEMPFILE3.${reset}"
        COUNT_RESULT=$(xsv count $TEMPFILE3)
        XSVErrorEscape
        COUNT=" --count $COUNT_RESULT"

        # Clean up
        rm $TEMPFILE1 $TEMPFILE2

        return

    fi

}

XSVErrorEscape()
{
    status="$?"
    if [ $status -ne 0 ]; then 
        echo -e "${yellow}XSV encountered an error.${reset}" 
        echo -e "${red}The program has exited.${reset}"
        exit
    else
        echo -e "    ${green}Success.${reset}"
    fi
}

ParseColumnNames()
{
    if [ $# -lt 2 ]; then
        echo -e "${red}Error: Please include 2 arguments after the option -s.${reset}"
        exit
    fi

    ARGID=$1
    ARGLINK=$2

    if [ "${ARGID:0:1}" == "-" ]; then
        echo -e "${red}Error: No argument given to declare the ID column. After the -s option, please include 2 arguments separated by a single space.${reset}"
        exit
    else
        IDCOL=$1
        ID_OPTION=" --id ${IDCOL}"
    fi

    # Works when reversed. Figure out why.
    if [ "${ARGLINK:0:1}" == "-" ]; then
        echo -e "${red}Error: No argument given to declare the links column. After the -s option, please include 2 arguments separated by a single space.${reset}"
        exit
    else
        LINKCOL=$2
        LINKS_OPTION=" --links ${LINKCOL}"
    fi

}

# ---------------------------------------------
#               MAIN PROCESS
# ---------------------------------------------
Process()
{
    echo -e "\n----------------------------------------"
    if [ -f $1 ] && [[ $1 == *.csv ]] || [[ $1 == *.csv.gz ]]; then
        echo -e "Working on file ${inverted}${1}${reset}."
        GetBasename $1
        PreProcess $1
        if [ $DIR ]; then
            OUTPUT=""
            LOG=""
        fi
        echo "running python script with options: ${1}${ID_OPTION}${LINKS_OPTION}${COUNT}${OUTPUT}${LOG}"
        python dummy.py ${1}${ID_OPTION}${LINKS_OPTION}${COUNT}${OUTPUT}${LOG}
    else
        echo -e "Skipping ${inverted}${1}${reset} because it is not a CSV file."
    fi
}

# ---------------------------------------------
#                MAIN SCRIPT
# ---------------------------------------------

mkdir -p preprocessing
IDCOL="id"
LINKCOL="links"

# ---------------------------------------------
#   PARSING OPTIONS
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
            ParseColumnNames $2 $3
            shift
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

if [ -d $DATA ]; then DIR=$DATA
elif [ -f $DATA ] && [[ $DATA == *.csv ]] || [[ $DATA == *.csv.gz ]]; then FILE=$DATA
else
    echo -e "${yellow}Error: The first argument must be either a directory or a CSV file. Only the '.gz' extension is permitted for compressed CSV files.${reset}"
    exit
fi

if [ $FILE ]; then Process $FILE
else
    for FILE in $DIR*; do
        Process $FILE
    done
fi
