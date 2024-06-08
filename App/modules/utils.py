import thermoelectric

def get_total_offer(thermoelectrics: "list[thermoelectric.ThermoElectric]"):
    offer = 0
    for thermoelectric in thermoelectrics:
        if thermoelectric.is_working():
            offer += thermoelectric.offer
    return offer


