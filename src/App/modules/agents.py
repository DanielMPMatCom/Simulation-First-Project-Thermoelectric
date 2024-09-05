import random as rnd


# class Operator:
#     def __init__(self, options: "list[function]") -> None:  # funtions/0
#         self.options = options

#     def decision(self, thermoElectrics, circuits):
#         pass


# class Random_Operator(Operator):
#     def __init__(self, options) -> None:
#         Operator.__init__(options)

#     def decision(self, thermoElectrics, circuits):
#         choice = rnd.randint(0, len(self.options) - 1)
#         return self.options[choice]()\

class Agent:

    def __init__(self, thermoelectric_func, circuit_func):
        self.Manage_Thermoelectrics = thermoelectric_func
        self.Manage_Circuits = circuit_func


          

