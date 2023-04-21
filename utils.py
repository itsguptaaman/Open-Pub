import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import folium

from streamlit_folium import folium_static
from folium import plugins
from branca.element import Figure
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt


df = pd.read_csv("clean_data.csv")


def dist(lat1, long1, lat2, long2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula 
    dlon = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def find_nearest(lat, long):
    distances = df.apply(lambda row: dist(lat, long, row['latitude'], row['longitude']),axis=1)
    l = dict(distances.sort_values().iloc[:5])
    
    return df.loc[l.keys(), 'name'], l

def plot1():
    fig, ax = plt.subplots(figsize=(15, 7))

    dflc = df.groupby('local_authority').size().reset_index(name='pubs')
    dflc = dflc.nlargest(20, 'pubs')
    dflc = dflc.sort_values('pubs', ascending=False)

    g = sns.barplot(x='local_authority', y='pubs', data=dflc)
    g.set(title='Local authorities with largest number of pubs', xlabel='Local authorities', ylabel='Number of pubs')
    g.set_xticklabels(g.get_xticklabels(), rotation=90)
    st.pyplot(fig)

def plot2():
    fig, ax = plt.subplots(figsize=(15, 7))
    dflc = df.groupby('local_authority').size().reset_index(name='pubs')
    dflc = dflc.nsmallest(20, 'pubs').sort_values('pubs', ascending=False).reset_index(drop=True)

    g = sns.barplot(x='local_authority', y='pubs', data=dflc, color='red')
    g.set(title='Local authorities with smallest number of pubs', xlabel='Local authorities', ylabel='Number of pubs')
    g.set_xticklabels(g.get_xticklabels(), rotation=90)
    st.pyplot(fig)

def plot3():
    fig, ax = plt.subplots(figsize=(15, 7))
    dfn = df.groupby('name').size().reset_index(name='pubs').nlargest(20, 'pubs')
    dfn = dfn.sort_values('pubs', ascending=False)

    g = sns.barplot(x='name', y='pubs', data=dfn, order=dfn['name'], palette='Blues_d')
    g.set_title('Top 20 of most frequent pub names in England')
    g.set_xlabel('Pub names')
    g.set_ylabel('Number of pubs')
    g.set_xticklabels(g.get_xticklabels(), rotation=90)
    st.pyplot(fig)

def lat_lon_inputs():
    lat = st.text_input('Enter your current Latitude')
    lon = st.text_input('Enter your current Longtitude')
    return lat, lon

def display_locations(lat, lon):
    x, l= find_nearest(lat, lon)
    y = list(x.keys())

    lat1 = df.iloc[y[0]]["latitude"]
    lon1 = df.iloc[y[0]]["longitude"]
    name1 = df.iloc[y[0]]["name"]
    
    lat2 = df.iloc[y[1]]["latitude"]
    lon2 = df.iloc[y[1]]["longitude"]
    name2 = df.iloc[y[1]]["name"]
    
    lat3 = df.iloc[y[2]]["latitude"]
    lon3 = df.iloc[y[2]]["longitude"]
    name3 = df.iloc[y[2]]["name"]
    
    lat4 = df.iloc[y[3]]["latitude"]
    lon4 = df.iloc[y[3]]["longitude"]
    name4 = df.iloc[y[3]]["name"]
    
    lat5 = df.iloc[y[4]]["latitude"]
    lon5 = df.iloc[y[4]]["longitude"]
    name5 = df.iloc[y[4]]["name"]
    
    show_five_locations(lat, lon, lat1, lon1, name1, lat2, lon2, name2, lat3, lon3, name3, lat4, lon4, name4, lat5, lon5, name5)
    
    dt = {"Names(Pubs)":list(x), "Distance(Km)":list(l.values())}
    
    df1 = pd.DataFrame(dt)
    
    st.dataframe(df1)

def show_map():
    
    fig = Figure(width=800, height=50)
    m = folium.Map(location=[51.958698, 1.059041], zoom_start=11)
    fig.add_child(m)

    # add marker for Liberty Bell
    tooltip = "Ark Bar Restaurant"
    folium.Marker([51.958698, 1.059041], popup="Ark Bar Restaurant", tooltip=tooltip).add_to(m)
    # call to render Folium map in Streamlit
    folium_static(m)

def show_five_locations(lat, lon, lat1, lon1, name1, lat2, lon2, name2, lat3, lon3, name3, lat4, lon4, name4, lat5, lon5, name5):
    fig = Figure(width=900,height=350)
    m = folium.Map(location=[lat, lon], zoom_start=11)
    fig.add_child(m)

    #Adding markers to the map
    folium.Marker(location=[lat, lon],popup="Current Location", tooltip="Current Location").add_to(m)
    folium.Marker(location=[lat1, lon1],popup=name1, tooltip=name1).add_to(m)
    folium.Marker(location=[lat2, lon2],popup=name2, tooltip=name2).add_to(m)
    folium.Marker(location=[lat3, lon3],popup=name3, tooltip=name3).add_to(m)
    folium.Marker(location=[lat4, lon4],popup=name4, tooltip=name4).add_to(m)
    folium.Marker(location=[lat5, lon5],popup=name5, tooltip=name5).add_to(m)
    folium_static(m)