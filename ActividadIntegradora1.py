import streamlit as st
import pandas as pd
import numpy as np
#Importar el Dataframe
df=pd.read_csv("Policev1.csv")
df = df[['Incident Number','Incident Datetime','Incident Category','Incident Subcategory','Incident Description',
         'Resolution','Police District','Analysis Neighborhood','Latitude','Longitude', 'Incident Day of Week',
         'Incident Year']]
#Opciones para el usuario
#Distrito
distritos=df['Police District'].unique() # Todos los distritos
distrito=st.sidebar.selectbox("Selecte the Police District", distritos)
df=df[df['Police District']==distrito]
#Vecindario
vecindarios=df['Analysis Neighborhood'].unique()
vecindario=st.sidebar.selectbox("Neighborhood: ", vecindarios)
df=df[df['Analysis Neighborhood']==vecindario]
st.title('Police Department Incident Reports ')
st.write('Police District :', distrito)
st.write('Neighborhood :', vecindario)
#st.write('Year :', año)
# Tabla de Incidentes
st.subheader('Incidents')
st.dataframe(df)
# INCIDENTES POR AÑO
import plotly.express as px
st.subheader('Incidents per year')
fig1 = px.histogram(df, x='Incident Year', nbins=3,text_auto=True)
fig1=fig1.update_layout(bargap=0.2)
st.plotly_chart(fig1 , use_container_width=True)
#GRAFICAS POR AÑO
tab1,tab2,tab3,tab4= st.tabs(['All years', '2018','2019','2020'])
with tab1:
#Incidentes
incidentes=len(df.axes[0])
st.metric('Total incidents', incidentes)
#Pie
st.subheader('Resolution')
pie=df.groupby('Resolution')['Incident Number'].count()
piet1= px.pie(pie, values='Incident Number', names=pie.index,
color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(piet1 , use_container_width=True)
#Mapa
st.subheader('Incidents Map')
mp1 = df[['Latitude','Longitude']]
mp1=mp1.rename(columns={"Latitude": "lat", "Longitude": "lon"})
mp1 = mp1.dropna()
st.map(mp1)
#Histograma
st.subheader('Incidents Category')
dft1=df[['Incident Category','Incident Subcategory']]
dft1=dft1.dropna()
figt1 = px.histogram(dft1, x='Incident Category', color='Incident Subcategory')
st.plotly_chart(figt1 , use_container_width=True)
st.subheader('Incidents per Day')
hist1 = px.histogram(df, x='Incident Day of Week',color='Incident Year',
nbins=3,text_auto=True)
hist1=hist1.update_layout(bargap=0.2)
st.plotly_chart(hist1 , use_container_width=True)
with tab2:
#Selección de datos
year_t2=df[df['Incident Year']==2018]
#Incidentes
incidentes=len(year_t2.axes[0])
st.metric('Total incidents in 2018', incidentes)
#Pie
st.subheader('Resolution')
pie=year_t2.groupby('Resolution')['Incident Number'].count()
piet2= px.pie(pie, values='Incident Number', names=pie.index,
color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(piet2 , use_container_width=True)
#Mapa
st.subheader('Incidents Map')
mp2 = year_t2[['Latitude','Longitude']]
mp2=mp2.rename(columns={"Latitude": "lat", "Longitude": "lon"})
mp2 = mp2.dropna()
st.map(mp2)
#Histograma
st.subheader('Incidents Category')
t2=year_t2[['Incident Category','Incident Subcategory']]
t2=t2.dropna()
figt2 = px.histogram(t2, x='Incident Category', color='Incident Subcategory')
st.plotly_chart(figt2 , use_container_width=True)
st.subheader('Incidents per Day')
hist2 = px.histogram(year_t2, x='Incident Day of Week',color='Incident Year',
nbins=3,text_auto=True)
hist2=hist2.update_layout(bargap=0.2)
st.plotly_chart(hist2 , use_container_width=True)
with tab3:
#Selección de datos
year_t3=df[df['Incident Year']==2019]
#Incidentes
incidentes=len(year_t3.axes[0])
st.metric('Total incidents in 2019', incidentes)
#Pie
st.subheader('Resolution')
pie=year_t3.groupby('Resolution')['Incident Number'].count()
piet3= px.pie(pie, values='Incident Number', names=pie.index,
color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(piet3 , use_container_width=True)
#Mapa
st.subheader('Incidents Map')
mp3 = year_t3[['Latitude','Longitude']]
mp3=mp3.rename(columns={"Latitude": "lat", "Longitude": "lon"})
mp3 = mp3.dropna()
st.map(mp3)
#Histograma
st.subheader('Incidents Category')
t3=year_t3[['Incident Category','Incident Subcategory']]
t3=t3.dropna()
figt3 = px.histogram(t3, x='Incident Category', color='Incident Subcategory')
st.plotly_chart(figt3 , use_container_width=True)
st.subheader('Incidents per Day')
hist3 = px.histogram(year_t3, x='Incident Day of Week',color='Incident Year',
nbins=3,text_auto=True)
hist3=hist3.update_layout(bargap=0.2)
st.plotly_chart(hist3 , use_container_width=True)
with tab4:
year_t4=df[df['Incident Year']==2020]
incidentes=len(year_t4.axes[0])
st.metric('Total incidents in 2020', incidentes)
st.subheader('Resolution')
pie=year_t4.groupby('Resolution')['Incident Number'].count()
piet4= px.pie(pie, values='Incident Number', names=pie.index,
color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(piet4 , use_container_width=True)
st.subheader('Incidents Map')
mp4 = year_t4[['Latitude','Longitude']]
mp4=mp4.rename(columns={"Latitude": "lat", "Longitude": "lon"})
mp4 = mp4.dropna()
st.map(mp4)
st.subheader('Incidents Category')
t4=year_t4[['Incident Category','Incident Subcategory']]
t4=t4.dropna()
figt4 = px.histogram(t4, x='Incident Category', color='Incident Subcategory')
st.plotly_chart(figt4 , use_container_width=True)
st.subheader('Incidents per Day')
hist4 = px.histogram(year_t4, x='Incident Day of Week',color='Incident Year',
nbins=3,text_auto=True)
hist4=hist4.update_layout(bargap=0.2)
st.plotly_chart(hist4 , use_container_width=True)

