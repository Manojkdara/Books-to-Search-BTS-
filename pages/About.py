import streamlit as st
import graphviz
import pandas as pd
import plotly.express as px
from config import GetDataFrameFromSqlQuery, GetSelectBooksQuery, GetSelectEmbeddingsQuery, SetStyle

# Style
SetStyle(st)

# Title
st.markdown(' ### Here you can get to know more about our dataset')

# Row A for for adding 3 description boxes
col1, col2, col3 = st.columns(3)
col1.metric("Books", "1470")
col2.metric("Source", "Kaggle")
col3.metric("Domain","Educational")

option = st.selectbox(
    'How would you like to be view the flow?',
     ('Simple Flow of our Model', 'Detailed Flow of our Model'))
     
graph = graphviz.Digraph()

if option == 'Simple Flow of our Model':
    graph.edge('User','Input')
    graph.edge('Input','Semantic Search','Word Embedding')
    graph.edge('Semantic Search','Recommendation','Similarity Score')
    graph.edge('Recommendation','Visualization')
    graph.edge('Visualization','Input')
else:
    graph.edge('MySQL(Database)','Backend')
    graph.edge('Backend','Data Cleaning','Model')
    graph.edge('Data Cleaning','Pre-Trained Model(BERT)')
    graph.edge('Pre-Trained Model(BERT)','Embeddings')
    graph.edge('Embeddings','Semantic Search','Similarity Score')
    graph.edge('Semantic Search','Recommendations','Top 10')
    graph.edge('User','Input')
    graph.edge('Input','Embeddings')
    graph.edge('Embeddings','Semantic Search')
    graph.edge('Recommendations', 'Visualization')
    graph.edge('Visualization', 'Input')

graph.node_attr['style'] = 'filled,rounded'
graph.node_attr['fillcolor'] = '#152c45'
graph.node_attr['fontcolor'] = '#cfe5fc'
graph.node_attr['color'] = '#cfe5fc'
graph.node_attr['shape'] = 'box'
graph.edge_attr['fillcolor'] = '#cfe5fc'
graph.edge_attr['fontcolor'] = '#cfe5fc'
graph.edge_attr['color'] = '#cfe5fc'
graph.graph_attr['bgcolor'] = '#0c1f33'
st.graphviz_chart(graph)




