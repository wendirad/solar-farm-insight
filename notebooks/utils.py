"""
Helper functions for the notebooks.
"""

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from windrose import WindroseAxes


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
    ncols=2,
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

    # List to hold the labels for the common legend
    handles, labels = [], []

    for i, column in enumerate(columns):
        values = data[column]
        percentile_values = np.percentile(values, percentiles)

        axes[i].hist(
            values, bins=bins, alpha=0.7, color="blue", edgecolor="black"
        )
        for p, val in zip(percentiles, percentile_values):
            line = axes[i].axvline(
                x=val,
                color=plt.cm.viridis(
                    np.random.rand()
                ),  # pylint: disable=no-member
                linestyle="--",
                label=f"{p}th: {val:.2f}",
            )
            # Collect handle and label for the legend
            handles.append(line)
            labels.append(f"{p}th: {val:.2f}")

        axes[i].set_title(f"Histogram of {column}")
        axes[i].set_xlabel(column)
        axes[i].set_ylabel("Frequency")

    for j in range(len(columns), len(axes)):
        axes[j].axis("off")

    plt.figlegend(
        handles,
        labels,
        loc="upper center",
        ncol=len(percentiles),
        bbox_to_anchor=(0.5, -0.05),
    )

    plt.show()


def plot_entries(data, columns, figsize=(12, 8), bar_width=0.1):
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
        "Data Distribution: Negative, Zero, and Positive Values (Percentage)",
    )
    plt.ylabel("Percentage", fontdict={"size": 6})
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1), prop={"size": 5})
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

    return plt.gcf()


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


def plot_correlation_heatmap(data, columns, *, figsize=(8, 6)):
    """
    Plot a heatmap of correlations for RH, temperature, and solar radiation.

    Args:
        data (pd.DataFrame): The dataset containing relevant columns.

    Returns:
        None
    """

    corr_matrix = data[columns].corr()
    plt.figure(figsize=figsize)
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
    plt.title("Correlation Heatmap: " + ", ".join(columns))
    plt.show()

    return plt.gcf()


def plot_scatter_matrix(data, columns, resample_period="D", figsize=(10, 10)):
    """
    Plot a scatter matrix for specified columns after resampling data to the
    given period.

    Args:
        data (pd.DataFrame): The dataset containing the columns.
        columns (list): List of column names to include in the scatter matrix.
        resample_period (str): The resampling period (default: 'D' for daily).
        figsize (tuple): Figure size for the scatter matrix (default:(10, 10)).

    Returns:
        None
    """
    resampled_data = data.resample(resample_period).mean()

    pd.plotting.scatter_matrix(
        resampled_data[columns], figsize=figsize, alpha=0.7
    )
    plt.suptitle(
        f"Scatter Matrix for {resample_period.capitalize()} Data", fontsize=16
    )
    plt.show()

    return plt.gcf()


def plot_windrose_distribution(data):
    """
    Plot windrose diagrams for wind speed, wind gust speed, and wind
    direction variability.

    Args:
        data (pd.DataFrame): The dataset containing columns 'WD', 'WS',
                             WSgust', and 'WDstdev'.

    Returns:
        None
    """

    bins = np.arange(0, 361, 10)
    data["WD_bin"] = pd.cut(
        data["WD"], bins=bins, labels=bins[:-1], include_lowest=True
    )

    avg_wdstdev = data.groupby("WD_bin")["WDstdev"].mean().reset_index()
    avg_wdstdev["WD_bin"] = avg_wdstdev["WD_bin"].astype(float)

    fig = plt.figure(figsize=(18, 6))

    ax1 = WindroseAxes(fig, [0.05, 0.1, 0.25, 0.8])
    fig.add_axes(ax1)
    ax1.bar(
        data["WD"], data["WS"], normed=True, opening=0.8, edgecolor="white"
    )
    ax1.set_title("Wind Speed Distribution")

    ax2 = WindroseAxes(fig, [0.35, 0.1, 0.25, 0.8])
    fig.add_axes(ax2)
    ax2.bar(
        data["WD"], data["WSgust"], normed=True, opening=0.8, edgecolor="white"
    )
    ax2.set_title("Wind Gust Speed Distribution")

    ax3 = WindroseAxes(fig, [0.65, 0.1, 0.25, 0.8])
    fig.add_axes(ax3)
    ax3.bar(
        avg_wdstdev["WD_bin"],
        avg_wdstdev["WDstdev"],
        normed=False,
        opening=0.8,
        edgecolor="white",
    )
    ax3.set_title("Wind Direction Variability Distribution")

    plt.show()


