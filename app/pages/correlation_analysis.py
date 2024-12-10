"""
A Correlation Analysis Page
"""

import pandas as pd
import streamlit as st
from utils import (  # pylint: disable=import-error
    plot_correlation_heatmap,
    plot_scatter_matrix,
)

if "data" in st.session_state:
    name: str = st.session_state.data[0]
    dataset: pd.DataFrame = st.session_state.data[1]

    st.write(
        (
            "<h2 style='color: teal;'>Correlation Analysis</h2>"
            "<p>Visualize variables over time using a chart"
            "charts to identify monthly patterns, daily trends, and anomalies"
            "like peaks in solar irradiance or temperature fluctuations."
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

    st.write("#### Data Visualization")

    numeric_columns = list(dataset.select_dtypes(include=["number"]).columns)

    input_cols = st.columns(2)
    plot_cols = st.columns(2)

    with input_cols[0]:
        columns = st.multiselect("Columns", numeric_columns)
    with input_cols[1]:
        period = st.selectbox(
            "Period:", ["Daily", "Weekly", "Monthly"], index=1
        )

    if len(columns) > 0:
        with plot_cols[0]:
            cplt = plot_correlation_heatmap(
                dataset,
                columns=columns,
                figsize=(10, 5),
            )
            st.pyplot(
                cplt,
                use_container_width=False,
            )
            cplt.clf()

        with plot_cols[1]:
            splt = plot_scatter_matrix(
                dataset,
                columns=columns,
                resample_period=period[0],
                figsize=(10, 5),
            )
            st.pyplot(
                splt,
                use_container_width=False,
            )
            splt.clf()
