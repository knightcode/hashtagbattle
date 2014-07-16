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
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_secret)

        self.update_battles()
        self.update_time = datetime.datetime.now()

    def start(self):
        self.stream = Stream(self.auth, self)
        if len(self.tags) > 0:
            self.stream.filter(track=self.tags)

    def on_data(self, data):
        tweetDict = json.loads(data)
        for hashtagDict in tweetDict['entities']['hashtags']:
            tag = hashtagDict['text'].lower()

            if tag in self.tag_set:
                # This hashtag is one in a battle
                print str(tag)
                self.update_counts("#" + tag)
        if (datetime.datetime.now() - self.update_time > UPDATE_INTERVAL):
            self.stream.disconnect()
            self.update_battles()
            if len(self.tags) > 0:
                self.stream.filter(track=self.tags)
            self.update_time = datetime.datetime.now()
        return True

    def on_error(self, status):
        print "ERROR: {0}".format(status)

    def update_counts(self, tag):
        for b_tag in BattleTag.objects.filter(tag=tag):
            b_tag.count += 1
            b_tag.save()

    def update_battles(self):
        self.tags = []
        self.tag_set = set()
        for t in BattleTag.objects.values('tag').distinct():
            print "tag: {0}".format(t['tag'][1:])
            self.tags.append(t['tag'])
            self.tag_set.add(t['tag'][1:])

def main(argv=None): # IGNORE:C0111
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    updater = BattleUpdater()
    updater.start()

if __name__ == "__main__":
    sys.exit(main())