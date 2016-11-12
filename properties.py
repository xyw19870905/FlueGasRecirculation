import cantera as ct

gas = ct.Solution('gri30.xml')

species = 'CO2:0.1130, H2O:0.3057, O2:0.0293, N2:0.5520'

gas.TPX = 393.0, ct.one_atm, species

print(gas.report())

gas.TPX = 273.15, ct.one_atm, species

print(gas.report())
