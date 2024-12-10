"""
A Summary Statistics Page
"""

import pandas as pd
import streamlit as st

if "data" not in st.session_state:
    st.write(
        (
            "<h2 style='text-align: center;color: tomato;margin-top: 10rem;'>"
            "Please Upload the dataset first</h2>"
        ),
        unsafe_allow_html=True,
    )
else:
    name: str = st.session_state.data[0]
    dataset: pd.DataFrame = st.session_state.data[1]

    st.write(
        (
            "<h2 style='color: teal;'>Summary Statistics</h2>"
            "<p>Displays key statistical measures including mean, median,"
            "standard deviation, and more for each numeric column, providing"
            "insights into data distribution.</p>"
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        (
            "<h4 style='color: dodgerblue; margin-top: 1rem'>"
            f"Processing {name} Data</h4>"
        ),
        unsafe_allow_html=True,
    )

    st.write("#### Data Description")
    st.write("##### Dataset")
    st.dataframe(dataset, use_container_width=True)
    st.write("##### Description")
    st.dataframe(dataset.describe(), use_container_width=True)

    st.write("#### Data Visualization")
    cols = st.columns(2)

    with cols[0]:
        aggregation_method = st.selectbox(
            "Aggregation Method:", ["Mean", "Median", "Min", "Max"], index=0
        )

    with cols[1]:
        period = st.slider(
            "Period:", min_value=1, max_value=30, value=1, format="%dD"
        )

    st.write(aggregation_method)
    data = getattr(
        dataset.resample(f"{period}D"), aggregation_method.lower()
    )()
    st.line_chart(data)
