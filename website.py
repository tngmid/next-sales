import streamlit as st
import altair as alt
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

with st.sidebar:
    st.write("Welcome!")

st.title("NEXT Group Sales Analysis")

df = pd.read_csv("group_sales.csv")
df["Year"] = ["2026", "2025", "2024", "2023", "2022"]
df["Year"] = pd.to_datetime(df["Year"], format="%Y")

area_list = ["Retail Stores", "Online", "NEXT Finance", "Total Platform", "Other business activities", "NEXT's share of sales from investments", "Total Group sales"]
cbAll = st.sidebar.checkbox("Select All")

if cbAll:
    selected_layers = [type for type in area_list if st.sidebar.checkbox(type, value=cbAll, disabled=True)]
else:
    selected_layers = [type for type in area_list if st.sidebar.checkbox(type)]

if selected_layers != []:
    new_df = {"Year": ["2026", "2025", "2024", "2023", "2022"]}
    for layer in selected_layers:
        new_df[layer] = df[layer]
    new_df["Year"] = pd.to_datetime(new_df["Year"], format="%Y")

    show_prediction = st.sidebar.toggle("Show 10-year prediction")
    
    if show_prediction:
        years = new_df["Year"].dt.year.values.reshape(-1, 1)
        future_years = np.arange(2027, 2037).reshape(-1, 1)
        
        historical = new_df.copy()
        historical["Type"] = "Historical"
        
        prediction = pd.DataFrame({
            "Year": pd.to_datetime(future_years.flatten(), format="%Y"),
            "Type": "Prediction"
        })
    for layer in selected_layers:
        model = LinearRegression()
        model.fit(years, new_df[layer])

        prediction[layer] = model.predict(future_years)

    plot_df = pd.concat([historical, prediction], ignore_index=True)

else:
    st.write("Please add more arguments on the left.")
