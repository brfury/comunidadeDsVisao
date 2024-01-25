import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import folium
from streamlit_folium import folium_static


df = pd.read_csv(r'dataSetFood/train.csv')

def preprocessDataSet(df):
  select_rows = (df['Delivery_person_Age'] != 'NaN ')
  df1 = df.loc[select_rows, :]
  df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

  #convertendo Ratings para float
  df1.Delivery_person_Ratings = df1.Delivery_person_Ratings.astype(float)

  # convertendo Date para datatime

  df1['Order_Date'] =  pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

  # convertendo multiple_deliveries
  df1 = df1.loc[(df['multiple_deliveries'] != 'NaN '), :]
  df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(bool)

  df1 = df1.loc[(df['Road_traffic_density'] != 'NaN '), :]


  #Retirando espaços
  print(f'j = {df1.shape[1]}')
  print(f'I = {df1.shape[0]}')
  for j in range(df1.shape[1]):
    print(j)
    try:
      for i in range(df1.shape[0]):

        df1.iloc[i, j] = df1.iloc[i, j].replace(' ', '')
    except:
      print('*')
      continue

  #RETIRANDO OS ESPAÇOS MANEIRA 2
  for i in df.columns:
    try:
      df1.loc[:, i] = df1.loc[:, i].str.strip()
      print('pass')
    except:
      print('unpass')
      pass
  df1['week_of_year'] = df1['Order_Date'].dt.strftime(date_format='%U')
  with open('df1.csv', 'w') as df:
    df.write(df1.to_csv())


df1 = pd.read_csv('df1.csv')

#------------------------------
#   sidebar streamlit
#------------------------------
st.header('Visão cliente')
image = Image.open(r'images/analysis.png')
st.sidebar.image(image=image)
st.sidebar.markdown("# Curry company")
st.sidebar.markdown("## fasted delivere in tow")
st.sidebar.markdown('''___''')
st.sidebar.markdown("## selecione uma data limite")


# venv/Scripts/activate
#  streamlit run tes.py
from datetime import datetime
import streamlit as st
import pandas as pd

slider_value = datetime(2022, 4, 13)

data_slider = st.sidebar.slider(
    'Até qual valor?',
    value=slider_value,
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
)

trafic_options = st.sidebar.multiselect(
  'condições de transito',
    df1['Road_traffic_density'].unique().tolist(),
    default=df1['Road_traffic_density'].unique().tolist()
    )


# selecionar por data
linhas = pd.to_datetime(df1['Order_Date']) <= data_slider
df1 = df1.loc[linhas, :]
st.header(data_slider)

st.markdown('Visão entregadores')

tab1,tab2,tab3 = st.tabs(['visão grencial', '_', '_'])


with tab1:
    with st.container():
      st.title('Overal Metrics')
      col1,col2,col3,col4 = st.columns(4, gap='large')
      with col1:
        st.subheader('Maior de Idade')
        col1.metric(label='maior de idade',value=df1['Delivery_person_Age'].max())
      with col2:
        st.subheader('Menor de Idade')
        col2.metric(label='menor de idade',value=df1['Delivery_person_Age'].min())
      with col3:
        st.subheader('Melhor condição de veiculos')
      with col4:
        st.subheader('Pior condição de veiculos')
    with st.container():
      st.markdown('''___''')
      st.title('Avalições')
      col1,col2 = st.columns(2)
      with col1:
        st.subheader('Avaliação media por transito')
      with col2:
        st.subheader('Avaliação media por clima')
    with st.container():
      st.markdown('''___''')
      st.title('Velocidade entrgadores')
      col1,col2 = st.columns(2)
      with col1:
        st.subheader('top entregador mais rapido')
      with col2:
        st.subheader('top entregador mais lento')
      

