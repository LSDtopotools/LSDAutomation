# Run_drivers_for_mn.py
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# This script looks in a directory designated
# by DataDirectory, finds all the sub-directories,
# and executes the driver in each sub-directory.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FJC 28/09/17
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


import os
from glob import glob
import subprocess


#DataDirectory =  "/home/smudd/papers/Rahul_Himalaya/Chi_analysis/Mandakini/Junction_76/"
DataDirectory =  "/home/s0923330/MN_postdoc/Experimental_data/"
fname_prefix = 'get_terraces'

print DataDirectory
#subprocess.call(['ls',DataDirectory,'-l'])

# get all the subdirectories
sub_dirs = [x[0] for x in os.walk(DataDirectory)]
print sub_dirs

# assigns a number to each iteration (i.e. for every .tree file in the directory)
for directory in sub_dirs:
    FileName = directory+fname_prefix+'.driver'

    print "filename is: " + FileName

    system_call = "nice ./get_terraces_from_shapefile.out "+directory+ " "+ fname_prefix+".driver"
    print "system call is: " + system_call


    subprocess.call(system_call, shell=True)
