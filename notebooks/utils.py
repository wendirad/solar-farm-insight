"""
Helper functions for the notebooks.
"""

import math

import matplotlib.pyplot as plt


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
    axes = axes.flatten()  # Flatten axes to iterate easily

    for idx, method in enumerate(aggregation_methods):
        # Resample the data using the specified method
        getattr(
            dataframe.resample(resample_period, on=time_column), method
        )().plot(ax=axes[idx], legend=False)

        # Set titles and labels
        axes[idx].set_title(f"{title} ({method.capitalize()})")
        axes[idx].set_xlabel(xlabel)
        axes[idx].set_ylabel(ylabel)

    for idx, ax in enumerate(axes):
        if idx >= len(aggregation_methods):
            ax.axis("off")

    fig.legend(
        *axes[idx].get_legend_handles_labels(), loc="upper center", ncol=5
    )

    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leave space for the legend
    plt.show()
