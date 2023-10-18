import streamlit as st
import pandas as pd
import numpy as np
import datetime
import spacy
import re
from sklearn.metrics.pairwise import cosine_similarity



#Función para leer distintas sheets del excel
def load_data(n_rows=None):
    polizas_df = pd.read_excel(uploaded_xlsx, sheet_name="POLIZAS", nrows=n_rows)
    siniestros_df = pd.read_excel(uploaded_xlsx, sheet_name="SINIESTROS", nrows=n_rows)
    return polizas_df, siniestros_df

#Título de la página
st.header('Extracción de información polizas y siniestros')

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.write('  ')

with col3:
    st.image("https://coacharya.com/wp-content/uploads/2017/09/kpmg-logo.png", use_column_width=False, width=150)

#Imagen
st.image("https://segurosypensionesparatodos.fundacionmapfre.org/media/seguros/principios-seguro-1194x535-1.png", caption=None)

#Subir Excel
uploaded_xlsx = st.file_uploader("Cargar un archivo XLSX", type=["xlsx"], key='xlsx')

try:
    # Extrae el texto del XLSX
    data = load_data()
    st.session_state['data_key'] = data
except:
    st.error("Please make sure that you input an xlsx file")
    st.stop()



#df ordenado por fecha
data_0 = data[0].set_index('FECHA DE EFECTO')

#Dropdown para seleccionar que columnas mostar
columns = st.sidebar.multiselect("Elige que columnas mostar", data_0.columns)

#Dropdown para seleccionar que paises mostar
countries = st.sidebar.multiselect("Elige que paises mostar", data_0['PAIS'].unique())

#Seleccionar fecha inicio y final
col1, col2 = st.columns(2)

with col1:
    ini_date = st.date_input('Fecha de inicio', value=datetime.date(2018, 1, 1))
with col2:
    fin_date = st.date_input('Fecha límite')

#df mostrando datos entre fecha inicio y final
data_filt_date = data_0.loc[str(ini_date):str(fin_date)]


#distintos casos para mostrar df filtrado
if len(columns) == 0 and len(countries) == 0:
    st.write(data_filt_date)

elif len(columns) == 0 and len(countries) != 0:
    data_filt_date_country = data_filt_date.loc[data_filt_date['PAIS'].isin(countries)]
    st.write(data_filt_date_country)
else:
    if len(countries) != 0:
        data_filt_date_country = data_filt_date.loc[data_filt_date['PAIS'].isin(countries)]
        st.write(data_filt_date_country[columns])
    else:
        st.write(data_filt_date[columns])
