"""
@Created on:  Thursday, July 13, 2023, 3:19:15 AM

PROJECT: NATIONAL UNIVERSITY RANK APP

"""

# Importing Libraries
import pandas as pd
import streamlit as st
import plotly.express as px

# Setting th epage size and title
st.set_page_config(layout='wide', page_title='National University Rank App')

# App Setup
with st.expander(':violet[PROJECT TITLE]', expanded=True):
  st.markdown("<h1 style='text-align:center;'>National University Rank App</h1>", unsafe_allow_html=True)
  st.markdown("<h3 style='text-align:center;'>Research Idea</h3>", unsafe_allow_html=True)
  st.markdown("""<center>
  Developing a searchable database to help high school students identify colleges that match 
  their criteria in terms of tuition, graduation rate, location, and rank.
    </center>""", unsafe_allow_html=True)

# App Image
st.markdown("""
<p align="center">
<img width="900" height="500" src="https://storage.googleapis.com/kaggle-datasets-images/2700487/4646217/3150dd9c507c09c6fe0d7e38c9cef15d/dataset-cover.png?t=2022-12-03-17-10-45">
</p>
""", unsafe_allow_html=True)

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

# @st.cache_data
# def connect_db():
#   username = st.secrets
  
df_nur = load_data()

fig1 = px.bar(df_nur[:3].sort_values('rank', ascending=False), y="rank", x="name", text_auto=True,height = 400, width= 550, labels={'name':'', 'rank':''})
fig1.update_layout(xaxis={"categoryorder": "total ascending"}, title_text="Top Universities by Rank")
fig1.update_yaxes(showticklabels=False)

top_tf = df_nur.sort_values(by='tuition_and_fees', ascending=False)[:3]
fig2 = px.bar(top_tf, y="tuition_and_fees", x="name", text_auto=True,height=400, width=550,
             labels={'name':'', 'tuition_and_fees': ''})
fig2.update_layout(xaxis={"categoryorder": "total descending"}, title_text="Top Universities by Tuition and fees")
fig2.update_yaxes(showticklabels=False)

top_ins = df_nur.sort_values(by='in_state', ascending=False)[:3]
fig3 = px.bar(top_ins, x="in_state", y="name", text_auto=True,height=400, width=550,
             labels={'name':'', 'in_state': ''}, title="Top Universities by In-State fees")
fig3.update_xaxes(showticklabels=False)

top_ins = df_nur[df_nur['year'] != 0].sort_values(by='year')[:3]
fig4 = px.bar(top_ins, y="year", x="name", text_auto=True,height=400, width=550,
             labels={'name':'', 'year': ''}, title="Oldest Universities")
fig4.update_yaxes(showticklabels=False)

with st.expander('Top Ranking School', expanded=True):
  col1, col2 = st.columns([3,3], gap='small')
  with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)  
  with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)

with st.expander('Northeast Selection'):
  st.text('In Progres.......')
  
with st.expander('Midwest Selection'):
  st.text('In Progres.......')  
  
with st.expander('South Selection'):
  st.text('In Progres.......')  
  
with st.expander('West Selection'):
  st.text('In Progres.......')

with st.expander('School Recommender'):
  st.text('In Progres.......')
  
  