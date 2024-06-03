import random
import math

def weibull(a, b):
    return random.weibullvariate(a, b)

def log_normal(a, b):
    return random.lognormvariate(a, b)

def break_thermoelectric(broken, i, t, N, a=1, b=1):
    break_time = t + math.floor(weibull(a, b))

    if break_time > N:
        print("Thermoelectric " + str(i) + " does not break again before simulation end")
    else:
        print("Thermoelectric " + str(i) + " out of service on day " + str(break_time))
        broken[break_time].append(i)

def repair_thermoelectric(repaired, i, t, N, a=1, b=1):
    repair_time = t + math.floor(log_normal(a, b))

    if repair_time > N:
        print("Thermoelectric " + str(i) + " is not fixed again before simulation end")
    else:
        print("Thermoelectric " + str(i) + " re-enter service on day " + str(repair_time))
        repaired[repair_time].append(i) 