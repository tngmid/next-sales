import streamlit as st
import pandas as pd

with st.sidebar:
    st.write("Welcome!")

st.title("NEXT Group Sales Analysis")

df = pd.read_csv("group_sales.csv")
df["Year"] = pd.to_datetime(df["Year"], format="%Y")

area_list = ["Retail Stores", "Online (UK)", "Online (International)", "NEXT Finance", "Other business activities", "NEXT's share of sales from investments", "Total Group sales"]
cbAll = st.sidebar.checkbox("Select All")

if cbAll:
    print("first")
    selected_layers = [type for type in area_list if st.sidebar.checkbox(type, value=cbAll, disabled=True)]
else:
    print("second")
    selected_layers = [type for type in area_list if st.sidebar.checkbox(type)]

for layer in selected_layers:
    print(layer)
st.line_chart(df, x="Year")
