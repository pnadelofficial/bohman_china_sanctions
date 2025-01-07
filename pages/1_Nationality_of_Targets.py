import streamlit as st
import pandas as pd 
import plotly.express as px
import utils

st.title('Nationality of Targets')  

df = utils.load_data()

## precentage notes from email - will be important
#### should be by the ones in the filter
#### Possible to have denominator to be total number of sanctions NOT total number of targets
#### Could just fix the number ahead of time

## might go back to sunburst and just ignore clickability IN ADDITION to the bar chart

@st.cache_data
def prep_data(df, form_of_restriction=[], sector=[], year=[]):
    df_national = df[~df['Nationality of Targets'].isnull()]

    if len(form_of_restriction) > 0:
        df_national = df_national[df_national['Form of Restriction'].isin(form_of_restriction)]

    if len(sector) > 0:
        df_national = df_national[df_national['Sector'].apply(lambda x: any(s in [item.strip() for item in x.split(';')] for s in sector))]
    
    if len(year) > 0:
        df_national = df_national[df_national['Year'].isin(year)]

    hierarchy = pd.DataFrame(df_national['Nationality of Targets'].str.split('; ').explode())
    hierarchy['Continent'] = hierarchy['Nationality of Targets'].str.extract(r'\((.*)\)')[0]
    hierarchy['Country'] = hierarchy['Nationality of Targets'].str.extract(r'(.*) \(')[0]
    
    hierarchy = hierarchy.groupby(['Continent', 'Country']).size().reset_index(name='Count').sort_values(by='Count', ascending=False).reset_index(drop=True)
    # hierarchy['Percentage'] = round(hierarchy['Count'] / hierarchy['Count'].sum(), 3) * 100
    return df_national, hierarchy

form_of_restriction = st.multiselect('Form of Restriction', df['Form of Restriction'].unique())
sector = st.multiselect('Sector', [e.strip() for e in df['Sector'].str.split(';').explode().unique()])
year = st.multiselect('Year', df['Year'].unique())

org, hierarchy = prep_data(df, form_of_restriction, sector, year)
sunburst = px.sunburst(hierarchy, path=['Continent', 'Country'], values='Count')
st.plotly_chart(sunburst)

fig = px.bar(hierarchy, x='Country', y='Count', color='Continent')
event = st.plotly_chart(fig, on_select="rerun")

if event:
    if event["selection"]["points"]:
        country = event['selection']['points'][0]['x']
        st.write(country)
        res = org[org['Nationality of Targets'].str.contains(country)]
        if len(year) > 0:
            res = res[res['Year'].isin(year)]
        utils.show_df_rows(res)