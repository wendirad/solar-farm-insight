"""
A Dashboard for Solar Farm Insight
"""

import streamlit as st
from utils import load_data  # pylint: disable=import-error

# Page configuration
st.set_page_config(page_title="Solar Dashboard", layout="wide")

# Sidebar
with st.sidebar:

    st.markdown(
        "**Contact:** [Wendirad Demelash](mailto:wendiradame@gmail.com)"
    )

# Header
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>Solar Farm Insight</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    (
        "<p style='text-align: center; color: gray;'>Explore solar data"
        "insights with interactive charts and analysis</p>"
    ),
    unsafe_allow_html=True,
)

# Layout: Three sections
col1, _, col2 = st.columns([2, 2, 1])

with col1:
    st.markdown(
        "<h3 style='color: #FFC107;'>Data Upload</h3>", unsafe_allow_html=True
    )
    files = st.file_uploader(
        "Upload your dataset here:", type=["csv"], accept_multiple_files=True
    )

with col2:
    st.markdown(
        "<h3 style='color: #FF5722;'>Quick Actions</h3>",
        unsafe_allow_html=True,
    )
    run_analysis = st.button("Run Analysis", use_container_width=True)
    st.button("Reset Dashboard", use_container_width=True)

if files:
    names = load_data(files)
    dataset = st.selectbox("Select a dataset:", names.keys())
    df = names[dataset]

    if dataset:
        st.markdown(
            f"<h3 style='color: #FF5722;'>{dataset}</h3>",
            unsafe_allow_html=True,
        )
        st.write(df)

    if run_analysis:
        st.markdown(
            "<h3 style='color: #2196F3;'>Summary</h3>", unsafe_allow_html=True
        )
        st.write(df.describe(), use_container_width=True)

        st.markdown(
            "<h3 style='color: #2196F3;'>Data Visualization</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='color: #2196F3;'>Data Visualization</h3>",
            unsafe_allow_html=True,
        )
        x = st.selectbox("Select X:", df.columns)

        st.markdown(
            "<h3 style='color: #2196F3;'>Insights</h3>", unsafe_allow_html=True
        )

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    (
        "<footer style='text-align: center;'>Powered by Streamlit |"
        "Designed for Solar Farm Insights</footer>"
    ),
    unsafe_allow_html=True,
)
