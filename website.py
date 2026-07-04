#import streamlit as st
#import altair as alt
#import pandas as pd
#from sklearn.linear_model import LinearRegression
#import numpy as np

#with st.sidebar:
#    st.write("Welcome!")

#st.title("NEXT Group Sales Analysis")

#df = pd.read_csv("group_sales.csv")
#df["Year"] = ["2026", "2025", "2024", "2023", "2022"]
#df["Year"] = pd.to_datetime(df["Year"], format="%Y")

#area_list = ["Retail Stores", "Online", "NEXT Finance", "Total Platform", "Other business activities", "NEXT's share of sales from investments", "Total Group sales"]
#cbAll = st.sidebar.checkbox("Select All")

#if cbAll:
#    selected_layers = [type for type in area_list if st.sidebar.checkbox(type, value=cbAll, disabled=True)]
#else:
#    selected_layers = [type for type in area_list if st.sidebar.checkbox(type)]

#if selected_layers != []:
#    new_df = {"Year": ["2026", "2025", "2024", "2023", "2022"]}
#    for layer in selected_layers:
#        new_df[layer] = df[layer]
#    new_df["Year"] = pd.to_datetime(new_df["Year"], format="%Y")

#    show_prediction = st.sidebar.toggle("Show 10-year prediction")
    
#    if show_prediction:
#        years = new_df["Year"].year.values.reshape(-1, 1)
#        future_years = np.arange(2027, 2037).reshape(-1, 1)
#        
#        historical = new_df.copy()
#        historical["Type"] = "Historical"
        
#        prediction = pd.DataFrame({
#            "Year": pd.to_datetime(future_years.flatten(), format="%Y"),
#            "Type": "Prediction"
#        })
#        for layer in selected_layers:
#            model = LinearRegression()
#            model.fit(years, new_df[layer])
    
#            prediction[layer] = model.predict(future_years)

#    plot_df = pd.concat([historical, prediction], ignore_index=True)

#else:
#    st.write("Please add more arguments on the left.")


import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

with st.sidebar:
    st.write("Welcome!")

st.title("NEXT Group Sales Analysis")

# Load data
df = pd.read_csv("group_sales.csv")

# Create Year column
df["Year"] = pd.to_datetime(
    ["2026", "2025", "2024", "2023", "2022"],
    format="%Y"
)

# Categories
area_list = [
    "Retail Stores",
    "Online",
    "NEXT Finance",
    "Total Platform",
    "Other business activities",
    "NEXT's share of sales from investments",
    "Total Group sales"
]

# Sidebar
cbAll = st.sidebar.checkbox("Select All")

if cbAll:
    selected_layers = [
        area for area in area_list
        if st.sidebar.checkbox(area, value=True, disabled=True)
    ]
else:
    selected_layers = [
        area for area in area_list
        if st.sidebar.checkbox(area)
    ]

show_prediction = st.sidebar.toggle("Show 10-year prediction")

if selected_layers:

    # Create dataframe for plotting
    new_df = pd.DataFrame({
        "Year": df["Year"]
    })

    for layer in selected_layers:
        new_df[layer] = df[layer]

    # No prediction
    if not show_prediction:

        st.line_chart(
            new_df,
            x="Year",
            y=selected_layers,
            y_label="Sales (£m)"
        )

    # Prediction enabled
    else:

        # Historical years
        years = new_df["Year"].dt.year.to_numpy().reshape(-1, 1)

        # Future years (2027-2036)
        future_years = np.arange(2027, 2037).reshape(-1, 1)

        historical = new_df.copy()
        historical["Type"] = "Historical"

        prediction = pd.DataFrame({
            "Year": pd.to_datetime(
                future_years.flatten(),
                format="%Y"
            ),
            "Type": "Prediction"
        })

        # Train one regression model for each selected category
        for layer in selected_layers:

            y = new_df[layer].to_numpy()

            model = LinearRegression()
            model.fit(years, y)

            prediction[layer] = model.predict(future_years)

        # Combine historical + prediction
        plot_df = pd.concat(
            [historical, prediction],
            ignore_index=True
        )

        # Convert to long format
        plot_long = plot_df.melt(
            id_vars=["Year", "Type"],
            value_vars=selected_layers,
            var_name="Category",
            value_name="Sales"
        )

        # Plot
        chart = (
            alt.Chart(plot_long)
            .mark_line(strokeWidth=3)
            .encode(
                x=alt.X("Year:T", title="Year"),
                y=alt.Y("Sales:Q", title="Sales (£m)"),
                color=alt.Color("Category:N", title="Category"),
                strokeDash=alt.StrokeDash("Type:N", title=""),
                tooltip=[
                    alt.Tooltip("Year:T"),
                    alt.Tooltip("Category:N"),
                    alt.Tooltip("Sales:Q", format=",.0f"),
                    alt.Tooltip("Type:N")
                ]
            )
            .interactive()
        )

        st.altair_chart(chart, use_container_width=True)

else:
    st.write("Please add more arguments on the left.")
