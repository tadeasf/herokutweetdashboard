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
# nejdriv vytazeny tweety z monga do aws mysql db
# properties nasledujici: bud int, text nebo varchar(1000)
# pak to jde
# problem je v tom, ze proste nejak nevim jak to vyresit tak, aby zacaly fungovat tweety, ktery jsou spellchecknuty
# cesta muze byt v tom prave nejdriv procistit, stahnout csv, nahrat do db a s tim az pracovat
# cesta ve vyse zminenem neni, pak to vyhodnoti vse stejne. vzit proste cisty body, na tom to funguje

def get_con():
    return create_engine(googlesql)


df = pd.read_sql_table('tokTweetsExcelled', get_con())
text = df['body']

#rawtext = text.to_string()
#spell = Speller(lang='en')
#blbcorrected = spell(rawtext)

sent_i = SentimentIntensityAnalyzer()


def vader_sentiment(text):
    """ Calculate and return the nltk vadar (lexicon method) sentiment """
    return sent_i.polarity_scores(text)['compound']


df['sentiment'] = text.apply(vader_sentiment)
print(df)
df.to_csv("/home/tadeas/stunome-socialmedianalysis-python/tokTweetsSentimented.csv",
          encoding="utf-8", index=False)