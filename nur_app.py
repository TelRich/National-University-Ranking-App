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
import streamlit.components.v1 as components

# Setting th epage size and title
st.set_page_config(layout='wide', page_title='National University Rank App')

# App Setup
with st.expander(':red[PROJECT TITLE]', expanded=True):
  st.markdown("<h1 style='text-align:center;'>National University Rank App</h1>", unsafe_allow_html=True)
  st.markdown("""<center>
In the dynamic landscape of higher education, the quest for the perfect college can be both exciting and bewildering for high school students. 
Faced with a multitude of options, students often grapple with considerations ranging from tuition expenses and graduation rates to geographical preferences 
and institutional rankings. To streamline this intricate journey, we have embarked on a mission to develop a streamlined, user-friendly searchable database. 
Leveraging the power of Streamlit, an innovative framework, we have created an intuitive app that enables students to pinpoint colleges that resonate with their specific criteria.

Recognizing that the decision to pursue higher education is a pivotal life choice, our project goes beyond traditional search capabilities. It aims to serve as a navigational tool, 
providing tailored guidance to help students traverse the sea of choices and make informed selections. By seamlessly integrating crucial factors such as tuition affordability, 
graduation rates indicative of institutional commitment, preferred geographic settings, and prestigious rankings, our app offers a comprehensive viewpoint that nurtures each student's aspirations.
The essence of our app's success lies in Streamlit's capacity to deliver an interactive and dynamic user experience. With its user-centric design philosophy, Streamlit empowers us to create an intuitive 
interface where students effortlessly input preferences and receive personalized results. Through data visualization and user-friendly controls, we believe our app will become an indispensable 
asset in the college search, facilitating decision-making and steering students towards institutions where they can flourish academically and personally.

In an age where technology bridges information gaps, our project seeks to leverage this potential for the benefit of education. By merging data-driven insights and an intuitive design, our searchable 
database, fueled by Streamlit, stands as a beacon of guidance. It aids high school students in charting their path towards a promising future within higher education institutions that resonate with their individual aspirations.
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

reg_cnt = df_nur['region'].value_counts().sort_values().to_frame()
fig3 = px.bar(reg_cnt, x=reg_cnt.index, y="count", text_auto=True,height=400, width=550,
             labels={'count':'', 'index': ''}, title="School Count by Region", color_discrete_sequence=px.colors.qualitative.Vivid)
fig3.update_yaxes(showticklabels=False)
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
    st.plotly_chart(fig3, use_container_width=True)  
  with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)
    
with st.expander(':red[Region Search]', expanded=True):
  st.text('Not sure which region you fall into! Insert your state and find out')
  all_states = df_nur['state_full'].unique().tolist() 
  usr_state = st.selectbox('Select State', all_states)
  state_reg = df_nur[df_nur['state_full'] == usr_state]['region'].iloc[0]
  st.write(f'{usr_state} is in the {state_reg} region')     

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

def inner_rank(reg):
  top_rank_user_state = f"""
  SELECT re.name, 
  RANK() OVER (ORDER BY rank_num)
  FROM nur_app.{reg} re
  JOIN nur_app.rank r
  ON r.id = re.rank_id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY rank_num
  LIMIT 3
  """ 
  df3 = pd.read_sql_query(top_rank_user_state, conn)
  fig3 = px.bar(df3, y="rank", x="name", text_auto=True,height = 350, width= 550, labels={'name':'', 'rank':''},
                color_discrete_sequence=px.colors.qualitative.G10)
  fig3.update_layout(title_text=f"Top Universities by Rank in {user_state}")
  fig3.update_yaxes(showticklabels=False)
  fig3.update_traces(textfont_color=text_color) 
  return fig3

def inner_fees(reg):
  top_fees_user_state = f"""
  SELECT re.name, tuition_and_fees
  FROM nur_app.{reg} re
  JOIN nur_app.rank r
  ON r.id = re.rank_id
  WHERE state_id = (SELECT DISTINCT state_id FROM nur_app.state WHERE state_full = '{user_state}')
  ORDER BY tuition_and_fees DESC
  LIMIT 3
  """
  df4 = pd.read_sql_query(top_fees_user_state, conn)
  fig4 = px.bar(df4, y="tuition_and_fees", x="name", text_auto=True,height = 350, width= 550, labels={'name':'', 'tuition_and_fees':''},
                color_discrete_sequence=px.colors.qualitative.G10)
  fig4.update_layout(title_text=f"Universities by High Fees in {user_state}")
  fig4.update_yaxes(showticklabels=False)
  fig4.update_traces(textfont_color=text_color)
  return fig4

def tab_viz(df):
  table_trace = go.Table(
      header=dict(values=list(df.columns),
                  fill_color='steelblue',
              align='left'),
      cells=dict(values=[df[col] for col in df.columns],
              fill_color='royalblue',
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
  
all_reg = ['Northeast', 'Midwest', 'South', 'West']
usr_region = st.selectbox('Select Region', all_reg) 

if usr_region == 'Northeast': 
  # NORTHEAST

  with st.expander(':red[Northeast Selection]', expanded=True):
    ne_states = region_df('Northeast')
    col1, col2 = st.columns([3,3], gap='small')
    
    with col1:
      st.plotly_chart(rank_plot('northeast'), use_container_width=True)
    with col2:
      st.plotly_chart(fees_plot('northeast'), use_container_width=True)
    
    user_state = st.selectbox('Select State', ne_states)
    col3, col4 = st.columns([3,3], gap='small')

    with col3:
      st.plotly_chart(inner_rank('northeast'), use_container_width=True)
      st.plotly_chart(tab_viz(top_instate_df('northeast')), use_container_width=True)
    with col4:
      st.plotly_chart(inner_fees('northeast'), use_container_width=True)
      st.plotly_chart(tab_viz(top_undrgrd_df('northeast')), use_container_width=True)

elif usr_region == 'Midwest':
  # MIDWEST
  with st.expander(':red[Midwest Selection]', expanded=True):
    mw_states = df_nur[df_nur['region']=='Midwest']['state_full'].unique().tolist() 
    col1, col2 = st.columns([3,3], gap='small')

    with col1:
      st.plotly_chart(rank_plot('midwest'), use_container_width=True)
    with col2:
      st.plotly_chart(fees_plot('midwest'), use_container_width=True)
      
    user_state = st.selectbox('Select State', mw_states)
    col3, col4 = st.columns([3,3], gap='small')
    
    with col3:
      st.plotly_chart(inner_rank('midwest'), use_container_width=True)
      st.plotly_chart(tab_viz(top_instate_df('midwest')), use_container_width=True)
    with col4:
      st.plotly_chart(inner_fees('midwest'), use_container_width=True)
      st.plotly_chart(tab_viz(top_undrgrd_df('midwest')), use_container_width=True)

elif usr_region == 'South':
  # SOUTH
  with st.expander(':red[South Selection]', expanded=True):
    s_states = df_nur[df_nur['region']=='South']['state_full'].unique().tolist() 
    col1, col2 = st.columns([3,3], gap='small')

    with col1:
      st.plotly_chart(rank_plot('south'), use_container_width=True)
    with col2:
      st.plotly_chart(fees_plot('south'), use_container_width=True)
      
    user_state = st.selectbox('Select State', s_states)
    col3, col4 = st.columns([3,3], gap='small')
    
    with col3:
      st.plotly_chart(inner_rank('south'), use_container_width=True) 
      st.plotly_chart(tab_viz(top_instate_df('south')), use_container_width=True)
    with col4:
      st.plotly_chart(inner_fees('south'), use_container_width=True)
      st.plotly_chart(tab_viz(top_undrgrd_df('south')), use_container_width=True)

elif usr_region == 'West':
  # WEST
  with st.expander(':red[West Selection]', expanded=True):
    w_states = df_nur[df_nur['region']=='West']['state_full'].unique().tolist() 
    col1, col2 = st.columns([3,3], gap='small')
    
    with col1:
      st.plotly_chart(rank_plot('west'), use_container_width=True)
    with col2:
      st.plotly_chart(fees_plot('west'), use_container_width=True)
      
    user_state = st.selectbox('Select State', w_states)
    col3, col4 = st.columns([3,3], gap='small')

    with col3:
      st.plotly_chart(inner_rank('west'), use_container_width=True)
      st.plotly_chart(tab_viz(top_instate_df('west')), use_container_width=True)

    with col4:
      st.plotly_chart(inner_fees('west'), use_container_width=True)   
      st.plotly_chart(tab_viz(top_undrgrd_df('west')), use_container_width=True)

with st.expander(':red[Power BI]', expanded=True):
  power = """<iframe title="Report Section" width="1200" height="1000" 
              src="https://app.powerbi.com/view?r=eyJrIjoiYTFlZTIwZGQtYzA4NS00YTNiLWJkZGEtZTQ3MmNjMWIyNmI1IiwidCI6ImNlMzBlNGMzLWM4NjItNGVlZC1hMzdjLWU3NmJjODNhY2ZmYSJ9" 
              frameborder="0" allowFullScreen="true"></iframe>"""
  components.html(power, height=600, width=1000)

with st.expander(':red[School Recommender]', expanded=True):
  st.text('In Progres.......')