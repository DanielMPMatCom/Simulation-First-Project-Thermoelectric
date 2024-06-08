import App.modules.thermoelectric as thermoelectricClass
import App.modules.agents as agentsClass
import App.modules.weibull as weibullClass
import App.modules.lognormal as lognormalClass
import random as rnd
import numpy as np


def create_theroelectric(
    days,
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
):
    w = weibullClass.Weibull(
        rnd.uniform(min_scala_alpha, max_scala_alpha),
        rnd.uniform(min_shape_lambda, max_scala_alpha),
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
):
    simulations_thermoelectrics: list[thermoelectricClass.ThermoElectric] = []
    for _ in range(thermoelectrics):
        t = create_theroelectric(
            days,
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
        simulations_thermoelectrics.append(t)
    return simulations_thermoelectrics


def get_next_general_event(
    thermoelectrics_list: list[thermoelectricClass.ThermoElectric], days, current_day
):
    next_event = days
    next_thermoelectric = None
    for t in thermoelectrics_list:
        tmp = t.get_next_future_event_day()
        if tmp < next_event and tmp >= current_day:
            next_event = tmp
            next_thermoelectric = t
    return (next_event, next_thermoelectric)


def simulate(
    thermoelectrics: list[thermoelectricClass.ThermoElectric],
    days,
    agent: agentsClass.Agent = None,
):
    working_thermoelectrics = []
    working_thermoelectrics.append(np.ones(len(thermoelectrics)))

    event_date, event_thermoelectric = get_next_general_event(thermoelectrics, days, 0)

    for current_day in range(0, days):

        if agent is not None:
            agent.Manage_Thermoelectrics(current_day)

        while event_thermoelectric != None and np.floor(event_date) == current_day:
            event_thermoelectric.pop_next_future_event()
            event_date, event_thermoelectric = get_next_general_event(
                thermoelectrics, days, current_day
            )

        thermoelectrics_state = [t.is_working() for t in thermoelectrics]
        working_thermoelectrics.append(thermoelectrics_state)

        if agent is not None:
            agent.Manage_Circuits(current_day)

    return working_thermoelectrics


def average_worktime(planification, days, amount):

    total_sum = 0
    total_intervals = 0

    for i in range(amount):
        sum = 0
        for j in range(days):
            if planification[j][i]:
                sum += 1
            elif sum != 0:
                total_sum += sum
                total_intervals += 1
                sum = 0
        if sum != 0:
            total_sum += sum
            total_intervals += 1
            sum = 0
    return total_sum, total_intervals


def k_simulation(
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
):

    total_sum = 0
    intervals = 0

    for i in range(number_of_simulations):
        my_thermoelectrics = prepare_data_thermoelectrics(
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
        thermoelectrics_state = simulate(my_thermoelectrics, days)
        partial_sum, partial_intervals = average_worktime(
            thermoelectrics_state, days, thermoelectrics
        )
        total_sum += partial_sum
        intervals += partial_intervals

    return total_sum / intervals if intervals != 0 else 0
