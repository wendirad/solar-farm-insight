"""
Helper functions for the notebooks.
"""

import math

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose


def report_null_columns(df):
    """
    Identifies columns causing NULL values and returns a report.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        dict: A dictionary with column names as keys
              and count of NULL values as values.
    """
    null_report = {
        col: int(df[col].isnull().sum())
        for col in df.columns
        if df[col].isnull().sum() > 0
    }
    return null_report


def plot_statistical_summary(
    dataframe,
    resample_period,
    aggregation_methods,
    *,
    time_column=None,
    figsize=(15, 5),
    xlabel="Time",
    ylabel="Value",
    title="Resampled Data",
):
    """
    Plots resampled data for each aggregation method in a grid
    with two columns and a common legend.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the data.
        resample_period (str): The resampling period (e.g., "1W", "1D").
        time_column (str): The name of the timestamp column.
        aggregation_methods (list): List of aggregation methods to apply
                                    (e.g., ["mean", "median"]).
        figsize (tuple): Figure size as (width, height) for each subplot.
        xlabel (str): Label for the X-axis.
        ylabel (str): Label for the Y-axis.
        title (str): Title of the plot.

    Returns:
        None
    """

    ncols = 2
    nrows = math.ceil(len(aggregation_methods) / ncols)

    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(figsize[0], figsize[1] * nrows),
        constrained_layout=True,
    )
    axes = axes.flatten()

    for idx, method in enumerate(aggregation_methods):
        getattr(
            dataframe.resample(resample_period, on=time_column), method
        )().plot(ax=axes[idx], legend=False)

        axes[idx].set_title(f"{title} ({method.capitalize()})")
        axes[idx].set_xlabel(xlabel)
        axes[idx].set_ylabel(ylabel)

    for idx, ax in enumerate(axes):
        if idx >= len(aggregation_methods):
            ax.axis("off")

    fig.legend(
        *axes[idx].get_legend_handles_labels(), loc="upper center", ncol=5
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


def plot_histogram_with_percentiles(
    data,
    columns,
    *,
    percentiles=None,
    bins=30,
    ncols=2,
    figsize=(15, 5),
):
    """
    Plot histograms with percentile thresholds for multiple columns in a grid
    layout.

    Args:
        data (pd.DataFrame): The dataset containing the columns.
        columns (list): List of columns to visualize.
        percentiles (list): Percentile thresholds to highlight
                            (default: [10, 25, 50, 75, 90]).
        ncols (int): Number of columns in the grid (default: 2).
        figsize (tuple): Figure size as (width, height) for each subplot row.

    Returns:
        None
    """
    if percentiles is None:
        percentiles = [10, 25, 50, 75, 90]

    nrows = math.ceil(len(columns) / ncols)
    _, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(figsize[0], figsize[1] * nrows),
        constrained_layout=True,
    )
    axes = axes.flatten()

    for i, column in enumerate(columns):
        values = data[column]
        percentile_values = np.percentile(values, percentiles)

        axes[i].hist(
            values, bins=bins, alpha=0.7, color="blue", edgecolor="black"
        )
        for p, val in zip(percentiles, percentile_values):
            axes[i].axvline(
                x=val,
                color=plt.cm.viridis(
                    np.random.rand()
                ),  # pylint: disable=no-member
                linestyle="--",
                label=f"{p}th: {val:.2f}",
            )

        axes[i].set_title(f"Histogram of {column}")
        axes[i].set_xlabel(column)
        axes[i].set_ylabel("Frequency")
        axes[i].legend()

    for j in range(len(columns), len(axes)):
        axes[j].axis("off")

    plt.show()


def plot_outliers(dataframe, columns, ncols=2, figsize=(15, 5)):
    """
    Draws box plots for multiple columns in a grid to visualize outliers.

    Args:
        dataframe (pd.DataFrame): The dataset containing the columns.
        columns (list): List of column names to visualize with box plots.
        ncols (int): Number of columns in the grid layout.
        figsize (tuple): Figure size for the entire grid.

    Returns:
        None
    """
    nrows = math.ceil(len(columns) / ncols)
    _, axes = plt.subplots(nrows, ncols, figsize=figsize)

    axes = axes.flatten()

    for idx, column in enumerate(columns):
        sns.boxplot(data=dataframe[column], ax=axes[idx])
        axes[idx].set_title(f"Box Plot of {column}")
    for idx in range(len(columns), len(axes)):
        axes[idx].axis("off")

    plt.tight_layout()
    plt.show()


