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
seas_avg_dict = {}
list_streams_avg = []

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
for file, state in zip(list_of_files, list_of_states):

    # Call the NetCDF file.
    nc = Dataset(file)
    nc.variables.keys()
    nc.dimensions.keys()

    # Define variables from the NetCDF file.
    riv = nc.variables['rivid'][:].tolist()
    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    avgQ = nc.variables['average_flow'][:]
    sQ = nc.variables['std_dev_flow'][:]
    maxQ = nc.variables['max_flow']
    minQ = nc.variables['min_flow']

    # Make a list of each day in the year.
    dates = pd.date_range('2014-01-01', '2014-12-31').strftime('%b %d')

    temp_dictionary = {}
    counter = 0

    # Loop through each stream.
    for n in riv:
        str=state+'-avg-{}'.format(n)
        temp_dictionary['{}'.format(str)] = pd.DataFrame(data=avgQ[counter, :], index=dates, columns=[str])
        seas_avg_dict.update(temp_dictionary)
        list_streams_avg.append(str)
        counter += 1

list_avg_condensed = list(set(list_streams_avg))
list_avg_condensed.sort()

# Now there is a dictionary called 'seas_avg_dict' that has the seasonal averages stored in a pandas DataFrame.
# Each array has the datetime and flowrate.
# Each data frame is named in the format '{state}-{streamID}' (eg: 'az-7' or 'col-9').
# There are a total of 180 streams, or 180 keys in the dictionary: seas_avg_dict['az-7']
# list_streams_condensed = list of all the stream names, or names of the data frames.

# ***************************************************************************************************************

# Extract specific dataframe for a specific stream. This only includes the watershed mouths.
az_lowres = seas_avg_dict['az-avg-9']
az_medres = seas_avg_dict['az-avg-21']
az_highres = seas_avg_dict['az-avg-69']

id_lowres = seas_avg_dict['id-avg-8']
id_medres = seas_avg_dict['id-avg-17']
id_highres = seas_avg_dict['id-avg-39']

mo_lowres = seas_avg_dict['mo-avg-7']
mo_medres = seas_avg_dict['mo-avg-15']
mo_highres = seas_avg_dict['mo-avg-43']

ny_lowres = seas_avg_dict['ny-avg-9']
ny_medres = seas_avg_dict['ny-avg-20']
ny_highres = seas_avg_dict['ny-avg-48']

or_lowres = seas_avg_dict['or-avg-7']
or_medres = seas_avg_dict['or-avg-16']
or_highres = seas_avg_dict['or-avg-51']

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

x_df = or_obs_full.drop(columns=['Flow-cms', 'Estimation'])

# ------------------------------------------------------------------------------------------------------

# This list shows which comparison is being made (eg: AZ Lov vs Med):
list_titles = ['AZ Rapid Daily Avg: Low vs Obs', 'AZ Rapid Daily Avg: Med vs Obs', 'AZ Rapid Daily Avg: High vs Obs',
               'ID Rapid Daily Avg: Low vs Obs', 'ID Rapid Daily Avg: Med vs Obs', 'ID Rapid Daily Avg: High vs Obs',
               'MO Rapid Daily Avg: Low vs Obs', 'MO Rapid Daily Avg: Med vs Obs', 'MO Rapid Daily Avg: High vs Obs',
               'NY Rapid Daily Avg: Low vs Obs', 'NY Rapid Daily Avg: Med vs Obs', 'NY Rapid Daily Avg: High vs Obs',
               'OR Rapid Daily Avg: Low vs Obs', 'OR Rapid Daily Avg: Med vs Obs', 'OR Rapid Daily Avg: High vs Obs']


# These lists show the list_riv_part index that will be used in each comparison:
list_sim = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
list_obs = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]


# Dynamic Input: Change plot details --------------------------------------------------------------

# These lists control the color. It is set up so that Low, Med, and High Res each have their own color
color1 = ['r-', 'g-', 'b-', 'r-', 'g-', 'b-', 'r-', 'g-', 'b-', 'r-', 'g-', 'b-', 'r-', 'g-', 'b-', 'r-', 'g-', 'b-']
c2 = 'k-'

# These lists control the Legend. It should correlate to "list_titles" above.
series1 = ['Low Res', 'Med Res', 'High Res', 'Low Res', 'Med Res', 'High Res', 'Low Res', 'Med Res', 'High Res',
           'Low Res', 'Med Res', 'High Res', 'Low Res', 'Med Res', 'High Res']
s2 = 'Observed'

# This list specifies which metrics to use:
metrics = []

# This list controls the axis labels:
labels=['Datetime', 'Streamflow (cms)']


# End of Dynamic Input. Do NOT Change the following -------------------------------------------

for s, o, t, c1, s1 in zip(list_sim, list_obs, range(15), color1, series1):
    temp_merged = hd.merge_data(sim_df=x_df, obs_df=list_obs_df[o])
    temp_davg = hd.daily_average(temp_merged)
    obs_loop_df = temp_davg.drop(index='02/29', columns='Simulated')

    sim_temp_df = list_riv_mouth[s]
    sim_loop_in = sim_temp_df.index=pd.date_range('2001-01-01', '2001-12-31').strftime("%m/%d")
    # dates=pd.date_range('2001-01-01', '2001-12-31').strftime("%m/%d")
    sim_loop_df = pd.DataFrame(sim_loop_in, index=pd.date_range('2001-01-01', '2001-12-31').strftime("%m/%d"))


    group = [sim_loop_df, obs_loop_df]
    merged_df = pd.concat(group, axis=1)
    filename = list_titles[t]
    hv.plot(merged_data_df=merged_df,
            title=filename,
            linestyles=[c1, c2],
            legend=(s1, s2),
            labels=labels,
            metrics = metrics,
            x_season=True,
            grid=True)
    plt.savefig('/home/chrisedwards/Documents/rapid_output/graphs/{}.png'.format(filename))
