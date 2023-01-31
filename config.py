# function for setting css
def SetStyle(st):
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    with open('style.css') as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                footer:after {
    	               content:'Made by Neurons ❤';
                	    visibility: visible;
    	                 display: block;
    	                position: relative;
                	    #background-color: red;
            	         padding: 5px;
    	                top: 2px;
                }
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    return
    
def ValidEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    import re
    return re.fullmatch(regex, email)
    
# function for getting SQL Connection
def SqlEngine():
    from sqlalchemy import create_engine
    return create_engine("mysql://root:Hello268@localhost/books")

def GetDataFrameFromSqlQuery(query, engine = SqlEngine()):
    import pandas as pd
    from sqlalchemy import text
    with engine.begin() as con:
        df = pd.read_sql(text(query),con) #MySQL Query Result into a panda DataFrame
    return df
    
def GetSelectRawBooksQuery():
    return "Select * from books"
def GetSelectBooksQuery():
    return "Select * from books_processed"
def GetSelectEmbeddingsQuery():
    return "Select * from books_embeddings"
def GetSelectQueryStatistic():
    return "Select * from query_statistic"
    