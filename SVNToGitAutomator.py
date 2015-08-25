# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:31:39 2015

@author: smudd
"""

#===============================================================================
# This script is for automating the posting of the latest versions of our
# development code. It is a bridge between subversion systems and github
# It 
# 1) Finds all the makefiles in a directory supplied by the user
# 2) Takes all the files that are used in the makefiles and copies them over
#    to the directory in the github folder
# 
# To designate the name of the directory, go to the bottom of this file and
#  change the 
#===============================================================================

import numpy as np
from glob import glob
import LSDOSystemTools as LSDost
import os

def GetRequiredFilesFromFolder(DataDirectory):
    
    #print "Current directory is: " + os.getcwd()   
    
    #Append a closing slash to the data directory if one is not already there
    NewDataDirectory = LSDost.ReformatSeperators(DataDirectory)   
    DataDirectory = LSDost.AppendSepToDirectoryPath(NewDataDirectory)
    
    #print "DataDirectory is (2): " + DataDirectory    

    # Start with a master list of required files
    required_files = []

    # find all the makefiles in the directory
    for FileName in glob(DataDirectory+"*.make"):
        #print "FileName is: " + FileName
        
        # Now you need to find all the sources in the makefile
        f = open(FileName,'r')  # open file
        lines = f.readlines()   # read in the data
        f.close()
        
        # Initiate an empty list that will contain the filenames
        cppfiles = []
        
        # loop through the lines, flag a start where SOURCES line starts
        start_flag = 0
        for line in lines:
            if "SOURCE" in line:
                start_flag = 1
            
            # If there is OBJECTS in the line, stop looking for ".cpp"
            if "OBJECTS" in line:
                start_flag = 0
            
            # Look for .cpp between SOURCES and OBJECTS
            if start_flag == 1:
                if ".cpp" in line:
                    # seperate the line using spaces
                    split_line = line.split(' ')
                    this_item = ""
                    
                    # Go through the split line looking for .cpp
                    for item in split_line:
                        if ".cpp" in item:
                            this_item = item
                            
                            # get rid of the SOURCES
                            new_this_item = this_item.replace("SOURCES=","")
                            
                    #print "This cpp file is: " + new_this_item
                    
                    # get rid of stupid escape characters
                    this_file = LSDost.RemoveEscapeCharacters(new_this_item)
                    
                    cppfiles.append(this_file)
                    
        # now print to screen the files required for this makefile
        #print "The files required for this makefile are: "
        #print cppfiles
        
        # now append to directory...this requires some logic because of the ../ seperators
        for filename in cppfiles:
            
            #print "Filename is: " + filename            
            
            # special logic for the ../ seperator            
            if "../" in filename:
                #print "There is a lower level in this filename, this means it is an object"
                thisfile =  filename.replace("../","")
                thisdirectory = LSDost.RemoveDirectoryLevel(DataDirectory)
                fullfile = thisdirectory+thisfile
                
                fullfile2 = fullfile.replace(".cpp",".hpp")
                required_files.append(fullfile2)
            else:
                fullfile = DataDirectory+filename  
        
            # append to the required files list
            required_files.append(fullfile)
                
    # now thin out the required files to remove duplicates
    nd = set(required_files)
    required_files_noduplicates = list(nd)

    #print "/n/n================================="    
    #print "Required files are: " 
    #print required_files
    #print "--------"
    #print "And removing duplicates:"
    #print required_files_noduplicates
    #print "====================================="
    
    return required_files_noduplicates

def CopyRequiredFilesToGitRepository(ObjectsDirectory,DriverDirectory,TargetDirectory):
    # Make sure directories have slashes at the end
    Od = LSDost.ReformatSeperators(ObjectsDirectory)   
    ObjectsDirectory = LSDost.AppendSepToDirectoryPath(Od)
    Dd = ObjectsDirectory+DriverDirectory
    DriverDirectory = LSDost.AppendSepToDirectoryPath(Dd)
    
    Td = LSDost.ReformatSeperators(TargetDirectory)   
    TargetDirectory = LSDost.AppendSepToDirectoryPath(Td)    
    
    # Check if the directories exist
    if not os.access(ObjectsDirectory,os.F_OK):
        print "The object directory for the code doesn't exist!"
        print "You wanted this directory: " + ObjectsDirectory
        return 0
    if not os.access(ObjectsDirectory,os.F_OK):
        print "The driver directory for the code doesn't exist!"
        print "You wanted this directory: " + DriverDirectory
        return 0        
    if not os.access(ObjectsDirectory+"TNT"+os.sep,os.F_OK):
        print "The TNT directory for the code doesn't exist!"
        print "You wanted this directory: " + ObjectsDirectory+"TNT"+os.sep
        return 0 
        
    if not os.access(TargetDirectory,os.F_OK):
        print "The target directory for the code doesn't exist!"
        print "You wanted this directory: " + TargetDirectory
        print "I am making that now"
        #os.mkdir(TargetDirectory)
         

    # Now get the required files
    print "================================="
    print "I am getting the files from all the .make files in this directory:"
    print DriverDirectory
    required_files_noduplicates = GetRequiredFilesFromFolder(DriverDirectory) 
    print "The files are: "
    print required_files_noduplicates

    # loop through these files, collecting the filenames and directory names
    # first you need to know what directory level the driver files are in
    print "\n\n\n======================================"
    n_level_of_driver_directory = LSDost.GetPathLevel(DriverDirectory)
    for FileName in required_files_noduplicates:
        # you need to know what level the file is
        ThisPath = LSDost.GetPath(FileName)
        ThisLevel = LSDost.GetPathLevel(ThisPath)
        
        #if it is the same level as the driver directory, it is in the driver directory!
        if ThisLevel == n_level_of_driver_directory:        
            CopyDirectory = TargetDirectory+DriverDirectory+os.sep
            CopyFileName = LSDost.GetFileNameNoPath(FileName)
            CopyFileNameWithPath = CopyDirectory+CopyFileName
        else:
            CopyDirectory = TargetDirectory
            CopyFileName = LSDost.GetFileNameNoPath(FileName)
            CopyFileNameWithPath = CopyDirectory+CopyFileName            
            
        print "The filename is: " + FileName
        print "The copy filename is: " + CopyFileNameWithPath   
    print "=============================================="             
                    


if __name__ == "__main__":
    # YOU NEED TO MODIFY THIS DIRECTORY
    
    # THis one is for running in windows
    ObjectsDirectory = 'T:\devel_projects\LSDTopoTools\trunk'
    DriverDirectory = 'driver_functions_MuddChi2014'
    TargetDirectory = 'T:\Git_projects\LSDTopoTools_ChiMudd2014'
    
    CopyRequiredFilesToGitRepository(ObjectsDirectory,DriverDirectory,TargetDirectory)    
    
    
    #DataDirectory =  'T:\devel_projects\LSDTopoTools\trunk\driver_functions_MuddChi2014'
    # THis one is for running directly in linux    
    #DataDirectory =  '/home/smudd/SMMDataStore/devel_projects/LSDTopoTools/trunk/driver_functions_MuddChi2014'        
    #required_files_noduplicates = GetRequiredFilesFromFolder(DataDirectory)   
    
    #print required_files_noduplicates