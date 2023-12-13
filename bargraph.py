import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

pd.read_csv('Meteorite_Landings.csv')
meteor_df = pd.read_csv("Meteorite_Landings.csv", usecols = ['mass (g)','name'])

#use pd.cut to separate data into groups using mass
meteor_df['bin'] = pd.cut(meteor_df['mass (g)'], bins=[0, 1, 5, 10, 50, 100, 500, 1000, 10000, 100000, 1000000, 1000000000])

#group the pieces together by count
meteor_df2 = meteor_df.groupby(['bin'])['bin'].count().reset_index(name="count")

# pretty colors
my_colors = [(x/10.0, x/20.0, 0.75) for x in range(len(meteor_df))]

#print horizontal bar chart (using colors above)
#df2.plot.barh(x='bin', 
 #             y='count', 
  #            stacked=True, 
   #           color=my_colors, 
    #          title='Meteorite Landings by Mass (g)', 
     #         xlabel='Number of landings recorded by NASA',
      #        ylabel='Mass of Meteorite',
       #       figsize=(12, 4))
chart = alt.Chart(meteor_df2).mark_bar().encode(
 y = 'bin',
 x= 'count'
)
st.altair_chart(chart, use_container_width = True)