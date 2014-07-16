#Hashtag Battle

This is a small, simple Django based web app that monitors the Twitter
Streaming API for any mentions of a set of hashtags. Hashtags are arranged by
the user of the app into a set of pairs, each referred to as a _battle_. These
are shown on the main and only page of the site with respective counts of how
many times the hashtag was mentioned in the twitter stream since the time at
which the battle began.

Above this list of battles, is a small form by which anyone can add a new
battle to the list.

## Simplifications/Hacks/Issues

The app currently assumes only a single user. It'd take some work to update it
to let multiple users authenticate with Twitter, using OAuth, and then
associate a set of battles to each user. But it could be done.

The CSS and JS for the app is a bit light at the moment. The battle creation
form could be hidden until the user wishes to create a new battle. The method
of updating the tweet counts is current just a page refresh, which is kind of a
jarring experience. A better one would hit an additional AJAX endpoint to get
an updated list of battles and counts, which would then be rendered to the page.
I'm sure there's even a web sockets approach that could take it a step further.

Also, there's some strings in the JS file that are given to JQuery to render a
new battle on the page once the creation endpoint returns. That design isn't
maintainable, especially as the HTML in the strings gets more sophisicated. I
could have employed a JS templating framework like mustache or handlebars, but
this works for this app.

I solved the communication between the frontend code and the backend script
using the database, which is kind of gross and isn't scalable. A more elegant
design would use some kind of message queue infrastructure. The front end needs
to communicate new hashtags to the backend, and updated counts need to flow in
the reverse direction. For simplicity, each gets stored in the database. The
backend queries and increments each count in the database, and it periodically
collects a list of the unique hashtags from it as well. As such, there's a bit
of a delay (currently set to a maximum of 3 minutes) before a new battle starts
getting filtered from the twitter stream.


## Dependencies
- Django (tested on 1.6)
- Tweepy (python twitter client)
- MySQL

## Setup

To configure the db, the _settings.py_ file will need to be updated to point to
the appropriate mysql server. The 'HOST' parameter of DATABASES dictionary, at
least, probably need to be updated. A database with the name _battle_, user
named _battle_, and password _battle123_ will need to be created on the server.
the SQL script in the sql directory must also be executed on the database prior
to starting the app.

Django comes with a test server that can be brought up with the following
command executed in the top level directory of the repo:

```
$ python manage.py runserver 0.0.0.0:8000
```

The parameter, `0.0.0.0:8000`, is optional, but a browser will only be able to
connect to `localhost:8000`. This binds to any address.