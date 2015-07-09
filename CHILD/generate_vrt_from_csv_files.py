# generate_vrt_from_csv_files.py
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# This script looks in a directory designated
# by DataDirectory and then creates a .vrt file for
# each csv file in the directory.  This is then used
# by the script vrt_to_raster.py to create a raster
# from the csv file using GDAL.
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FJC 07/07/15
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


import os
from glob import glob
import subprocess


#DataDirectory =  "/home/smudd/papers/Rahul_Himalaya/Chi_analysis/Mandakini/Junction_76/"
#DataDirectory = "Z:\\CHILD\\CHILD_Fiona\\Runs_n1\\Error_bars\\"
DataDirectory =  "/exports/csce/datastore/geos/users/s0923330/CHILD/CHILD_Fiona/Runs_n1/Error_bars/"

print DataDirectory
#subprocess.call(['ls',DataDirectory,'-l'])

uprate='Up030'


# assigns a number to each iteration (i.e. for every .csv file in the directory)
for FileName in glob(DataDirectory+"*"+uprate+"*.csv"): 

    print "filename is: " + FileName
    
    split_fname = FileName.split('.')
    #print split_fname
    no_sections = len(split_fname) 
    fname_prefix  = split_fname[0]  
    if (no_sections > 2):
        for i in range (1,no_sections-1):
            fname_prefix+= "."+split_fname[i]
    
    print fname_prefix
    
    short_fname = fname_prefix.split('/')
    no_sections = len(short_fname) 
    short_fname = short_fname[no_sections-1]
    
    print short_fname
    
    this_fname = short_fname + '.vrt'
    
    f = open(DataDirectory + this_fname,'w')
    
    lines = []
    
    lines.append('<OGRVRTDataSource>\n')
    lines.append('    <OGRVRTLayer name="'+short_fname +'">\n')
    lines.append('        <SrcDataSource>'+short_fname+'.csv</SrcDataSource>\n')
    lines.append('        <GeometryType>wkbPoint</GeometryType>\n')
    lines.append('        <GeometryField encoding="PointFromColumns" x="X" y="Y" z="Z"/>\n')
    lines.append('    </OGRVRTLayer>\n')
    lines.append('</OGRVRTDataSource>\n')
    
    f.writelines(lines)
    f.close()




