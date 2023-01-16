# create a web using streamlit 
import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from sentence_transformers.util import semantic_search
import pandas as pd
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot
model = SentenceTransformer('bert-base-cased')

df= pd.read_csv('Data.xlsx - Merged Dataset_1.csv')
df2 = pd.read_pickle('Embeddings.pkl')

st.title("BTS Semantic Search")
st.write("This is a web app for semantic search")

query = st.text_input("Enter your query")
if st.button("Search"):
    query_embedding = model.encode(query, convert_to_tensor=True,device='cpu')
    top_k = 10
    results = semantic_search(query_embedding, df2['Embeddings'].to_list(), top_k=top_k)
    output ={}        
    
    for i in results[0]:
        id = i['corpus_id']
        score = i['score']
        title = df['title'][id]
        output[id] = {"score": score, "title": title}
        
    df_output = pd.DataFrame.from_dict(output, orient='index')
    st.write(df_output)
    
    # plot the results
    matplotlib.pyplot.bar(df_output['title'], df_output['score'])
    
    st.pyplot()
    
# run the web app
