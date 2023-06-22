# todo modularise

from datetime import datetime

from broadbandbug.library.constants import TIME_FORMAT

import matplotlib.pyplot as plt
import matplotlib.dates as md


# Converts date strings to a datetime - this is here for easy changing.
def formatTimeForGraph(string):
    return datetime.strptime(string, TIME_FORMAT)


yaxis_extension = 10  # How much to add to the y limit so that the line doesn't reach the top

# Gets readings from file
results_file = open("broadband_results.txt", "r")
results = results_file.readlines()
results_file.close()

# Parses reading, by splitting each reading by the § character. This produces a list of the values
# with download speed at index 0, upload at 1, and times in 2. The up/down speeds are type casted to float.
# Times are converted.
download_speeds = [float(result.split('§')[0]) for result in results]
upload_speeds = [float(result.split('§')[1]) for result in results]
datetimes = [formatTimeForGraph(result.split('§')[2].strip('\n')) for result in results]


# Styling
plt.style.use("seaborn-darkgrid")
fig, ax = plt.subplots(facecolor="#0d0433")
ax.tick_params(labelcolor="orange")

plt.gcf().autofmt_xdate()
xfmt = md.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
plt.ylim(0, max(download_speeds + upload_speeds) + yaxis_extension)

# Labels
plt.xlabel("Time (hour:min)", color="white")
plt.ylabel("Megabits/s", color="white")
plt.title("Broadband Speed", color="white")

# Plots
plt.plot(datetimes, download_speeds, marker="x", label="Download", color="black", linewidth=2)
plt.plot(datetimes, upload_speeds, marker="+", label="Upload", color="red", linewidth=1)

plt.legend()
plt.show()
