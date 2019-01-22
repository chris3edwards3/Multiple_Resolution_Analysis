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
                                        'seasonal_averages_erai_t511_24hr_19800101to20141231.nc'))
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
    Qavg = nc.variables['average_flow'][:]
    Qsdv = nc.variables['std_dev_flow'][:]
    Qmin = nc.variables['min_flow'][:]
    Qmax = nc.variables['max_flow'][:]
    # time = nc.variables['time'][:].tolist()

    # Convert time from 'seconds since 1970' to the actual date.
    dates = pd.date_range('2013-01-01', '2013-12-31').strftime('%b %d')

    temp_dictionary = {}
    counter = 0

    for n in riv:
        str=state+'-{}'.format(n)
        temp_dictionary['{}'.format(str)] = pd.DataFrame(data=Qavg[:, counter], index=dates, columns=[str])
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

# ***********************************************************************************************************

# Extract specific dataframe for a specific stream. This only includes the watershed mouths.
az_lowres = streamflow_dict['az-9']
az_medres = streamflow_dict['az-21']
az_highres = streamflow_dict['az-69']

id_lowres = streamflow_dict['id-8']
id_medres = streamflow_dict['id-17']
id_highres = streamflow_dict['id-39']

mo_lowres = streamflow_dict['mo-7']
mo_medres = streamflow_dict['mo-15']
mo_highres = streamflow_dict['mo-43']

ny_lowres = streamflow_dict['ny-9']
ny_medres = streamflow_dict['ny-20']
ny_highres = streamflow_dict['ny-48']

or_lowres = streamflow_dict['or-7']
or_medres = streamflow_dict['or-16']
or_highres = streamflow_dict['or-51']

col_lowres = streamflow_dict['col-7']
col_medres = streamflow_dict['col-15']
col_highres = streamflow_dict['col-39']

# This list holds all 18 DataFrames, which each hold th 35-yr Time Series Data
list_riv_mouth = [az_lowres, az_medres, az_highres, id_lowres, id_medres, id_highres,
                  mo_lowres, mo_medres, mo_highres, ny_lowres, ny_medres, ny_highres,
                  or_lowres, or_medres, or_highres, col_lowres, col_medres, col_highres]

print(az_lowres)