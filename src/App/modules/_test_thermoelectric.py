import weibull, lognormal, thermoelectric

w1 = weibull.Weibull(lambd=2, alpha=1)
ln1 = lognormal.LogNormal(1, 2)

th1 = thermoelectric.ThermoElectric(offer=0, weibull=w1, logNormal=ln1)

th1.get_distributions_info()
th1.planificate_events(100)
print(th1.get_state())
th1.print_future_events()
print(th1.history)
print(th1.get_next_future_event_day())

th1.repair_and_replanificate(100)
print(th1.get_state())
print(th1.history)

th1.get_history()
th1.get_state()
th1.get_next_future_event_day()

th1.plot(0, 100)
