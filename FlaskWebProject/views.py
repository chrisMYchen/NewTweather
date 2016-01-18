"""
Routes and views for the flask application.
"""
import operator
import datetime
from flask import render_template
from FlaskWebProject import app
from TwitterSearch import *
import re
import string
import json
import urllib2
import requests



#--------------Weather Description--------------
#Basic natural language processing to determine what 
#the overarching weather is like.
#Weights weather keywords in tweets to find highest ranking words.
#Input: Array of tweets collected
#Output: Top ranking notion/temp/prec as an array
def weather_desc(tweets):
    notions = {'windy': 0.0,
               'comfortable': 0.0,
               'refreshing': 0.0,
               'beautiful': 0.0,
               'ominous': 0.0,
               'miserable': 0.0,
               'foggy': 0.0,
               'severe': 0.0,
               'humid': 0.0,
               'muggy': 0.0,
               'stormy': 0.0,
               'flooding': 0.0}
    temps = {'warm': 0.0,
             'hot': 0.0,
             'cold': 0.0,
             'freezing': 0.0}
    precs = {'clear': 0.0,
             'overcast': 0.0,
             'raining': 0.0,
             'sunny': 0.0,
             'hailing': 0.0,
             'snowing': 0.0,
             'foggy': 0.0,
             'cloudy': 0.0}
 
    texts = []
 
    for tweet in tweets:
        if "windy" in tweet['text'] or "wind" in tweet['text']:
            notions['windy'] += 5.0
 
        if "comfortable" in tweet['text']:
            notions['comfortable'] += 5.0
 
        if "refreshing" in tweet['text']:
            notions['refreshing'] += 5.0
 
        if "beautiful" in tweet['text'] or "nice weather" in tweet['text']:
            notions['beautiful'] += 5.0
 
        if "ominous" in tweet['text']:
            notions['ominous'] += 5.0
            notions['stormy'] += 3.5
            notions['miserable'] += 3.0
 
        if "miserable" in tweet['text']:
            notions['miserable'] += 5.0
 
        if "foggy" in tweet['text'] or "fog" in tweet['text']:
            notions['foggy'] += 5.0
            notions['humid'] += 2.5
            notions['muggy'] += 1.0
 
        if "severe" in tweet['text'] or "thunderstorm" in tweet['text'] or "storm" in tweet['text']:
            notions['severe'] += 5.0
            notions['stormy'] += 4.0
 
        if "humid" in tweet['text']:
            notions['humid'] += 5.0
            notions['muggy'] += 2.0
 
        if "muggy" in tweet['text']:
            notions['muggy'] += 5.0
            notions['humid'] += 3.5
 
        if "stormy" in tweet['text'] or "thunderstorm" in tweet['text'] or "storm" in tweet['text']:
            notions['stormy'] += 5.0
            notions['severe'] += 3.5
 
        if "tornado" in tweet['text'] or "hurricane" in tweet['text']:
            notions['stormy'] += 10.0
            notions['severe'] += 6.5
 
        if "flooding" in tweet['text'] or "flood" in tweet['text']:
            notions['flooding'] += 5.0
 
        if "warm" in tweet['text']:
            temps['warm'] += 5.0
            temps['hot'] += 1.5
 
        if "hot" in tweet['text']:
            temps['hot'] += 5.0
            temps['warm'] += 3.0
 
        if "cold" in tweet['text']:
            temps['cold'] += 5.0
 
        if "freezing" in tweet['text']:
            temps['freezing'] += 5.0
            temps['cold'] += 3.0
 
        if "clear" in tweet['text']:
            precs['clear'] += 5.0
 
        if "overcast" in tweet['text']:
            precs['overcast'] += 5.0
 
        if "raining" in tweet['text']:
            precs['raining'] += 5.0
 
        if "sunny" in tweet['text']:
            precs['sunny'] += 5.0
 
        if "hailing" in tweet['text']:
            precs['hailing'] += 5.0
            precs['snowing'] += 1.0
 
        if "snowing" in tweet['text']:
            precs['snowing'] += 5.0
 
        if "foggy" in tweet['text']:
            precs['foggy'] += 5.0
 
        if "cloudy" in tweet['text']:
            precs['cloudy'] += 5.0
 
        if "precipitation" in tweet['text']:
            precs['raining'] += 2.0
            precs['snowing'] += 1.5
            precs['hailing'] += 1.0
        try:
            # What about shift + 0-9 characters and quotes?

            texts.append([tweet['text'], tweet['geo']['coordinates']])
        except TypeError as e:
            print(e)
 
    return [[max(notions, key=notions.get), max(temps, key=temps.get), max(precs, key=precs.get)],
            texts]
 
 #API for Geolocation
 #Solution doesn't work unless locally hosted
 #because it finds the server's location.
 #Need to migrate tweet grabbing and analysis 
 #to Javascript on client side.
 #-----get current location----
