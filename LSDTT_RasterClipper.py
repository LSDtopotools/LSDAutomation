"""
    LSDTT_RasterClipper
    This is a script that takes a header file and clips a larger raster to that header extent.
    It uses GDAL command line tools rather than python command line bindings.
    
    We do this because 
    1) Most of our raster manipulation when preparing papers is done in command line so we want to reproduce that. 
    2) Getting gdal bindings to work requires downloading and installing of a massive number of libraries so this should 
    
    Args:
        Som args
        
    Author: SMM
    Date: 10/11/2017
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys
import subprocess
import argparse
from glob import glob

#=============================================================================
# This is just a welcome screen that is displayed if no arguments are provided.
#=============================================================================
def print_welcome():

    print("\n\n=======================================================================")
    print("Hello! I'm going to transform and clip rasters for you.")
    print("I do this with system calls to GDAL.")
    print("IF YOU DO NOT HAVE GDAL COMMAND LINE TOOLS THIS PROGRAM WILL NOT WORK!")
    print("You need to have the header file and the larger raster in the same directory!")
    print("The command takes three arguments: ")
    print("   i)   The data directory of the files. ")
    print("   ii)  The name of the header file. ")
    print("   iii) The name of the larger raster. ")
    print("For help type:")
    print("   python LSDTT_RasterClipper.py -h\n")
    print("=======================================================================\n\n ")
    
#==============================================================================
# Function to read the original file's projection:
def ReadHeader(FileName):
    """This gets information from the header file

    Args:
        FileName (str): The filename (with path and extension) of the raster.

    Return:
        float: A vector that contains:
            * NDV: the nodata values
            * xsize: cellsize in x direction
            * ysize: cellsize in y direction
            * GeoT: the tranform (a string)
            * Projection: the Projection (a string)
            * DataType: The type of data (an int explaing the bits of each data element)

    Author: SMM
    """

    #See if the parameter files exist
    if not os.access(FileName,os.F_OK):
        raise Exception('[Errno 2] No such file or directory: \'' + FileName + '\'') 
    else:
        this_file = open(FileName, 'r')
        lines = this_file.readlines()
        
        NRows = -9999
        NCols = -9999
        MI_string = "NULL"

        XLL = "NULL"
        YLL = "NULL"
        NorS = "NULL"
        Zone = "NULL"
        dx = "NULL"
        dy = "NULL"
        Xmax = "NULL"
        Ymax = "NULL"
        
        # now get the list of DEM prefixes
        for line in lines:
            
            if "samples" in line:
                line_split = line.split("=")
                NCols = int(line_split[1])
                print("Found samples, they are: " + str(NCols))
            if "lines" in line:
                line_split = line.split("=")
                NRows = int(line_split[1])
                print("Found lines, they are: " + str(NRows))
            if "map info" in line:
                line_split = line.split("=")
                MI_string = line_split[1]
                MI_string = MI_string.split("{")
                MI_string = MI_string[1]
                MI_string = MI_string.split("}")
                MI_string = MI_string[0]                
                print("Found map info string, it is: " + str(MI_string))
                
        # Now parse the MI_string
        if MI_string == "NULL":
            print("I didn't find the map info string. ")
        else:
            MI_string = MI_string.split(",")
            XLL = str(MI_string[3].replace(" ", ""))
            YLL = str(MI_string[4].replace(" ", ""))
            NorS = str(MI_string[8].replace(" ", ""))
            Zone = str(MI_string[7].replace(" ", ""))
            dx = str(MI_string[5].replace(" ", ""))
            dy = str(MI_string[6].replace(" ", ""))
            
            # now get the upper extents
            f_XLL = float(XLL)
            f_YLL = float(YLL)
            f_dx = float(dx)
            f_dy = float(dy)
            
            # Add a bit extra to ensure we get the final row and column
            XUR = f_XLL+ NCols*f_dx+f_dx*0.001
            YUR = f_YLL+NRows*f_dy+ f_dy*0.001
            
            Xmax = str(XUR)
            Ymax = str(YUR)
        
        print("Here are the vitalstatistix: ")
        print([NRows,NCols,XLL,YLL,NorS,Zone,dx,dy,Xmax,Ymax])
        return NRows,NCols,XLL,YLL,NorS,Zone,dx,dy,Xmax,Ymax
            

#==============================================================================

def CreateTransformCall(NRows,NCols,XLL,YLL,NorS,Zone,dx,dy,Xmax,Ymax):
    """
    This function creates the string for a gdal coordinate transofrmation call. 
    It will be fed to a subprocess
    
    Args:
    
    Author: SMM
    Date: 10/11/2017
    """
    
    start_string = "gdalwarp -t_srs \'+proj=utm +zone="
    start_string = start_string+Zone+" +"+NorS+" +datum=WGS84\'"
    start_string = start_string+ " -tr "+dx+" "+dy+" -r cubic"
    
    print("The start string is: "+ start_string)

    
    


#=============================================================================
# This is the main function that runs the whole thing
#=============================================================================
def main(argv):


    # If there are no arguments, send to the welcome screen
    if not len(sys.argv) > 1:
        full_paramfile = print_welcome()
        sys.exit()    
    
    # Get the arguments
    parser = argparse.ArgumentParser()
    # The location of the data files
    parser.add_argument("-dir", "--base_directory", type=str, help="The base directory. If this isn't defined I'll assume it's the same as the current directory.")
    parser.add_argument("-hname", "--header_name", type=str, help="The name of your header file without the path.")
    parser.add_argument("-DEMname", "--DEM_name", type=str, help="The name of your larger DEM. I will clip to this DEM.")
    
    args = parser.parse_args()
    
    # get the base directory
    if args.base_directory:
        this_dir = args.base_directory
        # Make sure the parth ends in a seperator
        if this_dir[-1] != os.sep:
            this_dir = this_dir+os.sep
    else:
        this_dir = os.getcwd()    

    # Get the header files
    these_headers = []
    if not args.header_name:
        print("You didn't give me a header name. I will use all the .hdr files in this directory!")
        
        for FileName in glob(this_dir+"*.hdr"):
            print("Found a header called"+FileName)
            these_headers.append(FileName)
    else:
        these_headers.append(this_dir+os.sep+args.header_name)
        
    # Get the DEM name
    if not args.DEM_name:
        print("You didn't give me a DEM name. Im afraid I need a DEM and am exiting. Please provide one next time.")
        sys.exit()
        
    # Now process the header file
    NRows,NCols,XLL,YLL,NorS,Zone,dx,dy,Xmax,Ymax = ReadHeader(these_headers[0])
    CreateTransformCall(NRows,NCols,XLL,YLL,NorS,Zone,dx,dy,Xmax,Ymax)
     
#=============================================================================
if __name__ == "__main__":
    main(sys.argv[1:])        
        