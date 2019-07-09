from __future__ import print_function
import tweepy
import json
import mysql.connector
from dateutil import parser

WORDS = ['#torontoeats', '#Summerlicous']

CONSUMER_KEY = 'KEY'
CONSUMER_SECRET = 'SECRET'
ACCESS_TOKEN = 'TOKEN'
ACCESS_TOKEN_SECRET = 'TOKEN SECRET'

HOST = "HOST"
USER = "USER"
PASSWD = "PASSWORD"
DATABASE = "DATABASE"

# A function to store the 'created_at', 'text', 'screen_name' and 'tweet_id'
# into the MySQL database
def store_data(created_at, text, screen_name, tweet_id):
    # connect to the running MySQL server
    db=mysql.connector.connect(host=HOST,
     user=USER,
      passwd=PASSWD,
       db=DATABASE,
        charset="utf8")
    # create the control structure for traversing db records
    cursor = db.cursor()
    # insert the data into respective db columns
    insert_query =
     "INSERT INTO twitter (tweet_id, screen_name, created_at, text) VALUES (%s, %s, %s, %s)"
    # execute insertion with the cursor
    cursor.execute(insert_query, (tweet_id, screen_name, created_at, text))
    db.commit() # commit changes
    cursor.close()
    db.close()
    return

class StreamListener(tweepy.StreamListener):
    #This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        # connect to the MySQL database and store data from stream
        try:
           # Decode the JSON from Twitter
            datajson = json.loads(data)

            #grab the wanted data from the Tweet
            text = datajson['text']
            screen_name = datajson['user']['screen_name']
            tweet_id = datajson['id']
            created_at = parser.parse(datajson['created_at'])

            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))

            #insert the data into the MySQL database
            store_data(created_at, text, screen_name, tweet_id)

        except Exception as e:
           print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# Set up the listener.
# The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)
