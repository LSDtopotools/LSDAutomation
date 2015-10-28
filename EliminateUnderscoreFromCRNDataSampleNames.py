# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:24:48 2015

@author: smudd
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 17:35:16 2015

@author: smudd
"""

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#  PrepareDirectoriesForBasinSpawn 
# This function prepaers directories to be spawned 
# by 
"""
Created on Thu Jul 09 11:08:51 2015

@author: smudd
"""

import os
import LSDOSystemTools as LSDost
import numpy as np
import glob

# This goes through all the CRNData.scv files in a directory and removes the 
# underscore in the filename
def EliminateUnderscoreFromCRNData(path):
    
    # loop through all the files in the directory
    for FileName in glob(path+"*CRNData.csv"):
        RemoveUnderscoreFromSampleNames(FileName)    


# This removes any sample names with an underscore, and replaces the underscore 
# with a `-` character
def RemoveUnderscoreFromSampleNames(CRNData_fname):
    
    if os.access(CRNData_fname,os.F_OK):

        # initiate the list for holding the processed data
        new_lines = []
        
        # The with statement just ensures the file closes after we are done with it
        with open(CRNData_fname, 'r') as this_file:
            lines = this_file.readlines()
        
            # Get the first line, then pop is out
            first_line = lines[0]
            lines.pop[0]
            
            # append the first line to the new list
            new_lines.append(first_line)
        
            # now loop through the file, getting rid of the "_" characters in the sample names            
            for line in lines:
                linelist = line.split(",")
                sample_name = linelist[0]
                
                # Replace the underscores
                sample_name.replace("_","-")
                linelist[0]= sample_name                
                
                # put the line back together
                new_line = ",".join(linelist)
                
                # add the new line to the list
                new_lines.append(new_line)
         
        # Now overwrite the data file
        with open(CRNData_fname, 'w') as outfile:
            for line in new_lines:    
                outfile.write("%s\n" % line)  


    
     
if __name__ == "__main__":
    #path = "/home/smudd/SMMDataStore/test_clone/topodata"
    path = "T:\test_clone\topodata"    
    #path = "c:\basin_data\Chile\test_Snow"

    EliminateUnderscoreFromCRNData(path)   