send_url = 'http://freegeoip.net/json'
r = requests.get(send_url)
j = json.loads(r.text)
#lat = j['latitude']
lat = 40.7127
#lon = j['longitude']
lon = -74.0059
mip = j['ip']


#-------------------Twitter Scraper-------------
#Uses TwitterSearch https://github.com/ckoepp/TwitterSearch
#Finds tweets with according keywords, language, within 20km
#of the provided longitude/latitude.
#Then stores parts of the weather_desc in variables to later pass

from TwitterSearch import *
try:
    tso = TwitterSearchOrder()
    tso.set_keywords(['weather', 'rain', 'rainy', 'raining', 'sunny', 'cloudy', 'cold', 'colder',
                      'foggy', 'fog', 'hail', 'hailing', 'snow', 'snowing',
                      'wind', 'windy', 'overcast'], or_operator=True)
    #tso.set_until(datetime.date(2015, 11, 13))
    tso.set_language('en')
    tso.set_geocode(lat, lon, 20, True)
    tso.set_include_entities(False)
 
    ts = TwitterSearch(
                       consumer_key = '0foq3ttMublojZmIuth76mzDP',
                       consumer_secret = '72t1Iaa4JOc60ZJb8UgejqcjIWK3g5OiJt2JnXXnNy2MbDuZ7K',
                       access_token = '4188038303-tlz5WruG6b78FugN2CBq9lsuRa5IJYtnzxgRMwr',
                       access_token_secret = 'bLLK8LDSyAVUL9EVtQkNGDHx8DP1FGRleNwi5FVqMrNVi'
                       )
 
    var = (weather_desc(ts.search_tweets_iterable(tso)))
    sentiment = var[0]
    temps = sentiment[1]
    notions = sentiment[0]
    precs = sentiment[2]
    lotTweets = var[1]
 
    #for tweet in ts.search_tweets_iterable(tso):
       
        #print( '@%s tweeted: %s at %s at %s' % ( tweet['user']['screen_name'], tweet['text'], tweet['geo'], tweet['created_at'] ) )
 
except TwitterSearchException as e:
    print(e)


#Temperature of current location based on API needs to be moved to Javascript
#on Client Side

#Same with City name.

#Future to add:
#Clothing recommendation/Actions to take



#Renders the html pages based on template.
#Basic template provides

#Home page
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
      #  year=datetime.now().year,
    )

#Contact page
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
      #  year=datetime.now().year,
        message='Your contact page.'
    )


#About page
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
       # year=datetime.now().year,
        message='Your application description page.'
    )


#Collects first 25 tweets as well as the three most recent
Tweeters = lotTweets[:25]
Tweet0 = lotTweets[0][0]
Tweet1 = lotTweets[1][0]
Tweet2 = lotTweets[2][0]

#Renders the Tweather page and passes necessary variables
@app.route('/tweather')
def tweather():
    """Renders the tweather page."""
    return render_template(
        'tweather.html',
        title='Tweather',
#        year=datetime.now().year,
        message= notions.title() + ', ',
        message1= precs.title() + ',',
        message4= temps.title() + '.',
        message5= 'Today\'s Tweets:',
        lTweets = Tweeters,
        t1 = Tweet0,
        t2 = Tweet1,
        t3 = Tweet2,
        clothes = "Wear...",
        temp_loc = "NY Temp..."
    )




#---------------Retired Code (left if need in future) -----------
#Temperature of current location based on API needs to be moved to Javascript
#on Client Side

#Same with City name.

#temp_f = 0
#location = ""
#f = urllib2.urlopen('http://api.wunderground.com/api/72d0d0413d94447d/geolookup/conditions/q/MA/Boston.json')
#json_string = f.read()
#parsed_json = json.loads(json_string)
#location = parsed_json['location']['city']
#temp_f = parsed_json['current_observation']['temp_f']
#print "Current temperature in %s is: %s" % (location, temp_f)
#f.close()


    #weatherTweets = "holder" #gettweets in area
#tweetsToShow = "holder" #getlast4tweets on weather in area
#weatherWords = "holder" #parse python weatherTweets for appropriate key words
#commonWords = "holder" #finds most commonWords


#tweet0 = example_tweets[0] #gets sentiment of tweets/qualitative, emotion words
#tweet1 = example_tweets[1]
#tweet2 = example_tweets[2]



