# import libraries
import warnings

import pandas as pd
from numpy import ndarray
from sqlalchemy import text
from config import SqlEngine, GetDataFrameFromSqlQuery, GetSelectRawBooksQuery

#Create Engine to connect with MySQL
engine = SqlEngine()

# Define query (select all books)
dfBooks = GetDataFrameFromSqlQuery(GetSelectRawBooksQuery(), engine) #MySQL Query Result into a panda DataFrame
print('Data is loaded', dfBooks.shape)
# insert index column  
dfBooks.insert(0, 'index', range(0, 0 + len(dfBooks)))

# replace missing nan values with NO AUTHOR in authors column 
dfBooks['author'].fillna('NO AUTHOR', inplace = True)
dfBooks['complete_link'].fillna('Link is not avaliable', inplace = True)

# convert rating to integer
dfBooks['rating'] = pd.to_numeric(dfBooks['rating'],errors='coerce')
dfBooks['rating']=dfBooks['rating']*10

# fill missing values with mean of rating column
dfBooks['rating'].fillna(dfBooks['rating'].mean(), inplace = True)

# delete duplicate rows
dfBooks.drop_duplicates(subset=['title'], keep='first', inplace=True)
print('After Cleanup',dfBooks.shape)

# save dataframe into MySQL
with engine.begin() as con:
    inserted = dfBooks.to_sql(con=con, name='books_processed', if_exists='replace', method='multi');

print('Processed ', inserted, 'books')

# save the dataframe to a csv file
#dfBooks.to_csv('Dataset_Cleaned.csv', index=False)

# insert bert embeddings 
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('bert-base-cased')
    
# function for column embeddings 
def column_embeddings(column_name):
    sentences_column = dfBooks[column_name].tolist()
    sentences_embeddings_column = []
    
    for i in sentences_column:
        temp_embeddings = model.encode(i, convert_to_numpy=True, device='cpu')
        sentences_embeddings_column.append(temp_embeddings)
    
    return sentences_embeddings_column
    
# Get numpy array
sentences_embeddings_column = column_embeddings('title')

#convert to Panda DataFrame to save it
dfEmb = pd.DataFrame(sentences_embeddings_column)
dfEmb.insert(0, 'index', 0) # add missing index 
dfEmb['index'] = dfBooks['index'].tolist() # copy original index to it

# save the model into mysql 
with engine.begin() as con:
    inserted = dfEmb.to_sql(con=con, name='books_embeddings', if_exists='replace', method='multi');
print('-'*50 )
print('Data processing is done')
