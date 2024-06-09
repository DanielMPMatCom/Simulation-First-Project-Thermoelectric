from enum import Enum
from App.modules.event import Event, Event_type
from App.modules.thermoelectric import ThermoElectric, ThermoElectric_State
import numpy as np


class Circuit_State(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class Circuit:
    def __init__(self, id: int, demand: float, days: int):
        self.id: int = id
        self.demand: float = demand
        self.deficit_history: list[float] = np.zeros(days)
        self.total_deficit: float = 0
        self.days: int = days

    def disconnect(self, percentage: float, current_day: int):
        # print(f"Disconnecting {self.demand * percentage} from circuit {self.id} on day {current_day}")
        self.total_deficit += self.demand * percentage
        self.deficit_history[current_day] += self.demand * percentage

    def __str__(self):
        return f"Circuit {self.id} with demand {self.demand} and {self.days_disconnected} days disconnected"
