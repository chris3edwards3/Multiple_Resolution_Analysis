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

# This list holds all 18 DataFrames, which each hold th 35-yr Time Series Data
list_riv_mouth = [az_lowres, az_medres, az_highres, id_lowres, id_medres, id_highres,
                  mo_lowres, mo_medres, mo_highres, ny_lowres, ny_medres, ny_highres,
                  or_lowres, or_medres, or_highres]

# -----------------------------Format Gauge Data---------------------------------------------------

az_obs_full = pd.read_csv('/home/chrisedwards/Documents/gauge_data/09494000_1-1-1980_12-31-2014.csv', index_col=0)
az_obs_cms = az_obs_full.drop(columns=["Flow-cfs", "Estimation"])

id_obs_full = pd.read_csv('/home/chrisedwards/Documents/gauge_data/13340600_1-1-1980_12-31-2014.csv', index_col=0)
id_obs_cms = id_obs_full.drop(columns=["Flow-cfs", "Estimation"])

mo_obs_full = pd.read_csv('/home/chrisedwards/Documents/gauge_data/07014500_1-1-1980_12-31-2014.csv', index_col=0)
mo_obs_cms = mo_obs_full.drop(columns=["Flow-cfs", "Estimation"])

ny_obs_full = pd.read_csv('/home/chrisedwards/Documents/gauge_data/01413500_1-1-1980_12-31-2014.csv', index_col=0)
ny_obs_cms = ny_obs_full.drop(columns=["Flow-cfs", "Estimation"])

or_obs_full = pd.read_csv('/home/chrisedwards/Documents/gauge_data/14306500_1-1-1980_12-31-2014.csv', index_col=0)
or_obs_cms = or_obs_full.drop(columns=["Flow-cfs", "Estimation"])

list_obs_df = [az_obs_cms, id_obs_cms, mo_obs_cms, ny_obs_cms, or_obs_cms]

# ------------------------------------------------------------------------------------------------------

# This list shows which comparison is being made (eg: AZ Lov vs Med):
list_titles = ['AZ Low vs Gauge', 'AZ Med vs Gauge', 'AZ High vs Gauge',
               'ID Low vs Gauge', 'ID Med vs Gauge', 'ID High vs Gauge',
               'MO Low vs Gauge', 'MO Med vs Gauge', 'MO High vs Gauge',
               'NY Low vs Gauge', 'NY Med vs Gauge', 'NY High vs Gauge',
               'OR Low vs Gauge', 'OR Med vs Gauge', 'OR High vs Gauge']

# These lists show the list_riv_part index that will be used in each comparison:
list_sim = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
list_obs = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]


# Dynamic Input: Change plot details --------------------------------------------------------------

# Full Time Series is 01-01-1984 to 12-31-2014
begin_date = '1980-01-01'
end_date = '1981-12-31'

# The 'year' parameter is used in the filename. '/' Cannot be used
year = '1980-1981'

# # These lists control the color. It is set up so that Low, Med, and High Res each have their own color
color1 = ['r-', 'g-', 'b-', 'r-', 'g-', 'b-', 'r-', 'g-', 'b-', 'r-', 'g-', 'b-', 'r-', 'g-', 'b-', 'r-', 'g-', 'b-']
# color2 = ['b-', 'r-', 'r-', 'b-', 'r-', 'r-', 'b-', 'r-', 'r-', 'b-', 'r-', 'r-', 'b-', 'r-', 'r-', 'b-', 'r-', 'r-']

# These lists control the Legend. It should correlate to "list_titles" above.
series1 = ['Low Res', 'Med Res', 'High Res', 'Low Res', 'Med Res', 'High Res', 'Low Res', 'Med Res', 'High Res',
           'Low Res', 'Med Res', 'High Res', 'Low Res', 'Med Res', 'High Res']
series2 = 'Observed'

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

for s, o, c1, t, s1 in zip(list_sim, list_obs, color1, range(18), series1):
    merged_df = hd.merge_data(sim_df=list_riv_part[s], obs_df=list_obs_df[o])
    filename = year + ': ' + list_titles[t]
    hv.plot(merged_data_df=merged_df,
            title=filename,
            linestyles=[c1, 'k-'],
            legend=(s1, series2),
            labels=labels,
            metrics = metrics,
            grid=True)
    plt.savefig('/home/chrisedwards/Documents/rapid_output/graphs/{}.png'.format(filename))