def plot_entries(data, columns, figsize=(12, 8)):
    """
    Plot stacked bar charts showing the percentage distribution of negative,
    zero, and positive values for multiple columns.

    Args:
        data (pd.DataFrame): The dataset.
        columns (list): List of columns to check for data distribution.

    Returns:
        None
    """
    total_counts = [len(data[col]) for col in columns]
    negative_counts = [np.sum(data[col] < 0) for col in columns]
    zero_counts = [np.sum(data[col] == 0) for col in columns]
    positive_counts = [np.sum(data[col] > 0) for col in columns]

    negative_percent = [
        count / total * 100
        for count, total in zip(negative_counts, total_counts)
    ]
    zero_percent = [
        count / total * 100 for count, total in zip(zero_counts, total_counts)
    ]
    positive_percent = [
        count / total * 100
        for count, total in zip(positive_counts, total_counts)
    ]

    bar_width = 0.6
    x = np.arange(len(columns))

    plt.figure(figsize=figsize)
    plt.bar(
        x,
        negative_percent,
        color="red",
        label="Negative Values",
        width=bar_width,
    )
    plt.bar(
        x,
        zero_percent,
        bottom=negative_percent,
        color="green",
        label="Zero Values",
        width=bar_width,
    )
    plt.bar(
        x,
        positive_percent,
        bottom=np.array(negative_percent) + np.array(zero_percent),
        color="blue",
        label="Positive Values",
        width=bar_width,
    )

    plt.xticks(x, columns, rotation=45)
    plt.title(
        "Data Distribution: Negative, Zero, and Positive Values (Percentage)"
    )
    plt.xlabel("Columns")
    plt.ylabel("Percentage")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


def plot_trends(
    dataframe,
    columns,
    *,
    period="Month",
    ncols=2,
    figsize=(20, 10),
    title_prefix="Solar Farm",
):
    """
    Plot bar charts for specified columns by month and year in a grid layout.

    Args:
        dataframe (pd.DataFrame): The dataset containing the solar data with
                                  a DateTime index.
        columns (list): List of column names to plot.
        period (str): The period to plot by (default: "Month").
        ncols (int): Number of columns in the grid (default: 2).
        figsize (tuple): Figure size as (width, height) (default: (20, 10)).
        title_prefix (str): Prefix for the plot titles (default:
                                                        "Benin Solar Farm").

    Returns:
        None
    """

    nrows = -(-len(columns) // ncols)
    plt.figure(figsize=figsize)

    for i, var in enumerate(columns):
        plt.subplot(nrows, ncols, i + 1)
        sns.barplot(
            data=dataframe,
            x={
                "m": dataframe.index.month,
                "d": dataframe.index.day,
                "h": dataframe.index.hour,
            }[period[0].lower()],
            y=var,
            hue=dataframe.index.year,
        )
        plt.title(f"{title_prefix} - {var} by {period}")
        plt.xlabel(period)
        plt.ylabel(var)
        plt.legend(title="Year", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    plt.show()


def plot_seasonal_decomposition(
    data, columns, period, ncols=2, figsize=(20, 5)
):
    """
    Perform seasonal decomposition and plot results for multiple
    columns in a grid layout.

    Args:
        data (pd.DataFrame): The dataset with a DateTime index.
        columns (list): List of column names to decompose.
        period (int): The period of the seasonality
                      (e.g., 365 for daily data over a year).
        ncols (int): Number of columns in the grid layout.
        figsize (tuple): Figure size for the entire grid.

    Returns:
        None
    """
    nrows = math.ceil(len(columns) / ncols)
    _, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    axes = axes.flatten()

    for i, column in enumerate(columns):

        decomposition = seasonal_decompose(
            data[column], model="additive", period=period
        )

        axes[i].plot(decomposition.trend, label="Trend", color="blue")
        axes[i].plot(decomposition.seasonal, label="Seasonal", color="green")
        axes[i].plot(decomposition.resid, label="Residual", color="red")
        axes[i].set_title(f"Seasonal Decomposition of {column}")
        axes[i].legend()

    for i in range(len(columns), len(axes)):
        axes[i].axis("off")

    plt.tight_layout()
    plt.show()


def plot_cleaning_impact(
    data, columns, time_column=None, figsize=(15, 10), ncols=2
):
    """
    Plot box plots and line plots for sensor readings before and after
    cleaning in a grid.

    Args:
        data (pd.DataFrame): The dataset containing the cleaning,
                             sensor, and time data.
        columns (list): List of sensor columns to plot.
        time_column (str): The name of the time column.
        figsize (tuple): The size of the figure (default: (15, 10)).
        ncols (int): Number of columns in the grid layout (default: 2).

    Returns:
        None
    """
    nrows = len(columns)
    _, axes = plt.subplots(
        nrows=nrows, ncols=ncols, figsize=figsize, constrained_layout=True
    )

    for i, column in enumerate(columns):
        sns.boxplot(ax=axes[i, 0], data=data, x="Cleaning", y=column)
        axes[i, 0].set_title(f"Efect: {column}")
        axes[i, 0].set_xlabel("Cleaning (0 = Before, 1 = After)")
        axes[i, 0].set_ylabel("Readings")

        for status in data["Cleaning"].unique():
            subset = data[data["Cleaning"] == status]
            axes[i, 1].plot(
                (
                    subset[time_column]
                    if time_column is not None
                    else subset.index
                ),
                subset[column],
                label=f"Cleaning {status}",
            )
        axes[i, 1].set_title(f"Trend Plot: {column}")
        axes[i, 1].set_xlabel("Time")
        axes[i, 1].set_ylabel("Readings")
        axes[i, 1].legend(title="Cleaning Status")
        axes[i, 1].grid()

    plt.suptitle("Impact of Cleaning on Sensor Readings", fontsize=16)
    plt.show()
