import streamlit as st
import pandas as pd

def apply_css():
    return st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #f7f3e4;
            color: #333333 !important; /* Force dark text */
        }
        [data-testid="stHeader"] {
            background-color: #f7f3e4;
            color: #333333 !important;
        }       
        [data-testid="stSidebarContent"] {
            background-color: #fbfaf2;
            color: #333333 !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #fbfaf2;
            color: #333333 !important;
        }
        /* Fix dropdowns */
        ul[data-testid="stSelectboxVirtualDropdown"] {
            background-color: #fbfaf2;
            color: #333333 !important;
        }
        /* Ensure all text elements use dark text */
        p, div, span, label, .stMarkdown, .stText {
            color: #333333 !important;
        }
        /* Fix specific Streamlit components if needed */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            color: #333333 !important;
        }
        </style>
    """.strip(), unsafe_allow_html=True) # alt for sidebar: #ece3c7 
 
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
    df = pd.read_excel('PRC Sanctions Data.xlsm', sheet_name='Master Sheet')
    df = df.dropna(subset=['Title'])
    df['Year'] = df['Imposition Date'].dt.year   
    return df.fillna('N/A')

def show_df_rows(df, cols=None):
    if cols:
        df = df[cols]

    for i, row in df.iterrows():
        esc_title = row['Title'].replace('$', r'\$')
        with st.expander(f"{esc_title}"):
            row = row.fillna('N/A')
            st.write(f"**Imposition Date**: {row['Imposition Date'].strftime('%B, %Y')}")
            # st.write(f"**Counter vs. Primary**: {row['Counter vs. Primary']}")
            # st.write(f"**Issue Area of Perceived Provocation**: {row['Issue Area of Perceived Provocation']}")
            # st.write(f"**Restriction Specifications**: {row['Restriction Specifications']}")
            # st.write(f"**Mechanism**: {row['Mechanism']}")
            # st.write(f"**Formality**: {row['Formality']}")
            st.write(f"**Form of Restriction**: {row['Form of Restriction']}")
            st.write(f"**Targeted Individuals**: {row['Targeted Individuals']}")
            st.write(f"**Targeted Entities**: {row['Targeted Entities']}")
            st.write(f"**Nationality of Targets**: {row['Nationality of Targets']}")
            st.write(f"**Sector**: {row['Sector']}")
            st.write(f"**Targeted Product Categories**: {row['Targeted Product Categories']}")

