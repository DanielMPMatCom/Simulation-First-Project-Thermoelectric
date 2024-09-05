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
CIRCUITS_MAX_VALUE = 1000

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

    st.sidebar.subheader("Circuits")

    circuits = st.sidebar.slider(
        "Circuits Amount",
        min_value=0,
        max_value=CIRCUITS_MAX_VALUE,
        value=115,
    )

    st.sidebar.subheader("LogNormal")

    circuits_min_mean_mu = st.sidebar.slider(
        "Min Mean(mu) Circuits",
        min_value=0.0,
        max_value=float(MEAN_MAX_VALUE_MU),
        value=float(2),
    )
    circuits_max_mean_mu = st.sidebar.slider(
        "Max Mean(mu) Circuits",
        min_value=float(0),
        max_value=float(MEAN_MAX_VALUE_MU),
        value=2.5,
    )
    circuits_min_deviation_sigma = st.sidebar.slider(
        "Min Deviation Circuits",
        min_value=0.0,
        max_value=float(DEVIATION_MAX_VALUE_SIGMA),
        value=0.2,
    )
    circuits_max_deviation_sigma = st.sidebar.slider(
        "Max Deviation Circuits",
        min_value=0.0,
        max_value=float(DEVIATION_MAX_VALUE_SIGMA),
        value=0.4,
    )

    # ThermoElectrics
    st.sidebar.subheader("ThermoElectrics")

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
    st.title("First Experiment: Thermoelectric Events")
    st.subheader("Plot at least first three thermoelectric events")
    st.write("Thermoelectric events")
    st.write("1 Means Thermoelectric is working, 0 means is break")

    # Create thermoelectrics

    generated_thermoelectrics = utils.prepare_data_thermoelectrics(
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
    )

    fig = go.Figure()
    for i in range(3):
        fig = generated_thermoelectrics[i].plot(0, days, False)
        st.plotly_chart(fig)

    # Create circuits
    generated_circuits = utils.create_circuits(
        circuits,
        days,
        circuits_min_mean_mu,
        circuits_max_mean_mu,
        circuits_min_deviation_sigma,
        circuits_max_deviation_sigma,
    )

    # Running simulation

    simulations_initial_stored_energy = st.sidebar.slider(
        "Initial Stored Energy",
        min_value=0,
        max_value=DAYS_MAX_VALUE,
        value=0,
    )

    first_example_th = copy.deepcopy(generated_thermoelectrics)
    first_example_c = copy.deepcopy(generated_circuits)

    (
        working_thermoelectrics_without_strategy,
        deficit_per_day_without_strategy,
        stored_energy_without_strategy,
        circuits_without_strategy,
    ) = utils.simulate(
        first_example_th,
        days,
        circuits=first_example_c,
        stored_energy=simulations_initial_stored_energy,
    )

    working_thermoelectrics_without_strategy = [
        sum(x) for x in working_thermoelectrics_without_strategy
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(range(0, days)),
            y=working_thermoelectrics_without_strategy,
            mode="lines",
        )
    )

    fig.update_layout(
        title="Working thermoelectrics per day",
        xaxis_title="Days",
        yaxis_title="Working thermoelectrics",
    )

    st.plotly_chart(fig)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(range(0, days)),
            y=stored_energy_without_strategy,
            mode="lines",
            name="Stored Energy",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=list(range(0, days)),
            y=deficit_per_day_without_strategy,
            mode="lines",
            name="Deficit",
        )
    )

    fig.update_layout(
        title="Energy per day",
        xaxis_title="Days",
        yaxis_title="Energy",
    )

    st.plotly_chart(fig)

    # 2nd Experiment
    st.write("Second Experiment: Maintenance Strategy")
    st.write("Generating some strategy to manage the thermoelectrics")
    second_example_th = copy.deepcopy(generated_thermoelectrics)
    second_example_c = copy.deepcopy(generated_circuits)

    st.write("Find the mean of active days of thermoelectrics in K simulations")
    k = st.slider("K-simulations", min_value=0, max_value=100, value=10)

    average, _, _, _, _, _, _ = utils.k_simulation(
        days,
        thermoelectrics,
        k,
        None,
        circuits,
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
        circuits_min_mean_mu,
        circuits_max_mean_mu,
        circuits_min_deviation_sigma,
        circuits_max_deviation_sigma,
    )

    def decorator_context_give_maintenance():

        def give_maintenance_heuristic(
            current_day,
            stored_energy,
            circuits,
            thermoelectrics: "list[thermoelectricClass.ThermoElectric]",
            rotation,
        ):
            if stored_energy <= 1e-8:
                return

            if (
                sum(
                    [
                        thermoelectric.is_on_maintenance()
                        for thermoelectric in thermoelectrics
                    ]
                )
                >= 1
            ):
                return

            for thermoelectric in thermoelectrics:

                if not thermoelectric.is_working():
                    continue
                last_repair = thermoelectric.get_last_repair_day()
                if current_day - last_repair >= average:
                    thermoelectric.repair_and_replanificate(
                        current_day,
                        days,
                        lognormalClass.LogNormal(
                            rnd.uniform(min_mean_mu, max_mean_mu),
                            rnd.uniform(min_deviation_sigma, max_deviation_sigma),
                        ),
                    )
                    maintainance_thermoelectric = thermoelectric
                    return

        return give_maintenance_heuristic

    # Running simulation with agent and Maintenance heuristic
    (
        working_thermoelectrics_maintenance_heuristic,
        deficit_per_day_maintenance_heuristic,
        stored_per_day_maintenance_heuristic,
        circuits_maintenance_heuristic,
    ) = utils.simulate(
        second_example_th,
        days,
        agentsClass.Agent(
            decorator_context_give_maintenance(),
            utils.empty_func,
        ),
        second_example_c,
        simulations_initial_stored_energy,
    )

    working_thermoelectrics_maintenance_heuristic = [
        sum(x) for x in working_thermoelectrics_maintenance_heuristic
    ]

    fig_maintenance_heuristic = go.Figure()
    fig_maintenance_heuristic.add_trace(
        go.Scatter(
            x=list(range(0, days)),
            y=working_thermoelectrics_maintenance_heuristic,
            mode="lines",
        )
    )
    fig_maintenance_heuristic.update_layout(
        title="Maintenance heuristic",
        xaxis_title="Days",
        yaxis_title="Working thermoelectrics",
    )

    st.plotly_chart(fig_maintenance_heuristic)

    fig_energy_deficit_and_stored_maintenance_heuristic = go.Figure()

    fig_energy_deficit_and_stored_maintenance_heuristic.add_trace(
        go.Scatter(
            x=list(range(0, days)),
            y=stored_per_day_maintenance_heuristic,
            name="Stored Energy",
        )
    )

    fig_energy_deficit_and_stored_maintenance_heuristic.add_trace(
        go.Scatter(
            x=list(range(0, days)),
            y=deficit_per_day_maintenance_heuristic,
            name="Deficit Energy",
        )
    )

    fig_energy_deficit_and_stored_maintenance_heuristic.update_layout(
        title="Energy per day",
        xaxis_title="Days",
        yaxis_title="Energy",
        legend=dict(x=0.7, y=0.95),
        showlegend=True,
    )
    st.plotly_chart(fig_energy_deficit_and_stored_maintenance_heuristic)

    # 3rd Experiment
    st.title("Third Experiment : Circuit Management")
    st.write("Strategy to manage the circuits")
    st.write(
        "Using round robin to shut down a percentage of a circuit to cover the deficit"
    )

    third_example_th = copy.deepcopy(generated_thermoelectrics)
    third_example_c = copy.deepcopy(generated_circuits)

    # Running simulation with both strategies
    (
        working_thermoelectrics_both_heuristic,
        deficit_per_day_both_heuristic,
        stored_energy_per_day_both_heuristic,
        circuits_result,
    ) = utils.simulate(
        third_example_th,
        days,
        agentsClass.Agent(
            decorator_context_give_maintenance(),
            utils.disconnect_circuit_heuristic,
        ),
        third_example_c,
        simulations_initial_stored_energy,
    )

    total_deficit_by_circuit = [x.total_deficit for x in circuits_result]
    demand_by_circuit = [sum(x.demand) / len(x.demand) for x in circuits_result]
    x = list(range(len(total_deficit_by_circuit)))

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=x,
            y=total_deficit_by_circuit,
        )
    )

    fig.update_layout(
        title="Total Deficit per Circuit",
        xaxis_title="Circuit ID",
        yaxis_title="Deficit",
    )

    st.plotly_chart(fig)

    fig = go.Figure()

    fig.add_trace(go.Bar(x=x, y=demand_by_circuit))
    fig.update_layout(
        title="Total Demand per Circuit",
        xaxis_title="Circuit ID",
        yaxis_title="Demand",
    )

    st.plotly_chart(fig)

    # Plotting some circuits' deficits
    st.write("Plotting some circuits' deficits")
    for c in circuits_result[:10]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(days)), y=c.deficit_history))
        fig.update_layout(
            title=f"Deficit per day in Circuit {c.id}",
            xaxis_title="Days",
            yaxis_title="Deficit",
        )
        st.plotly_chart(fig)

    # 4th Experiment
    st.title("Fourth Experiment: Maintenance VS Non Maintenance")
    st.write("Comparing the two strategies")

    list_of_days = list(range(0, days))
    fig_comparison_working_thermoelectrics = go.Figure()
    fig_comparison_working_thermoelectrics.add_trace(
        go.Scatter(
            x=list_of_days,
            y=working_thermoelectrics_maintenance_heuristic,
            mode="lines",
            name="Maintenance Strategy",
        )
    )

    fig_comparison_working_thermoelectrics.add_trace(
        go.Scatter(
            x=list_of_days,
            y=working_thermoelectrics_without_strategy,
            mode="lines",
            name="Without Maintenance Strategy",
        )
    )

    fig_comparison_energy = go.Figure()

    fig_comparison_energy.add_trace(
        go.Scatter(
            x=list_of_days,
            y=stored_per_day_maintenance_heuristic,
            mode="lines",
            name="Maintenance Strategy",
        )
    )

    fig_comparison_energy.add_trace(
        go.Scatter(
            x=list_of_days,
            y=stored_energy_without_strategy,
            mode="lines",
            name="Without Maintenance Strategy",
        )
    )

    fig_comparison_deficit = go.Figure()

    fig_comparison_deficit.add_trace(
        go.Scatter(
            x=list_of_days,
            y=deficit_per_day_maintenance_heuristic,
            mode="lines",
            name="Maintenance Strategy",
        )
    )

    fig_comparison_deficit.add_trace(
        go.Scatter(
            x=list_of_days,
            y=deficit_per_day_without_strategy,
            mode="lines",
            name="Without Maintenance Strategy",
        )
    )

    fig_comparison_working_thermoelectrics.update_layout(
        title="Working Thermoelectric per day",
        xaxis_title="Days",
        yaxis_title="Thermoeelctrics",
        legend=dict(x=0.7, y=0.95),
        showlegend=True,
    )

    fig_comparison_energy.update_layout(
        title="Stored Energy per day",
        xaxis_title="Days",
        yaxis_title="Energy",
        legend=dict(x=0.7, y=0.95),
        showlegend=True,
    )

    fig_comparison_deficit.update_layout(
        title="Deficit per day",
        xaxis_title="Days",
        yaxis_title="Energy",
        legend=dict(x=0.7, y=0.95),
        showlegend=True,
    )

    st.plotly_chart(fig_comparison_working_thermoelectrics)
    st.plotly_chart(fig_comparison_energy)
    st.plotly_chart(fig_comparison_deficit)

    #########################################################

    st.subheader("Repeat the experiments K-times")

    K_SIMULATIONS = st.slider(
        label="K-Simulations", min_value=1, max_value=1000, value=300
    )

    # non maintenance
    (
        _,
        non_maintenance_average_of_working_per_day,
        non_maintenance_average_deficit_per_day,
        non_maintenance_average_stored_energy_per_day,
        non_maintenance_average_of_working,
        non_maintenance_average_deficit,
        non_maintenance_average_stored_energy,
    ) = utils.k_simulation(
        days,
        thermoelectrics,
        K_SIMULATIONS,
        None,
        circuits,
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
        circuits_min_mean_mu,
        circuits_max_mean_mu,
        circuits_min_deviation_sigma,
        circuits_max_deviation_sigma,
    )

    # maintenance
    (
        _,
        maintenance_average_of_working_per_day,
        maintenance_average_deficit_per_day,
        maintenance_average_stored_energy_per_day,
        maintenance_average_of_working,
        maintenance_average_deficit,
        maintenance_average_stored_energy,
    ) = utils.k_simulation(
        days,
        thermoelectrics,
        K_SIMULATIONS,
        agentsClass.Agent(
            decorator_context_give_maintenance(),
            utils.disconnect_circuit_heuristic,
        ),
        circuits,
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
        circuits_min_mean_mu,
        circuits_max_mean_mu,
        circuits_min_deviation_sigma,
        circuits_max_deviation_sigma,
    )

    ## print stadistics in md format
    st.write("## Results")
    st.write("### Non Maintenance")
    st.write(
        f"""Average in {K_SIMULATIONS} simulations:
    Working Thermoelectrics: {non_maintenance_average_of_working}
    Deficit: {non_maintenance_average_deficit}
    Stored Energy: {non_maintenance_average_stored_energy}
    """
    )

    st.write("### Maintenance")
    st.write(
        f"""Average in {K_SIMULATIONS} simulations:
    Working Thermoelectrics: {maintenance_average_of_working}
    Deficit: {maintenance_average_deficit}
    Stored Energy: {maintenance_average_stored_energy}
    """
    )

    list_of_days = list(range(days))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list_of_days, y=maintenance_average_of_working_per_day, name="Maintenance"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=list_of_days,
            y=non_maintenance_average_of_working_per_day,
            name="Non Maintenance",
        )
    )

    fig.update_layout(
        title="Maintenance vs Non Maintenance: Day Average Working Thermoelectrics",
        xaxis_title="Days",
        yaxis_title="Working Thermoelectrics",
        legend=dict(x=0.7, y=0.95),
        showlegend=True,
    )

    st.plotly_chart(fig)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list_of_days, y=maintenance_average_deficit_per_day, name="Maintenance"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=list_of_days,
            y=non_maintenance_average_deficit_per_day,
            name="Non Maintenance",
        )
    )

    fig.update_layout(
        title="Maintenance vs Non Maintenance: Day Average Deficit",
        xaxis_title="Days",
        yaxis_title="Energy",
        legend=dict(x=0.7, y=0.95),
        showlegend=True,
    )

    st.plotly_chart(fig)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list_of_days,
            y=maintenance_average_stored_energy_per_day,
            name="Maintenance",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=list_of_days,
            y=non_maintenance_average_stored_energy_per_day,
            name="Non Maintenance",
        )
    )

    fig.update_layout(
        title="Maintenance vs Non Maintenance: Day Stored Energy",
        xaxis_title="Days",
        yaxis_title="Energy",
        legend=dict(x=0.7, y=0.95),
        showlegend=True,
    )

    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