def analyze_rh_impact(data, group_period="D", *, figsize=(15, 10)):
    """
    Analyze the impact of relative humidity (RH) on temperature and solar
    radiation by grouping data into periods.

    Args:
        data (pd.DataFrame): The dataset containing RH, temperature, and solar
                                radiation columns with a DateTime index.
        group_period (str): The period for grouping ('D' for daily, 'W' for
                                weekly, 'M' for monthly).

    Returns:
        None
    """

    numeric_data = data.select_dtypes(include=["number"])

    grouped_data = numeric_data.resample(group_period).mean()

    variables = ["TModA", "TModB", "GHI", "DNI", "DHI"]

    plt.figure(figsize=figsize)
    for i, var in enumerate(variables, 1):
        if var not in grouped_data.columns:
            continue

        plt.subplot(2, 3, i)
        sns.scatterplot(data=grouped_data, x="RH", y=var, alpha=0.7)
        sns.regplot(
            data=grouped_data,
            x="RH",
            y=var,
            scatter=False,
            color="red",
            line_kws={"linewidth": 2},
        )
        plt.title(f"{var} vs RH ({group_period} Mean)")
        plt.xlabel("Relative Humidity (RH)")
        plt.ylabel(var)

    plt.tight_layout()
    plt.show()


def plot_boxplot_rh_categories(data):
    """
    Plot box plots of temperature and solar radiation by RH categories.

    Args:
        data (pd.DataFrame): The dataset containing RH, temperature, and solar
                              radiation columns.

    Returns:
        None
    """
    data["RH_category"] = pd.cut(
        data["RH"], bins=[0, 30, 60, 100], labels=["Low", "Medium", "High"]
    )

    variables = ["TModA", "TModB", "GHI", "DNI", "DHI"]
    plt.figure(figsize=(15, 10))
    for i, var in enumerate(variables, 1):
        plt.subplot(2, 3, i)
        sns.boxplot(data=data, x="RH_category", y=var)
        plt.title(f"{var} by RH Category")
        plt.xlabel("RH Category")
        plt.ylabel(var)
    plt.tight_layout()
    plt.show()


