"""
A helper module for dashboard for Solar Farm Insight
"""

import pandas as pd


def process_name(name) -> str:
    """
    Process the name of the file to be displayed in the dashboard

    Args:
        name (str): The name of the file

    Returns (str):
    """
    return name.replace(".csv", "").replace("_", " ").title()


def load_data(files):
    """
    Load the data from the uploaded files

    Args:
        files (list): A list of uploaded files

    Returns (dict):
    """
    names = {}
    for file in files:
        name = process_name(file.name)
        names[name] = pd.read_csv(file)
    return names
