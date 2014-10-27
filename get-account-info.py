#!/usr/env python
# -*- coding: utf-8 -*-
#
# twitter_info.py
# ---------------

# TODO: 2014-10-24 chokes on InsaneCastleBot & HexagonBot for some reason? With:
# TypeError: sequence item 3: expected string or Unicode, NoneType found

import codecs
import sys
import os
from twython import Twython
from ttp import utils

# TODO: you fill these in!!
# Based on (and indebted to) @thricedotted's original script
# https://gist.github.com/thricedotted/b6eb938059ca3d69f886
# Modified by way of http://stackoverflow.com/questions/10580220/read-text-in-a-file-to-check-environment-variables

api_key = os.getenv('TWITTER_API_KEY')
api_secret = os.getenv('TWITTER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

input_file = sys.argv[1]
output_file = sys.argv[2]

with codecs.open(input_file, encoding='utf-8') as f:
    screen_names = [l.strip() for l in f.readlines()]

with codecs.open(output_file, 'w', encoding='utf-8') as f:
    f.write(
        'screen_name,id,location,expanded_url,created_at,client,client_url\n')

twitter = Twython(api_key, api_secret, access_token, access_token_secret)

for i in range(0, len(screen_names), 100):
    names = ','.join(screen_names[i:i + 100])

    print('Getting info for: {}'.format(names))

    users = twitter.lookup_user(screen_name=names)

    for user in users:
        screen_name = user['screen_name']
        id = user['id_str']
        location = user['location']
        try:
            expanded_url = user['entities']
            # looks like {u'url': {u'urls': [{u'url':
            # u'http://t.co/gOMyUN9I01', u'indices': [0, 22], u'expanded_url':
            # u'http://tullyhansen.com', u'display_url': u'tullyhansen.com'}]},
            # u'description': {u'urls': []}}
            expanded_url = expanded_url['url']
            expanded_url = expanded_url['urls']
            expanded_url = expanded_url.pop()
            expanded_url = expanded_url['expanded_url']
        except:
            expanded_url = '**null**'
        created_at = user['created_at']

        try:
            source = user['status']['source']
        except KeyError, e:
            print 'Looks like I can\'t find any tweets by "%s"' % str(screen_name)
            source = '<a href="**null**" rel="nofollow">**null**</a>'
        client = source.split('>')[1].split('<')[0]
        client_url = source.split('"')[1]

        with codecs.open(output_file, 'a', encoding='utf-8') as f:
            f.write(','.join(
                [screen_name, id, location, expanded_url, created_at, client, client_url]) + '\n')

print('Done! Info written to {}'.format(output_file))
