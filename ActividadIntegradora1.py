import streamlit as st
import pandas as pd 
import numpy as np
import datetime
from datetime import date, time, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

#Extracción de Datos. 
#El csv utilizado se encuentra en la sección de Anexos. 
#Se usa la libreria de Pandas para leer el archivo y cargar los datos al entorno de ejecución.
df = pd.read_csv('Policev1.csv')

#Limpieza de Datos
#Borramos aquellos atributos que tengan más del 75% de sus registros con valores nulos
df.dropna(axis = 1, thresh = int(len(df)*.75), inplace = True)
#Atributos eliminados:
#Filed Online
#HSOC Zones as of 2018-06-05
#OWED Public Spaces
#Central Market/Tenderloin Boundary Polygon - Updated
#Parks Alliance CPSI (27+TL sites)
#ESNCAG - Boundary File
#A partir de este punto hay dos opciones para seguir con la limpieza de datos sin manipular la información.
#Borrar los valores nulos sin tomar en cuenta antes la información dada sobre la base de datos por lo que queda una dataframe de 285237 rows × 30 columns
#O Eliminar los atributos que no estan definidos en el diccionario de variables que son: 'SF Find Neighborhoods','Current Police Districts','Current Supervisor Districts','Analysis Neighborhoods','Areas of Vulnerability, 2016'
#Se opta por la segunda opción.
df.drop(['SF Find Neighborhoods','Current Police Districts','Current Supervisor Districts','Analysis Neighborhoods','Areas of Vulnerability, 2016'], axis = 1, inplace = True)
df.dropna(inplace =True)

#Transformación de Datos.
#A continuación se usa las librerias Datetime y Pandas para la tranformación de algunas variables que se leyeron como tipo texto pero son referentes al tiempo
#Pasar variables correspondientes tipo texto a tipo fecha
df['Incident Datetime'] = pd.to_datetime(df['Incident Datetime'], format = '%Y/%m/%d %I:%M:%S %p')
df['Incident Date'] = pd.to_datetime(df['Incident Date'], format = '%Y/%m/%d')
h = []
for i in df.index:
    h.append(datetime.time(datetime.strptime(df.loc[i,'Incident Time'], '%H:%M')))
df['Incident Time'] = h
df['Report Datetime'] = pd.to_datetime(df['Report Datetime'], format = '%Y/%m/%d %I:%M:%S %p')

#Cambios que se requeriran para gráficos posteriores
df['diff'] =df['Report Datetime'] - df['Incident Datetime']
df['contador'] = 1

#Cambio requisito para establecer los filtros
df['Incident Datetime'] = df['Incident Datetime'].astype('M8[ms]').astype('O')
df['Incident Date'] = df['Incident Date'].astype('M8[D]').astype('O')
df['Report Datetime'] = df['Report Datetime'].astype('M8[ms]').astype('O')

#Empezamos con la creación de la app con la libreria de Streamlit
#Se especifica que se usará la anchura de la pantalla sin importar el tamaño por lo que los objetos en la app podrán ajustarse
st.set_page_config(layout = 'wide')
#Se establece el titulo principal del Dashboard
st.title ("Police Department Incident Reports")

#Creación de los Filtros
#Se crean listas con los valores únicos correspondientes a las columnas categoricas elegidas como filtros. Se establecerán 5 filtros.
Year = df['Incident Year'].unique().tolist()
Descripcion = df['Report Type Description'].unique().tolist()
Solucion = df['Resolution'].unique().tolist()
Vecindario = df['Analysis Neighborhood'].unique().tolist()
Fecha = df['Incident Date'].unique()

#Integración de los filtros al Dashboard. Estos se encontrarán en la parte superior, debajo del titulo.
#Se crea la primera fila con tres objetos correspondientes a los filtros de Año, Descripción del Incidente y Estado del Reporte
#Definición de los contenedores con st.columns()
a1,a2,a3 = st.columns(3)
#Asignación de los objetos a los contenedores
with a1:
    Year_s = st.multiselect('Year: ',
                       Year,
                       default = Year)
with a2:
    Descripcion_s = st.multiselect('Report Description: ',
                       Descripcion,
                       default = Descripcion)
with a3:
    Solucion_s = st.multiselect('Resolution: ',
                       Solucion,
                       default = Solucion)

#Se crea la segunda fila con dos objetos correspondientes a los filtros por Fecha y Vecindario
b1,b2 = st.columns((1,3))
with b2:
    Vecindario_s = st.multiselect('Neighborhood: ',
                       Vecindario,
                       default = Vecindario)
with b1:
    Fecha_s = st.date_input('Date: ',value=(Fecha.min(),Fecha.max()))

#Se crea una máscara que contiene la manipulación de los filtros por parte del cliente para que todos los gráficos respondan correctamente
mask = (df['Incident Year'].isin(Year_s)) & (df['Report Type Description'].isin(Descripcion_s)) & (df['Resolution'].isin(Solucion_s))& (df['Analysis Neighborhood'].isin(Vecindario_s)) & (df['Incident Date'].between(*Fecha_s))


#Las 6 figuras presentes fueron hechas con la libreria Plotly.

