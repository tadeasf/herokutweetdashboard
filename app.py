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
from sqlalchemy import create_engine, null
from config import DBConfig
import unicodedata
import nltk
import matplotlib.pyplot as plt

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
def get_data():
    timeisvaluable = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    df1 = pd.read_sql_table('test-oracle3', get_con())
    df1 = df1.rename(columns={'body': 'Tweet', 'tweet_date': 'Timestamp',
                              'followers': 'Followers', 'sentiment': 'Sentiment',
                              'keyword': 'Subject', 'tweetsource': 'Tweeting platform', 'tweetid': 'Tweet ID'})
    return df1, timeisvaluable


@st.cache(show_spinner=False)
def filter_by_date(df2, start_date, end_date):
    df_filtered = df2.loc[(df2.Timestamp.dt.date >= start_date) & (
        df2.Timestamp.dt.date <= end_date)]
    return df_filtered


@st.cache(show_spinner=False)
def filter_by_subject(df3, subjects):
    return df3[df3.Subject.isin(subjects)]


@st.cache
def count_plot_data(df4, freq):
    plot_df = df4.set_index('Timestamp').groupby('Subject').resample(
        freq).id.count().unstack(level=0, fill_value=0)
    plot_df.index.rename('Date', inplace=True)
    plot_df = plot_df.rename_axis(None, axis='columns')
    return plot_df


@st.cache
def sentiment_plot_data(df5, freq):
    plot_df = df5.set_index('Timestamp').groupby('Subject').resample(freq).Sentiment.mean().unstack(level=0,
                                                                                                    fill_value=0)
    plot_df.index.rename('Date', inplace=True)
    plot_df = plot_df.rename_axis(None, axis='columns')
    return plot_df


@st.cache(allow_output_mutation=True, show_spinner=False)
def get_data_charts():
    df6 = pd.read_sql_table('test-oracle3', get_con())
    return df6


df = get_data_charts()

topics = ''.join(df['body'])
topics = re.sub(r"http\S+", "", topics)
topics = topics.replace('RT ', ' ').replace('&amp;', 'and')
topics = re.sub('[^A-Za-z0-9]+', ' ', topics)
topics = topics.lower()

tokenized_words = word_tokenize(topics)
stop_words = set(stopwords.words("english"))

stop_words.update(('uyghur', 'uyghurs', 'uighur', 'uighurs', 'house')) # tady jsou stopwords, přidej podle bi-gramů

filtered_sent = []
for w in tokenized_words:
    if w not in stop_words:
        filtered_sent.append(w)
fdist = FreqDist(filtered_sent)
fd = pd.DataFrame(fdist.most_common(20),
                  columns=["Word", "Frequency"]).drop([0]).reindex()

# End of data prep

st.set_page_config(layout="wide", page_title='StreamListenerDashboard')

data, timestamp = get_data()

st.header('Tweepy StreamListener Dashboard: Reflections of communism in Romania')
st.markdown('Total tweet count: **{}**'.format(data.shape[0]))
st.markdown('Data last loaded **{}**'.format(timestamp))
st.markdown('Running since: **21/7/2022**')
st.markdown('Listening to following keywords: **Ceaușescu, Ceausescu, ceaușescu, ceaușescu, tovaras, decree 770, decree770, #decree770, #Ceaușescu,'
            '#Ceausescu, #ceaușescu, #ceaușescu, Tovarășul, tovarășul, tovarasul, Gheorghiu-Dej, dheorghiu-dej, comunistă, geniul din carpati, Geniul din Carpati,'
            'communist nostalgia, Iliescu, iliescu, Dăscălescu, dăscălescu, Dascalescu, dascalescu, Stănculescu, stănculescu, stanculescu, Stanculescu, Bârlădeanu,'
            'Barladeanu, caramitru, Caramitru, dinescu, nicolaescu**')

col1, col2 = st.columns(2)

date_options = data.Timestamp.dt.date.unique()
start_date_option = st.sidebar.selectbox(
    'Select Start Date', date_options, index=0)
end_date_option = st.sidebar.selectbox(
    'Select End Date', date_options, index=len(date_options) - 1)

keywords = data.Subject.unique()
data_subjects = data
data_daily = filter_by_date(data_subjects, start_date_option, end_date_option)

top_daily_tweets = data_daily.sort_values(
    ['Followers'], ascending=False).head(10)

col1.subheader('Recent Tweets')
col1.dataframe(data_daily[['Tweet', 'Timestamp', 'Followers', 'Subject']].sort_values(['Timestamp'], ascending=False).
               reset_index(drop=True).head(10))

plot_freq_options = {
    'Hourly': 'H',
    'Four Hourly': '4H',
    'Daily': 'D'
}
plot_freq_box = st.sidebar.selectbox(
    label='Plot Frequency:', options=list(plot_freq_options.keys()), index=0)
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

ADDITIONAL_STOPWORDS = [
    'nuyghursnxinjiangnsoundofhopeoh', 'nuyghursnxinjiangnsoundofhopeoh,']


def basic_clean(text):
    wnl = nltk.stem.WordNetLemmatizer()
    stopwordsforbigram = nltk.corpus.stopwords.words(
        'english') + ADDITIONAL_STOPWORDS
    text = (unicodedata.normalize('NFKD', text)
            .encode('ascii', 'ignore')
            .decode('utf-8', 'ignore')
            .lower())
    words = re.sub(r'[^\w\s]', '', text).split()
    return [wnl.lemmatize(word) for word in words if word not in stopwordsforbigram]


