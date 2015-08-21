#==============================================================================
# These are some scripts for testing the functionality of LSDMappingTools
#==============================================================================
# -*- coding: utf-8 -*-
"""
Created on 9 July 2015

@author: smudd
"""

import numpy as np
import LSDOSystemTools as LSDost

def TestOSTools():
    
    path1 = "C://basin_data//Chile//lat26p0//"
    path2 = "M:/Yo/ma/yoyo.ma"
    path3 = "/home/smudd/devel_projects/LSDTopoTools/branches/LSDModel"
    path4 = "C:\\basin_data\\Chile\\lat26p0\\heyJude_DEM.flt"
    
    
    newpath1 = LSDost.ReformatSeperators(path1)
    print "Old path: " + path1   
    print "New path: " + newpath1
    
    newpath2 = LSDost.ReformatSeperators(path2)
    print "Old path: " + path2   
    print "New path: " + newpath2

    newpath3 = LSDost.ReformatSeperators(path3)
    print "Old path: " + path3   
    print "New path: " + newpath3

    newpath4 = LSDost.ReformatSeperators(path4)
    print "Old path: " + path4   
    print "New path: " + newpath4

    # test the directory adder
    # test the directory adder
    print "\n\n"
    newpath = LSDost.AppendSepToDirectoryPath(path1)  
    print "Sep appended path is: " + newpath    
    
    print "\n\n"
    newpath = LSDost.AppendSepToDirectoryPath(path3)  
    print "Sep appended path is: " + newpath
    
    # Test the file prefix grabber
    fprefix = LSDost.GetFilePrefix(path4)
    print "\n\n"
    print "File prefix is: "+ fprefix 
    
    
    # Test the remove path level
    print "\n\n"
    print "Removing a directory level from: " + newpath
    newnewpath = LSDost.RemoveDirectoryLevel(newpath)
    print "The new directory is: " + newnewpath 
    
if __name__ == "__main__":
    TestOSTools()     