#GRAF 1 (fig)
#Es un mapa que muestra los dónde ocurrieron los incidentes de acuerdo a la Latitud y Longitud.
#Cuando el señalador pasa sobre los puntos se muestra el Id del reporte, el Vecindario, las calles que intersectan el lugar del incidente, el distrito policiaco y la descripción del Incidente a manera de tooltip/label.


fig = px.scatter_mapbox(df[mask],
                        lat="Latitude",
                        lon="Longitude",
                        hover_name="Row ID",
                        hover_data=['Analysis Neighborhood','Intersection','Police District','Report Type Description'],
                        color_discrete_sequence=["red"],
                        zoom=11,
                        height=500)
fig.update_layout(mapbox_style="stamen-toner")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(title='San Francisco Crime Map')



#GRAF 2 (fig1)
#Es un diagrama de lineas que muestra la cantidad promedio de reportes de incidentes por Hora del día (Hora-Minuto-Segundo)
#Como tooltip/label se muestra (HORA DEL DÍA, INCIDENTES PROMEDIO)
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df[mask]['Incident Time'].sort_values().unique(),
                          y=df[mask].groupby(['Incident Time']).count()['contador']/df[mask].groupby(['Incident Time','Incident Datetime']).count()['contador'].groupby('Incident Time').count(),
                          line=dict(color='red', width=4)))
fig1.update_layout(title='Cases throughout the day', xaxis_title='Time', yaxis_title='Average Cases')
fig1.update_xaxes(showgrid=False)
fig1.update_yaxes(showgrid=False)

#GRAF 3 (fig2)
#Con la libreria pandas se crea un subconjunto que agrupa las variables de Día de la Semana con el Estado del Reporte y regresa la media en días que se tardo en levantar el reporte desde que sucedio el incidente. 
df1 = pd.DataFrame({'count' : df[mask].groupby(['Incident Day of Week','Resolution'])['diff'].mean()}).reset_index()
df1['Incident Day of Week'] = pd.Categorical(df1['Incident Day of Week'], ["Monday", "Tuesday", 'Wednesday', 'Thursday','Friday','Saturday', "Sunday"])
df1.sort_values("Incident Day of Week", inplace = True)
#Es una grafica de barras que muestra el promedio de días de diferencia entre el levantamiento del reporte y la fecha del incidente por día categorizando al mismo tiempo con el Estado del Reporte. 
fig2 = px.bar(df1,
              x="Incident Day of Week",
              y=((df1['count']/60)/60)/24,
              color="Resolution",
              color_discrete_sequence = ['#c40000','#e00110','#ff3030','#ff7676'],
              title = "Days of Difference: Report and Incident by Day of the Week and Incident Resolution")
fig2.update_layout(yaxis_title='Days of Difference between Report and Incident', xaxis_title='Day of the Week')


#GRAF 4 (fig3)
#Es un diagrama de lineas que muestra un conteo de Incidentes a traves del tiempo: Historial de Incidentes de Crimen
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df[mask].sort_values(by=['Incident Date'])['Incident Date'].unique(), y=df[mask].sort_values(by=['Incident Date']).groupby(['Incident Date']).sum()['contador'], line=dict(color='red', width=4)))
fig3.update_layout(title = 'Crime Record', xaxis_title = 'Date', yaxis_title='Amount of Crimes')
fig3.update_xaxes(showgrid=False)
fig3.update_yaxes(showgrid=False)



#GRAF 5 (fig4)
#Es un gráfico jerárquico que muestra en un circulo interior el Distrito Policial que atendió el reporte y en un circulo exterior el Vecindario donde el Incidente ocurrió. El área de estos circulos dependerá de la cantidad de Reportes registrados. 
fig4 = px.sunburst(df[mask], color_discrete_sequence = ['#c40000','#ff7676'], values='contador', path=['Analysis Neighborhood','Police District'], hover_name='Analysis Neighborhood')
fig4.update_layout(plot_bgcolor="white", title = 'Crimes by Police District and Neighborhood')

#GRAF 6 (fig5)
#Es un gráfico jerárquico que muestra en un área exterior el Estado del reporte y en un área interior la Subcaegoría del Incidente. El área general de estos cuadrados dependerá de la cantidad de Reportes registrados.
fig5 = px.treemap(df[mask], color_discrete_sequence = ['#c40000','#ff7676'], values='contador', path=['Resolution','Incident Subcategory'], hover_name='Incident Subcategory')
fig5.update_layout(plot_bgcolor="white", title = 'Crimes by Resolution and Incident Subcategory')

#Agregamos los gráficos hechos a la aplicación con la libreria de Streamlit
#En la tercera fila, después de los filtros, estarán las figuras fig4 y fig 
c1,c2 = st.columns((3,5))
with c1:
    st.plotly_chart(fig4)
with c2:
    st.plotly_chart(fig)
#En la cuarta fila estarán las figuras fig3 y fig5 
d1,d2 = st.columns((1,1))
with d1:
    st.plotly_chart(fig3)
with d2:
    st.plotly_chart(fig5)
#En la quinta fila estarán las figuras fig2 y fig1
e1,e2 = st.columns((1,1))
with e1:
    st.plotly_chart(fig2)
with e2:
    st.plotly_chart(fig1)
