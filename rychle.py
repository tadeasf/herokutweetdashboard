import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from config import DBConfig
import datetime
import sqlalchemy
import matplotlib.pyplot as plt
import random
import numpy
import matplotlib.font_manager as fm
from textblob import TextBlob
from streamlit_echarts import st_echarts

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


@st.cache(allow_output_mutation=True, show_spinner=False, ttl=5*60)
def get_data():
    df = pd.read_sql_table('tweets', get_con())
    df = df.rename(columns={'body': 'Tweet', 'tweet_date': 'Timestamp',
                            'followers': 'Followers', 'sentiment': 'Sentiment',
                            'keyword': 'Subject', 'tweetsource': 'Tweeting platform', 'tweetid': 'Tweet ID'})
    return df

print(df)
