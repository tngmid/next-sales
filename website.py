import streamlit as st
import pandas as pd

st.title("NEXT Group Sales Analysis")

df = pd.read_csv("group_sales.csv")
df["Year"] = pd.to_datetime(df["Year"], format="%Y")

st.line_chart(df, x="Year")
