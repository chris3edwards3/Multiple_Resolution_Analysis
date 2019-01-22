import numpy as np
import pandas as pd
import hydrostats.data as hd
import hydrostats.visual as hv
import HydroErr as he
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset

# Put all the directories (different states and resolutions) and corresponding NetCDF files into lists.
list_of_files_era5 = []
list_of_dir_era5 = []
streamflow_dict_era5 = {}
list_streams_era5 = []

for i in os.listdir('/home/chrisedwards/Documents/rapid_output/mult_res_output'):
    for j in os.listdir(os.path.join('/home/chrisedwards/Documents/rapid_output/mult_res_output', i)):
        list_of_files_era5.append(os.path.join('/home/chrisedwards/Documents/rapid_output/mult_res_output', i, j,
                                        'Qout_era5_t640_24hr_20010101to20151231.nc'))
        list_of_dir_era5.append(os.path.join('/home/chrisedwards/Documents/rapid_output/mult_res_output', i, j))

list_of_dir_era5.sort()
list_of_files_era5.sort()

list_of_states=['az', 'id', 'mo', 'ny', 'or', 'col',
                'az', 'id', 'mo', 'ny', 'or', 'col',
                'az', 'id', 'mo', 'ny', 'or', 'col']
list_of_states.sort()

nc = Dataset(list_of_files_era5[0])

Qout = nc.variables['Qout'][:]

print(Qout)