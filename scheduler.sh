#! /usr/bin/env bash

sudo ./daemon.sh > /dev/null 2>&1


touch templog.txt # Our logfile
touch currentcron # Cron tempfile

# Append this new job to existing cron list
if crontab -l; then
	crontab -l  > currentcron
fi

if grep -q "$PWD/measure.py" currentcron; then
	echo "Measuring job already scheduled"
else
	# Working around crontab's 1-minute time resolution
	echo "* * * * * $PWD/measure.py >> $PWD/templog.txt" >> currentcron
	echo "* * * * * (sleep 30; $PWD/measure.py >> $PWD/templog.txt)" >> currentcron
	crontab currentcron
	echo "Measuring job added to cron"
fi




rm currentcron


# TODO: Possibly add a curator script to the cronjob
# TODO: And also add app.py IF it's not already on.
