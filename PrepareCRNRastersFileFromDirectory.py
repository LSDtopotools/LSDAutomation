# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:41:48 2016

@author: smudd
"""


# This contains the CRNResults object, used for interpreting and plotting
# CRN dat
import LSDOSystemTools as LSDOst
import os
import numpy as np
from glob import glob

def prepare_CRNRasters_file(path,prefix):
    
    # first, make sure path is working
    path = LSDOst.ReformatSeperators(path)
    path = LSDOst.AppendSepToDirectoryPath(path)
    
    # initiate some empty lists
    raster_names = []
    toposhield_names = []
    basin_names = []
    self_shield_names = []
    snow_shield_names = []
    csv_strings =[]
    
    # now check to see if the path exists
    if not os.access(path,os.F_OK):
        print "The path you have chosen: " + path + " does not exist. Try with a new path."
    else:
        
        # now find all the rasters. These all have *.bil in them
        for FileName in glob(path+"*.bil"): 
            
            # now remove the extension from the file
            print "The filename is: " + FileName
            print "Removing the bil extension"
            Prefix = FileName[:-4]
            print "new_filename is" + Prefix
            
            # now we see if the files have shielding rasters
            if Prefix[-3:] == "_SH":
                print "This is a shielding raster"
                toposhield_names.append(Prefix)
            elif Prefix[-7:] == "_snowBL":
                print "This is a snow raster"
                snow_shield_names.append(Prefix)
            elif Prefix[-7:] == "_SnowBL":
                print "This is a snow raster"
                snow_shield_names.append(Prefix)                
            elif Prefix[-9:] == "_snowclip":
                print "This is a snow raster"
                snow_shield_names.append(Prefix)
            elif Prefix[-9:] == "_selfclip":
                print "This is a self raster"
                self_shield_names.append(Prefix)                
            elif Prefix[-7:] == "_BASINS":
                print "This is a basins raster"
                basin_names.append(Prefix)           
            elif Prefix[-7:] == "_HS":
                print "This is a hillshade raster"
            else:
                print "No matching pattern, assuming a DEM"
                raster_names.append(Prefix)
                
        # now print these to a rasters csv file
        for raster_name in raster_names:
            
            this_ts_name = "NULL"
            this_sns_name = "NULL"
            this_slfs_name = "NULL"
            
            # search for toposhield
            # There is probably a more efficient way to do this but it gets the job done
            # Loop through all the toposheidl names and find the one that contains the
            # raster name
            for ts in toposhield_names:
                if raster_name in ts:
                    this_ts_name = ts
                    
            # now the snow shield
            for sns in snow_shield_names:
                if raster_name in sns:
                    this_sns_name = sns          
            
            # now the snow shield
            for slfs in self_shield_names:
                if raster_name in slfs:
                    this_slfs_name = slfs
                    
            if (this_ts_name == "NULL" and this_sns_name == "NULL" and this_slfs_name == "NULL"):
                print "I can't find any other rasters for this DEM: " + raster_name
                this_csv_line = raster_name
            else:
                this_csv_line = raster_name+","
                
                if this_sns_name == "NULL":
                    this_csv_line = this_csv_line+"0,"
                else:
                    this_csv_line = this_csv_line+this_sns_name+","
                
                if this_slfs_name == "NULL":
                    this_csv_line = this_csv_line+"0"
                else:
                    this_csv_line = this_csv_line+this_slfs_name

                if not this_ts_name == "NULL":
                    this_csv_line = this_csv_line+","+this_ts_name

            # low append to the list                    
            csv_strings.append(this_csv_line)
            
        # now print the file
        fname_csv = path+prefix+"_CRNRasters.csv"
        f = open(fname_csv, 'w')
        
        for item in csv_strings:
            print>>f, item
            
        f.close()
    
if __name__ == "__main__":
    #path = "T:\\analysis_for_papers\\Manny_idaho\\HarringCreek"
    path = "C:\\basin_data\\Manny_Idaho\\"    
    prefix = "Idaho"
    prepare_CRNRasters_file(path,prefix)      