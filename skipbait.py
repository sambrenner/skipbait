import requests
import re
import urllib
from flask import Flask, jsonify, render_template
from flask.ext.cacheify import init_cacheify
from flask.ext.misaka import Misaka

app = Flask(__name__)
app.debug = True
Misaka(app)
cache = init_cacheify(app)

@app.route('/')
def index():
	# render README.md as index page. Misaka handles .md parsing in template
	with app.open_resource('README.md') as r:
		contents = r.read()
		return render_template('layout.html', markdown_text=contents)

# this is the route to access the meat of the application. you can test it with the following urls. 
# since the app consumes the url to skip as a url parameter, it is necessary to escape the url to skip.
# http://127.0.0.1:5000/skip/http%3A%2F%2Fwww.buzzfeed.com%2Fbradesposito%2Fno-pants-dance
# http://127.0.0.1:5000/skip/http%3A%2F%2Fsamjbrenner.com%2Fnotes%2Fmariah-careys-hand%2F
@app.route('/skip/<path:path>')
def skip_url(path):
	encoded_path = path
	site_url = urllib.unquote(path)

	sources = cache.get(encoded_path)

	if not sources:
		site_html = requests.get(site_url).text
		sources = get_sources(site_html)
		cache.set(encoded_path, sources)

	return jsonify(sources = sources, original_url = site_url)

if __name__ == '__main__':
	app.run()

def get_sources(site_html):
	# currently, it seems like this app will always have a bias towards what is considered
	# a primary source - a factor of what sites I build regexes to identify. I can limit the bias
	# by building a final regex that will check for all src attributes of <iframe> tags, but this
	# will throw a lot of false positives and miss a lot of actual primary sources. it will be
	# necessary to keep these regexes up-to-date with popular sources for stolen material.

	# when building the patterns, be sure to name the entire url as a capture group
	# called <url> and the id of the embedded content as <id>. we will refer to the 
	# groups in get_sources_from_regex_search()
	vine_pattern = '(?P<url>(https?://(www\.)?vine\.co/v/(?P<id>([A-Za-z0-9]+))/?))'
	youtube_pattern = '(?P<url>(https?://(www\.)?youtube\.com/watch\?v=(?P<id>([[a-zA-Z0-9_-]{11}))))'
	vimeo_pattern = '(?P<url>(https?://(www\.)?(player\.)?vimeo\.com/(video/)?(?P<id>([0-9]+))))'
	instagram_pattern = '(?P<url>(https?://(www\.)?instagram\.com/p/(?P<id>([A-Za-z0-9]+))/?))'
	twitter_pattern = '(?P<url>(https?://(www\.)?twitter\.com/[A-Za-z0-9]+/status/(?P<id>([0-9]+))))'
	reddit_comment_thread_pattern = '(?P<url>(https?://(www\.)?reddit\.com/r/[A-Za-z0-9]+/comments/[A-Za-z0-9]+/[a-z0-9_]+/(?P<id>([A-Za-z0-9]+))))'
	flickr_pattern = '(?P<url>(https?://(www\.)?flickr\.com/photos/[A-Za-z0-9]+/(?P<id>([0-9]+))(/in/photostream/?)?))'
	imgur_album_pattern = '(?P<url>(https?://(www\.)?imgur\.com/gallery/(?P<id>([A-Za-z0-9]+))))'
	imgur_image_pattern = '(?P<url>(https?://(www\.)?(i\.)?imgur\.com/(?P<id>([A-Za-z0-9]+))\.(jpg|gif|png|jpeg)))'
	tumblr_pattern = '(?P<url>(https?://(www\.)?([A-Za-z0-9\-]+)\.tumblr\.com/post/(?P<id>([0-9]+/[A-Za-z0-9\-]+))))'

	patterns = [vine_pattern, youtube_pattern, vimeo_pattern, instagram_pattern, twitter_pattern, reddit_comment_thread_pattern, flickr_pattern, imgur_image_pattern, imgur_album_pattern, tumblr_pattern]
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