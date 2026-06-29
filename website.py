import streamlit as st
import pandas as pd

with st.sidebar:
    st.write("Welcome!")

st.title("NEXT Group Sales Analysis")

df = pd.read_csv("group_sales.csv")
df["Year"] = pd.to_datetime(df["Year"], format="%Y")

area = st.selectbox("Select Crop Type:", ["<select>", "Retail Stores", "Online (UK)", "Online (International)", "NEXT Finance", "Other business activities", "NEXT's share of sales from investments", "Total Group sales"])

if area != "<select>":
    st.sidebar.header(area)
    cbAll = st.sidebar.checkbox("Select All")
else:
    st.write("Please select an area of interest.")


st.line_chart(df, x="Year")
