import streamlit as st
import plotly.express as px
import utils

st.title('Forms of Restriction') 

df = utils.load_data()

@st.cache_data
def prep_data(df):
    df_for = df.groupby(['Year', 'Form of Restriction']).count()['Title'].reset_index()
    return df_for

df_for = prep_data(df)
fig = px.bar(df_for, x='Year', y='Title', color='Form of Restriction', title='Forms of Restriction Over Time',  labels={'Title': 'Count'})

event = st.plotly_chart(fig, on_select="rerun")
if event:
    if event["selection"]["points"]:
        year = event['selection']['points'][0]['x']
        sanction = event['selection']['points'][0]['legendgroup']
        res = df[(df['Year'] == year) & (df['Form of Restriction'] == sanction)]
        utils.show_df_rows(res) 