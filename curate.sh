#! /usr/bin/env bash

# Temperature log curator
# ./curate.sh {upperlimit}
# Allows you to set the max number of lines in your log
# Won't really use this yet, but will keep in place for now

LINECOUNT=$(wc -l templog.txt  | sed s/\ templog\.txt//g)
UPPERLIMIT=$1 # For 1 year of data, upper limit is 1051200 lines. That's about 35 Mb.

if [ -z "$UPPERLIMIT" ]; then
	UPPERLIMIT=$(echo "1051200")
fi


if [ $LINECOUNT -gt $UPPERLIMIT ]; then 
	tail -n $UPPERLIMIT templog.txt | cat > templog2.txt
	mv templog2.txt templog.txt 
	#No idea why, but it won't let direct write to templog so we use a temp and copy it over
	LINECOUNT=$(wc -l templog.txt  | sed s/\ templog\.txt//g)
	echo "Templog curated to $LINECOUNT lines."
else 
	echo "Templog has not exceeded limit of $UPPERLIMIT lines yet."
fi
