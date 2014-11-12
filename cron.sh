#!/usr/bin/env bash

# sample cron job script for epheme
# example crontab line:
# * 1 * * * * /path/to/epheme/cron.sh
# (to run every hour)

# stop on errors
set -eo pipefail

# NOTE: we assume mongod is already running
# if it's not, we could spin up the daemon here

LOGFILE="/var/log/epheme.log"

# enter epheme's dir
cd "/path/to/epheme"

# activate virtual env
source bin/activate

# replace with your Twitter API credentials
export CONSUMER_KEY=abcdefgh12345678abcedefgh
export CONSUMER_SECRET=abcdefgh12345678abcedefgh
export ACCESS_TOKEN=abcdefgh12345678abcedefgh
export ACCESS_TOKEN_SECRET=abcdefgh12345678abcedefgh

# replace with your search, database, & images directory
# can run epheme multiple times here, storing in same db if desired
# NOTE: lo-fi logging with no log file roll over
echo -e "$(date)\trunning epheme" >> "$LOGFILE"
python epheme.py '#search term' -d 'database' -i "/path/to/images/dir" >> "$LOGFILE"
