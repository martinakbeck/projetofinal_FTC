import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from utils import *
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Países",
    page_icon="🌍",
    layout='wide'
)

#import dataframe
df = pd.read_csv("../repos/zomato.csv")

df1 = clean_code(df)


# ======================================
### Sidebar
# ======================================

st.header('🌍 Visão Países')

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
    
#========== Ligar Filtro =============
linhas_selecionadas = df1['country_code'].isin(selected_options)
df1 = df1.loc[linhas_selecionadas, :]


# ======================================
### Layout
# ======================================

with st.container():
    df_aux = (df1.loc[:, ['restaurant_id', 'country_code']]
              .groupby('country_code')
              .count()
              .sort_values(['restaurant_id','country_code'], ascending = False)
              .reset_index())
    
    fig = (px.bar(df_aux, x='country_code', y='restaurant_id', 
                  text='restaurant_id', 
                  labels={'restaurant_id': 'Quantidade de Restaurantes', 'country_code': 'Países'}, 
                  title='Quatidade de Restaurantes por País'))
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    df_sem_cidade_duplicada = df1.drop_duplicates('city')
    df1_cidade_pais = (df_sem_cidade_duplicada.loc[:, ['city', 'country_code']]
                    .groupby('country_code')
                    .count()
                    .sort_values('city', ascending=False)
                    .reset_index())
    
    fig = (px.bar(df1_cidade_pais, x='country_code', y='city', 
                  text='city', 
                  labels={'city': 'Quantidade de Cidades', 'country_code': 'Países'}, 
                  title='Quatidade de Cidade por País'))
    
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
       
        fig = grafico_media_pais(df1, 'votes')        
        st.plotly_chart(fig, use_container_width=True)        
        
    with col2:
        fig = grafico_media_pais(df1, 'average_cost_for_two')        
        st.plotly_chart(fig, use_container_width=True) 
