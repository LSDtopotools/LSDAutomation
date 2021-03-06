# Run_drivers_for_mn.py
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# This script looks in a directory designated
# by DataDirectory, finds all the sub-directories,
# and executes the driver in each sub-directory.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FJC 02/07/17
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


import os
from glob import glob
import subprocess


#DataDirectory =  "/home/smudd/papers/Rahul_Himalaya/Chi_analysis/Mandakini/Junction_76/"
DataDirectory =  "/home/s0923330/LSDTopoData/movern_analysis/sensitivity_analyses/chi_all_data/muddpile_movern0p5_n_is_one/"
fname_prefix = 'estimate_movern'

print DataDirectory
#subprocess.call(['ls',DataDirectory,'-l'])

# get all the subdirectories
sub_dirs = [x[0] for x in os.walk(DataDirectory)]
print sub_dirs

# assigns a number to each iteration (i.e. for every .tree file in the directory)
for directory in sub_dirs:
    FileName = directory+fname_prefix+'.driver'

    print "filename is: " + FileName

    system_call = "nohup nice ./chi_mapping_tool.exe "+directory+ " "+ fname_prefix+".driver" +" &"
    print "system call is: " + system_call


    subprocess.call(system_call, shell=True)
