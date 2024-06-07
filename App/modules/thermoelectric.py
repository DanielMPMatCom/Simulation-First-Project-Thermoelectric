import sys
from enum import Enum
from App.modules.event import Event, Event_type
import matplotlib.pyplot as plt
from App.modules.weibull import Weibull
from App.modules.lognormal import LogNormal

MAX_DAY = 1e9 + 5


class ThermoElectric_State(Enum):
    WORKING = "working"
    BREAK = "break"


class ThermoElectric:
    def __init__(self, offer, weibull: Weibull, logNormal: LogNormal):
        self.__future_events: list[Event] = []
        self.history: list[Event] = []
        self.offer = offer
        self.weibull = weibull
        self.logNormal = logNormal

    def print_future_events(self):
        for e in self.__future_events:
            print(e)

    def is_working(self) -> bool:
        if len(self.__future_events) <= 0:
            if len(self.history) <= 0:
                return True
            return self.history[-1].event_type == Event_type.REPAIR
        return self.__future_events[0].event_type == Event_type.BREAK

    def is_break(self) -> bool:
        return not self.is_working()

    def get_state(self) -> ThermoElectric_State:
        return (
            ThermoElectric_State.WORKING
            if self.is_working()
            else ThermoElectric_State.BREAK
        )

    def get_next_future_event_day(self) -> int:
        if len(self.__future_events) <= 0:
            return MAX_DAY
        return self.__future_events[0].event_day

    def pop_next_future_event(self) -> Event:
        if len(self.__future_events) <= 0:
            raise ValueError("There are no future events")
        event = self.__future_events.pop(0)
        self.history.append(event)
        return event

    def __generate_next_event(self, flip_flop: bool) -> Event:
        """if flip flop returns a Repair Event, Break Event in other case"""
        if flip_flop:
            return Event(Event_type.REPAIR, self.logNormal.generate())
        return Event(Event_type.BREAK, self.weibull.generate())

    def planificate_events(
        self, days: int, init_day=0, initial_state_flip_flop: bool = False
    ) -> None:

        flip_flop = initial_state_flip_flop
        event = self.__generate_next_event(flip_flop)
        event.event_day = init_day

        while event.event_day < days:
            self.__future_events.append(event)
            flip_flop = not flip_flop
            event = self.__generate_next_event(flip_flop)
            event.event_day += self.__future_events[-1].event_day

        return

    def repair_and_replanificate(self, init_day, days_to_replanificate) -> None:
        self.planificate_events(days_to_replanificate, init_day)
        return

    def get_history(self) -> "list[Event]":
        return self.history

    def get_distributions_info(self):
        print("Weibull Distribution:")
        print(f"Scale: {self.weibull.get_scale()}")
        print(f"Shape: {self.weibull.get_shape()}")

        print(f" - - - - - - - - - - - -")

        print("LogNormal Distribution:")
        print(f"Mean: {self.logNormal.get_mu()}")
        print(f"Des: {self.logNormal.get_sigma()}")
        return

    def plot(self, from_day=0, to_day=None):  # WARNING IN PROCESS
        images = []

        all_events: list[Event] = (
            self.history.extend(self.__future_events)
            if len(self.history) > 0
            else self.__future_events
        )

        to_day = all_events[-1].event_day if to_day is None else to_day

        if from_day > to_day:
            raise ValueError("from day must be lower equal then to_day")

        last_day = from_day

        for event in all_events:
            if event.event_day < from_day:
                continue
            if event.event_day > to_day:
                break
            value = 1 if event.event_type == Event_type.BREAK else 0
            images.extend([value] * int(event.event_day - last_day))
            last_day = event.event_day

        print(len(images))
        print(images)
        plt.plot(images)
        plt.ylabel("State")
        plt.xlabel("Day")
        plt.show()
