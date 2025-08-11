import matplotlib.pyplot as plt
from datetime import datetime, timedelta

dataset = [
    ["11-07-25", 25.6],
    ["13-07-25", 22.3],
    ["21-07-25", 24.3],
    ["23-07-25", 23.2],
    ["25-07-25", 23.8],
    ["28-07-25", 24.8],
    ["30-07-25", 24.3],
    ["01-08-25", 24.0],
    ["04-08-25", 24.1],
    ["06-08-25", 24.1],
    ["08-08-25", 23.7],
    ["11-08-25", 24.1],
]

dates = []
temps = []

for i in dataset:
    date = i[0]          #datetime.strptime(i[0], "%d-%m-%y")
    dates.append(date)

    temp = i[1]
    temps.append(temp)
    #plt.scatter(date, temp)

plt.plot(dates, temps)

plt.xlabel("Mess-Zeitpunkte")
plt.ylabel("Temperatur [°C]")
plt.xticks(rotation=45) 
plt.tight_layout()
plt.show()
