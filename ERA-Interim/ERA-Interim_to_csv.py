import numpy as np
import pandas as pd
import hydrostats.data as hd
import hydrostats.visual as hv
import HydroErr as he
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset

# *****************************************************************************************************
# *************ERA Interim*****************ERA Interim*****************ERA Interim*********************
# *****************************************************************************************************

# User Input Information:
location = 'india-1800-deltaT-ERAi' # Match output folder name from RAPIDpy
comid_list = [55596, 58238, 58317, 58384, 59818, 59909] # Comid's for which csv files are desired
dir = '/Users/chrisedwards/Documents/era5_test/India-DeltaT/outputNetCDF'
csv_dir = '/Users/chrisedwards/Documents/era5_test/India-DeltaT/timeSeries'
qout_file = 'Qout_1800dT_erai_t511_24hr_19800101to20141231.nc'

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

temp_dictionary_erai = {}
streamflow_dict_erai = {}
list_streams_erai = []
counter = 0

for n in riv:
    name = 'erai-{}-{}'.format(location, n)

    if Q.shape[0] > Q.shape[1]:
        temp_dictionary_erai['{}'.format(name)] = pd.DataFrame(data=Q[:, counter], index=dates, columns=['flowrate (cms)'])
    else:
        temp_dictionary_erai['{}'.format(name)] = pd.DataFrame(data=Q[counter, :], index=dates, columns=['flowrate (cms)'])

    streamflow_dict_erai.update(temp_dictionary_erai)
    list_streams_erai.append(name)
    counter += 1

# Now there is a dictionary called 'streamflow_dict_erai' that has the erai time series stored in a pandas DataFrame.
# Each array has the datetime and flowrate.
# Each data frame is named in the format 'erai-{location}-{streamID}' (eg: 'erai-nam_white-110079').
# list_streams_erai = list of all the stream names, or names of the data frames.

# ***************************************************************************************************************

# Save time-series for selected comid's as csv files:

for id in comid_list:
    comid = str(id)
    stream_name = 'erai-{}-{}'.format(location, comid)
    df = streamflow_dict_erai[stream_name]
    df.reset_index(level=0, inplace=True)
    df.rename(columns={'index': 'datetime'},inplace=True)
    csv_path = os.path.join(csv_dir, '{}.csv'.format(stream_name))
    df.to_csv(csv_path, index=False)

