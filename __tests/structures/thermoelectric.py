import generator.lognormal
import generator.weibull
import structures.thermoelectric

w1 = generator.weibull.Weibull(5, 10)
ln1 = generator.lognormal.LogNormal(10, 3)

th1 = structures.thermoelectric.ThermoElectric(weibull=w1, logNormal=ln1)

th1.get_distributions_info()
th1.planificate_events(100)
th1.get_state()
th1.get_next_future_event_day()
th1.repair_and_replanificate(100)
th1.get_history()
th1.get_state()
th1.get_next_future_event_day()
th1.get_distributions_info()

th1.plot_thermoelectric()
