# epheme

Small Twitter archiving project using [twarc](https://github.com/edsu/twarc) & MongoDB.

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

## Setup

Requires virtualenv & mongodb. On a Mac, you can get these with `sudo pip install virtualenv; brew install mongodb`.

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

- [ ] example - use mongo REST API to display wall of images
- [ ] mongo indexing wherever the db get queried
- [ ] logging of some sort? Can always just pipe command's output to a file
