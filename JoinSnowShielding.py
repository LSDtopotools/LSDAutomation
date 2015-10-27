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

# This function goes into a CRNRasters.csv file and makes a directory
# for each raster listed. The c++ program prints the derivative rasters
# into these folders
def GetSnowShieldingFromRaster(path, prefix):

    # get the DEM names
    #DEM_names = GetListOfRasters(path,prefix)
    Sample_names, SnowShield_values = GetCRNData(path, prefix)
    
    # now spawn the folders
    UpdateRasterWithShielding(path, prefix,Sample_names,SnowShield_values)

# This updates the raster file with an effective shielding
def UpdateRasterWithShielding(path, prefix,Sample_names,Snowshield_values):
    
    #first get directory path into the correct format 
    fmt_path = LSDost.ReformatSeperators(path)
    
    # add the trailing seperator
    fmt_path = LSDost.AppendSepToDirectoryPath(fmt_path) 
    
    # now find the correct file
    fname = fmt_path + prefix+"_CRNData.csv"

    new_lines = []    

    #See if the parameter files exist
    if os.access(fname,os.F_OK):
        this_file = open(fname, 'r')
        lines = this_file.readlines()
        
        # now get the list of DEM prefixes
        for line in lines:
            this_line = line.split(",")
            DEM_prefix = this_line[0]
            
            # Now get the sample name
            split_dem_prefix = DEM_prefix.split("_")
            sample_name = split_dem_prefix[-1]
            
            # get the index of the sample name to reference the shielding value
            i = Sample_names.index(sample_name)
            
            # calculate the effective depth. The 160 is the attenuation thickness in g/cm^2
            this_snow_depth = -160*np.log(Snowshield_values[i])
            print "The shielding is: " +str(Snowshield_values[i])+ " and eff_depth is: " + this_snow_depth
            
            # update the snow effective depth
            this_line[1] = str(this_snow_depth)
            
            # update the line
            this_new_line = ",".join(this_line)
            new_lines.append(this_new_line)
            
    # this will get printed to file        
    print "The file is: "
    print new_lines            
            

# This is the subfunction that actually makes the directories if none
# already exists
def GetCRNData(path, prefix):
 
    #first get directory path into the correct format 
    fmt_path = LSDost.ReformatSeperators(path)
    
    # add the trailing seperator
    fmt_path = LSDost.AppendSepToDirectoryPath(fmt_path) 
    
    # now find the correct file
    fname = fmt_path + prefix+"_CRNData.csv"
    
    Sample_names = []
    SnowShield_values = []
    
    #See if the parameter files exist
    if os.access(fname,os.F_OK):
        this_file = open(fname, 'r')
        lines = this_file.readlines()
        
        # now get the list of DEM prefixes
        for line in lines:
            this_line = line.split(",")
            SampleName = this_line[0]
            SnowShield = float(this_line[8])
            Sample_names.append(SampleName)
            SnowShield_values.append(SnowShield)

    else:
        print "*_CRNRData.csv file not found. Are you sure it is there and you have the correct path?"
        
    return Sample_names, SnowShield_values    

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
    path = "c:\basin_data\Chile\TestCRN"
    prefix = "CRN_chile"
    PrepareDirectoriesForBasinSpawn(path,prefix)   