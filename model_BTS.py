import warnings
warnings.filterwarnings("ignore")
import uvicorn
from fastapi import FastAPI
from sentence_transformers.util import semantic_search
import pandas as pd
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('bert-base-cased')

df= pd.read_csv('Data.xlsx - Merged Dataset_1.csv')
df2 = pd.read_pickle('Embeddings.pkl')



# query = input('Enter your query: ')
# query_embedding = model.encode(query, convert_to_tensor=True,device='cpu')

# top_k = 10
# results = semantic_search(query_embedding, df2['Embeddings'].to_list(), top_k=top_k)

# print("Query:", query)
# print("Top 10 most similar sentences in corpus:")
# for i in results[0]:
#     id = i['corpus_id']
#     print('corpus_id:', id, "\t","score:", i['score'], "\t", df['title'][id])
    

# use fastapi to create a web app
app = FastAPI()

@app.get("/")
def read_root():
    return {"Heartly Welcome to BTS": "This is a web app for semantic search"}

# input query
@app.get("/query/{query}")
def read_item(query: str):
    query_embedding = model.encode(query, convert_to_tensor=True,device='cpu')
    top_k = 10
    results = semantic_search(query_embedding, df2['Embeddings'].to_list(), top_k=top_k)
    output ={}        
    
    print("Query:", query)
    print("Top 10 most similar sentences in corpus:")
    for i in results[0]:
        id = i['corpus_id']
        score = i['score']
        title = df['title'][id]
        output[id] = {"score": score, "title": title}
        ('corpus_id:', id, "\t","score:", i['score'], "\t", df['title'][id])
    return {"query": query, "output": output}

if __name__ == "__main__":
    
    uvicorn.run(app)


    

