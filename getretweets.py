# import the module
import tweepy
from config import TwitterConfig
# assign the values accordingly
consumer_key = TwitterConfig.CONSUMER_KEY
consumer_secret = TwitterConfig.CONSUMER_SECRET
access_token = TwitterConfig.ACCESS_TOKEN
access_token_secret = TwitterConfig.ACCESS_TOKEN_SECRET

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth)

# the ID of the status
id = 1470676071398125569

# fetching the status
status = api.get_status(id)

# fetching the retweet_count attribute
retweet_count = status.retweet_count

print("The number of time the status has been retweeted is : " + str(retweet_count))
