#!/usr/bin/env bash
# runs every two minutes
echo '*/2 * * * * python /epheme.py -d "#ccarts" "#ccarts"' | crontab -
