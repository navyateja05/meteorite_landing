import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
meteor_df = pd.read_csv('Meteorite_Landings.csv')
alt.data_transformers.disable_max_rows()
url = "https://raw.githubusercontent.com/deldersveld/topojson/master/world-continents.json"
source = alt.topo_feature(url, "continent")

country = alt.Chart(source).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project(
    "equirectangular"
).properties(
    width=800,
    height=500
)

points = alt.Chart(meteor_df).mark_circle().encode(
    longitude='reclong:Q',
    latitude='reclat:Q',
    size=alt.value(10),
    tooltip='name',
    color=alt.value('slateblue')
)
country + points