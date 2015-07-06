# Run_drivers_for_mn.py
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# This script looks in a directory designated
# by DataDirectory and then finds and exectutes
# all the *.driver files located in this 
# directory
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Simon M. Mudd
# 16/12/2013
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


import os
from glob import glob
import subprocess


#DataDirectory =  "/home/smudd/papers/Rahul_Himalaya/Chi_analysis/Mandakini/Junction_76/"
DataDirectory =  "/home/mharel/Topo_Data/Rio_Torto/"

print DataDirectory
#subprocess.call(['ls',DataDirectory,'-l'])


# assigns a number to each iteration (i.e. for every .tree file in the directory)
for FileName in glob(DataDirectory+"*.driver"): 

    print "filename is: " + FileName
    
    split_fname = FileName.split('/')
    no_tree_levs = len(split_fname) 
    split_fname = split_fname[no_tree_levs-1]
    
    #print split_fname
    
    system_call = "nohup nice ./chi_m_over_n_analysis.exe "+DataDirectory+ " "+split_fname +" &"
    print "system call is: " + system_call
    
    #subprocess_call = "ls " + DataDirectory + " -l *.chan"
    #subprocess_call = "ls " + DataDirectory
    #print "Subprocess call is: " + subprocess_call
    
    subprocess.call(system_call, shell=True)



