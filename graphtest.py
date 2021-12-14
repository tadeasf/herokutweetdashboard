import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from config import DBConfig
import datetime
import sqlalchemy
import matplotlib.pyplot as plt
import numpy
import matplotlib.font_manager as fm
from streamlit_echarts import st_echarts
import json
import plotly.graph_objects as go
import plotly.express as px
import plotly
import seaborn as sns
import altair as alt


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


@st.cache(allow_output_mutation=True, show_spinner=False)
def get_data_charts():
    df = pd.read_sql_table('tweets', get_con())
    return df

df = get_data_charts()




valuecounts = df["keyword"].value_counts().tolist()

uniquesubject = df["keyword"].unique()
uniquesubjectlist = uniquesubject.tolist()
uniquesubjectjson = json.dumps(uniquesubjectlist)
valuecountsjson = json.dumps(valuecounts)


fig = px.pie(values=valuecounts, names=uniquesubject, title='Keyword distribution')
st.plotly_chart(fig)



import altair as alt

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
    tooltip=['compound_trunc', 'count']).properties(
    width=800,
    height=400
)
hist



scatter = alt.Chart(df).mark_point().encode(
    alt.X("tweet_date", axis=alt.Axis(title="")),
    y=alt.Y('sentiment', axis=alt.Axis(title="")),
    color=alt.Color('sentiment:Q', scale=alt.Scale(scheme='redyellowgreen')), 
    tooltip=['body', 'userid','sentiment:Q', 'tweet_date']).properties(width=800,height=400
)
scatter








# pie chart s tweetsource
