"""Visualise to help exploring the data."""

import matplotlib.pyplot as plt
import pandas as pd


def plot_histogram(df_series: pd.Series) -> None:
    """Plots a histogram of the specified column from the given DataFrame.

    Args:
        df_series: The series/column in the DataFrame to be plotted.
    """
    # Plot the histogram
    df_series.plot(kind="hist", bins=30, alpha=0.5, rwidth=0.85)
    plt.title("Histogram of " + df_series.name)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()
