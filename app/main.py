"""
A Dashboard for Solar Farm Insight EDA
"""

import streamlit as st
from utils import load_data  # pylint: disable=import-error


def run() -> None:
    """
    A function to run the main application
    """
    st.set_page_config(layout="wide")

    dashboard = st.Page(
        "pages/dashboard.py",
        title="Dashboard",
        icon=":material/dashboard:",
        default=True,
    )
    summary_page = st.Page(
        "pages/summary_statistics.py",
        title="Summary Statistics",
        icon=":material/analytics:",
    )
    data_quality_check = st.Page(
        "pages/data_quality_check.py",
        title="Data Quality Check",
        icon=":material/database:",
    )

    correlation_analysis = st.Page(
        "pages/correlation_analysis.py",
        title="Correlation Analysis",
        icon=":material/insights:",
    )
    pg = st.navigation(
        {
            "": [
                dashboard,
                summary_page,
                data_quality_check,
                correlation_analysis,
            ],
        }
    )

    with st.sidebar:
        files = st.file_uploader(
            "",
            type=["csv"],
            accept_multiple_files=True,
        )
        if files:
            datasets = load_data(files)
            name = st.selectbox("Select a dataset:", datasets.keys())
            if name:
                st.session_state["data"] = (name, datasets[name])

    st.markdown(
        (
            "<h1 style='text-align: center; color: #4CAF50;'>"
            "🌞 Solar Farm Insight</h1>"
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        (
            "<p style='text-align: center; color: gray;'>Explore solar data"
            " insights with interactive charts and analysis</p>"
        ),
        unsafe_allow_html=True,
    )

    if pg.title != "Dashboard" and "data" not in st.session_state:
        st.write(
            (
                "<h2 style='text-align: center;color: tomato;margin-top:"
                " 10rem;'>Please Upload the dataset first</h2>"
            ),
            unsafe_allow_html=True,
        )
    pg.run()


if __name__ == "__main__":
    run()
