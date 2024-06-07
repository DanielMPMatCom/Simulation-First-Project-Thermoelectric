# Description: This file contains the code to generate the Weibull and LogNormal distribution plots. 
# Need fix: The code is not working as expected. The Weibull and LogNormal plots are not being displayed.

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy import stats
import matplotlib.pyplot as plt

SHAPE_MAX_VALUE_LAMBDA = 100
SCALA_MAX_VALUE_ALPHA = 100

MEAN_MAX_VALUE_MU = 100
DEVIATION_MAX_VALUE_SIGMA = 100

# Available statistics functions
statistics_functions = {
    "Mean": (np.mean, "The average of the data."),
    "Median": (np.median, "The middle value of the data."),
    "Standard Deviation": (
        np.std,
        "A measure of the amount of variation or dispersion of the data.",
    ),
    "Variance": (np.var, "The average of the squared differences from the mean."),
    "Skewness": (stats.skew, "A measure of the asymmetry of the data distribution."),
    "Kurtosis": (
        stats.kurtosis,
        "A measure of the 'tailedness' of the data distribution.",
    ),
}

# Get all available statistic functions from scipy.stats
scipy_stats_functions = {
    name: (getattr(stats, name), f"Scipy.stats function: {name}.")
    for name in dir(stats)
    if callable(getattr(stats, name)) and not name.startswith("_")
}
statistics_functions.update(scipy_stats_functions)


# Streamlit app


def main():
    st.title("Bootstrapping vs Repeated Experiments Comparison")

    # Sidebar inputs
    st.sidebar.header("Configuration")

    # Weibull
    st.sidebar.subheader("Weibull")

    shape_alpha = st.sidebar.slider(
        "Shape(alpha)", min_value=0, max_value=SHAPE_MAX_VALUE_LAMBDA, value=100, format="%d"
    )
    shape_alpha = shape_alpha / 10

    scale_lambda = st.sidebar.slider(
        "Scale(scala)", min_value=0, max_value=SCALA_MAX_VALUE_ALPHA, value=100
    )

    # LogNormal
    st.sidebar.subheader("LogNormal")

    mean_mu = st.sidebar.slider(
        "Mean(mu)", min_value=0, max_value=MEAN_MAX_VALUE_MU, value=100
    )

    deviation_sigma = st.sidebar.slider(
        "Deviation", min_value=0, max_value=DEVIATION_MAX_VALUE_SIGMA, value=100
    )

    # Display results
    st.title("Plot Weibull")

    # Plot Weibull Distribution
    x = np.random.weibull(shape_alpha, scale_lambda)
    fig, ax = plt.subplots()
    ax.hist(x, bins=20)
    st.pyplot(fig)

    # Display results
    st.title("Plot LogNormal")

    # Plot Weibull Distribution
    x = np.random.lognormal(mean_mu, deviation_sigma, 365)
    fig, ax = plt.subplots()
    ax.hist(x, bins=20)
    st.pyplot(fig)


if __name__ == "__main__":
    main()
