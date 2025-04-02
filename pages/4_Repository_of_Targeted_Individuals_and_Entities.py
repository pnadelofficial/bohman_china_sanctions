import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import utils

st.title('Repository of Targeted Individuals and Entities') 

df = utils.load_data()
utils.apply_css()

@st.cache_data
def prep_data(df):
    def split_col_on_semicolon(df, col):
        df_split = df[~df[col].isnull()]
        df_split[col] = df_split[col].str.split('; ')
        df_split = df_split.explode(col)
        return df_split
    
    def groupby_on_year_cumsum(df, label):
        df_grouped = df.groupby(['Year']).count().reset_index()
        df_grouped['Title'] = df_grouped['Title'].cumsum()  
        df_grouped['label'] = label
        return df_grouped[['Year', 'Title', 'label']]

    df_ind = split_col_on_semicolon(df, 'Targeted Individuals')
    df_ent = split_col_on_semicolon(df, 'Targeted Entities')

    df_ind_grouped = groupby_on_year_cumsum(df_ind, 'Targeted Individuals')
    df_ent_grouped = groupby_on_year_cumsum(df_ent, 'Targeted Entities')

    df_combined = pd.concat([df_ind_grouped, df_ent_grouped])

    return df_combined, df_ind, df_ent

st.write("This graph shows the cumulative number of individuals and entities targeted by PRC sanctions. Note that some individuals and entities have been sanctioned more than once, and each instance is counted separately in the graph. Therefore, the number of unique targets is slightly lower than the total shown. ")

df_combined, df_ind, df_ent = prep_data(df)  
unique_inds = df_ind['Targeted Individuals'].unique().tolist() 
unique_ents = df_ent['Targeted Entities'].unique().tolist()

color_map = {
    'Targeted Individuals': '#0169CA',
    'Targeted Entities': '#FF2A2B'
}

hovertemplate_individuals = """
<b>Year:</b> %{x}<br>
<b>Number of Targeted Individuals:</b> %{y}<br>
<extra></extra>
""".strip()

hovertemplate_entities = """
<b>Year:</b> %{x}<br>
<b>Number of Targeted Entities:</b> %{y}<br>
<extra></extra>
""".strip()

min_year = df['Year'].min()
max_year = df['Year'].max()
fig = go.Figure() 
fig.add_trace(go.Scatter(
    x=df_combined[df_combined['label'] == 'Targeted Entities']['Year'], y=df_combined[df_combined['label'] == 'Targeted Entities']['Title'],
    fill="tozeroy", fillcolor=color_map['Targeted Entities'], name='Targeted Entities', mode='lines+markers', line=dict(color=color_map['Targeted Entities']),
    hovertemplate=hovertemplate_entities
))
fig.add_trace(go.Scatter(
    x=df_combined[df_combined['label'] == 'Targeted Individuals']['Year'], y=df_combined[df_combined['label'] == 'Targeted Individuals']['Title'],
    fill="tozeroy", fillcolor=color_map['Targeted Individuals'], name='Targeted Individuals', mode='lines+markers', line=dict(color=color_map['Targeted Individuals']),
    hovertemplate=hovertemplate_individuals
))

fig.update_xaxes(
    tickmode='array',
    tickvals=list(range(min_year, max_year + 1)), 
    ticktext=[str(year) for year in range(min_year, max_year + 1)]
)

fig = utils.style_plotly(fig)
event = st.plotly_chart(fig, on_select="rerun")

st.write("""
*Use these fields to search for individuals and entities targeted by China’s sanctions, and to identify the specific restrictions imposed on them.*

Please note that this is not a list of ‘active’ sanctions, but a repository of individuals and entities that have at some point in time been targeted by PRC sanctions. In some cases, restrictions against the target may no longer be in force.
""".strip())

ind = st.selectbox('Search Targeted Individuals', unique_inds, index=None, placeholder="Type name here")
if ind:
    ind_res = df_ind[(df_ind['Targeted Individuals'].str.contains(ind))]
    utils.show_df_rows(ind_res)

ent = st.selectbox('Search Targeted Entities', unique_ents, index=None, placeholder="Type name here")
if ent:
    ent_res = df_ent[(df_ent['Targeted Entities'].str.contains(ent))]
    utils.show_df_rows(ent_res)

st.markdown("<footer><small>Assembed by Peter Nadel | Tufts University | Tufts Technology Services | Reserch Technology </small></footer>", unsafe_allow_html=True)