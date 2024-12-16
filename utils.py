import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_excel('CSM.xlsm', sheet_name='Master Sheet')
    df = df.dropna(subset=['Title'])
    df['Year'] = df['Start Date'].dt.year   
    return df

def show_df_rows(df, cols=None):
    if cols:
        df = df[cols]

    for i, row in df.iterrows():
        with st.expander(f"Title: {row['Title']}"):
            st.write(f"Start Date: {row['Start Date']}")
            st.write(f"Form of Restriction: {row['Form of Restriction']}")
            st.write(f"Legal Basis: {row['Legal Basis']}")
            if row['Targeted Individuals']:
                st.write(f"Targeted Individuals: {row['Targeted Individuals']}")
            if row['Targeted Entities']:
                st.write(f"Targeted Entities: {row['Targeted Entities']}")
            if row['Nationality of Targets']:
                st.write(f"Nationality of Targets: {row['Nationality of Targets']}")
            st.write(f"Sector: {row['Sector']}")
            st.write(f"Targeted Product Categories: {row['Targeted Product Categories']}")
