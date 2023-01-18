'''import warnings
warnings.filterwarnings("ignore")
import uvicorn
from fastapi import FastAPI
import json
from flask import Flask, jsonify,request, render_template
import subprocess


from sentence_transformers.util import semantic_search
import pandas as pd
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt

model = SentenceTransformer('bert-base-cased')

df= pd.read_csv('Data.xlsx - Merged Dataset_1.csv')
df2 = pd.read_pickle('Embeddings.pkl')
#filename= "test.csv"

app= Flask(__name__)

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
#app = FastAPI()


@app.route("/")
def read_root():
    return {"Heartly Welcome to BTS": "This is a web app for semantic search"}

# input query
@app.route('/query/<query>', methods=['GET'])
def read_item(query):
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
        with open("output.json", "w") as f:
            json.dump(output, f)
    subprocess.run(["python", "vis.py"])  # call vis.py
    return jsonify({"query": query, "output": output})
   # return {"query": query, "output": output}


if __name__ == "__main__":

    app.run(debug=True)


'''
import warnings

warnings.filterwarnings("ignore")
import uvicorn
from fastapi import FastAPI
import json
from flask import Flask, jsonify, request, render_template
import subprocess
import json
import csv
import pandas as pd
import plotly.graph_objs as go
import plotly.subplots as sp
from pathlib import Path

from sentence_transformers.util import semantic_search
import pandas as pd
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt

model = SentenceTransformer('bert-base-cased')

df = pd.read_csv('Data.xlsx - Merged Dataset_1.csv')
df2 = pd.read_pickle('Embeddings.pkl')
# filename= "test.csv"

app = Flask(__name__)


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
# app = FastAPI()


@app.route("/")
def read_root():
    return {"Heartly Welcome to BTS": "This is a web app for semantic search"}


# input query
@app.route('/query', methods=['GET'])
def read_item():
    query = request.args.get('q')
    query_embedding = model.encode(query, convert_to_tensor=True, device='cpu')
    top_k = 10
    results = semantic_search(query_embedding, df2['Embeddings'].to_list(), top_k=top_k)
    output = {}

    print("Query:", query)
    print("Top 10 most similar sentences in corpus:")
    for i in results[0]:
        id = i['corpus_id']
        score = i['score']
        title = df['title'][id]
        output[id] = {"score": score, "title": title}
        ('corpus_id:', id, "\t", "score:", i['score'], "\t", df['title'][id])
        with open("output.json", "w") as f:
            json.dump(output, f)
    # subprocess.run(["python", "vis.py"])  # call vis.py

    with open("output.json", "r") as f:
        output = json.load(f)
        # print(output)
        table1 = pd.DataFrame.from_dict(output, orient='index')
        print(table1)  # score title and index

    merged_list = []

    with open('Data.xlsx - Merged Dataset_1.csv', 'r') as i:
        reader = csv.reader(i)
        next(reader)
        for row in reader:
            index = row[0]
            title = row[1]
            rating = row[3]
            # print(f"title:{title}")
            # print(f"rating:{rating}")
            merged_list.append(index)
            merged_list.append(title)
            merged_list.append(rating)
    # print(merged_list)        #merged list contaning title index and rating

    # creating dictionary
    output = []
    for i in range(0, len(merged_list), 3):
        output.append({
            "index": merged_list[i],
            "title": merged_list[i + 1],
            "rating": merged_list[i + 2]
        })
    # print(output)

    # Convert the list of dictionaries to a DataFrame
    table2 = pd.DataFrame(output)

    # Print the resulting table
    # print(table2)  #all data in form of table-index title and rating from all data set

    result = table2.loc[table2['index'].isin(table1.index), ['title', 'rating']]
    # print(result) #get title with same index no. from the merged list

    # Create a subplots figure
    fig = sp.make_subplots(rows=1, cols=2, specs=[[{'type': 'bar'}, {'type': 'pie'}]])

    # Add the first chart (bar chart)
    fig.add_trace(go.Bar(x=table1['title'], y=table1['score'], name='Score distribution of Books',
                         marker=dict(color='rgb(158,202,225)', line=dict(color='rgb(8,48,107)', width=1.5))), row=1,
                  col=1)
    # Add the second chart (pie chart)

    fig.add_trace(go.Pie(labels=result['title'], values=result['rating'], name='Book title-Rating distribution'), row=1,
                  col=2)
    # Update the layout
    fig.update_layout(title='Recommended Books - "' + query + '"', showlegend=True)
    fig.update_xaxes(title_text="Book Title", row=1, col=1)
    fig.update_yaxes(title_text="Score", row=1, col=1)

    txt = Path('header.html').read_text()

    return txt + fig.to_html(full_html=False, include_plotlyjs='cdn') + "</div></body></html>"


# return {"query": query, "output": output}


if __name__ == "__main__":
    app.run(debug=True)






    

