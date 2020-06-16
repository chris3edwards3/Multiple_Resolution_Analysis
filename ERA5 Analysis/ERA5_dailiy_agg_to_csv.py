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
# location = 'south_asia-geoglows-era_5'  # Match output folder name from RAPIDpy
location = 'sam_magdalena-aggQ'  # Match output folder name from RAPIDpy
comid_list = [132748, 133929, 135366, 133140, 131847, 131959, 132592, 133694, 134044, 133892, 132851, 133243, 134286, 135363, 131952, 133877, 134847, 132410, 134702] #Comid's for which csv files are desired
# comid_list = [5061131, 5070113, 5076664, 5074545, 5076937, 5077851, 5080349, 5080535, 5080177, 5080305]  # Comid's for which csv files are desired
dir = '/Users/chrisedwards/Documents/era5_test/output_netcdf'
# dir = '/Users/chrisedwards/Documents/era5_test/SouthAsiaGeoglows/outputNetCDF'
csv_dir = '/Users/chrisedwards/Documents/era5_test/output_timeseries'
# csv_dir = '/Users/chrisedwards/Documents/era5_test/SouthAsiaGeoglows/timeSeries'
# qout_file = 'DailyAggregatedERA5_Qout_era5_t640_1hr_19790101to20181231.nc4'
qout_file = 'DailyAggregated_Qout_era5_t640_1hr_19790101to20181231.nc4'

# Call the NetCDF file.
file = os.path.join(dir, location, qout_file)
nc = Dataset(file)
nc.variables.keys()
nc.dimensions.keys()

# Define variables from the NetCDF file.
riv = nc.variables['rivid'][:].tolist()
# lat = nc.variables['lat'][:]
# lon = nc.variables['lon'][:]
time = nc.variables['time'][:].tolist()
# Q_error = nc.variables['Qout_error'][:]
Q = nc.variables['Qout'][:]

newTime = []
countT = 0
while countT < len(time):
    newTime.append(time[countT] + 3287)
    countT += 1

# Convert time from 'seconds since 1970' to the actual date.
dates = pd.to_datetime(newTime, unit='d', origin='unix')

temp_dictionary_era5 = {}
streamflow_dict_era5 = {}
list_streams_era5 = []
counter = 0

for n in riv:
    comid = int(n)
    name = 'era5-{}-{}'.format(location, comid)

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
