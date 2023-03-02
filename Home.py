# create a web using streamlit 
import streamlit as st
import warnings
warnings.filterwarnings("ignore")
from sentence_transformers.util import semantic_search
import pandas as pd 
from sentence_transformers import SentenceTransformer
import plotly.express as px
import plotly.graph_objs as go
from config import SqlEngine, GetDataFrameFromSqlQuery, GetSelectBooksQuery, GetSelectEmbeddingsQuery, GetSelectQueryStatistic, SetStyle
import numpy as np

# Style
SetStyle(st)

# Title
title = "BTS - Book Recommendation System"
st.markdown("<h1 style='text-align:center; padding:20px;' >" + title + "</h1>", unsafe_allow_html=True)
title= "This website is a book recommendation system that uses embeddings and semantic search to suggest book titles based on a user's search query. The website utilizes the Sentence Transformer library and the BERT model to create embeddings and calculate similarity scores between books. The output of the website is interactive visualizations that display the top 10 book titles with the highest similarity scores and ratings. Users can also explore trends and compare similarities through various visualizations such as bar charts, line graphs, and pie charts. The website is built using Streamlit, making it easy to use and navigate."
st.markdown(
    "<p id='text-img' style='text-align:justify; padding:30px; background-color:#102945 ; color:#cfe5fc; "
    "font-family: sans serif; border-radius: 30px; font-size: 36px;font-size:1.2em; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);'>"
    + title +
    "</p>",
    unsafe_allow_html=True
)

#Create SQL Conection as it is used on multiple points
engine = SqlEngine()
    
#st.markdown("<div class='border' style='display: flex;padding:30px; background-color:#102945 ;box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);border-radius: 30px;'>", unsafe_allow_html=True)
col1, col2 = st.columns((5,5))

with col1:
    st.write(" ")
    st.image("pic_main.jpeg")

with col2:
    dfQuery = GetDataFrameFromSqlQuery(GetSelectQueryStatistic(), engine) #MySQL Query Result into a panda DataFrame
     # Sort the dataframe by the 'count' column in descending order
    dfQuery = dfQuery.sort_values(by='count', ascending=False)
    # Get the top 10 rows
    top_10 = dfQuery.head(10)
    top_10 = top_10[::-1]
    # Create a line chart
    fig = go.Figure(data=go.Scatter(x=top_10['query'], y=top_10['count']))

    # Set the chart title and axis labels
    fig.update_layout(title='Top 10 Book Searches in our Website', xaxis_title='Query', yaxis_title='Count')
    fig.update_traces(marker=dict(color='#83c9ff'))

    # Display the chart
    st.plotly_chart(fig)

def UpdateQueryStatistics(query, dfQuery, engine):
    if query in dfQuery['query'].values: # if query is already existing in dataframe
        dfQuery.loc[dfQuery['query'] == query, 'count'] += 1 # increment count
    else:
        dfQuery.loc[len(dfQuery)] = [query, 1] # add a new antry for query
        
    with engine.begin() as con: # save query statistics back in sql
        inserted = dfQuery.to_sql(con=con, name='query_statistic', if_exists='replace', method='multi', index=False);
    return

#user enters query
query = st.text_input("Enter your Query")
top_k = st.number_input(label='Amount of results', min_value=1, max_value=20, value=10, step=1,help="Set the amount of recommendations you wish to receive.")

if st.button("Search"):  # Get Search Query
    if not query or query == "": 
        st.stop() # dont proceed if empty request
    
    # Get Data of Books
    dfBooks = GetDataFrameFromSqlQuery(GetSelectBooksQuery(), engine)
    
    UpdateQueryStatistics(query.lower(),dfQuery, engine)  # save statistics about recent querys
    
    # get embeddings from mysql
    dfEmbTempAll = GetDataFrameFromSqlQuery(GetSelectEmbeddingsQuery(), engine)
    # convert Mixed Dataframe into numpy array
    dfEmbTempNumpy = dfEmbTempAll.drop(columns=['index']).to_numpy(dtype=np.float32)#tensor object
    
    if not hasattr(st.cache, 'model'): # cache model initalization for performance
        st.cache.model = SentenceTransformer('bert-base-cased')
    
    query_embedding = st.cache.model.encode(query, convert_to_numpy=True, device='cpu')
    results = semantic_search(query_embedding, dfEmbTempNumpy, top_k=top_k)
    output={}
    df_output_link={}
    
    for i in results[0]:
        id = i['corpus_id']
        score = i['score']
        title = dfBooks['title'][id]
        rating= dfBooks['rating'][id]
        link=dfBooks['complete_link'][id]
        output[id] = {"score": score, "title": title, "rating": rating}
        df_output_link[id]= {"title": title, "link": link}


    df_output = pd.DataFrame.from_dict(output, orient='index')
    st.write(df_output)
    st.cache.df_output_link=df_output_link

    #visualisation
    st.markdown('### Bar Chart showing top ' + str(len(df_output_link)) + ' Books according to the similarity score')
    fig = px.bar(df_output, x='title', y='score')
    fig.update_layout(xaxis={'categoryorder': 'total descending'}, yaxis={'title': 'score'},
                      xaxis_tickangle=-45, yaxis_title='title')
    fig.data[0].marker.color = ['peachpuff', 'palevioletred', 'midnightblue', 'palegoldenrod', 'mistyrose', 'paleturquoise', 'sienna', 'plum', 'lightsalmon', 'rosybrown','olive','khaki','lavender','lightcyan','lightgray','peru','salmon','wheat','lightcoral','goldenrod']
    st.plotly_chart(fig)


    st.markdown('### Pie Chart showing top ' + str(len(df_output_link)) + ' books according to User Rating')
    fig2 = px.pie(df_output, values='rating', names='title',
                  color_discrete_sequence=['peachpuff', 'palevioletred', 'midnightblue', 'palegoldenrod', 'mistyrose', 'paleturquoise', 'sienna', 'plum', 'lightsalmon', 'rosybrown','olive','khaki','lavender','lightcyan','lightgray','peru','salmon','wheat','lightcoral','goldenrod'])
    st.plotly_chart(fig2)

























