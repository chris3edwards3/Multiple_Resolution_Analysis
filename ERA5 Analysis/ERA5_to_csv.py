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

# User Input Information:
location = '' # Match output folder name from RAPIDpy
comid_list = [134104, 133894, 133872, 133439, 133166, 134191] # Comid's for which csv files are desired
# dir = '/Users/chrisedwards/Documents/era5_test/output_netcdf'
dir = '/Users/chrisedwards/Documents/era5_test/Initialization_continuous_era5'
# csv_dir = '/Users/chrisedwards/Documents/era5_test/output_timeseries'
csv_dir = '/Users/chrisedwards/Documents/era5_test/Initialization_continuous_era5'
# qout_file = 'Qout_era5_t640_1hr_19790101to20181231.nc'
# qout_file = 'Qout_era5_t640_24hr_19790101to20181231.nc'
qout_file = 'Qout_era5_t640_1hr_19790101to19801231.nc'

# Call the NetCDF file.
file = os.path.join(dir, location, qout_file)
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
streamflow_dict_era5 = {}
list_streams_era5 = []
counter = 0

for n in riv:
    name = 'era5-{}-{}'.format(location, n)

    if Q.shape[0] > Q.shape[1]:
        temp_dictionary_era5['{}'.format(name)] = pd.DataFrame(data=Q[:, counter], index=dates, columns=['flowrate (cms)'])
    else:
        temp_dictionary_era5['{}'.format(name)] = pd.DataFrame(data=Q[counter, :], index=dates, columns=['flowrate (cms)'])

    streamflow_dict_era5.update(temp_dictionary_era5)
    list_streams_era5.append(name)
    counter += 1

# Now there is a dictionary called 'streamflow_dict_era5' that has the era5 time series stored in a pandas DataFrame.
# Each array has the datetime and flowrate.
# Each data frame is named in the format 'era5-{location}-{streamID}' (eg: 'era5-nam_white-110079-era5').
# list_streams_era5 = list of all the stream names, or names of the data frames.

# ***************************************************************************************************************

# Save time-series for selected comid's as csv files:

for id in comid_list:
    comid = str(id)
    stream_name = 'era5-{}-{}'.format(location, comid)
    df = streamflow_dict_era5[stream_name]
    df.reset_index(level=0, inplace=True)
    df.rename(columns={'index': 'datetime'},inplace=True)
    csv_path = os.path.join(csv_dir, '{}.csv'.format(stream_name))
    df.to_csv(csv_path, index=False)

