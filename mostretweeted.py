# I want to get tweet ids of all stored tweets
# then I want to find the amount of retweets for each of them
# then I want to export this and plot a graph
# -> getting IDS is easy - access database -> get_data -> hotovo
# todo: -> teď ale jak to nakrmit do tweepy, aby mi to vypsalo počet retweetů?
# a potom vložit kam? udělat tohle v rámci streamlit aplikace? to bude strašně moc kontinuálních requestů. ne
# bude to chtít nový skript -> který to udělá separé a vypíše do nové tabulky v mysql databázi
# to pak vezme streamlit a vyplotuje z toho graf/tabulku
# podobný postup následně s userlocation
# todo: -> bar graph of total reactions by type -> like, comment, retweet
import sqlalchemy
import streamlit as st
from config import DBConfig
from sqlalchemy import create_engine
import pandas as pd
import tweepy
from config import TwitterConfig

# assign the values accordingly
consumer_key = TwitterConfig.CONSUMER_KEY
consumer_secret = TwitterConfig.CONSUMER_SECRET
access_token = TwitterConfig.ACCESS_TOKEN
access_token_secret = TwitterConfig.ACCESS_TOKEN_SECRET

googlesql = sqlalchemy.engine.url.URL.create(
    drivername="mysql+pymysql",
    username=DBConfig.db_user,
    password=DBConfig.db_pass,
    host=DBConfig.db_host,
    port=DBConfig.db_port,
    database=DBConfig.db_name)


@st.cache(allow_output_mutation=True, show_spinner=False)
def get_con():
    return create_engine(googlesql)


@st.cache(allow_output_mutation=True, show_spinner=False, ttl=5 * 60)
def get_retweet_data():
    df7 = pd.read_sql_table('tweets', get_con())
    return df7


retweetdf = get_retweet_data()

tweetids = pd.Series(retweetdf['tweetid'])

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth)

status = api.get_status(tweetids)
retweet_count = status.retweet_count
print("The number of time the status has been retweeted is : " + str(retweet_count))
