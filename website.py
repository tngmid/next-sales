import streamlit as st
import altair as alt
import pandas as pd

with st.sidebar:
    st.write("Welcome!")

st.title("NEXT Group Sales Analysis")

df = pd.read_csv("group_sales.csv")
df["Year"] = ["2026", "2025", "2025", "2024"]
df["Year"] = pd.to_datetime(df["Year"], format="%Y")

area_list = ["Retail Stores", "Online (UK)", "Online (International)", "NEXT Finance", "Other business activities", "NEXT's share of sales from investments", "Total Group sales"]
cbAll = st.sidebar.checkbox("Select All")

st.write(df)

if cbAll:
    selected_layers = [type for type in area_list if st.sidebar.checkbox(type, value=cbAll, disabled=True)]
else:
    selected_layers = [type for type in area_list if st.sidebar.checkbox(type)]

if selected_layers != []:
    new_df = {"Year": ["2026", "2025", "2025", "2024"]}
    for layer in selected_layers:
        new_df[layer] = df[layer]
    new_df["Year"] = pd.to_datetime(new_df["Year"], format="%Y")
    
    st.line_chart(new_df, x="Year", y_label="Sales (£m)")
else:
    st.write("Please add more arguments on the left.")
