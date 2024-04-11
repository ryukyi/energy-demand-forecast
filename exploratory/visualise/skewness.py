"""Visualise to help exploring the data."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import shapiro, skew


# Function to check if a column is normally distributed
def is_normally_distributed(column: pd.Series) -> bool:
    """Normal distribution helps understand if mean is sensible replacement of nan.

    Args:
        column (pd.Series): data inspected

    Returns:
        bool: confirms the data is normally distributed
    """
    # Check if the column has enough data points (at least 3)
    if len(column) < 3:
        return False, "Not enough data points"

    # Perform the Shapiro-Wilk test
    stat, p = shapiro(column)

    # If p > 0.05, we assume the data is normally distributed
    if p > 0.05:
        return True, f"p-value: {p:.5f}"
    else:
        return False, f"p-value: {p:.5f}"


def skewness(df_series: pd.Series) -> float:
    """Calculate the skewness of a given pandas Series.

    This function checks if the input series contains numerical
    data and then calculates the skewness.
    Skewness is a measure of the asymmetry of the probability
    distribution of a real-valued random variable about its mean.

    Args:
        df_series (pd.Series): The pandas Series for which skewness is to be calculated.

    Returns:
        float: The skewness of the input series.
            Returns NaN if the series is empty or contains non-numerical data.
    """
    if np.issubdtype(df_series.dtype, np.number):
        # Check for skewness
        return skew(df_series.dropna())


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
