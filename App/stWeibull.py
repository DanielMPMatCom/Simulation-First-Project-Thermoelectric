# HACER UNO ASI PARA NUESTRO PROYECTO

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

SHAPE_MAX_VALUE_ALPHA = 1000
SCALA_MAX_VALUE_LAMBDA = 1000


# Function to perform bootstrapping
def bootstrap(data, num_samples, statistic, alpha):
    samples = np.random.choice(data, (num_samples, len(data)), replace=True)
    stats = np.array([statistic(sample) for sample in samples])
    lower = np.percentile(stats, 100 * alpha / 2)
    upper = np.percentile(stats, 100 * (1 - alpha / 2))
    return np.mean(stats), lower, upper, stats


# Function to perform repeated experiments
def repeated_experiments(data, num_samples, statistic):
    stats = np.array(
        [
            statistic(np.random.choice(data, len(data), replace=True))
            for _ in range(num_samples)
        ]
    )
    return np.mean(stats), np.std(stats), stats


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

    shape_alpha = st.sidebar.slider("Shape", min_value=0, max_value=SHAPE_MAX_VALUE_ALPHA, value=100)
    scale_lambda = st.sidebar.slider("SCALE", min_value=0, max_value=SHAPE_MAX_VALUE_ALPHA, value=100)
    


    # Log
    st.sidebar.subheader("LogNormal")

    # File uploader

    data = np.random.randn(data_size)

    num_samples = st.sidebar.slider(
        "Number of Samples/Bootstrap Samples",
        min_value=100,
        max_value=10000,
        value=1000,
    )
    alpha = st.sidebar.slider(
        "Alpha (Significance Level)", min_value=0.01, max_value=0.10, value=0.05
    )
    statistic_name = st.sidebar.selectbox(
        "Statistic", list(statistics_functions.keys())
    )
    statistic_func, statistic_desc = statistics_functions[statistic_name]

    # Perform bootstrapping
    mean_stat_boot, lower_ci_boot, upper_ci_boot, stats_boot = bootstrap(
        data, num_samples, statistic_func, alpha
    )

    # Perform repeated experiments
    mean_stat_repeated, std_stat_repeated, stats_repeated = repeated_experiments(
        data, num_samples, statistic_func
    )

    # Display results
    st.write("### Summary of Original Data")
    st.write(
        f"Count: {len(data)}, Mean: {np.mean(data)}, Std: {np.std(data)}, Min: {np.min(data)}, Max: {np.max(data)}"
    )

    st.write("### Bootstrapping Results")
    st.write(f"Bootstrap {statistic_name}: {mean_stat_boot}")
    st.write(
        f"{100*(1-alpha)}% Confidence Interval: [{lower_ci_boot}, {upper_ci_boot}]"
    )
    st.write("#### Description of the Statistic")
    st.write(statistic_desc)

    # Plot the bootstrap distribution using Plotly
    fig_boot = go.Figure()
    fig_boot.add_trace(
        go.Histogram(
            x=stats_boot, nbinsx=30, name="Bootstrap Samples", marker_color="blue"
        )
    )
    fig_boot.add_vline(
        x=mean_stat_boot, line=dict(color="red", dash="dash"), name="Mean"
    )
    fig_boot.add_vline(
        x=lower_ci_boot,
        line=dict(color="green", dash="dash"),
        name=f"{100*alpha/2}% CI",
    )
    fig_boot.add_vline(
        x=upper_ci_boot,
        line=dict(color="green", dash="dash"),
        name=f"{100*(1-alpha/2)}% CI",
    )
    fig_boot.update_layout(
        title=f"Bootstrap Distribution of {statistic_name}",
        xaxis_title=statistic_name,
        yaxis_title="Frequency",
        legend=dict(x=0.7, y=0.95),
        showlegend=True,
    )

    st.plotly_chart(fig_boot)

    st.write("### Repeated Experiments Results")
    st.write(f"Mean of Repeated Experiments: {mean_stat_repeated}")
    st.write(f"Standard Deviation of Repeated Experiments: {std_stat_repeated}")

    # Plot the distribution of repeated experiments using Plotly
    fig_repeated = go.Figure()
    fig_repeated.add_trace(
        go.Histogram(
            x=stats_repeated,
            nbinsx=30,
            name="Repeated Experiment Samples",
            marker_color="orange",
        )
    )
    fig_repeated.add_vline(
        x=mean_stat_repeated, line=dict(color="red", dash="dash"), name="Mean"
    )
    fig_repeated.add_vline(
        x=mean_stat_repeated - std_stat_repeated,
        line=dict(color="green", dash="dash"),
        name="Mean ± Std",
    )
    fig_repeated.add_vline(
        x=mean_stat_repeated + std_stat_repeated,
        line=dict(color="green", dash="dash"),
        name="Mean ± Std",
    )
    fig_repeated.update_layout(
        title=f"Distribution of Repeated Experiments for {statistic_name}",
        xaxis_title=statistic_name,
        yaxis_title="Frequency",
        legend=dict(x=0.7, y=0.95),
        showlegend=True,
    )

    st.plotly_chart(fig_repeated)


if __name__ == "__main__":
    main()
