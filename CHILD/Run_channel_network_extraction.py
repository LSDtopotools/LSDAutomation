# Run_child_simulations.py
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# This script looks in a directory designated
# by DataDirectory and then runs the channel
# network extraction algorithm for all CHILD
# runs.  The file generate_dd_drivers.py must
# be run first to get driver files for each 
# ENVI file.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FJC 07/07/15
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


import os
from glob import glob
import subprocess


#DataDirectory =  "/home/smudd/papers/Rahul_Himalaya/Chi_analysis/Mandakini/Junction_76/"
#DataDirectory = "Z:\\LSD_local\\"
DataDirectory =  "/exports/csce/datastore/geos/users/s0923330/LSD_local/"

print DataDirectory
#subprocess.call(['ls',DataDirectory,'-l'])


# assigns a number to each iteration (i.e. for every .tree file in the directory)
for FileName in glob(DataDirectory+"*channel_heads_child*.driver"): 

    print "filename is: " + FileName
    
    split_fname = FileName.split('/')
    #print split_fname
    no_tree_levs = len(split_fname) 
    split_fname = split_fname[no_tree_levs-1]
    
    print split_fname
    
    system_call = "nice ./channel_heads.out " + DataDirectory + " " + split_fname
    print "system call is: " + system_call
    
    #subprocess_call = "ls " + DataDirectory + " -l *.chan"
    #subprocess_call = "ls " + DataDirectory
    #print "Subprocess call is: " + subprocess_call
    
    #subprocess.call(system_call, shell=True)
    subprocess.check_call(system_call, shell=True)
    print "Process finished"
    



