# import libraries
import warnings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
import re
import csv 
import mysql.connector as sql

nltk.download('wordnet')
from nltk.corpus import wordnet
nltk.download('punkt')
nltk.download('stopwords')


from nltk import word_tokenize,sent_tokenize

#df = pd.read_csv('Data.xlsx - Merged Dataset.csv')

mydb = sql.connect(
  host="localhost",
  user="root",
  password="Hello@268")

query = "Select * from books.books_merged;" #books_merged is the table name

df = pd.read_sql(query,mydb)
print('Data is loaded')
print(df.shape)
# insert index column  
df.insert(0, 'Index', range(0, 0 + len(df)))

# replace missing nan values with NO AUTHOR in authors column 
df['author'].fillna('NO AUTHOR', inplace = True)
df['complete_link'].fillna('Link is not avaliable', inplace = True)

# convert rating to integer
df['rating'] = pd.to_numeric(df['rating'],errors='coerce')
df['rating']=df['rating']*10

# fill missing values with mean of rating column
df['rating'].fillna(df['rating'].mean(), inplace = True)

# delete duplicate rows
df.drop_duplicates(subset=['title'], keep='first', inplace=True)
print('After deleting duplicates',df.shape)

# save the dataframe to a csv file
df.to_csv('Data.xlsx - Merged Dataset_1.csv', index=False)

# insert bert embeddings 
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('bert-base-cased')

"""sentences= df['title'].tolist()
sentences_embeddings=[]

for i in sentences:
    temp_embeddings = model.encode(i, convert_to_tensor=True,device='cpu')
    sentences_embeddings.append(temp_embeddings)

print('Embeddings are done')
# create a dataframe with the embeddings 
df2 = pd.DataFrame(columns=['Embeddings','Index'])
df2['Embeddings'] = sentences_embeddings
df2['Index'] = df['Index'].tolist()

# Embeddings for author column
sentences_author= df['author'].tolist()
sentences_embeddings_author=[]

for i in sentences_author:
    temp_embeddings = model.encode(i, convert_to_tensor=True,device='cpu')
    sentences_embeddings_author.append(temp_embeddings)"""
    
df2 = pd.DataFrame(columns=['Index']) 
df2['Index'] = df['Index'].tolist()  
    
# function for column embeddings 
def column_embeddings(column_name):
    sentences_column= df[column_name].tolist()
    sentences_embeddings_column=[]
    
    for i in sentences_column:
        temp_embeddings = model.encode(i, convert_to_tensor=True,device='cpu')
        sentences_embeddings_column.append(temp_embeddings)
    
    name = 'Embeddings_' + column_name
    df2[name]=sentences_embeddings_column
    
    print('Embeddings are done for', column_name)
    return df2
    

# call the function 
column_embeddings('title')


# save the model as pickle file 
df2.to_pickle('Embeddings.pkl')
print('-'*50 )
print('Data processing is done')
