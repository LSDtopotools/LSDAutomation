# Run_child_simulations.py
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# This script looks in a directory designated
# by DataDirectory and then finds and exectutes
# all the *.in files located in this 
# directory
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FJC 07/07/15
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


import os
from glob import glob
import subprocess


#DataDirectory =  "/home/smudd/papers/Rahul_Himalaya/Chi_analysis/Mandakini/Junction_76/"
#DataDirectory = "Z:\\CHILD\\CHILD_Fiona\\Runs_n1\\Error_bars\\UpRate_032\\"
DataDirectory =  "/exports/csce/datastore/geos/users/s0923330/CHILD/CHILD_Fiona/Runs_n1/Error_bars/"

uprate = 'Up030'

print DataDirectory
#subprocess.call(['ls',DataDirectory,'-l'])


# assigns a number to each iteration (i.e. for every .tree file in the directory)
for FileName in glob(DataDirectory+"*"+uprate+"*.in"): 

    print "filename is: " + FileName
    
    split_fname = FileName.split('/')
    #print split_fname
    no_tree_levs = len(split_fname) 
    split_fname = split_fname[no_tree_levs-1]
    
    print split_fname
    
    system_call = "nohup nice child --silent-mode " +split_fname + " &"
    print "system call is: " + system_call
    
    #subprocess_call = "ls " + DataDirectory + " -l *.chan"
    #subprocess_call = "ls " + DataDirectory
    #print "Subprocess call is: " + subprocess_call
    
    subprocess.call(system_call, shell=True)



