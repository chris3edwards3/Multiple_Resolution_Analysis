import numpy as np
import pandas as pd
import hydrostats.data as hd
import hydrostats.visual as hv
import HydroErr as he
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset

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

