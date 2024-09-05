import App.modules.thermoelectric as thermoelectricClass
import App.modules.circuit as circuitClass
import App.modules.agents as agentsClass
import App.modules.weibull as weibullClass
import App.modules.lognormal as lognormalClass
import App.modules.roundrobin as roundRobinClass
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


def create_circuits(
    circuits_amount, days, min_mean, max_mean, min_deviation, max_deviation
):
    circuits = []
    for i in range(circuits_amount):
        demand = lognormalClass.LogNormal(
            rnd.uniform(min_mean, max_mean), rnd.uniform(min_deviation, max_deviation)
        )
        c = circuitClass.Circuit(i, demand, days)
        circuits.append(c)

    return circuits


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
) -> list[thermoelectricClass.ThermoElectric]:
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
    circuits: list[circuitClass.Circuit] = None,
    stored_energy=0,
    rotation=roundRobinClass.RoundRobin(),
):
    """returns working_thermoelectrics, defict per day, stored energy, circuits"""

    working_thermoelectrics = []

    working_thermoelectrics.append(np.ones(len(thermoelectrics)))

    deficit_per_day = []

    deficit_per_day.append(0)

    stored_energy_per_day = []

    stored_energy_per_day.append(0)

    event_date, event_thermoelectric = get_next_general_event(thermoelectrics, days, 0)

    for current_day in range(0, days):
        total_demand = 0

        if circuits is not None:
            total_demand = sum([c.get_demand(current_day) for c in circuits])

        if agent is not None:
            agent.Manage_Thermoelectrics(
                current_day, stored_energy, circuits, thermoelectrics, rotation
            )

        while event_thermoelectric != None and np.floor(event_date) == current_day:

            event_thermoelectric.pop_next_future_event()

            event_date, event_thermoelectric = get_next_general_event(
                thermoelectrics, days, current_day
            )

        thermoelectrics_state = [t.is_working() for t in thermoelectrics]

        working_thermoelectrics.append(thermoelectrics_state)

        if circuits is not None:

            if agent is not None:

                agent.Manage_Circuits(
                    current_day, stored_energy, circuits, thermoelectrics, rotation
                )

            total_offer = (
                sum([x.offer for x in thermoelectrics if x.is_working()])
                + stored_energy_per_day[-1]
            )

            deficit_today = max(total_demand - total_offer, 0)

            deficit_per_day.append(deficit_today)

            stored_energy = max(total_offer - total_demand, 0)

            stored_energy_per_day.append(stored_energy)

    return working_thermoelectrics, deficit_per_day, stored_energy_per_day, circuits


def get_deficit_and_stored_energy(
    circuits: list[circuitClass.Circuit],
    thermoelectrics: list[thermoelectricClass.ThermoElectric],
    stored_energy,
    current_day,
):
    total_demand = sum([x.get_demand(current_day) for x in circuits])
    total_offer = (
        sum([x.offer for x in thermoelectrics if x.is_working()]) + stored_energy
    )
    return (
        (total_demand - total_offer, 0)
        if total_demand > total_offer
        else (0, total_offer - total_demand)
    )


# Calculates the average working time of the thermoelectrics


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
    thermoelectrics_amount,
    k,
    agent,
    circuits_amount,
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
    c_min_mean,
    c_max_mean,
    c_min_deviation,
    c_max_deviation,
):
    """returns working day average, thermoelectics average by day, deficit average by day, stored energy by day"""
    sum_time = 0
    intervals = 0

    average_active_thermoelectric = 0
    average_deficit = 0
    average_stored_energy = 0

    total_working_thermoelectrics_per_day = np.zeros(days + 1)
    total_deficit_per_day = np.zeros(days + 1)
    total_stored_energy_per_day = np.zeros(days + 1)

    for i in range(k):
        thermoelectrics = prepare_data_thermoelectrics(
            days,
            thermoelectrics_amount,
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
        circuits = (
            None
            if circuits_amount <= 0
            else create_circuits(
                circuits_amount,
                days,
                c_min_mean,
                c_max_mean,
                c_min_deviation,
                c_max_deviation,
            )
        )
        (
            thermoelectrics_state,
            deficit_per_day,
            stored_energy_per_day,
            circuits_result,
        ) = simulate(thermoelectrics, days, agent, circuits)
        (
            partial_sum_working_thermoelectrics,
            partial_intervals_working_thermoelectrics,
        ) = average_worktime(thermoelectrics_state, days, thermoelectrics_amount)

        sum_time += partial_sum_working_thermoelectrics
        intervals += partial_intervals_working_thermoelectrics

        number_of_working_thermoelectrics_current_simulation = [
            sum(x) for x in thermoelectrics_state
        ]

        total_working_thermoelectrics_per_day += np.array(
            number_of_working_thermoelectrics_current_simulation
        )
        total_deficit_per_day += np.array(deficit_per_day)
        total_stored_energy_per_day += np.array(stored_energy_per_day)

        average_active_thermoelectric += sum(
            number_of_working_thermoelectrics_current_simulation
        )
        average_deficit += sum(deficit_per_day)
        average_stored_energy += sum(stored_energy_per_day)

    working_average = sum_time / intervals if intervals != 0 else 0
    total_working_thermoelectrics_per_day /= k
    total_deficit_per_day /= k
    total_stored_energy_per_day /= k

    average_active_thermoelectric /= k * days
    average_deficit /= k * days
    average_stored_energy /= k * days

    return (
        working_average,
        total_working_thermoelectrics_per_day,
        total_deficit_per_day,
        total_stored_energy_per_day,
        average_active_thermoelectric,
        average_deficit,
        average_stored_energy,
    )
        

# A function for disconnecting circuits rotating through them and disconnecting 0.25 of the demand while there is still deficit
def disconnect_circuit_heuristic(
    current_day,
    stored_energy,
    circuits: list[circuitClass.Circuit],
    thermoelectrics: list[thermoelectricClass.ThermoElectric],
    rotation=roundRobinClass.RoundRobin(),
):
    deficit, stored_energy = get_deficit_and_stored_energy(
        circuits, thermoelectrics, stored_energy, current_day
    )

    while deficit - 1e-8 > 0:
        circuit = rotation.next(circuits)
        deficit -= circuit.disconnect(0.25, current_day)


def empty_func(arg0, arg1, arg2, arg3, rg4):
    pass
