import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from utils import *
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import time

st.set_page_config(
    page_title="Fome Zero",
    page_icon="🍽️",
    layout='wide'
)


# ======================================
### Import Dataframe
# ======================================

df = pd.read_csv("../repos/zomato.csv")
df1 = clean_code(df)
df2 = df1.copy()

# ======================================
### Sidebar
# ======================================

st.header('Fome Zero!')

image = Image.open('logo.png')
st.sidebar.image(image, width=60)

st.sidebar.markdown('# Fitros')

# ======================================
### Filtro
# ======================================
countries_list = df1['country_code'].unique()

countries = st.sidebar.container()
all = st.sidebar.checkbox("Selecionar todos", value=False)
 
if all:
    selected_options = countries.multiselect("Escolha os Paises que Deseja visualizar os Restaurantes:", countries_list, countries_list)
else:
    selected_options =  countries.multiselect("Escolha os Paises que Deseja visualizar os Restaurantes:", countries_list, default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

#========== Ligar Filtro =============
linhas_selecionadas = df1['country_code'].isin(selected_options)
df1 = df1.loc[linhas_selecionadas, :]


# ======================================
### Botão Download
# ======================================

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

    
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏙️ Visão Cidades", "🌍 Visão Países", "🍽️ Visão de Tipos Culinários", "🗺️ Mapa", "🎲 Métricas Gerais" ])
   
#===========================
# VISÃO CIDADES
#==========================
with tab1:
    top_rest = st.slider('Quantidade de restaurantes:', 0, 20, 10)  

    with st.container():

        fig = grafico_cidade_restaurante(df1, top_rest)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            fig = grafico_media_quatro(df1, top_rest)
            st.plotly_chart(fig, use_container_width=True) 

        with col2:
            fig = grafico_media_dois(df1, top_rest)
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

#===========================
# VISÃO PAÍSES
#==========================
        
with tab2:
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

            
#===========================
# VISÃO TIPOS CULINÁRIOS
#==========================
with tab3:

    cuisines_list = df1['cuisines'].unique()

    cuisines = st.container()
    selected_cuisines = (cuisines.multiselect("Escolha os tipos culinários:",cuisines_list,
                                              default=['Italian', 'Japanese', 'American', 'Brazilian', 'Indian', 'Arabian', 'BBQ' ] ))

    #========== Ligar Filtro =============
    linhas_selecionadas = df1['cuisines'].isin(selected_cuisines)
    df1 = df1.loc[linhas_selecionadas, :]

    with st.container():

        col1, col2 = st.columns(2)

        with col1:        
            fig = grafico_top_culinario(df1, 'Melhores', top_asc=False)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = grafico_top_culinario(df1,'Piores', top_asc=True)
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
            
#===========================
# MAPA
#==========================            
            
with tab4:   

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
            

#===========================
# NÚMEROS
#==========================
    
with tab5:
    with st.container():
        st.markdown('### Melhores Restaurantes dos Princpais tipos Culinários')
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
    
    st.markdown("""---""")
    with st.container():
        st.markdown('### Números da plataforma')
        col1, col2, col3, col4 = st.columns(4)

        restaurantes_unicos = metricas_gerais(df2, 'restaurant_id')
        col1.metric('Restaurantes Cadastrados', restaurantes_unicos)

        paises_unicos = metricas_gerais(df2, 'country_code')
        col2.metric('Países Cadastrados', paises_unicos)

        cidades_unicas = metricas_gerais(df2, 'city')
        col3.metric('Cidades Cadastradas', cidades_unicas)

        tipos_culinarios = metricas_gerais(df2, 'cuisines')
        col4.metric('Tipos de Culinárias', tipos_culinarios)


