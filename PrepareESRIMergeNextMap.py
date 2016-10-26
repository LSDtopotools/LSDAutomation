# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 11:28:25 2016


This function looks for adf files in a directory and returns a file with all of the full path names
that can be used with gdal_merge.py

@author: smudd
"""




from glob import glob
#import os


def GetESRIFileNamesNextMap():

    file_list = []    
    
    for DirName in glob("*/"):
        #print DirName
        
        directory_without_slash = DirName[:-1]
        
        this_filename = "./"+DirName+directory_without_slash+"dtme/hdr.adf\n"
        
        print this_filename
        file_list.append(this_filename)
        
    # write the new version of the file
    file_for_output = open("DEM_list.txt",'w')
    file_for_output.writelines(file_list)
    file_for_output.close()      
        
        
        
        
        
        
if __name__ == "__main__":
    GetESRIFileNamesNextMap()
    
