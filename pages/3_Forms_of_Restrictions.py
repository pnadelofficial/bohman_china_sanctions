import streamlit as st
import plotly.express as px
import utils

st.title('Forms of Restriction') 
st.write("This graph shows China’s sanctions broken down by form of restriction and year. Clicking the bars will open a list of all sanctions in the selection.")

df = utils.load_data()
utils.apply_css()

# perhaps a sunburst of restriction/sector by continent

@st.cache_data
def prep_data(df):
    df_for = df.groupby(['Year', 'Form of Restriction']).count()['Title'].reset_index()
    return df_for

hover_template = """
<b>Number of Sanctions:</b> %{value}<br>
<b>Year:</b> %{label}<br>
<extra></extra>
"""
# <b>Form of Restriction:</b> %{customdata[0]}<br>

df_for = prep_data(df)

color_map = {
    'Targeted Sanction': "#5D92D2",
    "Export Control": "#0169CA",
    "Import Control": "#FF2A2B",
    "Obstruction of Foreign Business in China": "#FF6E67",
    "Boycott": "#84C9FF",
    "Outbound Tourism Restriction": "#A8D5F7"
}

fig = px.bar(df_for, x='Year', y='Title', title='Forms of Restriction Over Time',  labels={'Title': 'Number of Sanctions'}, color='Form of Restriction', custom_data=["Form of Restriction"], color_discrete_map=color_map)
fig.update_traces(hovertemplate=hover_template)
fig = utils.style_plotly(fig)
event = st.plotly_chart(fig, on_select="rerun")
if event:
    if event["selection"]["points"]:
        year = event['selection']['points'][0]['x']
        # sanction = event['selection']['points'][0]['legendgroup']
        res = df[(df['Year'] == year)] # & (df['Form of Restriction'] == sanction)]
        utils.show_df_rows(res) 