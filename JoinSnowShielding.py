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
import shutil

# This function goes into a CRNRasters.csv file and makes a directory
# for each raster listed. The c++ program prints the derivative rasters
# into these folders
def GetSnowShieldingFromRaster(path, prefix):

    # get the DEM names
    #DEM_names = GetListOfRasters(path,prefix)
    Sample_names, SnowShield_values = GetCRNData(path, prefix)
    
    # get rid of the underscores
    Sample_names = RemoveUnderscoreFromSampleNames(Sample_names)   
    
    # now spawn the folders
    UpdateRasterWithShielding(path, prefix,Sample_names,SnowShield_values)
    
    new_extension = "SS"
    # now copy the parameter and CRNData files
    CopyDataAndParam(path, prefix,new_extension)


# this copies the CRNData and CNParameters file with a new extension
def CopyDataAndParam(path, prefix,new_extension):

    #first get directory path into the correct format 
    fmt_path = LSDost.ReformatSeperators(path)
    
    # add the trailing seperator
    fmt_path = LSDost.AppendSepToDirectoryPath(fmt_path)     

    # now find the correct file
    Datafname = fmt_path + prefix+"_CRNData.csv"
    Paramfname = fmt_path + prefix+".CRNParam"
    
    Datafname_out = fmt_path + prefix+"_"+new_extension+"_CRNData.csv"
    Paramfname_out = fmt_path + prefix+"_"+new_extension+".CRNParam"
    
    # copy the files
    shutil.copyfile(Datafname, Datafname_out)
    shutil.copyfile(Paramfname, Paramfname_out)
    

# sample names can't have an underscore so get rid of it    
def RemoveUnderscoreFromSampleNames(Sample_names):
    
    new_sample_names = []
    for name in Sample_names:
        namelist = name.split("_")
        this_new_name = ""
        for item in namelist:
            this_new_name = this_new_name+item
        new_sample_names.append(this_new_name)
        
        #print "Old name was: "+name+" and new name is: "+ new_sample_names[-1]
    
    return new_sample_names
        
    
# This updates the raster file with an effective shielding
def UpdateRasterWithShielding(path, prefix,Sample_names,Snowshield_values):
    
    #first get directory path into the correct format 
    fmt_path = LSDost.ReformatSeperators(path)
    
    # add the trailing seperator
    fmt_path = LSDost.AppendSepToDirectoryPath(fmt_path) 
    
    # now find the correct file
    fname = fmt_path + prefix+"_CRNRasters.csv"
    
    # also make the outfile
    outfname = fmt_path+prefix+"_SS_CRNRasters.csv"
    outfile = open(outfname, 'w')

    new_lines = []    

    print "The sample names are"
    print Sample_names
    
    print "The snow shield values are: "
    print Snowshield_values

    #See if the parameter files exist
    if os.access(fname,os.F_OK):
        this_file = open(fname, 'r')
        lines = this_file.readlines()
        
        # now get the list of DEM prefixes
        for line in lines:
            this_line = line.split(",")
            DEM_prefix = this_line[0]
            
            print "The DEM prefix is: " + DEM_prefix
            
            # Now get the sample name
            split_dem_prefix = DEM_prefix.split("_")
            sample_name = split_dem_prefix[-1]
            
            print "The sample name is: " + sample_name
            
            # get the index of the sample name to reference the shielding value
            i = Sample_names.index(sample_name)
            
            print "the index of the sample names is: " + str(i) 
            
            # calculate the effective depth. The 160 is the attenuation thickness in g/cm^2
            this_snow_depth = -160*np.log(Snowshield_values[i])
            print "The shielding is: " +str(Snowshield_values[i])+ " and eff_depth is: " + str(this_snow_depth)
            
            # update the snow effective depth
            this_line[1] = str(this_snow_depth)
            
            # update the line
            this_new_line = ",".join(this_line)
            new_lines.append(this_new_line)
            
    # this will get printed to file        
    for line in new_lines: 
        # you have to get rid of the control characters
        this_line = LSDost.RemoveEscapeCharacters(line)
        outfile.write("%s\n" % this_line)  
            

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
        
        # get rid of the first line, since this has header information
        lines.pop(0)
        
        # now get the list of DEM prefixes
        for line in lines:
            this_line = line.split(",")
            SampleName = this_line[0]
            
            print "This line is: "
            print this_line
            
            # check to see if there is a snow shield value
            N_entries= len(this_line)
            if (N_entries == 8):
                SnowShield = float(this_line[7])
                Sample_names.append(SampleName)
                SnowShield_values.append(SnowShield)
            else:
                print "there is no snow shielding on this line"
                SnowShield_values.append(1)
                Sample_names.append(SampleName)

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
    #path = "/home/smudd/SMMDataStore/test_clone/topodata"
    path = "T:\test_clone\topodata"    
    #path = "c:\basin_data\Chile\test_Snow"
    prefix = "SanBern_Spawned"
    GetSnowShieldingFromRaster(path,prefix)   