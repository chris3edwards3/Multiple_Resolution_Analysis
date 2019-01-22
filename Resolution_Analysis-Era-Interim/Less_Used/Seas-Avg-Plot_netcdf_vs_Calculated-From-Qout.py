import numpy as np
import pandas as pd
import hydrostats.data as hd
import hydrostats.visual as hv
import HydroErr as he
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset
pd.options.display.max_rows = 120

# Put all the directories (different states and resolutions) and corresponding NetCDF files into lists.
list_of_files = []
list_of_dir = []
streamflow_dict = {}
list_streams = []

for i in os.listdir('/home/chrisedwards/Documents/rapid_output/mult_res_output'):
    for j in os.listdir(os.path.join('/home/chrisedwards/Documents/rapid_output/mult_res_output', i)):
        list_of_files.append(os.path.join('/home/chrisedwards/Documents/rapid_output/mult_res_output', i, j,
                                        'Qout_erai_t511_24hr_19800101to20141231.nc'))
        list_of_dir.append(os.path.join('/home/chrisedwards/Documents/rapid_output/mult_res_output', i, j))

list_of_dir.sort()
list_of_files.sort()

list_of_states=['az', 'id', 'mo', 'ny', 'or', 'col',
                'az', 'id', 'mo', 'ny', 'or', 'col',
                'az', 'id', 'mo', 'ny', 'or', 'col']
list_of_states.sort()

# Loop through the lists to create the csv for each stream, in each resolution.
for file, direc, state in zip(list_of_files, list_of_dir, list_of_states):

    # Call the NetCDF file.
    nc = Dataset(file)
    nc.variables.keys()
    nc.dimensions.keys()

    # Define variables from the NetCDF file.
    riv = nc.variables['rivid'][:].tolist()
    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    Q = nc.variables['Qout'][:]
    sQ = nc.variables['sQout'][:]
    time = nc.variables['time'][:].tolist()

    # Convert time from 'seconds since 1970' to the actual date.
    dates = pd.to_datetime(time, unit='s', origin='unix')

    temp_dictionary = {}
    counter = 0

    for n in riv:
        str=state+'-{}'.format(n)
        temp_dictionary['{}'.format(str)] = pd.DataFrame(data=Q[:, counter], index=dates, columns=['Flow'])
        streamflow_dict.update(temp_dictionary)
        list_streams.append(str)
        counter += 1

list_streams_condensed = list(set(list_streams))
list_streams_condensed.sort()

# Now there is a dictionary called 'streamflow_dict' that has the 35-yr time series stored in a pandas DataFrame.
# Each array has the datetime and flowrate.
# Each data frame is named in the format '{state}-{streamID}' (eg: 'az-7' or 'col-9').
# There are a total of 180 streams, or 180 keys in the dictionary: streamflow_dict['az-7']
# list_streams_condensed = list of all the stream names, or names of the data frames.

# ***************************************************************************************************************

# Put all the directories (different states and resolutions) and corresponding NetCDF files into lists.
list_of_files = []
list_of_dir = []
seas_avg_dict = {}
list_streams_avg = []

for i in os.listdir('/home/chrisedwards/Documents/rapid_output/mult_res_output'):
    for j in os.listdir(os.path.join('/home/chrisedwards/Documents/rapid_output/mult_res_output', i)):
        list_of_files.append(os.path.join('/home/chrisedwards/Documents/rapid_output/mult_res_output', i, j,
                                        'seasonal_averages_erai_t511_24hr_19800101to20141231.nc'))
        list_of_dir.append(os.path.join('/home/chrisedwards/Documents/rapid_output/mult_res_output', i, j))

list_of_dir.sort()
list_of_files.sort()

list_of_states=['az', 'id', 'mo', 'ny', 'or', 'col',
                'az', 'id', 'mo', 'ny', 'or', 'col',
                'az', 'id', 'mo', 'ny', 'or', 'col']
list_of_states.sort()

# Loop through the lists to create the csv for each stream, in each resolution.
for file, state in zip(list_of_files, list_of_states):

    # Call the NetCDF file.
    nc = Dataset(file)
    nc.variables.keys()
    nc.dimensions.keys()

    # Define variables from the NetCDF file.
    riv = nc.variables['rivid'][:].tolist()
    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    avgQ = nc.variables['average_flow'][:]
    sQ = nc.variables['std_dev_flow'][:]
    maxQ = nc.variables['max_flow']
    minQ = nc.variables['min_flow']

    # Make a list of each day in the year.
    dates = pd.date_range('2014-01-01', '2014-12-31').strftime('%b %d')

    temp_dictionary = {}
    counter = 0

    # Loop through each stream.
    for n in riv:
        str=state+'-avg-{}'.format(n)
        temp_dictionary['{}'.format(str)] = pd.DataFrame(data=avgQ[counter, :], index=dates, columns=[str])
        seas_avg_dict.update(temp_dictionary)
        list_streams_avg.append(str)
        counter += 1

list_avg_condensed = list(set(list_streams_avg))
list_avg_condensed.sort()

# Now there is a dictionary called 'seas_avg_dict' that has the seasonal averages stored in a pandas DataFrame.
# Each array has the datetime and flowrate.
# Each data frame is named in the format '{state}-{streamID}' (eg: 'az-7' or 'col-9').
# There are a total of 180 streams, or 180 keys in the dictionary: seas_avg_dict['az-7']
# list_streams_condensed = list of all the stream names, or names of the data frames.

# ***************************************************************************************************************
# ***************************************************************************************************************

az_9 = streamflow_dict['mo-7']
az_avg_9 = seas_avg_dict['mo-avg-7']

merged_df = hd.merge_data(sim_df=az_9, obs_df=streamflow_dict['az-21'],
                          column_names=['9-calc', '21-calc'])
dailyavg2= hd.daily_average(merged_df)
avg_calc = dailyavg2.drop(columns='21-calc')

az_avg_9.index = pd.date_range("2001-01-01", "2001-12-31").strftime("%m/%d")

group = [avg_calc, az_avg_9]
calc_vs_ncdf = pd.concat(group, axis=1)
calc_vs_ncdf.drop(index='02/29', inplace=True)

labels=['Datetime', 'Streamflow (cms)']
hv.plot(merged_data_df=calc_vs_ncdf,
        title="MO Daily Avg: Hydrostats vs Rapid ",
        linestyles=['r-', 'k-'],
        legend=('Hydrostats', 'Rapid NetCDF'),
        labels=labels,
        x_season=True,
        grid=True)
plt.savefig('/home/chrisedwards/Documents/rapid_output/graphs/mo-dav_hd-vs-rapid.png')