import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# How many days to do rolling mean of weight
rolling_window = 4

# x-axis formatting options
myFmt_months = mdates.DateFormatter('%b \'%y')
myFmt_days = mdates.DateFormatter('%d')
years = mdates.YearLocator()
months = mdates.MonthLocator()
days = mdates.DayLocator()

# Open weight file of dates and weights
weight_file = open('weight.txt')
weight_lines = weight_file.readlines()
weight_file.close()

# Remove column definition row
del weight_lines[0]

# Append information from file into corresponding lists
date_time = []
date_time_fast = []
date_time_feast = []
date_time_heavy_caloric_restriction = []
weight = []
weight_fast = []
weight_feast = []
weight_heavy_caloric_restriction = []
fast = []
for i in range(len(weight_lines)):
    weight_lines[i] = weight_lines[i].split(';')
    date_time.append(datetime.datetime.strptime(weight_lines[i][0], '%Y%m%d%H%M'))
    weight.append(float(weight_lines[i][1]))
    if int(weight_lines[i][2]) == 0:
        weight_feast.append(float(weight_lines[i][1]))
        date_time_feast.append(datetime.datetime.strptime(weight_lines[i][0], '%Y%m%d%H%M'))
    elif int(weight_lines[i][2]) == 2:
        weight_fast.append(float(weight_lines[i][1]))
        date_time_fast.append(datetime.datetime.strptime(weight_lines[i][0], '%Y%m%d%H%M'))
    else:
        weight_heavy_caloric_restriction.append(float(weight_lines[i][1]))
        date_time_heavy_caloric_restriction.append(datetime.datetime.strptime(weight_lines[i][0], '%Y%m%d%H%M'))
    fast.append(weight_lines[i][2][:-1])

# Moving average function, modified from:
# https://gordoncluster.wordpress.com/2014/02/13/python-numpy-how-to-generate-moving-averages-efficiently-part-2/
def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return np.around(sma,2)

# Get rolling mean list
rolling_mean = movingaverage(weight, rolling_window)

# Initialize plot
fig, ax = plt.subplots()

# Shade regions of increase and decrease in rolling mean
for i in range(1,len(rolling_mean)):
    if rolling_mean[i] > rolling_mean[i-1]:
        plt.axvspan(date_time[rolling_window-1+i-1],date_time[rolling_window-1+i], color='red', alpha=0.25, lw=0)
    else:
        plt.axvspan(date_time[rolling_window-1+i-1],date_time[rolling_window-1+i], color='blue', alpha=0.25, lw=0)

# Plot shaded regions above and below rolling mean
plt.fill_between(date_time[rolling_window-1:], rolling_mean, weight[rolling_window-1:], where=rolling_mean >= weight[rolling_window-1:], facecolor='blue', alpha=0.5, interpolate=True)
plt.fill_between(date_time[rolling_window-1:], rolling_mean, weight[rolling_window-1:], where=rolling_mean <= weight[rolling_window-1:], facecolor='red', alpha=0.5, interpolate=True)

# Plot rolling mean over time
plt.plot(date_time[rolling_window-1:], rolling_mean, 'green', alpha=0.5, label=str(rolling_window)+'-day rolling mean')

# Plot weight over time
plt.plot(date_time_fast, weight_fast, 'ko', markerfacecolor='white', markersize=5, label='Fast')
plt.plot(date_time_feast, weight_feast, 'ko', markersize=5, label='Feast')
plt.plot(date_time_heavy_caloric_restriction, weight_heavy_caloric_restriction, 'ko', markerfacecolor='grey', markersize=5, label='Heavy Caloric Restriction')

# Plot legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# Format x-axis
ax.xaxis.set_major_formatter(myFmt_months)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(days)

# Fill in text for plot
plt.title('Daily weight')
plt.ylabel('Weight (lbs)')
plt.xlabel('Date')

# Save plot and close
plt.savefig('weight.png', bbox_inches='tight')
plt.close()
