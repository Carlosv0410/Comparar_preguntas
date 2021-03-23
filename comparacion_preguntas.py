# Librerias
import streamlit as st
import pandas as pd 
import altair as alt
from pandas import read_excel
import numpy as np
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)
# Lectura de Archivo Excel y convertir en DataFrame
df = pd.read_excel('DataInicial.xls',sheet_name='Variables')
# Crear una lista de las columnas del DataFrame 
nombre_columnas = df.columns
##### Seccion central de la aplicacion #####
st.title('Data Visualization')
# Crear Selectbox con la lista de columnas
selectbox1 = st.selectbox(
"select the question to analyze",
(nombre_columnas), index=1)
# Filtrar DataFrame en funcion de las columnas seleccionadas 1 Location 2 selectbox
df_group = df[['Location',selectbox1]]
st.subheader('DataFrame')
st.write(df_group)
# Tabla cruzada
tabla = pd.crosstab( index=df_group['Location'],columns=df_group[selectbox1], margins=True)
st.subheader('Crosstab')
st.write(tabla)
#Tabla cruzada porcentual
tabla2 = pd.crosstab( index=df_group['Location'],columns=df_group[selectbox1], normalize='index' , margins=True ).round(3)*100
st.subheader('Percentage crosstab')
st.write(tabla2)
# Filtrar dataframe en funcion de location experiencia con la radioactividad y el selectbox
#st.subheader('DataFrame 2')
df_group2 = df[['Location','Experience working with radioactivity',selectbox1]]
#Asignar Columna para contar en el dataframe 2 
df_group2 = df_group2.assign(conteo= 1)
#st.write(df_group2)
st.subheader('Pivot Table')
table = pd.pivot_table(df_group2, values='conteo', index=[ 'Location'],
                    columns=['Experience working with radioactivity', selectbox1], aggfunc=np.sum).apply(lambda r: r/r.sum(), axis=1)
st.write(table)
# Filtrar dataframe 2 por experiencia 
df_group3 = df_group2['Experience working with radioactivity'] == 'Yes'
filtro_experiencia = df_group2[df_group3]
#st.write(filtro_experiencia)
table2 = pd.pivot_table(filtro_experiencia, values='conteo', index=[ 'Location'],
                    columns=['Experience working with radioactivity', selectbox1], aggfunc=np.sum).apply(lambda r: r/r.sum(), axis=1)
st.subheader('Experience working with radioactivity Pivot Table')
st.write(table2)
df_group4 = df_group2['Experience working with radioactivity'] == 'No'
filtro_experiencia2 = df_group2[df_group4]
table3 = pd.pivot_table(filtro_experiencia2, values='conteo', index=[ 'Location'],
                    columns=['Experience working with radioactivity', selectbox1], aggfunc=np.sum).apply(lambda r: r/r.sum(), axis=1)
st.subheader('No Experience working with radioactivity Pivot Table')
st.write(table3)
st.subheader('Matplotlib Pivot Table')
table.T.plot(kind='bar')
st.pyplot() 
st.subheader('Matplotlib Pivot Table Experience working with radioactivity')
table2.T.plot(kind='bar')
st.pyplot() 
st.subheader('Matplotlib Pivot Table No Experience working with radioactivity')
table3.T.plot(kind='bar')
st.pyplot() 
st.subheader('Altair Visualization')
grafico1 = alt.Chart(df).mark_bar().encode(
	x= 'Location',
	y= 'count()',
	#column= alt.Column(selectbox1),
	#row=alt.Row(selectbox1),
	facet=alt.Facet(selectbox1,  columns=3),
	color= 'Location',
	tooltip=['Location','count()']   
).interactive().properties( width=150, height=160)
st.altair_chart(grafico1)