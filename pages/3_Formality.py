import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import utils

st.title('Formality') 

df = utils.load_data()

## no clickability on this one
## maybe color of chart

@st.cache_data
def prep_data(df):
    # df['Formality'] = df['Formality'].apply(lambda x: 'Informal' if x == 0 else 'Formal')
    df_formality = df.groupby(['Year', 'Formality']).count()['Title'].reset_index()
    # df_formality['Title'] = df_formality.groupby('Formality')['Title'].count() # .cumsum()
    return df_formality

df_formality = prep_data(df)
fig_scatter = px.scatter(df_formality, x='Year', y='Title', color='Formality', title='Formality Over Time', labels={'Title': 'Count'})
fig_line = px.line(df_formality, x='Year', y='Title', color='Formality', title='Formality Over Time', labels={'Title': 'Count'})
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