import streamlit as st
import plotly.express as px
import utils

st.title('Formal and Informal Sanctions') 

utils.download_data()

df = utils.load_data()
utils.apply_css()

@st.cache_data
def prep_data(df):
    df_formality = df.groupby(['Year', 'Formality']).count()['Title'].reset_index()
    return df_formality

df_formality = prep_data(df)

st.write("""
This graph shows China’s sanctions broken down by formality.

**Formal sanctions** are restrictions on economic exchange imposed by the state and which the PRC government acknowledges are motivated by political or security objectives. Formal sanctions are imposed under official laws, such as the Anti-Foreign Sanction Law, the Unreliable Entity List or the Export Control Law.

**Informal sanctions** are restrictions on economic exchange which are initiated or encouraged by the state but which are not officially acknowledged to be motivated by political or security objectives. In some cases, the government acknowledges having taken action but justifies the restrictions on other grounds (e.g., citing food safety regulations when imposing an import ban). In other cases, the government does not acknowledge being involved at all, attributing the restrictions to independent actions by commercial actors (e.g., patriotic consumers initiating a boycott).""".strip())

hover_template = """
<b>Form of Restriction:</b> %{customdata[0]}<br>
<b>Number of Sanctions:</b> %{customdata[2]}<br>
<b>Year:</b> %{customdata[1]}<br>
<extra></extra>
"""

color_map = {
    'Informal': "#FF2A2B",
    'Formal': "#0169CA"
}

fig = px.bar(df_formality, x='Year', y='Title', title='Formality Over Time',  labels={'Title': 'Number of Sanctions'}, color='Formality', custom_data=["Formality", "Year", "Title"], color_discrete_map=color_map)
fig.update_traces(hovertemplate=hover_template)

fig = utils.style_plotly(fig)
event = st.plotly_chart(fig, on_select="rerun")
if event is None: 
    st.write("*Click the bars to open a list of all sanctions in the selection.*")
elif not event.get("selection", {}).get("points"): 
    st.write("*Click the bars to open a list of all sanctions in the selection.*")

if event and event.get("selection", {}).get("points"):
    if event["selection"]["points"]:
        year = event['selection']['points'][0]['x']
        formality = event['selection']['points'][0]['legendgroup']
        res = df[(df['Year'] == year) & (df['Formality'] == formality)]
        utils.show_df_rows(res)

st.markdown("<footer><small>Assembed by Peter Nadel | Tufts University | Tufts Technology Services | Research Technology </small></footer>", unsafe_allow_html=True)