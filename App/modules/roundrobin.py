import sys
from enum import Enum
import matplotlib.pyplot as plt
from App.modules.event import Event, Event_type
from App.modules.weibull import Weibull
from App.modules.lognormal import LogNormal
import plotly.graph_objects as go

class RoundRobin:
    def __init__(self):
        self.current = 0

    def next(self):
        self.current += 1
        return (self.current)