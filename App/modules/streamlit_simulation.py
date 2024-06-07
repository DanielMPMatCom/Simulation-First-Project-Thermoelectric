# Description: This file contains the code to generate the Weibull and LogNormal distribution plots.
# Need fix: The code is not working as expected. The Weibull and LogNormal plots are not being displayed.

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import thermoelectric as thermoelectricClass
import weibull as weibullClass
import lognormal as lognormalClass
import random as rnd

SHAPE_MAX_VALUE_LAMBDA = 100
SCALA_MAX_VALUE_ALPHA = 100

MEAN_MAX_VALUE_MU = 100
DEVIATION_MAX_VALUE_SIGMA = 100

DAYS_MAX_VALUE = 800
THERMOELECTRICS_MAX_VALUE = 100

OFFER_MAX_VALUE = 1000
DEMAND_MAX_VALUE = 1000

# Streamlit app


def create_theroelectric(
    days,
    min_shape_alpha,
    max_shape_alpha,
    min_scale_lambda,
    max_scale_lambda,
    min_mean_mu,
    max_mean_mu,
    min_deviation_sigma,
    max_deviation_sigma,
    min_offer,
    max_offer,
):
    w = weibullClass.Weibull(
        rnd.uniform(min_scale_lambda, max_scale_lambda),
        rnd.uniform(min_shape_alpha, max_shape_alpha),
    )
    l = lognormalClass.LogNormal(
        rnd.uniform(min_mean_mu, max_mean_mu),
        rnd.uniform(min_deviation_sigma, max_deviation_sigma),
    )
    o = rnd.randrange(min_offer, max_offer)
    thermoelectric = thermoelectricClass.ThermoElectric(
        weibull=w,
        logNormal=l,
        offer=o,
    )
    thermoelectric.planificate_events(days=days)
    return thermoelectric


def prepare_data_thermoelectrics(
    days,
    thermoelectrics,
    min_shape_alpha,
    max_shape_alpha,
    min_scale_lambda,
    max_scale_lambda,
    min_mean_mu,
    max_mean_mu,
    min_deviation_sigma,
    max_deviation_sigma,
    min_offer,
    max_offer,
    min_demand,
    max_demand,
):
    simulations_thermoelectrics: list[thermoelectricClass.ThermoElectric] = []
    for _ in range(thermoelectrics):
        t = create_theroelectric(
            days,
            min_shape_alpha,
            max_shape_alpha,
            min_scale_lambda,
            max_scale_lambda,
            min_mean_mu,
            max_mean_mu,
            min_deviation_sigma,
            max_deviation_sigma,
            min_offer,
            max_offer,
        )
        simulations_thermoelectrics.append(t)
    return simulations_thermoelectrics


def main():
    st.title("Thermoelectric Simulation ")

    # Sidebar inputs
    st.sidebar.header("Configuration")

    # Days
    st.sidebar.subheader("Basic Configuration")

    days = st.sidebar.slider(
        "Days",
        min_value=0,
        max_value=DAYS_MAX_VALUE,
        value=365,
    )

    # ThermoElectrics
    thermoelectrics = st.sidebar.slider(
        "ThermoElectrics",
        min_value=0,
        max_value=THERMOELECTRICS_MAX_VALUE,
        value=50,
    )

    # offert
    min_offer = st.sidebar.slider(
        "Min Offer",
        min_value=0,
        max_value=OFFER_MAX_VALUE,
        value=365,
    )
    max_offer = st.sidebar.slider(
        "Max Offer",
        min_value=min_offer,
        max_value=OFFER_MAX_VALUE,
        value=OFFER_MAX_VALUE,
    )

    # demand
    min_demand = st.sidebar.slider(
        "Min Demand",
        min_value=0,
        max_value=OFFER_MAX_VALUE,
        value=OFFER_MAX_VALUE,
    )
    max_demand = st.sidebar.slider(
        "Max Demand",
        min_value=min_offer,
        max_value=DEMAND_MAX_VALUE,
        value=DEMAND_MAX_VALUE,
    )

    st.sidebar.subheader("Params Configuration")

    # Weibull
    st.sidebar.subheader("Weibull")

    min_shape_alpha = st.sidebar.slider(
        "Min Shape(alpha)",
        min_value=0.0,
        max_value=float(SHAPE_MAX_VALUE_LAMBDA),
        value=float(40),
    )

    max_shape_alpha = st.sidebar.slider(
        "Max Shape(alpha)",
        min_value=float(0),
        max_value=float(SHAPE_MAX_VALUE_LAMBDA),
        value=float(70),
    )

    min_scale_lambda = st.sidebar.slider(
        "Min Scale(scala)", min_value=0, max_value=SCALA_MAX_VALUE_ALPHA, value=1
    )

    max_scale_lambda = st.sidebar.slider(
        "Max Scale(scala)",
        min_value=float(0),
        max_value=float(SCALA_MAX_VALUE_ALPHA),
        value=3.0,
    )

    # LogNormal
    st.sidebar.subheader("LogNormal")
    min_mean_mu = st.sidebar.slider(
        "Min Mean(mu)",
        min_value=0.0,
        max_value=float(MEAN_MAX_VALUE_MU),
        value=float(2),
    )
    max_mean_mu = st.sidebar.slider(
        "Max Mean(mu)",
        min_value=float(0),
        max_value=float(MEAN_MAX_VALUE_MU),
        value=2.5,
    )
    min_deviation_sigma = st.sidebar.slider(
        "Min Deviation",
        min_value=0.0,
        max_value=float(DEVIATION_MAX_VALUE_SIGMA),
        value=0.2,
    )
    max_deviation_sigma = st.sidebar.slider(
        "Max Deviation",
        min_value=0.0,
        max_value=float(DEVIATION_MAX_VALUE_SIGMA),
        value=0.4,
    )

    # Display results
    st.subheader("Plot at least first five thermoelectric events")
    my_thermoelectrics: list[thermoelectricClass.ThermoElectric] = (
        prepare_data_thermoelectrics(
            days,
            thermoelectrics,
            min_shape_alpha,
            max_shape_alpha,
            min_scale_lambda,
            max_scale_lambda,
            min_mean_mu,
            max_mean_mu,
            min_deviation_sigma,
            max_deviation_sigma,
            min_offer,
            max_offer,
            min_demand,
            max_demand,
        )
    )
    for i in range(min(thermoelectrics, 5)):
        st.write(f"Thermoelectric {i+1}")
        fig, ax = my_thermoelectrics[i].plot(0, days)
        st.write(my_thermoelectrics[i].get_distributions_info())
        st.pyplot(fig)


if __name__ == "__main__":
    main()
