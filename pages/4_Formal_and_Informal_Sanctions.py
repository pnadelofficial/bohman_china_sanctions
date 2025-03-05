import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import utils

st.title('Formal and Informal Sanctions') 

df = utils.load_data()
utils.apply_css()

## no clickability on this one
## maybe color of chart

@st.cache_data
def prep_data(df):
    # df['Formality'] = df['Formality'].apply(lambda x: 'Informal' if x == 0 else 'Formal')
    df_formality = df.groupby(['Year', 'Formality']).count()['Title'].reset_index()
    # df_formality['Title'] = df_formality.groupby('Formality')['Title'].count() # .cumsum()
    return df_formality

df_formality = prep_data(df)

st.write("""
This graph shows China’s sanctions broken down by formality.

**Formal sanctions** are state-imposed measures that restrict economic exchange in pursuit of foreign policy objectives and the Chinese government publicly acknowledges as such. They are usually imposed under PRC sanctions laws such as the Anti-Foreign Sanction Law or the Unreliable Entity List. 

**Informal sanctions** are statex-supported measures that restrict economic exchange in pursuit of foreign policy objectives but are not officially recognized as sanctions by the PRC government. In some cases, the government acknowledges having taken action but justifies the restrictions on other grounds (e.g., citing an import ban as necessary for phytosanitary protection). In other cases, the government does not acknowledge being involved at all, attributing the restrictions to independent actions by commercial actors (e.g., patriotic consumers initiating a boycott).""".strip())

hover_template = """
<b>Form of Restriction:</b> %{customdata[0]}<br>
<b>Number of Sanctions:</b> %{customdata[2]}<br>
<b>Year:</b> %{customdata[1]}<br>
<extra></extra>
"""

color_map = {
    'Formal': "#0e4e88",
    'Informal': "#d83f03"
}

fig_scatter = px.scatter(df_formality, x='Year', y='Title', color='Formality', title='Formality Over Time', labels={'Title': 'Number of Sanctions'}, custom_data=["Formality", "Year", "Title"], color_discrete_map=color_map)
fig_scatter.update_traces(hovertemplate=hover_template)

fig_line = px.line(df_formality, x='Year', y='Title', color='Formality', title='Formality Over Time', labels={'Title': 'Number of Sanctions'}, custom_data=["Formality"], color_discrete_map=color_map)
fig_line.update_traces(showlegend=False)

min_year = df['Year'].min()
max_year = df['Year'].max()
fig = go.Figure(data=fig_scatter.data + fig_line.data)
fig.update_xaxes(
    tickmode='array',
    tickvals=list(range(min_year, max_year + 1)), 
    ticktext=[str(year) for year in range(min_year, max_year + 1)]
)
fig = utils.style_plotly(fig)
event = st.plotly_chart(fig, on_select="rerun")
# if event:
#     if event["selection"]["points"]:
#         year = event['selection']['points'][0]['x']
#         formality = event['selection']['points'][0]['legendgroup']
#         # if formality == 'Formal':
#         #     formality = 1
#         # else:
#         #     formality = 0
#         res = df[(df['Year'] == year) & (df['Formality'] == formality)]
#         utils.show_df_rows(res)