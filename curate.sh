#! /usr/bin/env bash

# Temperature log curator
# ./curate.sh {upperlimit}
# Allows you to set the max number of lines in your log
# Won't really use this yet, but will keep in place for now

LINECOUNT=$(wc -l datalog.txt  | sed s/\ datalog\.txt//g)
UPPERLIMIT=$1 # For 1 year of data, upper limit is 1051200 lines. That's about 35 Mb.

if [ -z "$UPPERLIMIT" ]; then
	UPPERLIMIT=$(echo "1051200")
fi


if [ $LINECOUNT -gt $UPPERLIMIT ]; then 
	tail -n $UPPERLIMIT datalog.txt | cat > datalog2.txt.txt
	mv datalog2.txt datalog.txt 
	#No idea why, but it won't let direct write to datalog so we use a temp and copy it over
	LINECOUNT=$(wc -l datalog.txt  | sed s/\ datalog\.txt//g)
	echo "Datalog curated to $LINECOUNT lines."
else 
	echo "Datalog has not exceeded limit of $UPPERLIMIT lines yet."
fi
