# vine
# https://vine.co/v/MPu0Tq52wiv/card

# youtube
# https://www.youtube.com/watch?v=ZwfLgXJpQd0

# vimeo
# http://player.vimeo.com/video/55880815
# http://vimeo.com/55880815

import requests
import re

# page = requests.get('http://www.buzzfeed.com/elliewoodward/victoria-beckham-and-samuel-l-jackson-so-awkward').text
page = requests.get('http://www.buzzfeed.com/bradesposito/no-pants-dance').text

vine_pattern = 'https?://[www\.]?vine.co/v/[A-Za-z0-9]+/'
vine = re.search(vine_pattern, page)

youtube_pattern = 'https?://[www\.]?youtube.com/watch\?v=[A-Za-z0-9]+'
youtube = re.search(youtube_pattern, page)

vimeo_pattern = 'https?://[www\.]?[player\.]?vimeo.com/[video/]?[0-9]+'
vimeo = re.search(vimeo_pattern, page)

if vine:
	print vine.group(0)

if youtube:
	print youtube.group(0)

if vimeo:
	print vimeo.group(0)