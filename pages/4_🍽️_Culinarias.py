import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from utils import *
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Culinárias",
    page_icon="🍽️",
    layout='wide'
)

#import dataframe
df = pd.read_csv("repos/zomato.csv")

df1 = clean_code(df)


# ======================================
### Sidebar
# ======================================

st.header('🍽️ Visão de Tipos Culinários')

image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Fitros')
st.sidebar.write('### Escolha os Paises que Deseja visualizar os Restaurantes')


# ======================================
###              FILTROS
# ======================================

#================Tipo de culinária===================
cuisines_list = df1['cuisines'].unique()

cuisines = st.sidebar.container()
selected_cuisines = (cuisines.multiselect("Escolha os tipos culinários:",cuisines_list,
                                          default=['Italian', 'Japanese', 'American', 'Brazilian', 'Indian', 'Arabian', 'BBQ' ] ))

top_rest = st.sidebar.slider('Quantidade de restaurantes:', 0, 20, 7)  

#========== Ligar Filtro =============
linhas_selecionadas = df1['cuisines'].isin(selected_cuisines)
df1 = df1.loc[linhas_selecionadas, :]

#================País===================
countries_list = df1['country_code'].unique()

countries = st.sidebar.container()
all = st.sidebar.checkbox("Selecionar todos", value=False)
 
if all:
    selected_options = countries.multiselect("Escolha os paises que deseja visualizar os restaurantes:",
        countries_list, countries_list)
else:
    selected_options =  countries.multiselect("Escolha os Paises que deseja visualizar os restaurantes:",
        countries_list, default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

#========== Ligar Filtro =============
linhas_selecionadas = df1['country_code'].isin(selected_options)
df1 = df1.loc[linhas_selecionadas, :]
    
    




# ======================================
### Layout
# ======================================

st.markdown('### Melhores Restaurantes dos Princpais tipos Culinários')

with st.container():
    
    col1, col2, col3, col4, col5 = st.columns(5)

    
    
    with col1:
        nome, nota = media_culinaria(df1, 'Italian')
        col1.metric(label=f'Italiana: {nome}', value=f'{nota}/5.0')          
        
    with col2:
        nome, nota = media_culinaria(df1, 'American')
        col2.metric(label=f'Americana: {nome}', value=f'{nota}/5.0')
        
    with col3:
        nome, nota = media_culinaria(df1, 'Japanese')
        col3.metric(label=f'Japanese: {nome}', value=f'{nota}/5.0')
        
    with col4:
        nome, nota = media_culinaria(df1, 'Indian')
        col4.metric(label=f'Indiana: {nome}', value=f'{nota}/5.0')
        
    with col5:
        nome, nota = media_culinaria(df1, 'Brazilian')
        col5.metric(label=f'Brasileira: {nome}', value=f'{nota}/5.0')
        


    
    
with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1:        
        fig = grafico_top_culinaria(df1, top_rest, 'Melhores', top_asc=False)
        st.plotly_chart(fig, use_container_width=True) 
        
    with col2:
        fig = grafico_top_culinaria(df1, top_rest, 'Piores', top_asc=True)
        st.plotly_chart(fig, use_container_width=True) 
        
        
with st.container():
    
    cols = ['restaurant_name', 'country_code', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']

    
    df_aux = (df1.loc[:, cols]
              .groupby('restaurant_name')
              .mean()
              .sort_values(['aggregate_rating'], ascending = False)
              .reset_index())
    df_top = df_aux.head(top_rest)
    st.markdown('### Tabela Top Restaurantes')
    with st.expander("Clique para expandir"):
        st.write(f'Top {top_rest} Restaurantes') 
        st.dataframe(df_top)
        
        
        
        
