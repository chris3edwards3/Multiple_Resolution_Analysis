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

# Extract specific dataframe for a specific stream. This section is for streams above the mouth.
az_60 = streamflow_dict['az-60']

mo_50 = streamflow_dict['mo-50']
mo_51 = streamflow_dict['mo-51']

ny_8 = streamflow_dict['ny-8']
ny_19 = streamflow_dict['ny-19']
ny_47 = streamflow_dict['ny-47']
ny_18 = streamflow_dict['ny-18']
ny_46 = streamflow_dict['ny-46']

or_20 = streamflow_dict['or-20']
or_58 = streamflow_dict['or-58']
or_15 = streamflow_dict['or-15']
or_47 = streamflow_dict['or-47']

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

# Upstream Gauges (Not OUTLET):

az_60_obs = pd.read_csv('/home/chrisedwards/Documents/gauge_data/09492400_1-1-1980_12-31-2014.csv', index_col=0)
az_60_obs_cms = az_60_obs.drop(columns=["Flow-cfs", "Estimation"])

mo_50_obs = pd.read_csv('/home/chrisedwards/Documents/gauge_data/07013000_1-1-1980_12-31-2014.csv', index_col=0)
mo_50_obs_cms = mo_50_obs.drop(columns=["Flow-cfs", "Estimation"])

mo_51_obs = pd.read_csv('/home/chrisedwards/Documents/gauge_data/07014000_3-5-2007_12-31-2014.csv', index_col=0)
mo_51_obs_cms = mo_51_obs.drop(columns=["Flow-cfs", "Estimation"])

ny_8_19_47_obs = pd.read_csv('/home/chrisedwards/Documents/gauge_data/01413408_12-5-1996_12-31-2014.csv', index_col=0)
ny_8_19_47_obs_cms = ny_8_19_47_obs.drop(columns=["Flow-cfs", "Estimation"])

# This one gauge is somewhat close to stream break, it might work.
ny_18_46_obs = pd.read_csv('/home/chrisedwards/Documents/gauge_data/01413398_10-1-1997_12-31-2014.csv', index_col=0)
ny_18_46_obs_cms = ny_18_46_obs.drop(columns=["Flow-cfs", "Estimation"])

or_20_58_obs = pd.read_csv('/home/chrisedwards/Documents/gauge_data/14306400_1-1-1980_9-29-1990.csv', index_col=0)
or_20_58_obs_cms = or_20_58_obs.drop(columns=["Flow-cfs", "Estimation"])

or_15_47_obs = pd.read_csv('/home/chrisedwards/Documents/gauge_data/14306100_1-1-1980_9-29-1989.csv', index_col=0)
or_15_47_obs_cms = or_15_47_obs.drop(columns=["Flow-cfs", "Estimation"])

# ------------------------------------------------------------------------------------------------------


# List containing all the simulated data frames in the correct order.
list_sim_df = [az_highres, id_highres, mo_highres, ny_highres, or_highres,
               az_60, mo_50, mo_51, ny_47, ny_46, or_58, or_47]

# List containing all the observed data frames, in the correct order.
list_obs_df = [az_obs_cms, id_obs_cms, mo_obs_cms, ny_obs_cms, or_obs_cms,
               az_60_obs_cms, mo_50_obs_cms, mo_51_obs_cms,
               ny_8_19_47_obs_cms, ny_18_46_obs_cms, or_20_58_obs_cms, or_15_47_obs_cms]

# The order of the graph titles
list_titles = ['AZ: Sim (Outlet) vs Obs (gauge-09494000)',
               'ID: Sim (Outlet) vs Obs (gauge-13340600)',
               'MO: Sim (Outlet) vs Obs (gauge-07014500)',
               'NY: Sim (Outlet) vs Obs (gauge-01413500)',
               'OR: Sim (Outlet) vs Obs (gauge-14306500)',
               'AZ: Sim (str-60) vs Obs (gauge-09492400)',
               'MO: Sim (str-50) vs Obs (gauge-07013000)',
               'MO: Sim (str-51) vs Obs (gauge-07014000)',
               'NY: Sim (str-47) vs Obs (gauge-01413408)',
               'NY: Sim (str-46) vs Obs (gauge-01413398)',
               'OR: Sim (str-58) vs Obs (gauge-14306400)',
               'OR: Sim (str-47) vs Obs (gauge-14306100)']

# This list specifies which metrics to use:
metrics = []

# This list controls the axis labels:
labels=['Datetime', 'Streamflow (cms)']

for s, o, t in zip(range(12), range(12), range(12)):
    merged_df = hd.merge_data(sim_df=list_sim_df[s], obs_df=list_obs_df[o])
    da_df = hd.daily_average(merged_df)
    filename = list_titles[t] + ' Daily Average'
    hv.plot(merged_data_df=da_df,
            title=filename,
            linestyles=['b-', 'k-'],
            legend=('Sim', 'Obs'),
            labels=labels,
            metrics=metrics,
            x_season=True,
            grid=True)
    plt.tight_layout()
    plt.savefig('/home/chrisedwards/Documents/rapid_output/graphs/{}.png'.format(filename))