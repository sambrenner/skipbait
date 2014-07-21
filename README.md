SkipBait
=========

SkipBait is a webservice and browser extension that allows clickbait to be skipped over in daily web browsing.

Sites like BuzzFeed and HuffPo use bombastic headlines and thumbnail images as bait to lure you towards embedded content so they can collect data on you and serve you ads. SkipBait bypasses this, meaning that links containing clickbait are redirected straight to the primary source (where you will likely encounter more ads and trackers, but that's for a different project to handle).

SkipBait pairs well with ad blockers, tracker blockers, and script blockers. SkipBait is created and maintained by [Sam Brenner](http://samjbrenner.com).

Download
---
SkipBait clients are currently available for Chrome and Firefox.

Why?
---
We need to demand more of online media outlets. If BuzzFeed and HuffPo want to be seen as legitimate journalists, they need to start acting responsibly in selecting, distributing and presenting content.

We also need to demand more of ourselves, as media consumers and sharers, to be aware of when we are being manipulated by media outlets.

These points address much larger issues than this project can solve, but I hope this helps create a conversation that will push us in the right direction.

About
---
###Source code
There are separate repos for the [SkipBait Server](https://github.com/sambrenner/skipbait), the [Chrome Extension](https://github.com/sambrenner/skipbait-chrome) and the Firefox Add-on.

###Using the SkipBait server
SkipBait is currently online via [Heroku](https://skipbait.herokuapp.com/). To use the server, hit the `/skip/<path>` endpoint, where `<path>` is a [percent-encoded](https://en.wikipedia.org/wiki/Percent-encoding) string referring to the URL you want to skip. The server will return a JSON object containing an array of URLs to primary sources, or an empty array if nothing was found.

For example, hitting the url

```
https://skipbait.herokuapp.com/skip/http%3A%2F%2Fwww.buzzfeed.com%2Fexpresident%2Fmaru-is-at-it-again%2330cfv3
```

Returns

```json
{
  "original_url": "http://www.buzzfeed.com/expresident/maru-is-at-it-again#30cfv3", 
  "sources": [
    "http://youtube.com/watch?v=lTwq3I_sqNI"
  ]
}
```

###Running your own SkipBait server
The server code is ready to deploy to as your own Heroku application. To do so:

1. Clone this repo: `git clone https://github.com/sambrenner/skipbait.git`
2. Create an account on [Heroku](http://heroku.com) and download the [Toolbelt](https://toolbelt.heroku.com/)
3. `cd skipbait/`
4. `heroku apps:create your-app-name` (This should automatically add the `heroku` remote to Git. You might have to log in to Heroku if this is your first time using the toolbelt.)
5. `heroku addons:add memcachier:dev` (SkipBait should theoretically work with any cache provider thanks to [flask-heroku-cacheify](https://github.com/rdegges/flask-heroku-cacheify) but I've only tested with MemCachier.)
6. `git push heroku master`
7. Your server will now be available at `http://your-app-name.herokuapp.com`.

###How it works
SkipBait is built on [Python](https://www.python.org/) with [Flask](http://flask.pocoo.org/).

When you send a URL to SkipBait, the application will first check its cache to see if it has already identified sources on the URL. If not, the application will load the HTML of the website (using [Requests](http://docs.python-requests.org/en/latest/)) and will then search the HTML for [regular expressions](https://en.wikipedia.org/wiki/Regular_expression) that match URLs of websites often used as sources for clickbait articles (like YouTube, Twitter and Vine).