def plot_histograms(data, variables, bins=30, figsize=(15, 10)):
    """
    Create histograms for the specified variables to visualize frequency
    distributions.

    Args:
        data (pd.DataFrame): The dataset containing the variables.
        variables (list): List of column names to create histograms for.
        bins (int): Number of bins for the histograms (default: 30).
        figsize (tuple): Size of the figure (default: (15, 10)).

    Returns:
        None
    """
    num_vars = len(variables)
    ncols = 3
    nrows = -(-num_vars // ncols)

    plt.figure(figsize=figsize)
    for i, var in enumerate(variables, 1):
        plt.subplot(nrows, ncols, i)
        data[var].dropna().hist(bins=bins, alpha=0.7, edgecolor="black")
        plt.title(f"Histogram of {var}")
        plt.xlabel(var)
        plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()


def calculate_z_scores(data, columns, threshold=3):
    """
    Calculate Z-scores for the specified columns and flag data points
    significantly
    different from the mean.

    Args:
        data (pd.DataFrame): The dataset containing the variables.
        columns (list): List of column names to calculate Z-scores for.
        threshold (float): Z-score threshold to flag significant deviations
                            (default: 3).

    Returns:
        pd.DataFrame: DataFrame with additional columns for Z-scores and flags.
    """
    z_score_results = data.copy()

    for column in columns:
        z_scores = (data[column] - data[column].mean()) / data[column].std()
        z_score_results[f"{column}_zscore"] = z_scores

        z_score_results[f"{column}_flagged"] = np.abs(z_scores) > threshold

    return z_score_results


def plot_bubble_chart(
    data, x_var, y_var, size_var, color_var=None, figsize=(10, 7), alpha=0.6
):
    """
    Plot a bubble chart to explore relationships between variables.

    Args:
        data (pd.DataFrame): The dataset containing the variables.
        x_var (str): Column name for the X-axis variable.
        y_var (str): Column name for the Y-axis variable.
        size_var (str): Column name for the bubble size variable.
        color_var (str): Column name for bubble color (optional).
        figsize (tuple): Size of the figure (default: (10, 7)).
        alpha (float): Transparency level for bubbles (default: 0.6).

    Returns:
        None
    """
    plt.figure(figsize=figsize)

    bubble_sizes = (
        (data[size_var] - data[size_var].min())
        / (data[size_var].max() - data[size_var].min())
        * 1000
    )

    scatter = plt.scatter(
        data[x_var],
        data[y_var],
        s=bubble_sizes,
        c=data[color_var] if color_var else None,
        cmap="viridis" if color_var else None,
        alpha=alpha,
        edgecolor="black",
    )

    if color_var:
        plt.colorbar(scatter, label=color_var)

    plt.title(f"{y_var} vs {x_var} with Bubble Size Representing {size_var}")
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()


def aggregate_solar_data(df, frequency="M"):
    """
    Aggregates GHI, DNI, and DHI data by specified frequency
    (monthly or yearly).

    Parameters:
    - df (DataFrame): Input DataFrame with a DateTime index and columns
                        ['GHI', 'DNI', 'DHI'].
    - frequency (str): Aggregation frequency
                        ('M' for monthly, 'Y' for yearly).

    Returns:
    - DataFrame: Aggregated DataFrame with averages for GHI, DNI, and DHI.
    """
    if frequency not in ["M", "Y"]:
        raise ValueError("Frequency must be 'M' (monthly) or 'Y' (yearly).")

    # Resample data based on the specified frequency and compute averages
    aggregated = df[["GHI", "DNI", "DHI"]].resample(frequency).mean()

    return aggregated


def clip_columns_to_range(df, column_ranges):
    """
    Clips the values of specified columns in the DataFrame to their real-world
    min and max.

    Parameters:
    - df (DataFrame): Input DataFrame.
    - column_ranges (dict): Dictionary where keys are column names, and values
                            are tuples (min, max).

    Returns:
    - DataFrame: DataFrame with values clipped to specified ranges.
    """
    for column, (min_val, max_val) in column_ranges.items():
        if column in df.columns:
            df[column] = df[column].clip(lower=min_val, upper=max_val)
    return df


def replace_outliers_with_mean_or_median(df, method="median", threshold=3):
    """
    Replaces outliers in the DataFrame with the column median or mean.

    Parameters:
    - df (DataFrame): Input DataFrame.
    - method (str): Method to replace outliers, either 'median' or 'mean'.
                    Default is 'median'.
    - threshold (float): Z-score threshold to identify outliers. Default is 3.

    Returns:
    - DataFrame: A DataFrame with outliers replaced.
    """
    df_cleaned = df.copy()

    for col in df_cleaned.select_dtypes(include=np.number).columns:
        # Calculate Z-scores
        col_mean = df_cleaned[col].mean()
        col_std = df_cleaned[col].std()
        z_scores = (df_cleaned[col] - col_mean) / col_std

        # Identify outliers
        outliers = z_scores.abs() > threshold

        # Replace outliers with mean or median
        if method == "mean":
            replacement_value = col_mean
        elif method == "median":
            replacement_value = df_cleaned[col].median()
        else:
            raise ValueError("Method must be either 'median' or 'mean'")

        df_cleaned.loc[outliers, col] = replacement_value

    return df_cleaned


def replace_neg_with_zero(df):
    """
    Replaces all negative values in the DataFrame with zero.

    Parameters:
    - df (DataFrame): The input DataFrame with numeric columns.

    Returns:
    - DataFrame: A DataFrame where all negative values have been
                replaced with zero.
    """
    # Replace negative values with zero
    df_cleaned = df.where(df >= 0, 0)
    return df_cleaned


def check_negative_values_nighttime(df, nighttime_start=18, nighttime_end=6):
    """
    Checks if negative values in a DataFrame occur during nighttime.

    Parameters:
    - df (DataFrame): The input DataFrame with a Timestamp
                        index and numeric columns.
    - nighttime_start (int): The hour when nighttime starts
                            (default is 18, 6:00 PM).
    - nighttime_end (int): The hour when nighttime ends
                            (default is 6, 6:00 AM).

    Returns:
    - DataFrame: A DataFrame containing rows with negative values, their hour,
      and a boolean indicating if they occur during nighttime.
    """
    negative_values = df[(df < 0).any(axis=1)].copy()

    negative_values["Hour"] = negative_values.index.hour

    is_nighttime = (negative_values["Hour"] >= nighttime_start) | (
        negative_values["Hour"] < nighttime_end
    )

    negative_values["Nighttime"] = is_nighttime

    return all(negative_values[["Hour", "Nighttime"] + list(df.columns)])
