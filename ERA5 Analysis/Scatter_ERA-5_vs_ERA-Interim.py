import numpy as np
import pandas as pd
import hydrostats.data as hd
import hydrostats.visual as hv
import HydroErr as he
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset

# *****************************************************************************************************
# **************ERA Interim****************ERA Interim******************ERA Interim********************
# *****************************************************************************************************

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
        temp_dictionary['{}'.format(str)] = pd.DataFrame(data=Q[:, counter], index=dates, columns=[str])
        streamflow_dict.update(temp_dictionary)
        list_streams.append(str)
        counter += 1

list_streams_condensed = list(set(list_streams))
list_streams_condensed.sort()

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
        temp_dictionary_era5['{}'.format(str)] = pd.DataFrame(data=(Q)[:, counter], index=dates, columns=['Flow'])
        ### Q is divided by 1000 becasue ERA 5 is actually given in mm, not meters. ###
        streamflow_dict_era5.update(temp_dictionary_era5)
        list_streams_era5.append(str)
        counter += 1

list_streams_era5_condensed = list(set(list_streams_era5))
list_streams_era5_condensed.sort()

# ***********************************************************************************************************
# ***********************************************************************************************************

# Now there is a dictionary called 'streamflow_dict' that has the 35-yr time series stored in a pandas DataFrame.
# Each array has the datetime and flowrate.
# Each data frame is named in the format '{state}-{streamID}' (eg: 'az-7' or 'col-9').
# There are a total of 180 streams, or 180 keys in the dictionary: streamflow_dict['az-7']
# list_streams_condensed = list of all the stream names, or names of the data frames.

# ***********************************************************************************************************
# Now there is a dictionary called 'streamflow_dict_era5' that has the era5 time series stored in a pandas DataFrame.
# Each array has the datetime and flowrate.
# Each data frame is named in the format '{state}-{streamID}' (eg: 'az-7-era5' or 'col-9-era5').
# There are a total of 180 streams, or 180 keys in the dictionary: streamflow_dict['az-7-era5']
# list_streams_condensed = list of all the stream names, or names of the data frames.

# ***********************************************************************************************************
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

# This list holds 18 DataFrames, which each hold the 35-yr ERA Interim Time Series Data
list_riv_mouth = [az_lowres, az_medres, az_highres, id_lowres, id_medres, id_highres,
                  mo_lowres, mo_medres, mo_highres, ny_lowres, ny_medres, ny_highres,
                  or_lowres, or_medres, or_highres, col_lowres, col_medres, col_highres]

# This list holds 18 DataFrames, which each hold the ERA 5 Time Series Data
list_riv_mouth_era5 = [az_low_era5, az_med_era5, az_high_era5,
                       id_low_era5, id_med_era5, id_high_era5,
                       mo_low_era5, mo_med_era5, mo_high_era5,
                       ny_low_era5, ny_med_era5, ny_high_era5,
                       or_low_era5, or_med_era5, or_high_era5,
                       col_low_era5, col_med_era5, col_high_era5]

# This list shows which comparison is being made (eg: AZ Lov vs Med):
list_titles = ['AZ Low Res ERA Interim vs 5', 'AZ Med Res ERA Interim vs 5', 'AZ High Res ERA Interim vs 5',
               'ID Low Res ERA Interim vs 5', 'ID Med Res ERA Interim vs 5', 'ID High Res ERA Interim vs 5',
               'MO Low Res ERA Interim vs 5', 'MO Med Res ERA Interim vs 5', 'MO High Res ERA Interim vs 5',
               'NY Low Res ERA Interim vs 5', 'NY Med Res ERA Interim vs 5', 'NY High Res ERA Interim vs 5',
               'OR Low Res ERA Interim vs 5', 'OR Med Res ERA Interim vs 5', 'OR High Res ERA Interim vs 5',
               'COL Low Res ERA Interim vs 5', 'COL Med Res ERA Interim vs 5', 'COL High Res ERA Interim vs 5']

# Sim = ERA Interim, Obs = ERA 5
list_sim = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
list_obs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

# Dynamic Input: Change plot details --------------------------------------------------------------

# Full Time Series is 01-01-1984 to 12-31-2014
begin_date = '2001-01-01'
end_date = '2014-12-31'

# The 'year' parameter is used in the filename. '/' Cannot be used
year = '2001-2014'

# These lists control the color. It is set up so that Low, Med, and High Res each have their own color
color1 = 'r-'
color2 = 'b-'

# These lists control the Legend. It should correlate to "list_titles" above.
series1 = 'ERA Interim'
series2 = 'ERA 5'

# This list specifies which metrics to use:
metrics = []

# This list controls the axis labels:
labels=['Datetime', 'Streamflow (cms)']


# End of Dynamic Input. Do NOT Change the following -------------------------------------------

# Create a list of 18 stream modified Time Series
list_riv_part = []
for riv in list_riv_mouth:
    riv_part = riv.loc[begin_date:end_date]
    list_riv_part.append(riv_part)

list_riv_part_era5 = []
for riv in list_riv_mouth_era5:
    riv_part_era5 = riv.loc[begin_date:end_date]
    list_riv_part_era5.append(riv_part_era5)

for s, o, t in zip(list_sim, list_obs, range(18)):
    merged_df = hd.merge_data(sim_df=list_riv_part[s], obs_df=list_riv_part_era5[o])
    filename = year + ': ' + list_titles[t]
    hv.scatter(merged_data_df=merged_df,
            title=filename,
            labels=(series1, series2),
            metrics = metrics,
            marker_style=".",
            grid=True,
            log_scale=True,
            line45 = True)
    # plt.tight_layout()
    plt.savefig('/home/chrisedwards/Documents/rapid_output/graphs/{}.png'.format(filename))
