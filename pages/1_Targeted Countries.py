import streamlit as st
import pandas as pd 
import plotly.express as px
import utils

st.title('Targeted Countries')  

df = utils.load_data()
utils.apply_css()

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
    percentages = hierarchy.groupby('Continent')['Count'].apply(lambda x: x / x.sum())
    percentages = percentages.iloc[percentages.index.sortlevel(1)[1]].reset_index(drop=True)
    hierarchy['Percentage'] = percentages*100
    return df_national, hierarchy.rename(columns={'Count': 'Number of Sanctions'})

st.write("These graphs show China’s sanctions broken down by the nationality of their targets. ")

form_of_restriction = st.multiselect('Form of Restriction', df['Form of Restriction'].unique())
sector = st.multiselect('Sector', [e.strip() for e in df['Sector'].str.split(';').explode().unique()])
year = st.multiselect('Year', df['Year'].unique())

def is_parent(path):
    return len(path.split('/')) == 1 

hover_template_parent = """
<b>Name:</b> %{label}<br>
<b>Number of Sanctions:</b> %{value:.2f}<br>
<extra></extra>
"""

hover_template_child = """
<b>Name:</b> %{label}<br>
<b>Number of Sanctions:</b> %{value:.2f}<br>
<b>Percent of Contintent's Sanctions:</b> %{customdata[0]:.3}%<br>
<extra></extra>
"""

def custom_hover(trace):
    hovers = []
    for path in trace.ids:
        if is_parent(path):
            hovers.append(hover_template_parent)
        else:
            hovers.append(hover_template_child)
    return hovers

org, hierarchy = prep_data(df, form_of_restriction, sector, year)
treemap = px.treemap(hierarchy, path=['Continent', 'Country'], values='Number of Sanctions', custom_data=["Percentage"])
treemap.data[0].hovertemplate = custom_hover(treemap.data[0])
treemap = utils.style_plotly(treemap)
st.plotly_chart(treemap)

hover_template = """
<b>Name:</b> %{label}<br>
<b>Number of Sanctions:</b> %{value:.2f}<br>
<b>Percent of Contintent's Sanctions:</b> %{customdata[0]:.3}%<br>
<extra></extra>
"""
fig = px.bar(hierarchy, x='Country', y='Number of Sanctions', color='Continent', custom_data=["Percentage"])
fig = utils.style_plotly(fig)
fig.update_traces(hovertemplate=hover_template)
event = st.plotly_chart(fig, on_select="rerun")

if event is None: 
    st.write("Clicking the bars will open a list of all sanctions in the selection.")
elif not event.get("selection", {}).get("points"): 
    st.write("Clicking the bars will open a list of all sanctions in the selection.")

if event and event.get("selection", {}).get("points"):
    if event["selection"]["points"]:
        country = event['selection']['points'][0]['x']
        st.write(f"Selected country: **{country}**")
        res = org[org['Nationality of Targets'].str.contains(country)]
        if len(year) > 0:
            res = res[res['Year'].isin(year)]
        utils.show_df_rows(res)

st.markdown("""
<small>Some sanctions are directed at multiple targets of different nationalities. These are counted several times in the visualization of these graphs (one time for each nationality), which results in the total number of visualized cases being higher than the actual number of sanctions. However, the percentages shown when hovering over individual countries accurately reflects the target’s share of the total number of sanctions. For example, if the United States shows a percentage value of 70, this means that 70 percent of the total number of sanctions in the selection targeted the United States.</small> 
""".strip(), unsafe_allow_html=True)