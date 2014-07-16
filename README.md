#Hashtag Battle

This is a small, simple Django based web app that monitors the Twitter
Streaming API for any mentions of a set of hashtags. Hashtags are arranged by
the user of the app into a set of pairs, each referred to as a _battle_. These
are shown on the main and only page of the site with respective counts of how
many times the hashtag was mentioned in the twitter stream since the time at
which the battle began.

Above this list of battles, is a small form by which anyone can add a new
battle to the list.

## Simplifications/Hacks


## Dependencies
- Django (tested on 1.6)
- Tweepy (python twitter client)

## Setup
