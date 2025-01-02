import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Mendefinisikan variabel input dan output
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')

# Mendefinisikan fungsi keanggotaan untuk variabel input dan output
temperature['cold'] = fuzz.membership.trimf(temperature.universe, [0, 10, 20])
temperature['comfortable'] = fuzz.membership.trimf(temperature.universe, [15, 25, 35])
temperature['hot'] = fuzz.membership.trimf(temperature.universe, [30, 40, 40])

humidity['dry'] = fuzz.membership.trimf(humidity.universe, [0, 30, 60])
humidity['comfortable'] = fuzz.membership.trimf(humidity.universe, [40, 60, 80])
humidity['humid'] = fuzz.membership.trimf(humidity.universe, [60, 90, 100])

fan_speed['low'] = fuzz.membership.trimf(fan_speed.universe, [0, 30, 60])
fan_speed['medium'] = fuzz.membership.trimf(fan_speed.universe, [40, 60, 80])
fan_speed['high'] = fuzz.membership.trimf(fan_speed.universe, [60, 90, 100])

# Mendefinisikan aturan fuzzy
rule1 = ctrl.Rule(temperature['cold'] & humidity['dry'], fan_speed['low'])
rule2 = ctrl.Rule(temperature['cold'] & humidity['comfortable'], fan_speed['low'])
rule3 = ctrl.Rule(temperature['cold'] & humidity['humid'], fan_speed['medium'])
rule4 = ctrl.Rule(temperature['comfortable'] & humidity['dry'], fan_speed['low'])
rule5 = ctrl.Rule(temperature['comfortable'] & humidity['comfortable'], fan_speed['medium'])
rule6 = ctrl.Rule(temperature['comfortable'] & humidity['humid'], fan_speed['medium'])
rule7 = ctrl.Rule(temperature['hot'] & humidity['dry'], fan_speed['medium'])
rule8 = ctrl.Rule(temperature['hot'] & humidity['comfortable'], fan_speed['high'])
rule9 = ctrl.Rule(temperature['hot'] & humidity['humid'], fan_speed['high'])

# Membuat sistem fuzzy
ac_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
ac = ctrl.ControlSystemSimulation(ac_ctrl)

# Meminta input dari pengguna
temperature_input = float(input("Masukkan suhu ruangan (°C): "))
humidity_input = float(input("Masukkan kelembapan (%): "))

# Menguji sistem fuzzy
ac.input['temperature'] = temperature_input
ac.input['humidity'] = humidity_input
ac.compute()
print("Kecepatan Kipas AC:", ac.output['fan_speed'])