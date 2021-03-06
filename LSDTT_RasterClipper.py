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
            Xmin = str(MI_string[3].replace(" ", ""))
            Ymax = str(MI_string[4].replace(" ", ""))
            NorS = str(MI_string[8].replace(" ", ""))
            Zone = str(MI_string[7].replace(" ", ""))
            dx = str(MI_string[5].replace(" ", ""))
            dy = str(MI_string[6].replace(" ", ""))
            
            # now get the upper extents
            f_Xmin = float(Xmin)
            f_Ymax = float(Ymax)
            f_dx = float(dx)
            f_dy = float(dy)
            
            # Add a bit extra to ensure we get the final row and column
            XLR = f_Xmin + NCols*f_dx + f_dx*0.001
            YLR = f_Ymax - NRows*f_dy - f_dy*0.001
            
            Xmax = str(XLR)
            Ymin = str(YLR)
        
        print("Here are the vitalstatistix: ")
        print([NRows,NCols,Xmin,Ymin,Xmax,Ymax,NorS,Zone,dx,dy])
        return NRows,NCols,Xmin,Ymin,Xmax,Ymax,NorS,Zone,dx,dy
            

#==============================================================================

def CreateTransformCall(NRows,NCols,Xmin,Ymin,Xmax,Ymax,NorS,Zone,dx,dy,data_dir,DEM_name,Header_name):
    """
    This function creates the string for a gdal coordinate transofrmation call. 
    It will be fed to a subprocess
    
    Args:
    
    Author: SMM
    Date: 10/11/2017
    """
    
    start_string = "gdalwarp -t_srs"
    
    projection_string = "+proj=utm +zone="
    projection_string = projection_string+Zone+" +"+NorS+" +datum=WGS84"
    print("The projection_string is: "+ projection_string)
    
    resample_string = "-tr "+dx+" "+dy+" -r cubic"
    
   
    # Now add the extents and format
    extent_string = "-te "+Xmin+" "+Ymin+" "+Xmax+" "+Ymax+" -of ENVI"
    print("Extent string is: ")
    print(extent_string)
    
    # combine these into a list
    start_list = start_string.split(" ")
    resample_list = resample_string.split(" ")
    extent_list = extent_string.split(" ")
    
    full_list = start_list
    full_list.append(projection_string)
    full_list = full_list+resample_list
    full_list = full_list+extent_list
    
    full_list.append(DEM_name)
    
    # Now update the output name
    header_list = Header_name.split(os.sep)
    this_header = header_list[-1]
    print("This header is: "+this_header)
    
    this_header = this_header.split(".")[0]
    
    New_fname = this_header
    New_fname = New_fname+"_Clip.bil"
    print("The new filename is: ")
    print(New_fname)
    
    new_full_file = data_dir+New_fname
    full_list.append(new_full_file)
    
    
    print("The full list is")
    print(full_list)
    
    return full_list
#=============================================================================    
    
    


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
    else:
        this_DEM = this_dir+args.DEM_name
        
    # Now process the header file
    NRows,NCols,XLL,YLL,NorS,Zone,dx,dy,Xmax,Ymax = ReadHeader(these_headers[0])
    system_call_list = CreateTransformCall(NRows,NCols,XLL,YLL,NorS,Zone,dx,dy,Xmax,Ymax, this_dir, this_DEM, these_headers[0])
    
    # now call GDAL
    print("I am going to call GDAL.")
    print("You need to have GDAL the gdal command line tools installed for this to work!")
    subprocess.call(system_call_list)
     
#=============================================================================
if __name__ == "__main__":
    main(sys.argv[1:])        
        