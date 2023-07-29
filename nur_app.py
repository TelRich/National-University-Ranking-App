"""
@Created on:  Thursday, July 13, 2023, 3:19:15 AM

PROJECT: NATIONAL UNIVERSITY RANK APP

"""

# Importing Libraries
import pandas as pd
import streamlit as st
import plotly.express as px
import psycopg2

# Setting th epage size and title
st.set_page_config(layout='wide', page_title='National University Rank App')

# App Setup
with st.expander(':red[PROJECT TITLE]', expanded=True):
  st.markdown("<h1 style='text-align:center;'>National University Rank App</h1>", unsafe_allow_html=True)
  st.markdown("<h3 style='text-align:center;'>Research Idea</h3>", unsafe_allow_html=True)
  st.markdown("""<center>
  Developing a searchable database to help high school students identify colleges that match 
  their criteria in terms of tuition, graduation rate, location, and rank.
    </center>""", unsafe_allow_html=True)

# App Image
st.markdown("""
<p align="center">
<img width="1000" height="500" src="https://storage.googleapis.com/kaggle-datasets-images/2700487/4646217/3150dd9c507c09c6fe0d7e38c9cef15d/dataset-cover.png?t=2022-12-03-17-10-45">
</p>
""", unsafe_allow_html=True)

# App External Links
st.sidebar.markdown("""
                    # [**Project Link**](https://national-university-ranking-app.streamlit.app/)
                    # [**Project Article**](https://github.com/users/TelRich/projects/5)
                    # [**Project Outline**](https://github.com/users/TelRich/projects/5)
                    """)

# FUnction to load the cleaned data
@st.cache_data
def load_data():
  df = pd.read_csv('dataset/cleaned_nur_data.csv', index_col=0)
  return df

@st.cache_data
def connect_db():
  username = st.secrets['user']
  password = st.secrets['pw']
  host = 'telrichserver.postgres.database.azure.com'
  database = 'nur_db'
  port = '5432'
  sslmode = 'require'
  conn_str = f'postgresql://{username}:{password}@{host}:{port}/{database}?sslmode={sslmode}'
  return conn_str
  
df_nur = load_data()
conn = psycopg2.connect(connect_db())
cur = conn.cursor()


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

with st.expander(':red[Top Ranking School]', expanded=True):
  col1, col2 = st.columns([3,3], gap='small')
  with col1:
    st.plotly_chart(fig1, use_container_width=True)
    # st.plotly_chart(fig3, use_container_width=True)  
  with col2:
    st.plotly_chart(fig2, use_container_width=True)
    # st.plotly_chart(fig4, use_container_width=True)
    
with st.expander(':red[Region Search]', expanded=True):
  st.text('Not sure which region you fall into! Insert your state and find out')
  all_states = df_nur['state'].unique().tolist() 
  usr_state = st.selectbox('Select State', all_states)
  state_reg = df_nur[df_nur['state'] == usr_state]['region'].iloc[0]
  st.write(f'{usr_state} is in the {state_reg}')     

with st.expander(':red[Northeast Selection]', expanded=True):
  ne_states = df_nur[df_nur['region']=='Northeast']['state'].unique().tolist() 
  col3, col4 = st.columns([3,3], gap='small')
  n_rnk = """
  SELECT n.name,
  RANK() OVER (ORDER BY rank_num)
  FROM nur_app.northeast n
  JOIN nur_app.rank r
  ON r.id = n.rank_id
  ORDER BY rank_num
  LIMIT 3
  """
  
  n_fee = """
  SELECT n.name, tuition_and_fees
  FROM nur_app.northeast n
  JOIN nur_app.rank r
  ON r.id = n.rank_id
  ORDER BY tuition_and_fees DESC
  LIMIT 3
  """
  df1 = pd.read_sql_query(n_rnk, conn)
  fig5 = px.bar(df1, y="rank", x="name", text_auto=True,height = 300, width= 550, labels={'name':'', 'rank':''})
  fig5.update_layout(title_text="Top Universities by Rank")
  fig5.update_yaxes(showticklabels=False)
  with col3:
    st.plotly_chart(fig5, use_container_width=True)
  
  df2 = pd.read_sql_query(n_fee, conn)
  fig6 = px.bar(df2, y="tuition_and_fees", x="name", text_auto=True,height = 300, width= 550, labels={'name':'', 'tuition_and_fees':''})
  fig6.update_layout(title_text="Universities by High Fees")
  fig6.update_yaxes(showticklabels=False)
  with col4:
    st.plotly_chart(fig6, use_container_width=True)
  
  user_state = st.selectbox('Select State', ne_states)
  col5, col6 = st.columns([3,3], gap='small')
  top_rank_user_state = f"""
  SELECT n.name, 
  RANK() OVER (ORDER BY rank_num)
  FROM nur_app.northeast n
  JOIN nur_app.rank r
  ON r.id = n.rank_id
  WHERE state_id = '{user_state}'
  ORDER BY rank_num
  """
  
  top_fees_user_state = f"""
  SELECT n.name, tuition_and_fees
  FROM nur_app.northeast n
  JOIN nur_app.rank r
  ON r.id = n.rank_id
  WHERE state_id = '{user_state}'
  ORDER BY tuition_and_fees DESC
  """
  
  df3 = pd.read_sql_query(top_rank_user_state, conn)
  fig7 = px.bar(df3, y="rank", x="name", text_auto=True,height = 300, width= 550, labels={'name':'', 'rank':''})
  fig7.update_layout(title_text=f"Top Universities by Rank in {user_state}")
  fig7.update_yaxes(showticklabels=False)
  with col5:
    st.plotly_chart(fig7, use_container_width=True)
    
  df4 = pd.read_sql_query(top_fees_user_state, conn)
  fig8 = px.bar(df4, y="tuition_and_fees", x="name", text_auto=True,height = 300, width= 550, labels={'name':'', 'tuition_and_fees':''})
  fig8.update_layout(title_text=f"Universities by High Fees in {user_state}")
  fig8.update_yaxes(showticklabels=False)
  with col6:
    st.plotly_chart(fig8, use_container_width=True)
  
with st.expander(':red[Midwest Selection]', expanded=True):
  st.text('In Progres.......')  
  
with st.expander(':red[South Selection]', expanded=True):
  st.text('In Progres.......')  
  
with st.expander(':red[West Selection]', expanded=True):
  st.text('In Progres.......')

with st.expander(':red[School Recommender]', expanded=True):
  st.text('In Progres.......')
  
  