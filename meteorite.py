import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from streamlit_lottie import st_lottie
import requests


meteor_df = pd.read_csv('Meteorite_Landings.csv', parse_dates=['year'])

recclasses = list(meteor_df['recclass'].unique())


@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.title("Exploring Meteorite Mass and Year by Recclass and Fall Type")



lottie_hello = load_lottieurl("https://lottie.host/2314d9b4-f9d3-4b90-bc4c-dc91961373f4/XT3H1PyKLY.json")
# Display the Lottie animation
st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",
    height = 300,
    width=300,key=None,)

st.markdown("Users can explore the complex links between meteorite mass, year of occurrence, recclass, and fall type through well designed graphics. A wide range of tools are available on the streamlit app, such as dynamic mass range selector, year range slider for temporal research, and multi-select widgets for recclass and fall type. The app, which is separated into three tabs, tells a compelling story. It begins with a line graph that shows the relationship between meteorite mass and year, moves to a bar graph that classifies meteorite masses, and ends with an eye-catching world map that shows the locations of meteorite landings throughout the world. This multipurpose instrument not only enables users to identify trends in meteorite data but also prompts them to consider the spatial details of astronomical contacts on Earth.")


recclass_select = st.sidebar.multiselect("Select 'Recclass(es):'", recclasses, default=['L6'])
fall_or_found = st.sidebar.multiselect("Select 'Fell' or 'Found':", ['', 'Fell', 'Found'])
year_slider = st.sidebar.slider("Select range of 'Years':", 1880, 2013, (1880, 2013), step=1)
mass_range = alt.selection_interval(encodings=['y'])



tab1, tab2, tab3 = st.tabs(['Mass Vs Year','Mass vs Count','Location'])

with tab1:
    
        filtered_df = meteor_df[meteor_df['recclass'].isin(recclass_select)]
        if fall_or_found:
            filtered_df = filtered_df[filtered_df['fall'].isin(fall_or_found)]

        chart = alt.Chart(filtered_df).mark_line().encode(
            x=alt.X('year', axis=alt.Axis(title='Year')),
            y=alt.Y('mass (g)', scale=alt.Scale(domain=mass_range), axis=alt.Axis(title='Mass')),
            color=alt.Color('recclass', title='Recclass'),
            opacity=alt.condition(mass_range, alt.value(1), alt.value(0.2)),
            tooltip=[
                alt.Tooltip('name', title='Name'),
                alt.Tooltip('year', title='Year'),
                alt.Tooltip('mass (g)', title='Mass'),
                alt.Tooltip('recclass', title='Recclass'),
                alt.Tooltip('GeoLocation', title='GeoLocation')
            ]
        ).add_selection(
            mass_range
        ).properties(
            title=f"Mass vs Year for {', '.join(recclass_select)} ({', '.join(fall_or_found) if fall_or_found else 'All meteors'})"
        ).transform_filter(
            alt.FieldRangePredicate(field='year', range=year_slider)
        )

        st.altair_chart(chart, use_container_width=True)


with tab2:

    meteor_df['bin'] = pd.cut(meteor_df['mass (g)'], bins=[0, 1, 10, 100, 1000, 10000, 100000, 1000000, 1000000000])

    # Group the pieces together by count
    meteor_df2 = meteor_df.groupby(['bin'])['bin'].count().reset_index(name="count")

    # Pretty colors
    my_colors = [(x/10.0, x/20.0, 0.75) for x in range(len(meteor_df2))]

    st.title("Masses of Meteorites")
    st.write("This is a bar graph grouping together the mass of all meteorites that have fallen, and sorting by ranges of minimum to 10x minimum capping out at 1 million.")
    st.write("This graph is important because it gives us a rough size of the meteorites that have fallen, and allows us to view if people should be worried about the size.")
    chart = alt.Chart(meteor_df2).mark_bar().encode(
        y=alt.Y('bin:O', title='Mass Range'),  # Explicitly specifying the type as ordinal (O)
        x=alt.X('count:Q', title='Count'),  # Explicitly specifying the type as quantitative (Q)
        color=alt.Color('count:Q', scale=alt.Scale(range=my_colors), title='Count')  # Explicitly specifying the type as quantitative (Q)
    )
    st.altair_chart(chart, use_container_width=True)

with tab3:
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

    st.title("Locations of Meteorites")
    st.write("This is a map of all locations of meteorites and where they fell based off of the longitude and latitude of fall location. ")
    st.write("This map answers the question of where meteorites are more likely and less likely to fall, showing where areas might need more meteorite protection.")
    points = alt.Chart(meteor_df).mark_circle().encode(
        longitude='reclong:Q',
        latitude='reclat:Q',
        size=alt.value(10),
        tooltip='name',
        color=alt.value('slateblue')
    )
    country + points