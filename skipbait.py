import requests
import re
import urllib
from flask import Flask
from flask import jsonify

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return 'SkipBait'

# this is the route to access the meat of the application. you can test it with the following urls. 
# since the app consumes the url to skip as a url parameter, it is necessary to escape the url to skip.
# http://127.0.0.1:5000/skip/http%3A%2F%2Fwww.buzzfeed.com%2Fbradesposito%2Fno-pants-dance
# http://127.0.0.1:5000/skip/http%3A%2F%2Fsamjbrenner.com%2Fnotes%2Fmariah-careys-hand%2F
@app.route('/skip/<path:path>')
def skip_url(path):
	site_url = urllib.unquote(path)
	site_html = requests.get(site_url).text
	sources = get_sources(site_html)

	return jsonify(sources = sources, original_url = site_url)

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

	# when building the patterns, be sure to name the entire url as a capture group
	# called <url> and the id of the embedded content as <id>. we will refer to the 
	# groups in get_sources_from_regex_search()
	vine_pattern = '(?P<url>(https?://(www\.)?vine.co/v/(?P<id>([A-Za-z0-9]+)/?)))'
	youtube_pattern = '(?P<url>(https?://(www\.)?youtube.com/watch\?v=(?P<id>([A-Za-z0-9]+))))'
	vimeo_pattern = '(?P<url>(https?://(www\.)?(player\.)?vimeo.com/(video/)?(?P<id>([0-9]+))))'

	patterns = [vine_pattern, youtube_pattern, vimeo_pattern]
	sources = []

	for pattern in patterns:
		# perform regex find
		find = re.finditer(pattern, site_html)

		# extract full string and store in array
		sources.extend(get_sources_from_regex_search(find))		

	return sources

def get_sources_from_regex_search(regex_search):
	sources = []
	ids = []
	
	for match in regex_search:
		# use the <id> capturing group to prevent duplicates
		id = match.group('id')

		if not (id in ids):
			ids.append(id)
			sources.append(match.group('url'))

	return sources