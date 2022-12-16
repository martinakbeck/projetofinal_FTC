import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from utils import *
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import time

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout='wide'
)

#import dataframe
df = pd.read_csv("../repos/zomato.csv")

df1 = clean_code(df)


# ======================================
### Sidebar
# ======================================

st.header('Fome Zero!')

image = Image.open('logo.png')
st.sidebar.image(image, width=60)

st.sidebar.markdown('# Fitros')



#============Filtro País=============
countries_list = df1['country_code'].unique()

countries = st.sidebar.container()
all = st.sidebar.checkbox("Selecionar todos", value=True)
 
if all:
    selected_options = countries.multiselect("Escolha os Paises que Deseja visualizar os Restaurantes:", countries_list, countries_list)
else:
    selected_options =  countries.multiselect("Escolha os Paises que Deseja visualizar os Restaurantes:", countries_list, default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

#========== Ligar Filtro =============
linhas_selecionadas = df1['country_code'].isin(selected_options)
df1 = df1.loc[linhas_selecionadas, :]


#============Botão Download=============

st.sidebar.markdown('### Dados Tratados')
csv = convert_df(df1)

st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='data.csv',
    mime='text/csv',
)



st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')


#====================================================
#               LAYOUT
#====================================================

st.markdown('### Encontre o seu Restaurante preferido!')



    
tab1, tab2 = st.tabs(["🎲 Números", "🗺️ Mapa"])


with tab1:
    col1, col2 = st.columns(2)
        
    restaurantes_unicos = metricas_gerais(df1, 'restaurant_id')
    col1.metric('Restaurantes Cadastrados', restaurantes_unicos)

    paises_unicos = metricas_gerais(df1, 'country_code')
    col1.metric('Países Cadastrados', paises_unicos)

    cidades_unicas = metricas_gerais(df1, 'city')
    col2.metric('Cidades Cadastradas', cidades_unicas)

    tipos_culinarios = metricas_gerais(df1, 'cuisines')
    col2.metric('Tipos de Culinárias', tipos_culinarios)



with tab2:   

    st.markdown( '## Mapa' )
    with st.spinner('Carregando mapa...'):
        data_plot = df1.loc[:, ['city', 'restaurant_name', 'longitude', 'latitude']].reset_index()
        # Desenhar o mapa
        map_ = folium.Map( zoom_start=11 )
        cluster = MarkerCluster().add_to(map_)

        for index, location_info in data_plot.iterrows():
            folium.Marker( [location_info['latitude'],
                location_info['longitude']],
                popup=location_info['restaurant_name'], icon= folium.Icon(color='lightgray', icon='home', prefix='fa') ).add_to( cluster )

        folium_static(map_)    

            


    
