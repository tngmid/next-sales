import streamlit as st
import altair as alt
import pandas as pd
import os.path as path

st.title("NEXT Group Sales Analysis")

df = pd.read_csv("group_sales.csv")

st.line_chart(df)
