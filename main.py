import numpy as np
from matplotlib import pyplot as plt

from fastf1.ergast import Ergast

ergast = Ergast()
races = ergast.get_race_schedule(2023)  # Races in year 2023
home_results = {}
all_results = {}
averages = {}
# number next to the drivers number is the round number for their home race
# not all drivers are included, because not all of them have home races during the season
home_races = {1: 14,
              11: 20,
              44: 11,
              14: 8,
              16: 7,
              4: 11,
              55: 8,
              63: 11,
              81: 3,
              18: 9,
              22: 17,
              2: 5}
drivers = list(home_races.keys())

for driver in drivers:
    all_results[driver] = []

# collecting data
for rnd, race in races['raceName'].items():
    temp = ergast.get_race_results(season=2023, round=rnd + 1)
    for driver in drivers:
        results = temp.content[0]
        position_info = results[results['number'] == driver]
        if not position_info.empty:
            position = int(position_info['position'].iloc[0])
            all_results[driver].append(position)
            if home_races[driver] == rnd + 1:
                home_results[driver] = position

# calculating averages
for driver in drivers:
    averages[driver] = np.mean(all_results[driver])

# sorting values according to the race number
sorted_drivers = sorted(drivers)
driver_names = ["VER", "SAR", "NOR", "PER", "ALO", "LEC", "STR", "TSU", "HAM", "SAI", "RUS", "PIA"]
sorted_averages = {k: averages[k] for k in sorted_drivers}
sorted_home = {k: home_results[k] for k in sorted_drivers}

# plotting
barWidth = 0.25

average = np.arange(len(averages))
home = [x + barWidth for x in average]

plt.bar(average, list(sorted_averages.values()), color='b', width=barWidth,
        edgecolor='grey', label="Average Result")
plt.bar(home, list(sorted_home.values()), color='r', width=barWidth,
        edgecolor='grey', label="Home Result")

plt.xticks([r + barWidth for r in range(len(drivers))], driver_names)
plt.yticks([i for i in range(1, 20 + 1)])
plt.title("Comparison between Home and Average race results in 2023", fontweight ='bold')

plt.grid(color='grey',
         linestyle='-.', linewidth=0.5,
         alpha=0.2)

plt.legend()
plt.show()