wordsforngram = basic_clean(''.join(str(df['body'].tolist())))

wordsforngram2 = basic_clean(''.join(str(df['body'].tolist())))

wordsforngram3 = basic_clean(''.join(str(df['body'].tolist())))

col5, col6 = st.columns(2)

bigram_series = (pd.Series(nltk.ngrams(wordsforngram, 2)).value_counts())[:12]
bigramgraphax = bigram_series.sort_values().plot.barh(
    color='darkgreen', width=.9, figsize=(14, 7))
plt.ylabel('Bigram')
plt.xlabel('# of Occurances')


col5.subheader('12 Most Frequently Occuring Bigrams')
col5.pyplot(bigramgraphax.figure, use_container_width=True)

trigram_series = (pd.Series(nltk.ngrams(
    wordsforngram2, 3)).value_counts())[:12]
trigramgraphax = trigram_series.sort_values().plot.barh(
    color='darkgreen', width=.9, figsize=(14, 7))
plt.ylabel('Trigram')
plt.xlabel('# of Occurances')


col6.subheader('12 Most Frequently Occuring Trigrams')
col6.pyplot(trigramgraphax.figure, use_container_width=True)

quadrigram_series = (pd.Series(nltk.ngrams(
    wordsforngram3, 4)).value_counts())[:12]
quadrigrampgraphax = quadrigram_series.sort_values().plot.barh(
    color='darkgreen', width=.9, figsize=(14, 7))
plt.ylabel('Quadrigram')
plt.xlabel('# of Occurances')

dalsiradek1, dalsiradek2 = st.columns(2)

dalsiradek1.subheader('12 Most Frequently Occuring Quadrigrams')
dalsiradek1.pyplot(quadrigrampgraphax.figure, use_container_width=True)

st.subheader(
    'Visualisation of compound score values provided by vaderSentiment')

compoundscore = df["sentiment"]
# Truncate compound scores into 0.1 buckets
df["compound_trunc"] = compoundscore.round(1)

res = (df.groupby(["compound_trunc"])["id"]
       .count()
       .reset_index()
       .rename(columns={"id": "count"})
       )

hist = alt.Chart(res).mark_bar(width=35).encode(
    alt.X("compound_trunc:Q", axis=alt.Axis(title="")),
    y=alt.Y('count:Q', axis=alt.Axis(title="")),
    color=alt.Color('compound_trunc:Q', scale=alt.Scale(
        scheme='redyellowgreen')),
    tooltip=['compound_trunc', 'count']
)

scatter = alt.Chart(df).mark_point().encode(
    alt.X("tweet_date", axis=alt.Axis(title="")),
    y=alt.Y('sentiment', axis=alt.Axis(title="")),
    color=alt.Color('sentiment:Q', scale=alt.Scale(scheme='redyellowgreen')),
    tooltip=['body', 'userid', 'sentiment:Q', 'tweet_date']
)

col7, col8 = st.columns(2)

col7.subheader('Truncated compound score distribution')
col7.altair_chart(hist, use_container_width=True)
col8.subheader('Scatter plot of clean compound score')
col8.altair_chart(scatter, use_container_width=True)
#  todo: Named entity recognition: get to know other topics
#  the users are tweeting about. Eg my topic is uyghurs in xinjiang. What they talk about the most? China? CCP? I
#  looked more into NER. Getting some output with spacy shouldn't be much of an issue. I don't need this to be
#  terrible thorough. Few issues I can think of that will need solving: Where to should I push the output? Inside the
#  SQL library? For one tweet they can be multiple terms.. How to set it up? In the end, what can I use this output
#  for? Checking most common keyword-NER pairs? Is it gonna be useful for my analysis? - also it looks like this is
#  implemented by Twitter itself to some extent. I have to do more research. Consult:
#  https://developer.twitter.com/en/docs/twitter-api/annotations/overview

st.subheader('Piecharts! Because who doesnt like Pacman?!')
col9, col10 = st.columns(2)

sourcevalue = df['tweetsource'].value_counts().tolist()
sourcesubject = df['tweetsource'].unique()

colors = color_discrete_sequence = px.colors.sequential.Aggrnyl

sourcepie = px.pie(df, values=sourcevalue, names=sourcesubject)
sourcepie.update_traces(textposition='inside', textinfo='percent+label', textfont_size=20,
                        marker=dict(colors=colors, line=dict(color='#000000', width=0.5)))

col9.subheader('Most used platforms for tweeting')
col9.plotly_chart(sourcepie, use_container_width=True)


piechartsource = get_data_charts()
keywordcount = piechartsource["keyword"].value_counts().tolist()
keywordindex = piechartsource["keyword"].value_counts().index.tolist()
uniquesubject = piechartsource["keyword"].unique()


fig = px.pie(values=keywordcount, names=keywordindex)
fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=0.5)))

col10.subheader('Keyword distribution')
col10.plotly_chart(fig, use_container_width=True)

# col9, col10 = st.columns(2)
# col9.subheader('Influential Tweets')
# col9.dataframe(top_daily_tweets[['Tweet', 'Sentiment', 'Followers', 'Subject']].reset_index(drop=True), 1000, 400)
# todo: add similar thing to col9 topdaily tweets where you'll show most retweeted tweets
# todo: add maps
