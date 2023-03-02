import streamlit as st
import plotly.express as px
import pandas as pd
from config import GetDataFrameFromSqlQuery, GetSelectBooksQuery, GetSelectEmbeddingsQuery, SetStyle

# Style
SetStyle(st)

# Title
title="Here you can get to know more about our dataset"
st.markdown("<h1 style='text-align:center; padding:20px;' >" + title + "</h1>", unsafe_allow_html=True)
dfBooks = GetDataFrameFromSqlQuery(GetSelectBooksQuery())

#Average rating distribution for all books

st.write('### Average rating distribution for all books')
dfBooks.rating = dfBooks.rating.astype(float)
fig3 = px.histogram(dfBooks, x='rating', nbins=50)#The number of bins (also known as intervals or classes) determines the granularity of the histogram.

fig3.update_layout( xaxis_title='Average rating',
                   font=dict(size=20),
                   xaxis_tickangle=-45)
fig3.update_traces(marker=dict(line=dict(color='black', width=1),
                                color='#83c9ff'))
st.plotly_chart(fig3)


#scatter graph
st.write('### Get to know our complete Data Set')
col1, col2 = st.columns(2)

x_axis_val = col1.selectbox('Select the X-axis', options=dfBooks.columns)
y_axis_val = col2.selectbox('Select the Y-axis', options=dfBooks.columns)

plot = px.scatter(dfBooks, x=x_axis_val, y=y_axis_val)
plot.update_traces(marker=dict(color='#83c9ff'))
st.plotly_chart(plot, use_container_width=True)


