import requests
import re
import urllib
from flask import Flask
from flask import jsonify

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return 'SkipBaitg'

# this is the route to access the meat of the application. you can test it with the following urls. 
# since the app consumes the url to skip as a url parameter, it is necessary to escape the url to skip.
# http://127.0.0.1:5000/skip/http%3A%2F%2Fwww.buzzfeed.com%2Fbradesposito%2Fno-pants-dance
# http://127.0.0.1:5000/skip/http%3A%2F%2Fsamjbrenner.com%2Fnotes%2Fmariah-careys-hand%2F
@app.route('/skip/<path:path>')
def skip_url(path):
	site_html = requests.get(urllib.unquote(path)).text
	sources = get_sources(site_html)

	return jsonify(sources = sources)

if __name__ == '__main__':
	app.run()

def get_sources(site_html):
	# here are example uris for embedded content to help build the regexes. currently, it seems like this
	# app will always have a bias towards what is considered a primary source - a factor of what sites I build 
	# regexes to identify. I can limit the bias by building a final regex that will check for all src attributes
	# of <iframe> tags, but this will throw a lot of false positives and miss a lot of actual primary sources.
	# it will be necessary to keep these regexes up-to-date with popular sources for stolen material.

	# vine
	# https://vine.co/v/MPu0Tq52wiv/card

	# youtube
	# https://www.youtube.com/watch?v=ZwfLgXJpQd0

	# vimeo
	# http://player.vimeo.com/video/55880815
	# http://vimeo.com/55880815

	vine_pattern = '(https?://(www\.)?vine.co/v/[A-Za-z0-9]+/?)'
	vine = re.finditer(vine_pattern, site_html)

	youtube_pattern = '(https?://(www\.)?youtube.com/watch\?v=[A-Za-z0-9]+)'
	youtube = re.finditer(youtube_pattern, site_html)

	vimeo_pattern = '(https?://(www\.)?(player\.)?vimeo.com/(video/)?[0-9]+)'
	vimeo = re.finditer(vimeo_pattern, site_html)

	sources = []

	if vine:
		for match in vine:
			sources.append(match.group(0))

	if youtube:
		for match in youtube:
			sources.append(match.group(0))

	if vimeo:
		for match in vimeo:
			sources.append(match.group(0))

	return sources