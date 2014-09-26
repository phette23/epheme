# epheme

Small archiving project using [twarc](https://github.com/edsu/twarc) & MongoDB to retain Twitter metadata & download native (not linked) images.

```
usage: epheme.py [-h] [-i IMAGES] text

positional arguments:
  text                  string to use in the Twitter search API

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGES, --images IMAGES
                        directory to place downloaded images in
```

Images directory defaults to "img".

The functionality built on top of twarc is modest but I'm specifically interested in grabbing images from Twitter. Setting epheme to run regularly (e.g. with cron) lets me continually archive search results, related images, & use mongo's API to display them. There's a small example included here.

## Setup

Requires virtualenv & mongodb. On a Mac with homebrew, you can get these with `sudo pip install virtualenv; brew install mongodb`.

```sh
# set up virtual env in the project root, activate, install dependencies
virtualenv .
source bin/activate
pip install -r requirements.txt 
# set OAUTH keys for Twitter in shell ENV
export CONSUMER_KEY abcdefgh12345678abcedefgh
# same for CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET…
# start mongo, run daemon in the background
# the included config file isn't necessary, just a convenience
mongod --config mongod.conf &
```

## To Do

- [x] example - use mongo REST API to display wall of images
- [ ] mongo indexing wherever the db get queried
- [ ] logging of some sort? Can always pipe output to a file
