# Run_drivers_for_polygonize.py
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# This script runs gdal_polygonize.py on all basins (called by their downstream junction numbers)
# present in a designated directory (DataDirectory)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# mharel
# 2015
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


import os
from glob import glob
import numpy as np, matplotlib.pyplot as plt
import subprocess

zonenb = '66'
DataDirectory ="/exports/csce/datastore/geos/users/mharel/Topo_Data/general/New_zone_ref/zone"+zonenb+"/"
#DataDirectory ="/exports/csce/datastore/geos/users/mharel/Topo_Data/general/zone20/"

print DataDirectory

for FileName in glob(DataDirectory+"*.driver"): 
    f = open(FileName,'r')  # open file
    lines = f.readlines()   # read in the data
    junction = int(float(lines[3]))
    print "junction is : " +str(junction)
    format = "'ESRI Shapefile'"
    if zonenb == '45':
        system_call = "python gdal_polygonize.py "+DataDirectory+"sanfransouth_basin_"+str(junction)+".flt -f "+format+" "+DataDirectory+"shape_"+str(junction)+".shp "
    else:
        system_call = "python gdal_polygonize.py "+DataDirectory+"zone"+zonenb+"_basin_"+str(junction)+".flt -f "+format+" "+DataDirectory+"shape_"+str(junction)+".shp "
   
    subprocess.call(system_call, shell=True)

