import numpy as np
import pandas as pd
import hydrostats.data as hd
import hydrostats.analyze as ha
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
        temp_dictionary['{}'.format(str)] = pd.DataFrame(data=Q[:, counter], index=dates, columns=[str])
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

# Specify which metrics to use.
my_metrics = ['r2', 'ME', 'RMSE', 'KGE (2012)']

# Create lists to specify which streams to compare
sim_list = [az_lowres, az_lowres, az_medres, id_lowres, id_lowres, id_medres, mo_lowres, mo_lowres, mo_medres,
            ny_lowres, ny_lowres, ny_medres, or_lowres, or_lowres, or_medres, col_lowres, col_lowres, col_medres]
obs_list = [az_medres, az_highres, az_highres, id_medres, id_highres, id_highres, mo_medres, mo_highres, mo_highres,
            ny_medres, ny_highres, ny_highres, or_medres, or_highres, or_highres, col_medres, col_highres, col_highres]
name_list = ['AZ: Low vs. Med Res',
             'AZ: Low vs. High Res',
             'AZ: Med vs. High Res',
             'ID: Low vs. Med Res',
             'ID: Low vs. High Res',
             'ID: Med vs. High Res',
             'MO: Low vs. Med Res',
             'MO: Low vs. High Res',
             'MO: Med vs. High Res',
             'NY: Low vs. Med Res',
             'NY: Low vs. High Res',
             'NY: Med vs. High Res',
             'OR: Low vs. Med Res',
             'OR: Low vs. High Res',
             'OR: Med vs. High Res',
             'COL: Low vs. Med Res',
             'COL: Low vs. High Res',
             'COL: Med vs. High Res']

# seasonal = [['01-01', '03-31'], ['04-01', '06-30'], ['07-01', '09-30'], ['10-01', '12-31']]

# Create df for each comparison, append to overall df
table = pd.DataFrame()

# Can make seasonal_periods=seasonal (see above)

for s, o, n in zip(sim_list, obs_list, name_list):
    merged_df = hd.merge_data(sim_df=s, obs_df=o)
    temp_table = ha.make_table(merged_df, metrics=my_metrics, seasonal_periods=None, location=n)
    table = table.append(temp_table)

table.to_csv('/home/chrisedwards/Documents/rapid_output/stat_comparison/Statistical_Summary.csv')
# print(table)


# # # CSV including: Full Time Series
# table_full_yr = table[table.index.str.contains('Full')]
# table_full_yr.to_csv('/home/chrisedwards/Documents/rapid_output/statistical_comparison/Full_Year_Stats.csv')
# # # print(table_full_yr)
#
#
# # CSV including: April-01 to June-30.
# table_jan_mar = table[table.index.str.contains('Jan')]
# table_jan_mar.to_csv('/home/chrisedwards/Documents/rapid_output/statistical_comparison/Jan_Mar_Stats.csv')
# # print(table_apr_jun)
#
#
# # CSV including: April-01 to June-30.
# table_apr_jun = table[table.index.str.contains('Apr')]
# table_apr_jun.to_csv('/home/chrisedwards/Documents/rapid_output/statistical_comparison/Apr_Jun_Stats.csv')
# # print(table_apr_jun)
#
#
# # CSV including: April-01 to June-30.
# table_jul_sep = table[table.index.str.contains('Jul')]
# table_jul_sep.to_csv('/home/chrisedwards/Documents/rapid_output/statistical_comparison/Jul_Sep_Stats.csv')
# # print(table_apr_jun)
#
#
# # CSV including: April-01 to June-30.
# table_oct_dec = table[table.index.str.contains('Oct')]
# table_oct_dec.to_csv('/home/chrisedwards/Documents/rapid_output/statistical_comparison/Oct_Dec_Stats.csv')
# # print(table_apr_jun)
#
#
# # CSV including: AZ
# az_table = table[table['Location'].str.contains('AZ')]
# az_table.to_csv('/home/chrisedwards/Documents/rapid_output/statistical_comparison/AZ_Stats.csv')
# # print(az_table)
#
# # CSV including: ID
# id_table = table[table['Location'].str.contains('ID')]
# id_table.to_csv('/home/chrisedwards/Documents/rapid_output/statistical_comparison/ID_Stats.csv')
# # print(az_table)
#
# # CSV including: MO
# mo_table = table[table['Location'].str.contains('MO')]
# mo_table.to_csv('/home/chrisedwards/Documents/rapid_output/statistical_comparison/MO_Stats.csv')
# # print(az_table)
#
# # CSV including: NY
# ny_table = table[table['Location'].str.contains('NY')]
# ny_table.to_csv('/home/chrisedwards/Documents/rapid_output/statistical_comparison/NY_Stats.csv')
# # print(az_table)
#
# # CSV including: OR
# or_table = table[table['Location'].str.contains('OR')]
# or_table.to_csv('/home/chrisedwards/Documents/rapid_output/statistical_comparison/OR_Stats.csv')
# # print(az_table)
#
# # CSV including: COL
# col_table = table[table['Location'].str.contains('COL')]
# col_table.to_csv('/home/chrisedwards/Documents/rapid_output/statistical_comparison/COL_Stats.csv')
# # print(az_table)
