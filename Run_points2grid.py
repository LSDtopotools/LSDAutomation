# Run_points2grid.py
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# This script looks in a directory designated by DataDirectory and grids all
# the .las files using points2grid. The parameters for gridding need to be set:
#       Output type: either min, max, mean, idw, den, or all
#       Input format: las or ascii
#       Output format: all, arc, or grid
#       Desired grid resolution
#       Fill window size: 3, 5, or 7              
#
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Fiona J. Clubb
# 21/06/16
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


import os
from glob import glob
import subprocess

# Set parameters for gridding
output_type = 'mean'
input_format = 'las'
output_format = 'arc'
resolution = '5'
fill_window_size = '7'

# set the data directory
DataDirectory =  "/home/s0923330/Datastore/river_cree/"
print DataDirectory

# loop through every file in the directory
for FileName in glob(DataDirectory+"*.las"): 

    print "filename is: " + FileName
    
    # get the name of the LAS file
    split_fname = FileName.split('/')
    fname_len = len(split_fname) 
    split_fname = split_fname[fname_len-1]
    
    # remove LAS extension from filename
    fname_noext = split_fname.split('.')
    fname_noext = fname_noext[0]
    
    # create the system call
    system_call = "points2grid -i " + DataDirectory + split_fname + " -o " + fname_noext + " --" + output_type + " --input_format=" + input_format + " --output_format=" + output_format+ " --resolution=" + resolution + " --fill --fill_window_size=" + fill_window_size
    print "system call is: " + system_call
    
    # run the program on this filename
    subprocess.call(system_call, shell=True)



