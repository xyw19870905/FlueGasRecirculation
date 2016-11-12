import cantera as ct
# 燃料量
B_j = 40.692        # t/h

# 燃料收到基成分
W_ar = 32.40        # 水分
A_ar = 13.66        # 灰分
C_ar = 26.72        # 碳
H_ar =  3.40        # 氢
O_ar = 23.33        # 氧
N_ar =  0.40        # 氮
S_ar =  0.09        # 硫
others = 0.00
fuel_index = "70%黄秆+30%灰秆，热输入111MW"

'''
# 燃料量
B_j = 35.683        # t/h

# 燃料收到基成分
W_ar = 30.80        # 水分
A_ar = 12.22        # 灰分
C_ar = 28.02        # 碳
H_ar =  3.48        # 氢
O_ar = 24.93        # 氧
N_ar =  0.44        # 氮
S_ar =  0.11        # 硫
others = 0.00
fuel_index = "90%黄秆+10%灰秆，热输入102.5MW"
'''
others = 100.0 - (W_ar+A_ar+C_ar+H_ar+O_ar+N_ar+S_ar)

if(abs(others)>0.1):
    print("Warning: The sum of all elements is not 100%, remaining %5.2f." % others)

V0 = 0.0889*(C_ar+0.375*S_ar)+0.265*H_ar-0.0333*O_ar    # 理论空气量, Nm^3/kg

V_CO2 = 1.866*C_ar/100.0        # 烟气中二氧化碳, Nm^3/kg
V_SO2 = 1.866*0.375*S_ar/100.0  # 烟气中二氧化硫, Nm^3/kg
V_H2O = 11.1*H_ar/100.0 + 1.24*W_ar/100.0 + 0.0161*V0      # 烟气中水蒸气, Nm^3/kg
V_N2 = 0.79*V0 + 0.8*N_ar/100.0     # 烟气中氮气, Nm^3/kg

V_ylg = V_SO2+V_CO2+V_N2        # 理论干烟气容积, Nm^3/kg
V_yl = V_ylg+V_H2O              # 理论烟气容积, Nm^3/kg

alpha = 1.15            # 过量空气系数
V_yr = V_yl + (alpha-1)*V0 + 0.0161*(alpha-1)*V0     # 实际烟气容积, Nm^3/kg
V_yrg = V_yr - V_H2O                                # 实际干烟气容积, Nm^3/kg

Q_y = B_j*1000*V_yr/3600        # 排烟量, Nm^3/s
Q_p = B_j*1000*V_yrg/3600       # 排烟量（干态）, Nm^3/s

# 湿烟气占比（体积分数），忽略二氧化硫
Y_CO2 = V_CO2/V_yr
Y_H2O = (V_H2O+0.0161*(alpha-1)*V0)/V_yr
Y_O2 = 0.21*(alpha-1)*V0/V_yr
Y_N2 = 1 - (Y_CO2+Y_H2O+Y_O2)

# 输出到文件
f = open('flue_gas', 'w')
f.write("CO2:%.4f, H2O:%.4f, O2:%.4f, N2:%.4f" % (Y_CO2, Y_H2O, Y_O2, Y_N2))
f.close()

# 再循环烟气信息 by Cantera
gas = ct.Solution('gri30.xml')

gas.TPX = 120+273.15, ct.one_atm, "CO2:%.4f, H2O:%.4f, O2:%.4f, N2:%.4f" % (Y_CO2, Y_H2O, Y_O2, Y_N2)

# 输出结果
print("%s" % fuel_index)
print("过量空气系数：%5.2f" % alpha)
print("烟气量：%10.2f Nm^3/h" % (Q_y*3600))
print("\n\n烟气成分：")
print("-----------------------------------------------------")
print("{0:>10s} {1:>18s} {2:>18s}".format("species", "Vol Fraction", "Mass Fraction"))
print("{0:>10s} {1:>18.4f} {2:>18.4f}".format("CO2", Y_CO2, gas.mass_fraction_dict()['CO2']))
print("{0:>10s} {1:>18.4f} {2:>18.4f}".format("H2O", Y_H2O, gas.mass_fraction_dict()['H2O']))
print("{0:>10s} {1:>18.4f} {2:>18.4f}".format("O2", Y_O2, gas.mass_fraction_dict()['O2']))
print("{0:>10s} {1:>18.4f} {2:>18.4f}".format("N2", Y_N2, gas.mass_fraction_dict()['N2']))
print("-----------------------------------------------------")
print("密度：%.4f kg/m^3" % gas.density)

gas.TP = 273.15, ct.one_atm
print("密度：%.4f kg/Nm^3" % gas.density)
