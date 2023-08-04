"""
@Created on:  Thursday, July 13, 2023, 3:19:15 AM

PROJECT: NATIONAL UNIVERSITY RANK APP

"""

# Importing Libraries
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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


fig1 = px.bar(df_nur[:3].sort_values('rank'), y="rank", x="name", text_auto=True,height = 400, width= 550, labels={'name':'', 'rank':''},
              color_discrete_sequence=px.colors.qualitative.Vivid)
fig1.update_layout(title_text="Top Universities by Rank")
fig1.update_yaxes(showticklabels=False)
text_color = 'white' 
fig1.update_traces(textfont_color=text_color)

top_tf = df_nur.sort_values(by='tuition_and_fees')[:3]
fig2 = px.bar(top_tf, y="tuition_and_fees", x="name", text_auto=True,height=400, width=550,
             labels={'name':'', 'tuition_and_fees': ''}, color_discrete_sequence=px.colors.qualitative.Vivid)
fig2.update_layout(xaxis={"categoryorder": "total descending"}, title_text="Top Universities by Tuition and fees")
fig2.update_yaxes(showticklabels=False)
fig2.update_traces(textfont_color=text_color)

top_ins = df_nur.sort_values(by='in_state', ascending=False)[:3]
fig3 = px.bar(top_ins, x="in_state", y="name", text_auto=True,height=400, width=550, color_discrete_sequence=px.colors.qualitative.Vivid,
             labels={'name':'', 'in_state': ''}, title="Top Universities by In-State fees")
fig3.update_xaxes(showticklabels=False)
fig3.update_traces(textfont_color=text_color)

top_ins = df_nur[df_nur['year'] != 0].sort_values(by='year')[:3]
fig4 = px.bar(top_ins, y="year", x="name", text_auto=True,height=400, width=550, color_discrete_sequence=px.colors.qualitative.Vivid,
             labels={'name':'', 'year': ''}, title="Oldest Universities")
fig4.update_yaxes(showticklabels=False)
fig4.update_traces(textfont_color=text_color)

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

# NORTHEAST

def region_df(reg):
  reg_fil = df_nur[df_nur['region']==reg]['state_full'].unique().tolist()
  return reg_fil

def rank_plot(reg):
  reg_rnk = f"""
  SELECT re.name,
  RANK() OVER (ORDER BY rank_num)
  FROM nur_app.{reg} re
  JOIN nur_app.rank r
  ON r.id = re.rank_id
  ORDER BY rank_num
  LIMIT 3
  """
  df1 = pd.read_sql_query(reg_rnk, conn)
  fig1 = px.bar(df1, y="rank", x="name", text_auto=True,height = 350, width= 550, labels={'name':'', 'rank':''},
                color_discrete_sequence=px.colors.qualitative.Vivid)
  fig1.update_layout(title_text="Top Universities by Rank")
  fig1.update_yaxes(showticklabels=False)
  fig1.update_traces(textfont_color=text_color)
  return fig1

def fees_plot(reg):
  reg_fee = f"""
  SELECT re.name, tuition_and_fees
  FROM nur_app.{reg} re
  JOIN nur_app.rank r
  ON r.id = re.rank_id
  ORDER BY tuition_and_fees DESC
  LIMIT 3
  """
  df2 = pd.read_sql_query(reg_fee, conn)
  fig2 = px.bar(df2, y="tuition_and_fees", x="name", text_auto=True,height = 350, width= 550, labels={'name':'', 'tuition_and_fees':''},
                color_discrete_sequence=px.colors.qualitative.Vivid)
  fig2.update_layout(title_text="Universities by High Fees")
  fig2.update_yaxes(showticklabels=False)
  fig2.update_traces(textfont_color=text_color)
  return fig2

def inner_rank(query_df):
  df3 = pd.read_sql_query(query_df, conn)
  fig3 = px.bar(df3, y="rank", x="name", text_auto=True,height = 350, width= 550, labels={'name':'', 'rank':''})
  fig3.update_layout(title_text=f"Top Universities by Rank in {user_state}")
  fig3.update_yaxes(showticklabels=False)
  fig3.update_traces(textfont_color=text_color) 
  return fig3

def inner_fees(query_df):
  df4 = pd.read_sql_query(top_fees_user_state, conn)
  fig4 = px.bar(df4, y="tuition_and_fees", x="name", text_auto=True,height = 350, width= 550, labels={'name':'', 'tuition_and_fees':''})
  fig4.update_layout(title_text=f"Universities by High Fees in {user_state}")
  fig4.update_yaxes(showticklabels=False)
  fig4.update_traces(textfont_color=text_color)
  return fig4

