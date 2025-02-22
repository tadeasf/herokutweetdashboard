import datetime
import re
import altair as alt
import pandas as pd
import plotly.express as px
import sqlalchemy
import streamlit as st
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from sqlalchemy import create_engine
from config import DBConfig
import unicodedata
import nltk
import matplotlib.pyplot as plt
from database import session_scope, init_db
from models import Tweet
from tweepy.streaming import StreamListener
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from autocorrect import Speller

googlesql = sqlalchemy.engine.url.URL.create(
    drivername="mysql+pymysql",
    username=DBConfig.db_user,
    password=DBConfig.db_pass,
    host=DBConfig.db_host,
    port=DBConfig.db_port,
    database=DBConfig.db_name)


def get_con():
    return create_engine(googlesql)


df = pd.read_sql_table('tokTweetsExcelled', get_con())
text = df['body']

rawtext = text.to_string()
spell = Speller(lang='en', fast=True)
blbcorrected = spell(rawtext)
blbcorrected = re.sub(r"http\S+", "", blbcorrected)
blbcorrected = blbcorrected.replace('RT ', ' ').replace('&amp;', 'and')
blbcorrected = re.sub('[^A-Za-z0-9]+', ' ', blbcorrected)
blbcorrected = blbcorrected.lower()

#sent_i = SentimentIntensityAnalyzer()

df['cleanedText'] = blbcorrected
df.to_csv("/home/tadeas/stunome-socialmedianalysis-python/upload-to-mysql.csv",
          encoding="utf-8", index=False)


"""def vader_sentiment(text):
     Calculate and return the nltk vadar(lexicon method) sentiment 
    return sent_i.polarity_scores(text)['compound']


df['sentiment'] = blbcorrected.apply(vader_sentiment)
print(df['sentiment'])
df.to_csv("/home/tadeas/stunome-socialmedianalysis-python/analysed_tweets4.csv",
          encoding="utf-8", index=False)
"""
