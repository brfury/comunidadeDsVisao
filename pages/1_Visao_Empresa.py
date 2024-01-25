import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import folium
from streamlit_folium import folium_static


df = pd.read_csv(r'dataSetFood\train.csv')

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
image = Image.open(r'images\analysis.png')
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

# selecionar por Trafico
linhas = df1['Road_traffic_density'].isin(trafic_options)
df1 = df1.loc[linhas, :]



st.sidebar.markdown('''___''')
st.sidebar.markdown('### by Bruno S Sousa')

#------------------------------
#   Layout streamlit
#------------------------------

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

#semanas = df1.loc[:, ['ID','week_of_year']].groupby('week_of_year').count().reset_index()
#char = plt.plot(semanas['week_of_year'], semanas['ID'])
colums = df1.loc[:,['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()

#ax.plot(semanas['week_of_year'], semanas['ID'])
fig = px.bar(colums, x='Order_Date', y='ID')
with tab1:
  with st.container():
    st.markdown('# order by')
    st.plotly_chart(fig)
  with st.container():
    col1, col2 = st.columns(2)

    with col1:
      st.markdown('# Trafic Order Share')
      dis = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
      dis['percentID'] = dis.ID / dis.ID.sum()
      print(dis.head())

      st.plotly_chart(px.pie(dis, values='percentID', names='Road_traffic_density'), use_container_width=True)
      
    with col2:
      st.markdown('# Trafic Order City')
      df1 = df1.loc[(df1['City'] != 'NaN'), :]

      citvol = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    
      st.plotly_chart(px.scatter(citvol, x='City', y='Road_traffic_density', size='ID',color='City'),use_container_width=True)

with tab2:
  st.markdown('Order By Week')
  #df1['week_of_year'] = df1['Order_Date'].dt.strftime(date_format='%U')
  semanas = df1.loc[:, ['ID','week_of_year']].groupby('week_of_year').count().reset_index()
  st.plotly_chart(px.line(semanas,x='week_of_year', y='ID'))  # Plotar a semana contra a contagem de IDs


with tab3:
  
  columns = [
  'City',
  'Road_traffic_density',
  'Delivery_location_latitude',
  'Delivery_location_longitude'
    ]
  columns_groupby = ['City', 'Road_traffic_density']
  data_plot = df1.loc[:, columns].groupby( columns_groupby ).median().reset_index()
  data_plot = data_plot[data_plot['City'] != 'NaN']
  data_plot = data_plot[data_plot['Road_traffic_density'] != 'NaN']
  # Desenhar o mapa
  map_ = folium.Map( zoom_start=11 )
  for index, location_info in data_plot.iterrows():
    folium.Marker( [location_info['Delivery_location_latitude'],
    location_info['Delivery_location_longitude']],
    popup=location_info[['City', 'Road_traffic_density']] ).add_to( map_ )

  folium_static(map_, width=800, height=600)
    

