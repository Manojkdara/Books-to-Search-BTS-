# create a web using streamlit 
import streamlit as st
import warnings
warnings.filterwarnings("ignore")
from sentence_transformers.util import semantic_search
import pandas as pd
from sentence_transformers import SentenceTransformer
from pathlib import Path
import plotly.express as px
import plotly.graph_objs as go




df= pd.read_csv('Data.xlsx - Merged Dataset_1.csv')
df2 = pd.read_pickle('Embeddings.pkl')

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("BTS-Book Recommendation System")

df3= pd.read_csv('query.csv')
# Sort the dataframe by the 'count' column in descending order
df3= df3.sort_values(by='count', ascending=True)
# Get the top 10 rows
top_10 = df3.head(10)
# Create a line chart
fig = go.Figure(data=go.Scatter(x=top_10['query'], y=top_10['count']))

# Set the chart title and axis labels
fig.update_layout(title='Top 10 Book Searches in our Website', xaxis_title='Query', yaxis_title='Rating')

# Display the chart
st.plotly_chart(fig)

#dataset
data=pd.read_csv('Data.xlsx - Merged Dataset_1.csv')

def create_table(query):
    filename = "query.csv"
    if Path(filename).is_file():
        df = pd.read_csv(filename)
        df['query'] = df['query'].str.lower()
        if query in df['query'].values:
            df.loc[df['query'] == query, 'count'] += 1
        else:
            df = df.append({'query': query, 'count': 1}, ignore_index=True)
        df.to_csv(filename, index=False)
    else:
        df = pd.DataFrame({'query': [query], 'count': [1]})
        df.to_csv(filename, index=False)
    return df

#user enters query

query = st.text_input("Enter your query")

if st.button("Search"):  # Get Search Query
    create_table(query.lower())  # save statistics about recent querys
    model = SentenceTransformer('bert-base-cased')
    query_embedding = model.encode(query, convert_to_tensor=True,device='cpu')
    top_k = 10
    results = semantic_search(query_embedding, df2['Embeddings_title'].to_list(), top_k=top_k)
    output={}
    df_output_link={}
    
    for i in results[0]:
        id = i['corpus_id']
        score = i['score']
        title = df['title'][id]
        rating= df['rating'][id]
        link=df['complete_link'][id]
        output[id] = {"score": score, "title": title, "rating": rating}
        df_output_link[id]= {"title": title, "link": link}


    df_output = pd.DataFrame.from_dict(output, orient='index')
    st.write(df_output)
    st.cache.df_output_link=df_output_link

    #vis
    st.markdown('### Bar Chart showing top 10 Books according to the similarity score')
    fig = px.bar(df_output, x='title', y='score')
    fig.update_layout(xaxis={'categoryorder': 'total descending'}, yaxis={'title': 'score'},
                      xaxis_tickangle=-45, yaxis_title='title')
    fig.data[0].marker.color = ['red', 'blue', 'green', 'purple', 'yellow', 'violet', 'indigo', 'orange', 'navy',
                                'brown']
    st.plotly_chart(fig)


    st.markdown('### Pie Chart showing top 10 books according to User Rating')
    fig2 = px.pie(df_output, values='rating', names='title',
                  color_discrete_sequence=['red', 'blue', 'green', 'purple', 'yellow', 'violet', 'indigo', 'orange',
                                           'navy',
                                           'brown'])
    st.plotly_chart(fig2)



























