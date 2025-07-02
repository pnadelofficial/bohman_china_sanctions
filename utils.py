import streamlit as st
import pandas as pd
from streamlit_theme import st_theme
import urllib.request
import os

MODE = st_theme()['base']
if "mode" not in st.session_state:
    st.session_state.mode = MODE
if st.session_state.mode != MODE:
    st.session_state.mode = MODE

FILENAME = "PRC Sanctions Data.xlsm"

@st.cache_resource
def download_data():
    if FILENAME not in os.listdir("."):
        dl_url = "https://tufts.box.com/shared/static/62w43uiqflnr74yejuiqnbzsrukif3x8.xlsm"
        urllib.request.urlretrieve(dl_url, FILENAME)

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
        [data-testid="stHeadingWithActionElements "] {
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
        p, div, span, label, .stMarkdown, .stText, h3, h2, h1 {
            color: #333333 !important;
        }
        /* Fix specific Streamlit components if needed */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            color: #333333 !important;
        }
        [data-testid="stExpander"] {
            border: 1px solid #555555 !important;
            background-color: #f7f3e4 !important;
            border-radius: 0.5rem !important;
            overflow: hidden !important;
        }
        .streamlit-expanderHeader {
            color: #333333 !important;
            background-color: #f7f3e4 !important;
            border-radius: 0.5rem !important;
        }
        [data-testid="stExpanderDetails"] {
            background-color: #fbfaf2 !important;
            color: #333333 !important;
            border-top: 1px solid #555555 !important;
        }
        [data-testid="stExpander"] svg {
            fill: #333333 !important;
        }
        [data-testid="stExpander"] [aria-expanded="false"] {
            border-radius: 0.5rem !important;
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

    is_dark_mode = MODE == "dark"
    if is_dark_mode:
        fig.update_layout(title_font_color="black")
        fig.update_xaxes(title_font_color="black")
        fig.update_yaxes(title_font_color="black")
        fig.update_layout(legend_font_color="black")
        fig.update_layout(legend_title_font_color="black")
        fig.update_xaxes(tickfont_color="black")
        fig.update_yaxes(tickfont_color="black")
    return fig

@st.cache_data
def load_data():
    print(os.listdir("."))
    print(os.getcwd())
    df = pd.read_excel(FILENAME, sheet_name='Master Sheet')
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
            st.write("\n")
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

