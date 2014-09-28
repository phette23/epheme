#!/usr/bin/env python
"""
Making Twitter ever so slightly less ephemeral.

Archive metadata of tweets containing a particular search string, such as a
hashtag. Download any native Twitter images (not links to images) in tweets.
"""
import twarc  # https://github.com/edsu/twarc
# http://api.mongodb.org/python/2.7.2/
from pymongo import MongoClient
from pymongo import errors
import os
import requests
import shutil
import argparse


class Epheme:

    """ Class for storing tweets & images.

    The class is a set of tools around a particular Twitter search
    for storing matching tweet JSON in mongo, noting any images, &
    downloading image files to images_dir.
    """

    def __init__(self, text, images_dir):
        """ Initialize Epheme & then kick off the twarc search. """
        # store tweet JSON in a db with same name as search text
        self.db = MongoClient()[text.replace(' ', '_')]
        self.images_dir = images_dir
        self.hashtag = text

        print 'Beginning to search Twitter API for', self.hashtag
        # note: first run through is a special case, most_recent_id()
        # returns None & twarc will return a bunch of recent tweets
        # then start stepping backwards in time. It's limited by the
        # Search API in that it cannot go back that far, a couple of
        # weeks is the limit I think.
        for tweet in twarc.search(self.hashtag,
                                  since_id=self.most_recent_id()):
            try:
                self.insert_tweet_into_db(tweet)
            # tweet already in db
            except errors.DuplicateKeyError:
                print 'Skipping duplicate Tweet', tweet['id']
                continue

        # done getting all the metadata? now grab the referenced images
        self.download_all_imgs()
        print 'Done searching Twitter for', self.hashtag, '& downloading images.'

    def most_recent_id(self):
        """ Return most recent id from mongo. """
        # http://stackoverflow.com/questions/14432862/how-to-get-the-document-with-max-value-for-a-field-with-map-reduce-in-pymongo
        mrt = self.db.tweets.find_one(sort=[("_id", -1)])

        # on first execution there'll be no tweets, so mrt is null
        # None is twarc's "since_id" default, so this works
        if mrt is None:
            return None

        print 'Starting from Tweet', mrt['_id']
        return mrt['_id']

    def insert_tweet_into_db(self, tweet):
        """ Insert tweet from twarc.search into db. """
        # mongo expects an '_id' primary key, let's use the logical one
        tweet['_id'] = tweet['id']
        print 'Inserted Tweet', tweet['_id']
        self.db.tweets.insert(tweet)
        self.img_url_into_db(tweet)

    def img_url_into_db(self, tweet):
        """
        If tweet has a photo attached, note that so we can download it later.

        Uses a 2nd collection in database, images.
        """
        if 'media' in tweet['entities']:
            for media in tweet['entities']['media']:
                if media['type'] == 'photo':
                    self.db.images.insert({
                        '_id': media['id'],
                        'url': media['media_url'],
                        'downloaded': False
                    })

    def download_all_imgs(self):
        """ Download all images marked as not downloaded. """
        # get all images that haven't been downloaded
        imgs = self.db.images.find({'downloaded': False})
        for img in imgs:
            success = self.download_img(img['url'])
            if success:
                self.db.images.update({'_id': img['_id']},
                                      {'$set': {
                                          "downloaded": True
                                      }
                    # don't insert if doesn't already exist
                }, upsert=False)

    def download_img(self, url):
        """
        Download single image into images_dir.

        Returns a boolean indicating whether the download was successful or not.
        """
        filename = url.split('/')[-1]
        dest = os.path.join(self.images_dir, filename)
        # http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(dest, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
                print 'Downloaded image from', url, 'to', dest
                return True
        else:
            # @todo should note failure in db.images
            # otherwise we'll just perpetually try to download
            # the image over & over, always failing
            print 'ERROR: HTTP Response != 200 from', url
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('text', help='string to use in the Twitter search API')
    parser.add_argument('-i', '--images', help='directory to place downloaded'
                        + ' images in', default='img')

    args = parser.parse_args()

    # kick things off
    archive = Epheme(args.text, args.images)
