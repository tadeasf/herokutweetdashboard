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

text = "I am very terible guy hahahahahahsshx I hope you will die hahah :D:D"

rawtext = text
spell = Speller(lang='en')
blbcorrected = spell(rawtext)

sent_i = SentimentIntensityAnalyzer()

print(blbcorrected)


def vader_sentiment(string):
    # Calculate and return the nltk vadar(lexicon method) sentiment
    return sent_i.polarity_scores(string)['compound']


sentiment = blbcorrected.apply(vader_sentiment)

print(sentiment)
"""
df['sentiment'] = blbcorrected.apply(vader_sentiment)
print(df['sentiment'])
df.to_csv("/home/tadeas/stunome-socialmedianalysis-python/analysed_tweets4.csv",
          encoding="utf-8", index=False)
"""