def tab_viz(df):
  table_trace = go.Table(
      header=dict(values=list(df.columns),
                  fill_color='lightsteelblue',
              align='left'),
      cells=dict(values=[df[col] for col in df.columns],
              fill_color='paleturquoise',
              align='left')
  )
  fig5 = go.Figure(data=[table_trace])
  fig5.update_layout(
      # title = title,
      height=450,  # Adjust the height value as desired
      width=1300,  # Adjust the width value as desired
      margin=dict(l=20, r=20, t=40, b=20)  # Adjust the margin values as desired
  )
  return fig5

def top_instate_df(reg):
  top_in_state = f"""
  SELECT re.name, r.in_state
  FROM nur_app.{reg} re
  JOIN nur_app.rank r ON re.rank_id = r.id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY r.in_state DESC
  LIMIT 5
  """
  tab1 = pd.read_sql_query(top_in_state, conn)
  return tab1 

def top_undrgrd_df(reg):
  top_undrgrd = f"""
  SELECT re.name, r.undergrad_enrollment
  FROM nur_app.{reg} re
  JOIN nur_app.rank r ON re.rank_id = r.id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY r.undergrad_enrollment DESC
  LIMIT 5
  """
  tab2 = pd.read_sql_query(top_undrgrd, conn) 
  return tab2
  

with st.expander(':red[Northeast Selection]', expanded=True):
  ne_states = region_df('Northeast')
  col1, col2 = st.columns([3,3], gap='small')
  # n_rnk = """
  # SELECT n.name,
  # RANK() OVER (ORDER BY rank_num)
  # FROM nur_app.northeast n
  # JOIN nur_app.rank r
  # ON r.id = n.rank_id
  # ORDER BY rank_num
  # LIMIT 3
  # """
  
  # n_fee = """
  # SELECT n.name, tuition_and_fees
  # FROM nur_app.northeast n
  # JOIN nur_app.rank r
  # ON r.id = n.rank_id
  # ORDER BY tuition_and_fees DESC
  # LIMIT 3
  # """
  
  with col1:
    st.plotly_chart(rank_plot('northeast'), use_container_width=True)
    
  with col2:
    st.plotly_chart(fees_plot('northeast'), use_container_width=True)
  
  user_state = st.selectbox('Select State', ne_states)
  col3, col4 = st.columns([3,3], gap='small')
  top_rank_user_state = f"""
  SELECT n.name, 
  RANK() OVER (ORDER BY rank_num)
  FROM nur_app.northeast n
  JOIN nur_app.rank r
  ON r.id = n.rank_id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY rank_num
  LIMIT 3
  """
  
  top_fees_user_state = f"""
  SELECT n.name, tuition_and_fees
  FROM nur_app.northeast n
  JOIN nur_app.rank r
  ON r.id = n.rank_id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY tuition_and_fees DESC
  LIMIT 3
  """

  with col3:
    st.plotly_chart(inner_rank(top_rank_user_state), use_container_width=True)
    st.plotly_chart(tab_viz(top_instate_df('northeast')), use_container_width=True)
  
  with col4:
    st.plotly_chart(inner_fees(top_fees_user_state), use_container_width=True)
    st.plotly_chart(tab_viz(top_undrgrd_df('northeast')), use_container_width=True)
  
with st.expander(':red[Midwest Selection]', expanded=True):
  mw_states = df_nur[df_nur['region']=='Midwest']['state_full'].unique().tolist() 
  col1, col2 = st.columns([3,3], gap='small')
  mw_rnk = """
  SELECT md.name,
  RANK() OVER (ORDER BY rank_num)
  FROM nur_app.midwest md
  JOIN nur_app.rank r
  ON r.id = md.rank_id
  ORDER BY rank_num
  LIMIT 3
  """
  
  mw_fee = """
  SELECT md.name, tuition_and_fees
  FROM nur_app.midwest md
  JOIN nur_app.rank r
  ON r.id = md.rank_id
  ORDER BY tuition_and_fees DESC
  LIMIT 3
  """

  with col1:
    st.plotly_chart(rank_plot(mw_rnk), use_container_width=True)
  
  with col2:
    st.plotly_chart(fees_plot(mw_fee), use_container_width=True)
    
  user_state = st.selectbox('Select State', mw_states)
  col3, col4 = st.columns([3,3], gap='small')
  top_rank_user_state_md = f"""
  SELECT md.name, 
  RANK() OVER (ORDER BY rank_num)
  FROM nur_app.midwest md
  JOIN nur_app.rank r
  ON r.id = md.rank_id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY rank_num
  LIMIT 3
  """
  
  top_fees_user_state_md = f"""
  SELECT md.name, tuition_and_fees
  FROM nur_app.midwest md
  JOIN nur_app.rank r
  ON r.id = md.rank_id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY tuition_and_fees DESC
  LIMIT 3
  """
  
  with col3:
    st.plotly_chart(inner_rank(top_rank_user_state_md), use_container_width=True)

  with col4:
    st.plotly_chart(inner_fees(top_fees_user_state_md), use_container_width=True)
  
  
