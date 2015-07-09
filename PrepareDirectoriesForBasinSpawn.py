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

# This function goes into a CRNRasters.csv file and makes a directory
# for each raster listed. The c++ program prints the derivative rasters
# into these folders
def PrepareDirectoriesForBasinSpawn(path, prefix):

    # get the DEM names
    DEM_names = GetListOfRasters(path,prefix)
    
    print "DEM_names are: "
    print DEM_names    
    
    # now spawn the folders
    SpawnFoldersFromDEMList(DEM_names)
        

# This is the subfunction that actually makes the directories if none
# already exists
def SpawnFoldersFromDEMList(DEM_names):
    
    # loop through the files checking if there are directories for the 
    # DEMs. If not, make them
    for name in DEM_names:
        path = LSDost.AppendSepToDirectoryPath(name)    
        
        if not os.access(path,os.F_OK):
            print "Making path: "
            os.mkdir(path)
            print path
        else:
            print "Path: " +path+" already exists."
            


# this reads a list of DEM names from the parameter file
def GetListOfRasters(path,prefix):
    
    #first get directory path into the correct format 
    fmt_path = LSDost.ReformatSeperators(path)
    
    # add the trailing seperator
    fmt_path = LSDost.AppendSepToDirectoryPath(fmt_path) 
    
    # now find the correct file
    fname = fmt_path + prefix+"_CRNRasters.csv"
    
    DEM_names = []
    
    #See if the parameter files exist
    if os.access(fname,os.F_OK):
        this_file = open(fname, 'r')
        lines = this_file.readlines()
        
        # now get the list of DEM prefixes
        for line in lines:
            this_line = line.split(",")
            DEM_prefix = this_line[0]
            DEM_names.append(DEM_prefix)           
            
    else:
        print "*_CRNRasters.csv file not found. Are you sure it is there and you have the correct path?"

    return DEM_names
     
if __name__ == "__main__":
    path = "c:\basin_data\Chile\CRN_data_analysis"
    prefix = "Chile_data_analysis"
    PrepareDirectoriesForBasinSpawn(path,prefix)   