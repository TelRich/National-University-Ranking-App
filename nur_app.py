"""
@Created on:  Thursday, July 13, 2023, 3:19:15 AM

PROJECT: NATIONAL UNIVERSITY RANK APP

"""

# Importing Libraries
import pandas as pd
import streamlit as st
import plotly.express as px

# Setting th epage size and title
st.set_page_config(layout='centered', page_title='National University Rank App')

# App Setup
with st.expander(':violet[PROJECT TITLE]', expanded=True):
  st.markdown("<h1 style='text-align:center;'>National University Rank App</h1>", unsafe_allow_html=True)
  st.markdown("<h3 style='text-align:center;'>Research Idea</h3>", unsafe_allow_html=True)
  st.markdown("""<center>
  Developing a searchable database to help high school students identify colleges that match 
  their criteria in terms of tuition, graduation rate, location, and rank.
    </center>""", unsafe_allow_html=True)

# App Image
st.image('https://storage.googleapis.com/kaggle-datasets-images/2700487/4646217/3150dd9c507c09c6fe0d7e38c9cef15d/dataset-cover.png?t=2022-12-03-17-10-45')

# App External Links
st.sidebar.markdown("""
                    # [**Project Link**](https://national-university-ranking-app.streamlit.app/)
                    # [**Project Article**](https://github.com/users/TelRich/projects/5)
                    # [**Project Outline**](https://github.com/users/TelRich/projects/5)
                    """)

@st.cache_data
def load_data():
  df = pd.read_csv('dataset/cleaned_nur_data.csv', index_col=0)
  return df
  
df_nur = load_data()
fig = px.bar(df_nur[:3], x="rank", y="name", color="name", text_auto=True,height = 500, width= 700, labels={'name':''})
fig.update_layout(xaxis={"categoryorder": "total ascending"}, title_text="Top Universities by Rank")
st.plotly_chart(fig)  

with st.expander('Top Ranking School'):
  st.text('In Progres.......')

with st.expander('School Selection'):
  st.text('In Progres.......')
  
with st.expander('School Recommender'):
  st.text('In Progres.......')
  
  