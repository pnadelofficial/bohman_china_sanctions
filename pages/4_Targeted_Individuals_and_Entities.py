import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import utils

st.title('Targeted Individuals and Entities') 

df = utils.load_data()

## shading underneath the lines
#### like in sketch 
#### hover for number of individuals/entities
## might need to do two graphs

## more of "search" feel for the individuals/entities

# ask kevin about url 

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

    df_combined = pd.concat([df_ind_grouped, df_ent_grouped])# df_ind_grouped.merge(df_ent_grouped, on='Year', how='outer')

    return df_combined, df_ind, df_ent# [['Year', 'Title_x', 'Title_y']].rename(columns={'Title_x': 'Targeted Individuals', 'Title_y': 'Targeted Entities'})

df_combined, df_ind, df_ent = prep_data(df)  
unique_inds = df_ind['Targeted Individuals'].unique().tolist() 
unique_ents = df_ent['Targeted Entities'].unique().tolist()

fig_scatter = px.scatter(df_combined, x='Year', y='Title', color='label', title='Targeted Individuals Over Time', labels={'Title': 'Count'})
fig_line = px.line(df_combined, x='Year', y='Title', color='label', title='Targeted Individuals Over Time', labels={'Title': 'Count'})
fig_line.update_traces(showlegend=False)

min_year = df['Year'].min()
max_year = df['Year'].max()
fig = go.Figure(data=fig_scatter.data + fig_line.data)
fig.update_xaxes(
    tickmode='array',
    tickvals=list(range(min_year, max_year + 1)), 
    ticktext=[str(year) for year in range(min_year, max_year + 1)]
)

event = st.plotly_chart(fig, on_select="rerun")

st.write("### Search")

ind = st.selectbox('Select Individual', unique_inds)
ind_res = df_ind[(df_ind['Targeted Individuals'].str.contains(ind))]
utils.show_df_rows(ind_res)

ent = st.selectbox('Select Entity', unique_ents)
ent_res = df_ent[(df_ent['Targeted Entities'].str.contains(ent))]
utils.show_df_rows(ent_res)
# if event:
#     if event["selection"]["points"]:
#         year = event['selection']['points'][0]['x']
#         kind = event['selection']['points'][0]['legendgroup']
#         if 'Individuals' in kind:
#             col_to_search = 'Targeted Individuals'
#         else:
#             col_to_search = 'Targeted Entities'
#         res = df[(df['Year'] == year) & (~df[col_to_search].isnull())]
#         utils.show_df_rows(res)