from enum import Enum
from App.modules.event import Event, Event_type
from App.modules.thermoelectric import ThermoElectric, ThermoElectric_State
from App.modules.lognormal import LogNormal
import numpy as np


class Circuit_State(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class Circuit:
    def __init__(self, id: int, logNormal: LogNormal, days: int):
        self.id: int = id
        self.demand: list[float] = [logNormal.generate() for i in range(days + 1)]
        self.deficit_history: list[float] = np.zeros(days)
        self.total_deficit: float = 0
        self.days: int = days

    def get_demand(self, current_day):
        return self.demand[current_day]

    def get_remnant(self, current_day):
        return self.get_demand(current_day) - self.deficit_history[current_day]

    def disconnect(self, percentage: float, current_day: int):
        if self.get_remnant(current_day) <= 0:
            print(f"Apagon pip ip{self.id} en el dia {current_day}")
            return 0

        disconnected = 0
        to_disconnect = (
            self.get_demand(current_day) - self.get_demand(current_day) * percentage - self.deficit_history[current_day]
        )
        if to_disconnect >= 0:
            disconnected = self.get_demand(current_day) * percentage
        else:
            disconnected = self.get_remnant()
        self.deficit_history[current_day] += disconnected
        self.total_deficit += disconnected
        return disconnected

    def __str__(self):
        return f"Circuit {self.id} with demand {self.demand} and {self.days_disconnected} days disconnected"
