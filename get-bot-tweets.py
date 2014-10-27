#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import sys
import unicodecsv
import datetime
import os

#Twitter API credentials

# Chuck in a newline-delimited list of usernames. Get back recent tweets from all of 'em.
# TODO: throwing "IndexError: list index out of range" on InParlWikiedits

api_key = os.getenv('TWITTER_API_KEY')
api_secret = os.getenv('TWITTER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

read_usernames_from_file = sys.argv[1]

# timestamp = datetime.datetime.now()

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print "...%s tweets downloaded so far" % (len(alltweets))
    
    #transform the tweepy tweets into a 2D array that will populate the csv
    #
    # tweet looks like this:
    #
    # Status(contributors=None
    # truncated=False
    # text=u'Benitez out. Mourinho in. Mark my words.'
    # in_reply_to_status_id=None
    # id=1250224240
    # favorite_count=0
    # _api=<tweepy.api.API object at 0x100e9d1d0>
    # author=User(follow_request_sent=False, profile_use_background_image=True, _json={u'follow_request_sent': False, u'profile_use_background_image': True, u'default_profile_image': False, u'id': 4319161, u'profile_background_image_url_https': u'https://abs.twimg.com/images/themes/theme1/bg.png', u'verified': False, u'profile_text_color': u'000000', u'profile_image_url_https': u'https://pbs.twimg.com/profile_images/1578321071/index2_normal.jpg', u'profile_sidebar_fill_color': u'E0FF92', u'entities': {u'description': {u'urls': []}}, u'followers_count': 37, u'profile_sidebar_border_color': u'87BC44', u'id_str': u'4319161', u'profile_background_color': u'9AE4E8', u'listed_count': 1, u'is_translation_enabled': False, u'utc_offset': 3600, u'statuses_count': 5, u'description': u'', u'friends_count': 17, u'location': u'London', u'profile_link_color': u'0000FF', u'profile_image_url': u'http://pbs.twimg.com/profile_images/1578321071/index2_normal.jpg', u'following': False, u'geo_enabled': False, u'profile_background_image_url': u'http://abs.twimg.com/images/themes/theme1/bg.png', u'screen_name': u'jaffa', u'lang': u'en', u'profile_background_tile': False, u'favourites_count': 0, u'name': u'tom henshaw', u'notifications': False, u'url': None, u'created_at': u'Thu Apr 12 07:49:12 +0000 2007', u'contributors_enabled': False, u'time_zone': u'London', u'protected': False, u'default_profile': False, u'is_translator': False}, time_zone=u'London', id=4319161, _api=<tweepy.api.API object at 0x100e9d1d0>, verified=False, profile_text_color=u'000000', profile_image_url_https=u'https://pbs.twimg.com/profile_images/1578321071/index2_normal.jpg', profile_sidebar_fill_color=u'E0FF92', is_translator=False, geo_enabled=False, entities={u'description': {u'urls': []}}, followers_count=37, protected=False, id_str=u'4319161', default_profile_image=False, listed_count=1, lang=u'en', utc_offset=3600, statuses_count=5, description=u'', friends_count=17, profile_link_color=u'0000FF', profile_image_url=u'http://pbs.twimg.com/profile_images/1578321071/index2_normal.jpg', notifications=False, profile_background_image_url_https=u'https://abs.twimg.com/images/themes/theme1/bg.png', profile_background_color=u'9AE4E8', profile_background_image_url=u'http://abs.twimg.com/images/themes/theme1/bg.png', name=u'tom henshaw', is_translation_enabled=False, profile_background_tile=False, favourites_count=0, screen_name=u'jaffa', url=None, created_at=datetime.datetime(2007, 4, 12, 7, 49, 12), contributors_enabled=False, location=u'London', profile_sidebar_border_color=u'87BC44', default_profile=False, following=False)
    # _json={u'contributors': None, u'truncated': False, u'text': u'Benitez out. Mourinho in. Mark my words.', u'in_reply_to_status_id': None, u'id': 1250224240, u'favorite_count': 0, u'source': u'<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>', u'retweeted': False, u'coordinates': None, u'entities': {u'symbols': [], u'user_mentions': [], u'hashtags': [], u'urls': []}, u'in_reply_to_screen_name': None, u'id_str': u'1250224240', u'retweet_count': 1, u'in_reply_to_user_id': None, u'favorited': False, u'user': {u'follow_request_sent': False, u'profile_use_background_image': True, u'default_profile_image': False, u'id': 4319161, u'profile_background_image_url_https': u'https://abs.twimg.com/images/themes/theme1/bg.png', u'verified': False, u'profile_text_color': u'000000', u'profile_image_url_https': u'https://pbs.twimg.com/profile_images/1578321071/index2_normal.jpg', u'profile_sidebar_fill_color': u'E0FF92', u'entities': {u'description': {u'urls': []}}, u'followers_count': 37, u'profile_sidebar_border_color': u'87BC44', u'id_str': u'4319161', u'profile_background_color': u'9AE4E8', u'listed_count': 1, u'is_translation_enabled': False, u'utc_offset': 3600, u'statuses_count': 5, u'description': u'', u'friends_count': 17, u'location': u'London', u'profile_link_color': u'0000FF', u'profile_image_url': u'http://pbs.twimg.com/profile_images/1578321071/index2_normal.jpg', u'following': False, u'geo_enabled': False, u'profile_background_image_url': u'http://abs.twimg.com/images/themes/theme1/bg.png', u'screen_name': u'jaffa', u'lang': u'en', u'profile_background_tile': False, u'favourites_count': 0, u'name': u'tom henshaw', u'notifications': False, u'url': None, u'created_at': u'Thu Apr 12 07:49:12 +0000 2007', u'contributors_enabled': False, u'time_zone': u'London', u'protected': False, u'default_profile': False, u'is_translator': False}, u'geo': None, u'in_reply_to_user_id_str': None, u'lang': u'en', u'created_at': u'Wed Feb 25 18:25:11 +0000 2009', u'in_reply_to_status_id_str': None, u'place': None}
    # coordinates=None
    # entities={u'symbols': [], u'user_mentions': [], u'hashtags': [], u'urls': []}
    # in_reply_to_screen_name=None
    # id_str=u'1250224240'
    # retweet_count=1
    # in_reply_to_user_id=None
    # favorited=False
    # source_url=u'http://twitter.com'
    # user=User(follow_request_sent=False, profile_use_background_image=True, _json={u'follow_request_sent': False, u'profile_use_background_image': True, u'default_profile_image': False, u'id': 4319161, u'profile_background_image_url_https': u'https://abs.twimg.com/images/themes/theme1/bg.png', u'verified': False, u'profile_text_color': u'000000', u'profile_image_url_https': u'https://pbs.twimg.com/profile_images/1578321071/index2_normal.jpg', u'profile_sidebar_fill_color': u'E0FF92', u'entities': {u'description': {u'urls': []}}, u'followers_count': 37, u'profile_sidebar_border_color': u'87BC44', u'id_str': u'4319161', u'profile_background_color': u'9AE4E8', u'listed_count': 1, u'is_translation_enabled': False, u'utc_offset': 3600, u'statuses_count': 5, u'description': u'', u'friends_count': 17, u'location': u'London', u'profile_link_color': u'0000FF', u'profile_image_url': u'http://pbs.twimg.com/profile_images/1578321071/index2_normal.jpg', u'following': False, u'geo_enabled': False, u'profile_background_image_url': u'http://abs.twimg.com/images/themes/theme1/bg.png', u'screen_name': u'jaffa', u'lang': u'en', u'profile_background_tile': False, u'favourites_count': 0, u'name': u'tom henshaw', u'notifications': False, u'url': None, u'created_at': u'Thu Apr 12 07:49:12 +0000 2007', u'contributors_enabled': False, u'time_zone': u'London', u'protected': False, u'default_profile': False, u'is_translator': False}, time_zone=u'London', id=4319161, _api=<tweepy.api.API object at 0x100e9d1d0>, verified=False, profile_text_color=u'000000', profile_image_url_https=u'https://pbs.twimg.com/profile_images/1578321071/index2_normal.jpg', profile_sidebar_fill_color=u'E0FF92', is_translator=False, geo_enabled=False, entities={u'description': {u'urls': []}}, followers_count=37, protected=False, id_str=u'4319161', default_profile_image=False, listed_count=1, lang=u'en', utc_offset=3600, statuses_count=5, description=u'', friends_count=17, profile_link_color=u'0000FF', profile_image_url=u'http://pbs.twimg.com/profile_images/1578321071/index2_normal.jpg', notifications=False, profile_background_image_url_https=u'https://abs.twimg.com/images/themes/theme1/bg.png', profile_background_color=u'9AE4E8', profile_background_image_url=u'http://abs.twimg.com/images/themes/theme1/bg.png', name=u'tom henshaw', is_translation_enabled=False, profile_background_tile=False, favourites_count=0, screen_name=u'jaffa', url=None, created_at=datetime.datetime(2007, 4, 12, 7, 49, 12), contributors_enabled=False, location=u'London', profile_sidebar_border_color=u'87BC44', default_profile=False, following=False)
    # geo=None
    # in_reply_to_user_id_str=None
    # lang=u'en'
    # created_at=datetime.datetime(2009, 2, 25, 18, 25, 11)
    # in_reply_to_status_id_str=None
    # place=None
    # source=u'Twitter Web Client'
    # retweeted=False)

    
    outtweets = []
    for tweet in alltweets:
        
#         try:
#             native_retweet_content = tweet.retweeted_status.encode("utf-8")
#         except AttributeError:
#             native_retweet_content = "**null**"
        outtweets.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")])
#     try:
#         outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.retweeted_status.encode("utf-8")] for tweet in alltweets]
#     except AttributeError:
#         outtweets = [["dang","blast","wtf","bbq"]]
    
    #write the csv    
    #with open('%s_tweets.csv' % screen_name, 'wb') as f:
    with open(str(screen_name) + '_' + str(datetime.datetime.now()) + '.csv', 'wb') as f:
        writer = unicodecsv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    
    pass

lines = open(read_usernames_from_file).readlines()

for i, line in enumerate(lines[:]):
#    print lines[:]
    print 'I\'m getting tweets for ' + line[:-1]
#    print i
    get_all_tweets(line[:-1])
    del lines[0]
#    print lines[:]

open(read_usernames_from_file, 'w').writelines(lines)


# if __name__ == '__main__':
#     #pass in the username of the account you want to download
#     get_all_tweets(account_to_query)