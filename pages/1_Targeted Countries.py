import streamlit as st
import pandas as pd 
import plotly.express as px
import utils

st.title('Targeted Countries')  

utils.download_data()

df = utils.load_data()
utils.apply_css()

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
    hierarchy['Percentage'] = (hierarchy.Count / hierarchy.Count.sum()) * 100
    return df_national, hierarchy.rename(columns={'Count': 'Number of Sanctions'})

st.write("These graphs show China’s sanctions broken down by the nationality of their targets.")

form_of_restriction = st.multiselect('Form of Restriction', df['Form of Restriction'].unique())
sector = st.multiselect('Sector', list(set([e.strip() for e in df['Sector'].str.split(';').explode().unique()])))
year = st.multiselect('Year', df['Year'].unique())

def is_parent(path):
    return len(path.split('/')) == 1 

hover_template_parent = """
<b>Name:</b> %{label}<br>
<b>Number of Sanctions:</b> %{value}<br>
<extra></extra>
"""

hover_template_child = """
<b>Name:</b> %{label}<br>
<b>Number of Sanctions:</b> %{value:}<br>
<b>Percent of Total Number of Sanctions:</b> %{customdata[0]:.3}%<br>
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

sunburst = px.sunburst(hierarchy, path=['Continent', 'Country'], values='Number of Sanctions', custom_data=["Percentage"], title="Targeted Countries by Continent",)
sunburst.data[0].hovertemplate = custom_hover(sunburst.data[0])
sunburst = utils.style_plotly(sunburst)
st.plotly_chart(sunburst)

hover_template = """
<b>Name:</b> %{label}<br>
<b>Number of Sanctions:</b> %{value}<br>
<b>Percent of Total Number of Sanctions:</b> %{customdata[0]:.3}%<br>
<extra></extra>
"""

fig = px.bar(hierarchy, x='Country', y='Number of Sanctions', custom_data=["Percentage"], title="Targeted Countries by Number of Sanctions",)

fig = utils.style_plotly(fig)
fig.update_traces(hovertemplate=hover_template)
event = st.plotly_chart(fig, on_select="rerun")

if event is None: 
    st.write("*Click the bars to open a list of all sanctions in the selection.*")
elif not event.get("selection", {}).get("points"): 
    st.write("*Click the bars to open a list of all sanctions in the selection.*")

if event and event.get("selection", {}).get("points"):
    if event["selection"]["points"]:
        country = event['selection']['points'][0]['x']
        st.write(f"Selected country: **{country}**")
        res = org[org['Nationality of Targets'].str.contains(country)]
        if len(year) > 0:
            res = res[res['Year'].isin(year)]
        utils.show_df_rows(res)

st.markdown("""
<small><b>Note</b>: Some sanctions target individuals or entities from multiple countries. In these graphs, each targeted nationality is counted separately, meaning that if a sanction includes targets from three different countries, it is counted three times. As such, the total number of entries in the graph is higher than the number of distinct sanctions. However, the percentage shown when hovering over a country accurately reflects that country’s share of all sanctions. For example, if the United States displays a value of 50 percent, it means that half of the sanctions in the selected dataset included at least one U.S. individual or entity.</small> 
""".strip(), unsafe_allow_html=True)

st.markdown("<footer><small>Assembed by Peter Nadel | Tufts University | Tufts Technology Services | Research Technology </small></footer>", unsafe_allow_html=True)