with st.expander(':red[South Selection]', expanded=True):
  s_states = df_nur[df_nur['region']=='South']['state_full'].unique().tolist() 
  col1, col2 = st.columns([3,3], gap='small')
  s_rnk = """
  SELECT s.name,
  RANK() OVER (ORDER BY rank_num)
  FROM nur_app.south s
  JOIN nur_app.rank r
  ON r.id = s.rank_id
  ORDER BY rank_num
  LIMIT 3
  """
  
  s_fee = """
  SELECT s.name, tuition_and_fees
  FROM nur_app.south s
  JOIN nur_app.rank r
  ON r.id = s.rank_id
  ORDER BY tuition_and_fees DESC
  LIMIT 3
  """

  with col1:
    st.plotly_chart(rank_plot(s_rnk), use_container_width=True)
  
  with col2:
    st.plotly_chart(fees_plot(s_fee), use_container_width=True)
    
  user_state = st.selectbox('Select State', s_states)
  col3, col4 = st.columns([3,3], gap='small')
  top_rank_user_state_s = f"""
  SELECT s.name, 
  RANK() OVER (ORDER BY rank_num)
  FROM nur_app.south s
  JOIN nur_app.rank r
  ON r.id = s.rank_id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY rank_num
  LIMIT 3
  """
  
  top_fees_user_state_s = f"""
  SELECT s.name, tuition_and_fees
  FROM nur_app.south s
  JOIN nur_app.rank r
  ON r.id = s.rank_id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY tuition_and_fees DESC
  LIMIT 3
  """
  
  with col3:
    st.plotly_chart(inner_rank(top_rank_user_state_s), use_container_width=True)
    
  with col4:
    st.plotly_chart(inner_fees(top_fees_user_state_s), use_container_width=True)
  
with st.expander(':red[West Selection]', expanded=True):
  w_states = df_nur[df_nur['region']=='West']['state_full'].unique().tolist() 
  col1, col2 = st.columns([3,3], gap='small')
  w_rnk = """
  SELECT w.name,
  RANK() OVER (ORDER BY rank_num)
  FROM nur_app.west w
  JOIN nur_app.rank r
  ON r.id = w.rank_id
  ORDER BY rank_num
  LIMIT 3
  """
  
  w_fee = """
  SELECT w.name, tuition_and_fees
  FROM nur_app.west w
  JOIN nur_app.rank r
  ON r.id = w.rank_id
  ORDER BY tuition_and_fees DESC
  LIMIT 3
  """
  
  with col1:
    st.plotly_chart(rank_plot(w_rnk), use_container_width=True)
  
  with col2:
    st.plotly_chart(fees_plot(w_fee), use_container_width=True)
    
  user_state = st.selectbox('Select State', w_states)
  col3, col4 = st.columns([3,3], gap='small')
  top_rank_user_state_w = f"""
  SELECT w.name, 
  RANK() OVER (ORDER BY rank_num)
  FROM nur_app.west w
  JOIN nur_app.rank r
  ON r.id = w.rank_id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY rank_num
  LIMIT 3
  """
  
  top_fees_user_state_w = f"""
  SELECT w.name, tuition_and_fees
  FROM nur_app.west w
  JOIN nur_app.rank r
  ON r.id = w.rank_id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY tuition_and_fees DESC
  LIMIT 3
  """

  with col3:
    st.plotly_chart(inner_rank(top_rank_user_state_w), use_container_width=True)

  with col4:
    st.plotly_chart(inner_fees(top_fees_user_state_w), use_container_width=True)   

with st.expander(':red[School Recommender]', expanded=True):
  st.text('In Progres.......')
  
  