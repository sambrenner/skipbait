SkipBait
=========

SkipBait is a webservice and browser extension that allows clickbait to be skipped over in daily web browsing.

Sites like BuzzFeed and HuffPo use bombastic headlines and thumbnail images as bait to lure you towards embedded content so they can collect data on you and serve you ads. SkipBait bypasses this, meaning that links containing clickbait are redirected straight to the primary source (where you will likely encounter more ads and trackers, but that's for a different project to handle).

SkipBait pairs well with ad blockers, tracker blockers, and script blockers. SkipBait is created and maintained by [Sam Brenner](http://samjbrenner.com).

Why?
---
We need to demand more of online media outlets. If BuzzFeed and HuffPo want to be seen as legitimate journalists, they need to start acting responsibly in selecting, distributing and presenting content.

We also need to demand more of ourselves, as media consumers and sharers, to be aware of when we are being manipulated by media outlets.

These points address much larger issues than this project can solve, but I hope this helps create a conversation that will push us in the right direction.

About
---
This repo contains the source code for the SkipBait server. There are separate repos for the Chrome and Firefox extensions.

###Using SkipBait
SkipBait is currently online on [Heroku](https://skipbait.herokuapp.com/). To use the server, hit the `/skip/<path>` endpoint, where `<path>` is a [percent-encoded](https://en.wikipedia.org/wiki/Percent-encoding) string referring to the URL you want to skip. The server will return a JSON object containing an array of URLs to primary sources, or an empty array if nothing was found.

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

###How it's made
SkipBait is built on [Python](https://www.python.org/) with [Flask](http://flask.pocoo.org/).

###Running your own SkipBait server
The server code is ready to deploy to as your own Heroku application. To do this: