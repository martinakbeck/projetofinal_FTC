import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from utils import *
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cidades",
    page_icon="🏙️",
    layout='wide'
)

#import dataframe
df = pd.read_csv("../repos/zomato.csv")

df1 = clean_code(df)


# ======================================
### Sidebar
# ======================================

st.header('🏙️ Visão Cidades')

image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Fitros')

#============Filtro País=============
countries_list = df1['country_code'].unique()

countries = st.sidebar.container()
all = st.sidebar.checkbox("Selecionar todos", value=False)
 
if all:
    selected_options = countries.multiselect("Escolha os Paises que Deseja visualizar os Restaurantes:",
        countries_list, countries_list)
else:
    selected_options =  countries.multiselect("Escolha os Paises que Deseja visualizar os Restaurantes:",
        countries_list, default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])
    
top_rest = st.sidebar.slider('Quantidade de restaurantes:', 0, 20, 10)  

    
#========== Ligar Filtro =============
linhas_selecionadas = df1['country_code'].isin(selected_options)
df1 = df1.loc[linhas_selecionadas, :]




# ======================================
### Layout
# ======================================

with st.container():
    df_aux = (df1.loc[:, ['restaurant_id', 'city', 'country_code']]
              .groupby('city')
              .count()
              .sort_values('restaurant_id', ascending = False)
              .reset_index())
    
    df_top = df_aux.head(top_rest)
    
    fig = (px.bar( df_top, x='city', y='restaurant_id', 
                  color='city', 
                  title=f'Top {top_rest} Cidades com mais Restaurantes na Base de Dados', 
                  text='restaurant_id', 
                  labels={'restaurant_id': 'Quantidade de Restaurantes', 'city': 'Cidades'} ))
    
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        df_aux = (df1.loc[df1['aggregate_rating'] > 4, ['city', 'restaurant_id', 'country_code']]
                  .groupby('city')
                  .count()
                  .sort_values('restaurant_id', ascending = False)
                  .reset_index())

        df_top = df_aux.head(top_rest)
        
        fig = (px.bar(df_top, x='city', y='restaurant_id', 
                      color='city', 
                      title=f'Top {top_rest} Cidades com Restaurantes com média de avaliação acima de 4', 
                      text='restaurant_id', 
                      labels={'restaurant_id': 'Quantidade de Restaurantes', 'city': 'Cidades'}))
        
        st.plotly_chart(fig, use_container_width=True) 

    with col2:
        df_aux = (df1.loc[df1['aggregate_rating'] < 2.5, ['city', 'restaurant_id']]
                  .groupby('city')
                  .count()
                  .sort_values('restaurant_id', ascending = False)
                  .reset_index())

        df_top = df_aux.head(top_rest)
        
                
        fig = (px.bar(df_top, x='city', y='restaurant_id', 
                      color='city', 
                      title=f'Top {top_rest} Cidades com Restaurantes com média de avaliação abaixo de 2.5', 
                      text='restaurant_id', 
                      labels={'restaurant_id': 'Quantidade de Restaurantes', 'city': 'Cidades'}))
        
        st.plotly_chart(fig, use_container_width=True) 
        
        
with st.container():
    df_aux = (df1.loc[:, ['cuisines', 'city','country_code']]
              .drop_duplicates()
              .groupby('city')
              .count()
              .sort_values('cuisines', ascending=False )
              .reset_index())
    
    df_top = df_aux.head(top_rest)

    fig = (px.bar(df_top, x='city', y='cuisines', 
                  color='city', 
                  title=f'Top {top_rest} Cidades com Restaurantes com Tipos Culinários Distintos',
                  text='cuisines', 
                  labels={'cuisines': 'Quantidade de Tipos Culinários', 'city': 'Cidades'}))
    
    st.plotly_chart(fig, use_container_width=True) 