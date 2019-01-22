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
        temp_dictionary_era5['{}'.format(str)] = pd.DataFrame(data=(Q/1000)[:, counter], index=dates, columns=['Flow'])
        ### Q is divided by 1000 becasue ERA 5 is actually given in mm, not meters. ###
        streamflow_dict_era5.update(temp_dictionary_era5)
        list_streams_era5.append(str)
        counter += 1

list_streams_era5_condensed = list(set(list_streams_era5))
list_streams_era5_condensed.sort()

# ***********************************************************************************************************
# ***********************************************************************************************************

# Now there is a dictionary called 'streamflow_dict_era5' that has the era5 time series stored in a pandas DataFrame.
# Each array has the datetime and flowrate.
# Each data frame is named in the format '{state}-{streamID}' (eg: 'az-7-era5' or 'col-9-era5').
# There are a total of 180 streams, or 180 keys in the dictionary: streamflow_dict['az-7-era5']
# list_streams_condensed = list of all the stream names, or names of the data frames.

# ***********************************************************************************************************
# ***********************************************************************************************************

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

# This list holds 18 DataFrames, which each hold the ERA 5 Time Series Data
list_riv_mouth_era5 = [az_low_era5, az_med_era5, az_high_era5,
                       id_low_era5, id_med_era5, id_high_era5,
                       mo_low_era5, mo_med_era5, mo_high_era5,
                       ny_low_era5, ny_med_era5, ny_high_era5,
                       or_low_era5, or_med_era5, or_high_era5,
                       col_low_era5, col_med_era5, col_high_era5]

# This list shows which comparison is being made (eg: AZ Lov vs Med):
list_titles = ['AZ Low vs Med', 'AZ Low vs High', 'AZ Med vs High',
               'ID Low vs Med', 'ID Low vs High', 'ID Med vs High',
               'MO Low vs Med', 'MO Low vs High', 'MO Med vs High',
               'NY Low vs Med', 'NY Low vs High', 'NY Med vs High',
               'OR Low vs Med', 'OR Low vs High', 'OR Med vs High',
               'COL Low vs Med', 'COL Low vs High', 'COL Med vs High']

# These lists show the list_riv_part index that will be used in each comparison:
list_sim = [0, 0, 1, 3, 3, 4, 6, 6, 7, 9, 9, 10, 12, 12, 13, 15, 15, 16]
list_obs = [1, 2, 2, 4, 5, 5, 7, 8, 8, 10, 11, 11, 13, 14, 14, 16, 17, 17]

# Dynamic Input: Change plot details --------------------------------------------------------------

# Full Time Series is 01-01-1984 to 12-31-2014
begin_date = '2001-01-01'
end_date = '2015-12-31'

# The 'year' parameter is used in the filename. '/' Cannot be used
year = '2001-2015'

# These lists control the color. It is set up so that Low, Med, and High Res each have their own color
color1 = ['r-', 'r-', 'g-', 'r-', 'r-', 'g-', 'r-', 'r-', 'g-', 'r-', 'r-', 'g-', 'r-', 'r-', 'g-', 'r-', 'r-', 'g-']
color2 = ['g-', 'b-', 'b-', 'g-', 'b-', 'b-', 'g-', 'b-', 'b-', 'g-', 'b-', 'b-', 'g-', 'b-', 'b-', 'g-', 'b-', 'b-']

# These lists control the Legend. It should correlate to "list_titles" above.
series1 = ['Low Res', 'Low Res', 'Med Res', 'Low Res', 'Low Res', 'Med Res', 'Low Res', 'Low Res', 'Med Res',
           'Low Res', 'Low Res', 'Med Res', 'Low Res', 'Low Res', 'Med Res', 'Low Res', 'Low Res', 'Med Res']
series2 = ['Med Res', 'High Res', 'High Res', 'Med Res', 'High Res', 'High Res', 'Med Res', 'High Res', 'High Res',
           'Med Res', 'High Res', 'High Res', 'Med Res', 'High Res', 'High Res', 'Med Res', 'High Res', 'High Res']

# This list specifies which metrics to use:
metrics = []

# This list controls the axis labels:
labels=['Datetime', 'Streamflow (cms)']


# End of Dynamic Input. Do NOT Change the following -------------------------------------------

# Create a list of 18 stream modified Time Series
list_riv_part_era5 = []
for riv in list_riv_mouth_era5:
    riv_part_era5 = riv.loc[begin_date:end_date]
    list_riv_part_era5.append(riv_part_era5)

for s, o, t, s1, s2 in zip(list_sim, list_obs, range(18), series1, series2):
    merged_df = hd.merge_data(sim_df=list_riv_part_era5[s], obs_df=list_riv_part_era5[o])
    filename = year + ' (ERA-5): ' + list_titles[t]
    hv.scatter(merged_data_df=merged_df,
            title=filename,
            labels=(s1, s2),
            metrics = metrics,
            marker_style=".",
            grid=True,
            log_scale=False,
            line45 = True)
    plt.tight_layout()
    plt.savefig('/home/chrisedwards/Documents/rapid_output/graphs/{}.png'.format(filename))