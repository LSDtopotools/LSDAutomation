#==============================================================================
# ManageShieldingComputation.py
# This script is to manage computation of shielding for CRN calculations
# 
# Shielding is extremely computationally expensive and this package tries to 
# break it into small chunks
#
# It reads the DEMs from which shielding will be calculated and then 
# breaks the parameter files into smaller parameter files that can be run
# seperately
# 
# @author smm
# @date 15-02-2015
#==============================================================================

import os
import subprocess
import LSDOSystemTools as LSDost

# You need to put the LSDMappingTools.py script into the working folder
# Get it from GitHub: https://github.com/LSDtopotools/LSDMappingTools
import LSDMappingTools as LSDmt

# This manages the computation of shielding by seperating the shielding calculations
# into seperate jobs
# NJobs is the number of Jobs you want to set. 
def ManageShieldingComputation(path,prefix,NJobs):
    
    # Do some housekeeping with the path names    
    LSDost.ReformatSeperators(path)
    LSDost.AppendSepToDirectoryPath(path)
    
    # Now open the csv files
    LSDRasters_fname = path+prefix+"_CRNRasters.csv"
    LSDData_fname = path+prefix+"_CRNData.csv"
    LSDParams_fname = path+prefix+".CRNParam"
    
    # And a command prompt fname this can be cut and paste into the command prompt
    LSDCommandPromt_fname = path+prefix+"_ShieldCommandPrompt.txt"
    
    # now go through the rasters listed, getting the n_nodes in each raster
    if os.access(LSDRasters_fname,os.F_OK):
        
        # this is the total lnumber of pixels to be analysed
        Ntotal_pixels = 0
        
        # open the file and get the data       
        Raster_file = open(LSDRasters_fname, 'r')
        lines = Raster_file.readlines()
        
        npixels_in_DEMs = []
        n_cum_pixels = []
        
        # loop through the file, collecting basin data
        for line in lines:
            split_line = line.split(",")
            basin_fname = split_line[0]
            
            # Add to the total number of pixels in the file            
            # IMPORTANT: it is assumed all files are in ENVI bil format
            npixels_in_DEMs.append(LSDmt.GetNPixelsInRaster(basin_fname+".bil"))
            Ntotal_pixels = Ntotal_pixels + npixels_in_DEMs[-1]
            n_cum_pixels.append(Ntotal_pixels) 
         
        print "The total number of pixels are: " + str(Ntotal_pixels)         
         
        # now go back through the loop, setting the seperation
        TargetPixels = Ntotal_pixels/NJobs
        #Next_Target = TargetPixels
        curr_line = 0
        pixels_so_far = 0
        breaks = []    # these are the indices into the breaks
        for line in lines:
            pixels_so_far = pixels_so_far+npixels_in_DEMs[curr_line]
            
            # if the number of pixels exceeds the target pixels, 
            # this raster is not included
            if pixels_so_far > TargetPixels:
                breaks.append(curr_line+1)
                pixels_so_far = 0
                
            curr_line = curr_line+1
            
        # now print out the details
        print "The target pixels are: "+str(TargetPixels)
        print "the pixels are: "
        print npixels_in_DEMs
        
        print "\nThe breaks are: "
        if len(breaks) > NJobs:
            breaks.pop()
            
        if len(breaks) < NJobs:
            breaks.append(len(lines))
        
        print breaks

        # now spawn the files
        Param_file = open(LSDParams_fname, 'r')
        Plines = Param_file.readlines() 
        Param_file.close()
        
        Data_file = open(LSDData_fname, 'r')  
        Dlines = Data_file.readlines() 
        Data_file.close()        
        
        # make the command prompt file
        CP_file = open(LSDCommandPromt_fname,'w')
        CP_file.write("Commands for running shielding calculations from command line.\n")
        CP_file.write("To be used with the University of Edinburgh's basinwide CRN programs.\n")
        CP_file.write("These are designed for use on a cluster without a job management system.\n")
        CP_file.write("If you want to use qsub you will need to write your own script!\n")
        CP_file.write("Copy and paste these into the command line.\n")
        
        
        bb = 1
        last_brk = 0
        for brk in breaks:
            new_param_name = path+prefix+"_brk"+str(bb)+".CRNParam"
            new_data_name = path+prefix+"_brk"+str(bb)+"_CRNData.csv"
            new_raster_name = path+prefix+"_brk"+str(bb)+"_CRNRasters.csv"
        
            New_Param_file = open(new_param_name, 'w')
            New_Param_file.writelines(Plines)
            New_Param_file.close()
            
            New_Data_file = open(new_data_name, 'w')
            New_Data_file.writelines(Dlines)
            New_Data_file.close()
            
            print "Last break: " + str(last_brk) + " and this break: " + str(brk)            
            
            New_Raster_file = open(new_raster_name,'w')
            thispx = npixels_in_DEMs[last_brk:brk]
            New_Raster_file.writelines(lines[last_brk:brk])
            New_Raster_file.close()
            
            last_brk = brk
                      
            print "these pixels are: "
            print thispx
            print "and sum is: " + str(sum(thispx))
            
            CP_file.write("nohup nice ./Shielding_for_CRN.exe "+path+" "+prefix+"_brk"+str(bb)+"\n")
            bb = bb+1

        CP_file.close()

                

if __name__ == "__main__":
    path = "c:\\basin_data\\Chile\\TestCRN\\"
    prefix = "CRN_chile_Spawned"
    NJobs = 3
    ManageShieldingComputation(path,prefix,NJobs)     