# Example - display images from mongo's "images" collection

It's a bit contrived & perhaps too much set up for such a simple result, but just as a demonstration:

- run `./epheme.py '#ccarts'` to get some tweets & downloaded images (or insert your own search term & change [the `db` var](https://github.com/phette23/epheme/blob/master/example/index.html#L11) in index.html)
    + either target the images directory in here with `-i example/img` or symlink the "img" dir alongside this example
- enable Mongo's JSONP API (see [included mongo.conf](https://github.com/phette23/epheme/blob/master/mongod.conf), uncomment the final section)
- run `./start.py` in this directory to start a local web server & open your browser to the index.html included here

You should see a long, vertical set of images you've downloaded from Twitter.
