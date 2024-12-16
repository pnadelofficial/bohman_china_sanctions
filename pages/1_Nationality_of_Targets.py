import streamlit as st
import pandas as pd 
import plotly.express as px
import utils

st.title('Nationality of Targets')  

df = utils.load_data()

@st.cache_data
def prep_data(df):
    df_national = df[~df['Nationality of Targets'].isnull()]
    hierarchy = pd.DataFrame(df_national['Nationality of Targets'].str.split('; ').explode())
    hierarchy['Continent'] = hierarchy['Nationality of Targets'].str.extract(r'\((.*)\)')[0]
    hierarchy['Country'] = hierarchy['Nationality of Targets'].str.extract(r'(.*) \(')[0]
    
    hierarchy = hierarchy.groupby(['Continent', 'Country']).size().reset_index(name='Count').sort_values(by='Count', ascending=False).reset_index(drop=True)
    hierarchy['Percentage'] = round(hierarchy['Count'] / hierarchy['Count'].sum(), 3) * 100
    return hierarchy

hierarchy = prep_data(df)
fig1 = px.sunburst(hierarchy, path=[px.Constant("China's Sanctions"), 'Continent', 'Country'], values='Count', hover_data=['Percentage'])
event1 = st.plotly_chart(fig1, on_select="rerun")

fig2 = px.treemap(hierarchy, path=[px.Constant("China's Sanctions"), 'Continent', 'Country'], values='Count', hover_data=['Percentage'])
fig2.data[0].texttemplate = "<br><br><em style='font-size:30px'>%{label}</em><br>Number of sanctions: %{value}<br>Percent of all sanctions: %{customdata[0]}"
event2 = st.plotly_chart(fig2, on_select="rerun")
