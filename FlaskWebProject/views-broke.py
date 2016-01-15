"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app
#from flask_debugtoolbar import DebugToolBarExtension

#app.debug = True
#from TwitterSearch import *

#weatherTweets = "holder"
#try:
 #   tso = TwitterSearchOrder() # create a TwitterSearchOrder object
 #   tso.set_keywords(['weather', 'rain', 'rainy', 'raining', 'sunny', 'cloudy'
 #                     'foggy', 'fog', 'hail', 'hailing', 'snow.' 'snowing'], or_operator=True)
 #   tso.set_language('en')
 #   tso.set_geocode(42.3744, -71.1169, 5, True)
 #   tso.set_include_entities(False) # and don't give us all those entity information

 #   ts = TwitterSearch(
#                       consumer_key = '0foq3ttMublojZmIuth76mzDP',
#                       consumer_secret = '72t1Iaa4JOc60ZJb8UgejqcjIWK3g5OiJt2JnXXnNy2MbDuZ7K',
#                       access_token = '4188038303-tlz5WruG6b78FugN2CBq9lsuRa5IJYtnzxgRMwr',
#                       access_token_secret = 'bLLK8LDSyAVUL9EVtQkNGDHx8DP1FGRleNwi5FVqMrNVi'
#                       )

    #or tweet in ts.search_tweets_iterable(tso):
    #    print( '@%s tweeted: %s at %s at %s' % ( tweet['user']['screen_name'], tweet['text'], tweet['geo'], tweet['created_at'] ) )
    

#except TwitterSearchException as e: # take care of all those ugly errors if there are some
#    print(e)


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page v2',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

#weatherTweets = "holder" #gettweets in area
#tweetsToShow = "holder" #getlast4tweets on weather in area
#weatherWords = "holder" #parse python weatherTweets for appropriate key words
#commonWords = "holder" #finds most commonWords
#tweetSentiments = "holder" #gets sentiment of tweets/qualitative, emotion words

#@app.route('/tweather')
#def tweather():
#    """Renders tweather page."""
#    return render_template(
#        'tweather.html',
#        title = 'Tweather',
#        year=datetime.now().year,
#        message='Hi ' + 'Nicholas' + '.' #name of user
#        #change message to
#        message2 = 'The weather today is...'
#        message3 = 'formatForMessage(commonWords)' #formatForMessage(commonWords)
#        message4 = 'People feel:'
#        message5 = 'tweetSentiments' #tweetSentiments var
#        message6 = 'People are saying: '
#        wTweets = 'weatherTweets'
#    )



