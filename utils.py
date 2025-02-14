import streamlit as st
import pandas as pd

def apply_css():
    return st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #f7f3e4;
    }
    [data-testid="stHeader"] {
        background-color: #f7f3e4;
    }       
    [data-testid="stSidebarContent"] {
        background-color:  #fbfaf2; 
    }
    div[data-baseweb="select"] > div {
        background-color:  #fbfaf2; 
    }
    ul[data-testid="stSelectboxVirtualDropdown"] {
        background-color: #fbfaf2;
    }                  
    </style> 
    """.strip(), unsafe_allow_html=True) # alth for sidebar: #ece3c7 
 
def style_plotly(fig, bgcolor="#f7f3e4", gridcolor="gray"):
    fig.update_layout(
        paper_bgcolor=bgcolor,
        plot_bgcolor=bgcolor,
        font_color="black",
    )
    fig.update_xaxes(gridcolor=gridcolor, griddash='dot')
    fig.update_yaxes(gridcolor=gridcolor, griddash='dot')
    return fig

@st.cache_data
def load_data():
    df = pd.read_excel('CSM.xlsm', sheet_name='Master Sheet')
    df = df.dropna(subset=['Title'])
    df['Year'] = df['Start Date'].dt.year   
    return df.fillna('N/A')

def show_df_rows(df, cols=None):
    if cols:
        df = df[cols]

    for i, row in df.iterrows():
        with st.expander(f"{row['Title']}"):
            row = row.fillna('N/A')
            st.write(f"**Start Date**: {row['Start Date'].strftime('%B %d, %Y')}")
            st.write(f"**Form of Restriction**: {row['Form of Restriction']}")
            st.write(f"**Legal Basis**: {row['Legal Basis']}")
            st.write(f"**Targeted Individuals**: {row['Targeted Individuals']}")
            st.write(f"**Targeted Entities**: {row['Targeted Entities']}")
            st.write(f"**Nationality of Targets**: {row['Nationality of Targets']}")
            st.write(f"**Sector**: {row['Sector']}")
            st.write(f"**Targeted Product Categories**: {row['Targeted Product Categories']}")
