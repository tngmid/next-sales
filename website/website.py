import streamlit as st
import pandas as pd

with st.sidebar:
    st.write("Welcome!")

st.title("NEXT Group Sales Analysis")

st.write("Welcome to the NEXT Group Sales Analysis page. Navigate to the left to pick areas of NEXT's sales you wish to view the yearly trend. The GitHub repository can be found at 'https://github.com/tngmid/next-sales'")
    
df = pd.read_csv("../data/group_sales.csv")
df["Year"] = ["2026", "2025", "2024", "2023", "2022"]
df["Year"] = pd.to_datetime(df["Year"], format="%Y")

area_list = ["Retail Stores", "Online", "NEXT Finance", "Total Platform", "Other business activities", "NEXT's share of sales from investments", "Total Group sales"]

cbAll = st.sidebar.checkbox("Select All")
if cbAll:
    selected_layers = [type for type in area_list if st.sidebar.checkbox(type, value=cbAll, disabled=True)]
else: selected_layers = [type for type in area_list if st.sidebar.checkbox(type)]
    
if selected_layers != []:
    new_df = {"Year": ["2026", "2025", "2024", "2023", "2022"]}
    
    for layer in selected_layers:
        new_df[layer] = df[layer]
        new_df["Year"] = pd.to_datetime(new_df["Year"], format="%Y")
        
    st.line_chart(new_df, x="Year", y_label="Sales (£m)")
else:
    st.write("Please add more arguments on the left.")
