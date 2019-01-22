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
begin_date = '1980-01-01'
end_date = '2014-12-31'

# The 'year' parameter is used in the filename. '/' Cannot be used
year = '1980-2014'

# These lists control the color. It is set up so that Low, Med, and High Res each have their own color
color1 = ['r-', 'r-', 'g-', 'r-', 'r-', 'g-', 'r-', 'r-', 'g-', 'r-', 'r-', 'g-', 'r-', 'r-', 'g-', 'r-', 'r-', 'g-']
color2 = ['g-', 'b-', 'b-', 'g-', 'b-', 'b-', 'g-', 'b-', 'b-', 'g-', 'b-', 'b-', 'g-', 'b-', 'b-', 'g-', 'b-', 'b-']

# These lists control the Lables. It should correlate to "list_titles" above.
series1 = ['Low Res', 'Low Res', 'Med Res', 'Low Res', 'Low Res', 'Med Res', 'Low Res', 'Low Res', 'Med Res',
           'Low Res', 'Low Res', 'Med Res', 'Low Res', 'Low Res', 'Med Res', 'Low Res', 'Low Res', 'Med Res']
series2 = ['Med Res', 'High Res', 'High Res', 'Med Res', 'High Res', 'High Res', 'Med Res', 'High Res', 'High Res',
           'Med Res', 'High Res', 'High Res', 'Med Res', 'High Res', 'High Res', 'Med Res', 'High Res', 'High Res']

# This list specifies which metrics to use:
metrics = ['KGE (2012)', 'dr', 'SMAPE2']


# End of Dynamic Input. Do NOT Change the following -------------------------------------------

# Create a list of 18 stream modified Time Series
list_riv_part = []
for riv in list_riv_mouth:
    riv_part = riv.loc[begin_date:end_date]
    list_riv_part.append(riv_part)

for s, o, t, c1, c2, s1, s2 in zip(list_sim, list_obs, range(18), color1, color2, series1, series2):
    merged_df = hd.merge_data(sim_df=list_riv_part[s], obs_df=list_riv_part[o])
    filename = year + ': ' + list_titles[t]
    hv.scatter(merged_data_df=merged_df,
            title=filename,
            labels=(s1, s2),
            metrics = metrics,
            marker_style=".",
            grid=True,
            log_scale=True,
            line45 = True)
    # plt.yscale("log")
    plt.tight_layout()
    plt.savefig('/home/chrisedwards/Documents/rapid_output/graphs/{}.png'.format(filename))





