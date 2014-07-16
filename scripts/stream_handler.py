#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Processes the Twitter Streaming API in the background. At the moment, this
includes all the hashtags the entire system wants to monitor, which isn't
scalable. However, the set of all unique hashtags can be, with some work,
partitioned into groups and distributed to seperate threads/processes/servers
as needed.

This script also queries the database for all hashtags periodically, which is
really gross and inefficient. An improvement would be an implementation that
relied upon a message passing architecture like beanstalk or rabbitMQ, through
which new hashtags could be communicated from the front end to this script.

@author:     PJ

'''

import datetime
import json
import sys

from tweepy import OAuthHandler, Stream, StreamListener

sys.path.append(".")
from hashtag_django.models import BattleTag

consumer_key="2Jco11NCA9lbjSkgj4c7FKe4b"
consumer_secret="TnHsMeGwfrJjktmyF75TpTLqhI0Ikm4ClRptGePBfNz5imm41X"

access_token="11021-NYlMlnjeXs2GvWe21U46TGtZcLhdzXhgutX945wJr7Re"
access_secret="HUYc4nPHybzGRDYryyv1hXFjy9w6zTmCtoS5e3mvQpak1"

UPDATE_INTERVAL = datetime.timedelta(minutes=3)

class BattleUpdater(StreamListener):
    """ Interacts with a tweepy client and the Twitter Streaming API to receive
        and process relavant twee
    """
    def __init__(self):
        self.stream = None
        self.tags = []
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_secret)

        self.update_battles()
        self.update_time = datetime.datetime.now()

    def start(self):
        if len(self.tags) > 0:
            self.stream = Stream(self.auth, self)
            self.stream.filter(track=self.tags)

    def on_data(self, data):
        tweetDict = json.loads(data)
        for hashtagDict in tweetDict['entities']['hashtags']:
            tag = hashtagDict['text'].lower()

            if tag in self.tag_set:
                # This hashtag is one in a battle
                self.update_counts("#" + tag)
        if (datetime.datetime.now() - self.update_time > UPDATE_INTERVAL):
            if self.update_battles():
                self.stream.disconnect()
                self.stream = None
            self.update_time = datetime.datetime.now()
        return True

    def on_error(self, status):
        if status != 420:
            # 420 is the rate limit error. the client sleeps and retries
            # automatically. Print anything elses.
            print "ERROR: {0}".format(status)

    def on_closed(self, resp):
        print "CLOSED: {0}".format(resp)

    def on_exception(self, exc):
        print "EXCEPTION: {0}".format(exc)

    def update_counts(self, tag):
        for b_tag in BattleTag.objects.filter(tag=tag):
            b_tag.count += 1
            b_tag.save()

    def update_battles(self):
        """
          Checks to see if the length of in memory tags differs from the db
          count. If so, update the in memory tags, and return True to signal
          that the twitter connection needs to be restarted with the new
          set of hashtags upon which to filter.
        """
        if len(self.tags) == BattleTag.objects.values('tag').distinct(
                                                                    ).count():
            return False
        self.tags = []
        self.tag_set = set()
        for t in BattleTag.objects.values('tag').distinct():
            self.tags.append(t['tag'])
            self.tag_set.add(t['tag'][1:])
        return True

def main(argv=None): # IGNORE:C0111
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    updater = BattleUpdater()
    while True:
        # each time we need to reconnect, start() will finally return
        # so call it again
        updater.start()

if __name__ == "__main__":
    sys.exit(main())