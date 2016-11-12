import cantera as ct

mass_air = 36.96*0.13
mass_gas = 0.52*6

gas_a = ct.Solution('air.xml')
gas_a.TPX = 318.0, ct.one_atm, 'O2:0.21, N2:0.79'
rho_a = gas_a.density

f = open('flue_gas', 'r')
species = f.readlines()
species = species[0].strip()
f.close()


gas_b = ct.Solution('gri30.xml')
gas_b.TPX = 393.0, ct.one_atm, species
rho_b = gas_b.density

res_a = ct.Reservoir(gas_a)
res_b = ct.Reservoir(gas_b)
downstream = ct.Reservoir(gas_b)

mixer = ct.IdealGasReactor(gas_b)

mfc1 = ct.MassFlowController(res_a, mixer, mdot=mass_air)
mfc2 = ct.MassFlowController(res_b, mixer, mdot=mass_gas)

outlet = ct.Valve(mixer, downstream, K=10.0)

sim = ct.ReactorNet([mixer])

t = 0.0
for n in range(30):
    tres = mixer.mass/(mfc1.mdot(t) + mfc2.mdot(t))
    t += 0.5*tres
    sim.advance(t)


gas = ct.Solution('gri30.xml')
gas.TPY = mixer.T, ct.one_atm, mixer.Y

print("混合气成分：")
print("温度：%.1f" % gas.T)
print("质量流量：%.2f kg/s" % (mass_air+mass_gas))
print("-----------------------------------------------------")
print("{0:>10s} {1:>18s} {2:>18s}".format("species", "Vol Fraction", "Mass Fraction"))
print("{0:>10s} {1:>18.4f} {2:>18.4f}".format("CO2", gas.mole_fraction_dict()['CO2'], gas.mass_fraction_dict()['CO2']))
print("{0:>10s} {1:>18.4f} {2:>18.4f}".format("H2O", gas.mole_fraction_dict()['H2O'], gas.mass_fraction_dict()['H2O']))
print("{0:>10s} {1:>18.4f} {2:>18.4f}".format("O2", gas.mole_fraction_dict()['O2'], gas.mass_fraction_dict()['O2']))
print("{0:>10s} {1:>18.4f} {2:>18.4f}".format("N2", gas.mole_fraction_dict()['N2'], gas.mass_fraction_dict()['N2']))
print("-----------------------------------------------------")
print("密度：%.4f kg/m^3" % gas.density)

gas.TP = 273.15, ct.one_atm
print("密度：%.4f kg/Nm^3" % gas.density)
