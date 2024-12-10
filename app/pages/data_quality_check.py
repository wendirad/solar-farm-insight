"""
Data Quality Checking Page
"""

import pandas as pd
import streamlit as st

from utils import (  # pylint: disable=import-error); isort: skip
    plot_entries,
    report_null_columns,
)

if "data" in st.session_state:
    name: str = st.session_state.data[0]
    dataset: pd.DataFrame = st.session_state.data[1]

    st.write(
        (
            "<h2 style='color: teal;'>Data Quality Check</h2>"
            "<p>Identifies missing values, outliers, and incorrect entries"
            "in critical columns, ensuring data accuracy and reliability.</p>"
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

    st.write("#### Missing Columns")
    st.table(report_null_columns(dataset))

    st.write("#### Data Visualization")

    numeric_columns = list(dataset.select_dtypes(include=["number"]).columns)

    input_cols = st.columns(1)
    plot_cols = st.columns(2)

    with input_cols[0]:
        columns = st.multiselect("Columns", numeric_columns)

    if len(columns) > 0:
        plt = plot_entries(
            dataset,
            columns=columns,
            figsize=(10, 5),
            bar_width=0.1 * len(columns),
        )
        with plot_cols[0]:
            st.pyplot(
                plt,
                use_container_width=False,
            )
            plt.clf()
        with plot_cols[1]:
            st.pyplot(
                dataset[columns].boxplot(figsize=(10, 5)).get_figure(),
                clear_figure=True,
            )
