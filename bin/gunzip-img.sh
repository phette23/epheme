#!/usr/bin/env bash
# gunzip-img.sh
# unzip images which have .jpg or .png file extensions
# but are actually gzip'd
# usage: ./gunzip-img.sh [IMAGES_DIR]

# Strict Mode
set -eou pipefail

IMAGES_DIR="${1:-img}"

function mvAndUnzip () {
    mv "$1" "${1}.gz" && gunzip "${1}.gz" && echo "Unzipped ${1}"
}

function needs () {
    command -v "$1" >/dev/null || (echo "This script requires ${1}"; exit 1)
}

needs file
needs grep
needs gunzip

for img in ${IMAGES_DIR}/*.{jpg,png}
do
    file --mime-type "$img" | grep "application/x-gzip" && mvAndUnzip "$img"
done
