import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from config import DBConfig
import datetime
import sqlalchemy
import matplotlib.pyplot as plt
import numpy
import matplotlib.font_manager as fm
import json
import plotly.graph_objects as go
import plotly.express as px
import plotly
import altair as alt
import re


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
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    df = pd.read_sql_table('tweets', get_con())
    df = df.rename(columns={'body': 'Tweet', 'tweet_date': 'Timestamp',
                            'followers': 'Followers', 'sentiment': 'Sentiment',
                            'keyword': 'Subject', 'tweetsource': 'Tweeting platform', 'tweetid': 'Tweet ID'})
    return df, timestamp


@st.cache(show_spinner=False)
def filter_by_date(df, start_date, end_date):
    df_filtered = df.loc[(df.Timestamp.dt.date >= start_date) & (df.Timestamp.dt.date <= end_date)]
    return df_filtered


@st.cache(show_spinner=False)
def filter_by_subject(df, subjects):
    return df[df.Subject.isin(subjects)]


@st.cache
def count_plot_data(df, freq):
    plot_df = df.set_index('Timestamp').groupby('Subject').resample(freq).id.count().unstack(level=0, fill_value=0)
    plot_df.index.rename('Date', inplace=True)
    plot_df = plot_df.rename_axis(None, axis='columns')
    return plot_df


@st.cache
def sentiment_plot_data(df, freq):
    plot_df = df.set_index('Timestamp').groupby('Subject').resample(freq).Sentiment.mean().unstack(level=0, fill_value=0)
    plot_df.index.rename('Date', inplace=True)
    plot_df = plot_df.rename_axis(None, axis='columns')
    return plot_df

@st.cache(allow_output_mutation=True, show_spinner=False)
def get_data_charts():
    df = pd.read_sql_table('tweets', get_con())
    return df

df = get_data_charts()

topics = ''.join(df['body'])
topics = re.sub(r"http\S+", "", topics)
topics = topics.replace('RT ', ' ').replace('&amp;', 'and')
topics = re.sub('[^A-Za-z0-9]+', ' ', topics)
topics = topics.lower()

import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

tokenized_words = word_tokenize(topics)
stop_words=set(stopwords.words("english"))
filtered_sent=[]
for w in tokenized_words:
    if w not in stop_words:
        filtered_sent.append(w)
fdist = FreqDist(filtered_sent)
fd = pd.DataFrame(fdist.most_common(10),
                  columns = ["Word", "Frequency"]).drop([0]).reindex()


# End of data prep

st.set_page_config(layout="wide", page_title='StreamListenerDashboard')

data, timestamp = get_data()

st.header('Tweepy StreamListener Dashboard: #FreeUyghurs, #FuckCCP')
st.write('Total tweet count: {}'.format(data.shape[0]))
st.write('Data last loaded {}'.format(timestamp))
st.write('Listening to following keywords: Uyghur,uyghur,#uyghur,#freeuyghurs,#FreeUyghurs,#FreeUyghur,#UyghurLivesMatter,')
st.write('#UyghurGenocide,#uyghur,#Uyghur,#Uyghurs,#uyghurs,freeyughurs,FreeUyghurs,Xinjiang,#Xinjiang,#EastTurkestan,uighur,Uighur,#uighur,#Uighur')

col1, col2 = st.columns(2)

date_options = data.Timestamp.dt.date.unique()
start_date_option = st.sidebar.selectbox('Select Start Date', date_options, index=0)
end_date_option = st.sidebar.selectbox('Select End Date', date_options, index=len(date_options)-1)

keywords = data.Subject.unique()
data_subjects = data
data_daily = filter_by_date(data_subjects, start_date_option, end_date_option)

top_daily_tweets = data_daily.sort_values(['Followers'], ascending=False).head(10)

# col1.subheader('Influential Tweets') 
# col1.dataframe(top_daily_tweets[['Tweet', 'Timestamp', 'Followers', 'Subject']].reset_index(drop=True), 1000, 400)

col1.subheader('Recent Tweets')
col1.dataframe(data_daily[['Tweet', 'Timestamp', 'Followers', 'Subject']].sort_values(['Timestamp'], ascending=False).
               reset_index(drop=True).head(10))

plot_freq_options = {
    'Hourly': 'H',
    'Four Hourly': '4H',
    'Daily': 'D'
}
plot_freq_box = st.sidebar.selectbox(label='Plot Frequency:', options=list(plot_freq_options.keys()), index=0)
plot_freq = plot_freq_options[plot_freq_box]


barchart = alt.Chart(fd).mark_bar().encode(
    alt.X('Frequency', axis=alt.Axis(title="")),
    alt.Y('Word', axis=alt.Axis(title="")),
    color=alt.Color('Frequency:Q', scale=alt.Scale(scheme='greens'))
)




col2.subheader('Tweet Volumes')
plotdata = count_plot_data(data_daily, plot_freq)
col2.line_chart(plotdata)



col3, col4 = st.columns(2)




col3.subheader('Most frequent words')
col3.altair_chart(barchart, use_container_width=True)

colors = color_discrete_sequence=px.colors.sequential.Aggrnyl

col4.subheader('Keyword distribution')
valuecounts = df["keyword"].value_counts().tolist()
uniquesubject = df["keyword"].unique()
fig = px.pie(values=valuecounts, names=uniquesubject)
fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=20, marker=dict(colors=colors, line=dict(color='#000000', width=0.5)))
col4.plotly_chart(fig, use_container_width=True)

st.subheader('Sentiment data analysis visualisation')

compoundscore = df["sentiment"]
df["compound_trunc"] = compoundscore.round(1) # Truncate compound scores into 0.1 buckets 

res = (df.groupby(["compound_trunc"])["id"]
        .count()
        .reset_index()
        .rename(columns={"id": "count"})
      )

hist = alt.Chart(res).mark_bar(width=35).encode(
    alt.X("compound_trunc:Q", axis=alt.Axis(title="")),
    y=alt.Y('count:Q', axis=alt.Axis(title="")),
    color=alt.Color('compound_trunc:Q', scale=alt.Scale(scheme='redyellowgreen')), 
    tooltip=['compound_trunc', 'count']
)

scatter = alt.Chart(df).mark_point().encode(
    alt.X("tweet_date", axis=alt.Axis(title="")),
    y=alt.Y('sentiment', axis=alt.Axis(title="")),
    color=alt.Color('sentiment:Q', scale=alt.Scale(scheme='redyellowgreen')), 
    tooltip=['body', 'userid','sentiment:Q', 'tweet_date']
)

col5, col6 = st.columns(2)

col5.subheader('Truncated compound vaderSentiment score')
col5.altair_chart(hist, use_container_width=True)
col6.subheader('Scatter plot of clean compound score provided by vaderSentiment')
col6.altair_chart(scatter, use_container_width=True)

