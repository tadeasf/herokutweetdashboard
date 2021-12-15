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
  
# the ID of the user
userid = 83833848
  
# fetching the user
user = api.get_user(id)
  
# fetching the location
location = user.location
  
print("The location of the user is : " + location)
