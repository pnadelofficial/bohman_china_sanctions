import streamlit as st
import plotly.express as px
import utils

st.title('Forms of Restriction') 
st.write("This graph shows China’s sanctions broken down by form of restriction and year. Clicking the bars will open a list of all sanctions in the selection.")

df = utils.load_data()
utils.apply_css()

@st.cache_data
def prep_data(df):
    df_for = df.groupby(['Year', 'Form of Restriction']).count()['Title'].reset_index()
    return df_for

hover_template = """
<b>Number of Sanctions:</b> %{value}<br>
<b>Year:</b> %{label}<br>
<extra></extra>
"""

df_for = prep_data(df)

color_map = {
    'Targeted Sanction': "#84C9FF",
    "Export Control": "#0169CA",
    "Import Control": "#FF2A2B",
    "Obstruction of Foreign Business in China": "#FF6E67",
    "Boycott": "#BC4EBA",
    "Outbound Tourism Restriction": "#D289D1"
}

fig = px.bar(df_for, x='Year', y='Title', title='Forms of Restriction Over Time',  labels={'Title': 'Number of Sanctions'}, color='Form of Restriction', custom_data=["Form of Restriction"], color_discrete_map=color_map, category_orders={'Form of Restriction': ["Export Control", 'Targeted Sanction', "Import Control", "Obstruction of Foreign Business in China", "Boycott", "Outbound Tourism Restriction"]})
fig.update_traces(hovertemplate=hover_template)
fig = utils.style_plotly(fig)
event = st.plotly_chart(fig, on_select="rerun")
if event is None: 
    st.write("*Clicking the bars will open a list of all sanctions in the selection.*")
elif not event.get("selection", {}).get("points"): 
    st.write("*Clicking the bars will open a list of all sanctions in the selection.*")

if event and event.get("selection", {}).get("points"):
    if event["selection"]["points"]:
        year = event['selection']['points'][0]['x']
        sanction = event['selection']['points'][0]['legendgroup']
        res = df[(df['Year'] == year) & (df['Form of Restriction'] == sanction)]
        utils.show_df_rows(res) 

st.markdown("<footer><small>Assembed by Peter Nadel | Tufts University | Tufts Technology Services | Reserch Technology </small></footer>", unsafe_allow_html=True)