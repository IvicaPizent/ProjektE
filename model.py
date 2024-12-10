import os
import csv
import random
import matplotlib.pyplot as plt
from datetime import datetime as dt

# putanja do tablice proizvedene energije na Sunčanoj elektrani Stankovci
path = os.getcwd() + ('\Timeseries_43.907_15.695_SA3_2500kWp_crystSi_14_v55deg_2023_2023.csv')

# putanja do tablice satnih cijena
path2 = os.getcwd() + ('\Day-ahead Prices_202301010000-202401010000.csv')

# putanja do tablice stanja tržišta
path3 = os.getcwd() + ('\Imbalance_202301010000-202401010000.csv')

# odstupanje u postotku
odstupanje = 0

# satne cijene EUR/MWh
cijene_h = []

# mjesečne cijene
cijene_m = {}

# zarada
zarada = 0

# snaga
power = []

# preljev snage
power_of = 0

# mjesečna snaga
power_m = {}

# godišnja snaga
power_y = 0

# stanje tržišta
stanje = []

with open(path, mode='r') as file:
	reader = csv.DictReader(file)

	for row in reader:
		if row["P"] != '':
			power.append((dt.strptime(row["time"], '%Y%m%d:%H%M'), float(row["P"]) * (1 + round(random.uniform(-odstupanje, odstupanje), 2) / 100)))

with open(path2, mode='r') as file2:
	reader2 = csv.DictReader(file2)

	for row in reader2:
		if row["price"] != '':
			cijene_h.append(float(row["price"]))

with open(path3, mode='r') as file3:
	reader3 = csv.DictReader(file3)

	for row in reader3:
		if row["Situation"] != '':
			stanje.append(row["Situation"])

# izračun zarade
for i in range(len(power)):
	key = str(power[i][0].month)

	if key not in cijene_m:
		cijene_m[key] = 0

	if key not in power_m:
		power_m[key] = 0

	if stanje[i] == 'Deficit':
		k = 1.4
	elif stanje[i] == 'Surplus':
		# k = 0.6
		k = 0
		power_of += power[i][1] / 1000000
		# zasad k = 0 jer ne prodajemo energiju dok je na tržištu ima previše
		# ić će u proizvodnju vodika
	else:
		# Ako je ravnoteža
		k = 1

	cijene_m[key] += power[i][1] * k * cijene_h[i] / 1000000
	power_m[key] += power[i][1] / 1000000
	power_y += power[i][1] / 1000000
	zarada += power[i][1] * k * cijene_h[i] / 1000000

print("Vrijednost prodane energije po mjesecima")
for k, v in cijene_m.items():
	print(f"{k}: {v:.2f} €")
print(f"Ukupna zarada: {zarada:.2f} €\n")

print("Proizvedena energija po mjesecima")
for k, v in power_m.items():
	print(f"{k}: {v:.2f} MWh")
print(f"Ukupna proizvedena energija: {power_y:.0f} MWh\n")

print(f"Višak energije koji nije prodan: {power_of:.0f} MWh")
print(f"Udio viška energije u ukupnoj energiji: {((power_of / power_y) * 100):.2f}%")

# grafovi
x_power = []
y_power = []

for i in power:
	x_power.append(i[0])
	y_power.append(i[1] / 1000000)

plt.plot(x_power, y_power)
plt.xlabel('Datum')
plt.ylabel('MWh')
plt.title('Proizvedena energija MWh (SE Stankovci)')
plt.show()