import numpy as np
import pandas as pd
import hydrostats.data as hd
import hydrostats.visual as hv
import HydroErr as he
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset

# *****************************************************************************************************
# ****************ERA 5**********************ERA 5**********************ERA 5**************************
# *****************************************************************************************************

# Put all the directories (different states and resolutions) and corresponding NetCDF files into lists.
list_of_files_era5 = []
list_of_dir_era5 = []
streamflow_dict_era5 = {}
list_streams_era5 = []

for i in os.listdir('/home/chrisedwards/Documents/rapid_output/era5_output'):
    for j in os.listdir(os.path.join('/home/chrisedwards/Documents/rapid_output/era5_output', i)):
        list_of_files_era5.append(os.path.join('/home/chrisedwards/Documents/rapid_output/era5_output', i, j,
                                        'Qout_era5_t640_24hr_20010101to20151231.nc'))
        list_of_dir_era5.append(os.path.join('/home/chrisedwards/Documents/rapid_output/era5_output', i, j))

list_of_dir_era5.sort()
list_of_files_era5.sort()

list_of_states=['az', 'id', 'mo', 'ny', 'or', 'col',
                'az', 'id', 'mo', 'ny', 'or', 'col',
                'az', 'id', 'mo', 'ny', 'or', 'col']
list_of_states.sort()

# Loop through the lists to create the csv for each stream, in each resolution.
for file, direc, state in zip(list_of_files_era5, list_of_dir_era5, list_of_states):

    # Call the NetCDF file.
    nc = Dataset(file)
    nc.variables.keys()
    nc.dimensions.keys()

    # Define variables from the NetCDF file.
    riv = nc.variables['rivid'][:].tolist()
    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    time = nc.variables['time'][:].tolist()
    # Q_error = nc.variables['Qout_error'][:]
    Q = nc.variables['Qout'][:]

    # Convert time from 'seconds since 1970' to the actual date.
    dates = pd.to_datetime(time, unit='s', origin='unix')

    temp_dictionary_era5 = {}
    counter = 0

    for n in riv:
        str=state+'-{}-era5'.format(n)
        temp_dictionary_era5['{}'.format(str)] = pd.DataFrame(data=Q[:, counter], index=dates, columns=['Flow'])
        streamflow_dict_era5.update(temp_dictionary_era5)
        list_streams_era5.append(str)
        counter += 1

list_streams_era5_condensed = list(set(list_streams_era5))
list_streams_era5_condensed.sort()

# Now there is a dictionary called 'streamflow_dict_era5' that has the era5 time series stored in a pandas DataFrame.
# Each array has the datetime and flowrate.
# Each data frame is named in the format '{state}-{streamID}' (eg: 'az-7-era5' or 'col-9-era5').
# There are a total of 180 streams, or 180 keys in the dictionary: streamflow_dict['az-7-era5']
# list_streams_condensed = list of all the stream names, or names of the data frames.

# ***************************************************************************************************************

# Extract specific dataframe for a specific stream. This only includes the watershed mouths.
az_low_era5 = streamflow_dict_era5['az-9-era5']
az_med_era5 = streamflow_dict_era5['az-21-era5']
az_high_era5 = streamflow_dict_era5['az-69-era5']

id_low_era5 = streamflow_dict_era5['id-8-era5']
id_med_era5 = streamflow_dict_era5['id-17-era5']
id_high_era5 = streamflow_dict_era5['id-39-era5']

mo_low_era5 = streamflow_dict_era5['mo-7-era5']
mo_med_era5 = streamflow_dict_era5['mo-15-era5']
mo_high_era5 = streamflow_dict_era5['mo-43-era5']

ny_low_era5 = streamflow_dict_era5['ny-9-era5']
ny_med_era5 = streamflow_dict_era5['ny-20-era5']
ny_high_era5 = streamflow_dict_era5['ny-48-era5']

or_low_era5 = streamflow_dict_era5['or-7-era5']
or_med_era5 = streamflow_dict_era5['or-16-era5']
or_high_era5 = streamflow_dict_era5['or-51-era5']

col_low_era5 = streamflow_dict_era5['col-7-era5']
col_med_era5 = streamflow_dict_era5['col-15-era5']
col_high_era5 = streamflow_dict_era5['col-39-era5']