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

# Eg datetime format: datetime.datetime.strptime('201701020748','%Y%m%d%H%M')

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
date_time_partial_fast = []
weight = []
weight_fast = []
weight_feast = []
weight_partial_fast = []
fast = []
for i in range(len(weight_lines)):
    weight_lines[i] = weight_lines[i].split(';')
    date_time.append(datetime.datetime.strptime(weight_lines[i][0], '%Y%m%d%H%M'))
    weight.append(float(weight_lines[i][1]))
    if float(weight_lines[i][2]) == 0.0:
        weight_feast.append(float(weight_lines[i][1]))
        date_time_feast.append(datetime.datetime.strptime(weight_lines[i][0], '%Y%m%d%H%M'))
    elif float(weight_lines[i][2]) == 2.0:
        weight_fast.append(float(weight_lines[i][1]))
        date_time_fast.append(datetime.datetime.strptime(weight_lines[i][0], '%Y%m%d%H%M'))
    else:
        weight_partial_fast.append(float(weight_lines[i][1]))
        date_time_partial_fast.append(datetime.datetime.strptime(weight_lines[i][0], '%Y%m%d%H%M'))
    fast.append(weight_lines[i][2][:-1])
    

# Moving averge functon, taken striaight from:
# https://gordoncluster.wordpress.com/2014/02/13/python-numpy-how-to-generate-moving-averages-efficiently-part-2/
def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

# Get rolling mean list
rolling_mean = movingaverage(weight, rolling_window)

# Plot everything:
fig, ax = plt.subplots()
# Plot lines connecting rolling mean and weight for each day vertically. Plot
# this first so that it lies underneath the other pots
for i in range(len(rolling_mean)):
    plt.plot([date_time[rolling_window+i-1],date_time[rolling_window+i-1]],[rolling_mean[i],weight[rolling_window+i-1]],'k--')
# Plot weight over time
plt.plot(date_time, weight,'k')
plt.plot(date_time_fast, weight_fast,'ko', markerfacecolor = 'white', markersize = 5, label = 'Fast')
plt.plot(date_time_feast, weight_feast,'ko', markersize = 5, label = 'Feast')
plt.plot(date_time_partial_fast, weight_partial_fast,'ko', markerfacecolor = 'grey', markersize = 5, label = 'Heavy Caloric Restriction')
# Plot rolling mean over time
plt.plot(date_time[rolling_window-1:],rolling_mean,'b',label = str(rolling_window)+'-day rolling mean')
#plt.xlim(min(date_time),max(date_time))
#plt.ylim(140,max(weight)+10)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# Format x-axis
#fig.autofmt_xdate()
ax.xaxis.set_major_formatter(myFmt_months)
#ax.xaxis.set_minor_formatter(myFmt_days)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(days)
#ax.xaxis.set_tick_params(which='major', pad=15)
plt.title('Daily weight during IF')
plt.ylabel('Weight (lbs)')
plt.xlabel('Date')
plt.savefig('weight.png', bbox_inches='tight')
plt.close()
