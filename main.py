import streamlit as st
import numpy as np
import plotly.graph_objects as go
import App.modules.thermoelectric as thermoelectricClass
import App.modules.weibull as weibullClass
import App.modules.lognormal as lognormalClass
import App.modules.agents as agentsClass
import random as rnd
import main_utils as utils
import copy

SCALA_MIN_VALUE_ALPHA = 0
SCALA_MAX_VALUE_ALPHA = 100

SHAPE_MIN_VALUE_LAMBDA = 0
SHAPE_MAX_VALUE_LAMBDA = 100

MEAN_MAX_VALUE_MU = 100
DEVIATION_MAX_VALUE_SIGMA = 100

DAYS_MAX_VALUE = 800
THERMOELECTRICS_MAX_VALUE = 100

OFFER_MAX_VALUE = 1000
DEMAND_MAX_VALUE = 1000

# Streamlit app

# utils


def main():
    st.title("Thermoelectric Simulation ")

    # Sidebar inputs
    st.sidebar.header("Configuration")

    # K-Simulations
    st.sidebar.subheader("K-Simulations")
    number_of_simulations = st.sidebar.slider(
        "Number of Simulations for Heuristic Strategy",
        min_value=0,
        max_value=500,
        value=200,
    )

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

    min_scala_alpha = st.sidebar.slider(
        "Min Scala(alpha)",
        min_value=0.0,
        max_value=float(SCALA_MIN_VALUE_ALPHA),
        value=float(40),
    )

    max_scala_alpha = st.sidebar.slider(
        "Max Scala(alpha)",
        min_value=float(0),
        max_value=float(SCALA_MAX_VALUE_ALPHA),
        value=float(70),
    )

    min_shape_lambda = st.sidebar.slider(
        "Min Shape(lambda)", min_value=0, max_value=SHAPE_MIN_VALUE_LAMBDA, value=1
    )

    max_shape_lambda = st.sidebar.slider(
        "Max Shape(lambda)",
        min_value=float(0),
        max_value=float(SHAPE_MAX_VALUE_LAMBDA),
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
    st.subheader("Plot at least first three thermoelectric events")
    my_thermoelectrics: list[thermoelectricClass.ThermoElectric] = (
        utils.prepare_data_thermoelectrics(
            days,
            thermoelectrics,
            min_scala_alpha,
            max_scala_alpha,
            min_shape_lambda,
            max_shape_lambda,
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
    for i in range(min(thermoelectrics, 3)):
        st.write(f"***Thermoelectric {i+1}***")
        st.write(my_thermoelectrics[i].get_distributions_info())
        st.write("`Plot State 1: Working, 0: Broken`")
        fig = my_thermoelectrics[i].plot(0, days, show=False)
        st.plotly_chart(fig)

    st.header(f"Thermoelectric Simulation for {days} days")
    tmp = copy.deepcopy(my_thermoelectrics)
    working_thermoelectrics = utils.simulate(tmp, days)
    working_thermoelectrics = [sum(x) for x in working_thermoelectrics]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(range(days)),
            y=working_thermoelectrics,
            mode="lines",
            name="Working Thermoelectrics",
        )
    )
    fig.update_layout(
        title="Working Thermoelectrics",
        xaxis_title="Days",
        yaxis_title="Working Thermoelectrics",
    )
    st.plotly_chart(fig)

    # K simulation
    st.header("Select best thermoelectric maintenance strategy")

    tmp = copy.deepcopy(my_thermoelectrics)
    average = utils.k_simulation(
        days,
        thermoelectrics,
        min_scala_alpha,
        max_scala_alpha,
        min_shape_lambda,
        max_shape_lambda,
        min_mean_mu,
        max_mean_mu,
        min_deviation_sigma,
        max_deviation_sigma,
        min_offer,
        max_offer,
        min_demand,
        max_demand,
        number_of_simulations,
    )

    def give_mantainance_heuristic(current_day):
        for thermoelectric in tmp:
            if not thermoelectric.is_working():
                continue
            last_repair = thermoelectric.get_last_repair_day()
            if current_day - last_repair >= average:
                thermoelectric.repair_and_replanificate(
                    current_day,
                    days,
                    lognormalClass.LogNormal(
                        rnd.uniform(1.5, 2), rnd.uniform(0.2, 0.4)
                    ),
                )

    def empty_func(current_day):
        pass

    working_thermoelectrics = utils.simulate(
        tmp, days, agentsClass.Agent(give_mantainance_heuristic, empty_func)
    )

    working_thermoelectrics = [sum(x) for x in working_thermoelectrics]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(range(days)),
            y=working_thermoelectrics,
            mode="lines",
            name="Working Thermoelectrics",
        )
    )
    fig.update_layout(
        title="Working Thermoelectrics",
        xaxis_title="Days",
        yaxis_title="Working Thermoelectrics",
    )
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
