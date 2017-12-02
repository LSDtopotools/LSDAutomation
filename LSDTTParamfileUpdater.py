# This is a python script that checks LSDTopoTools parameter files
# And then renames the read and write path to be the current path
# @author Simon M Mudd
# @date 30-10-2017
from __future__ import print_function
import os
from glob import glob
import subprocess
import sys

#=============================================================================
# This helper function looks for keywords in .driver and .LSDTT_driver files
# and replaces paths
#=============================================================================
def UpdatePathInParamfile(FileName,ThisPath):

    # Get the contents of the parameter file
    fo = open(FileName, "r")
    lines = fo.readlines()
    fo.close()

    new_lines = []

    for line in lines:
        if "read path: " in line:
            this_line = line.split(": ")
            path = this_line[1]
            #print("Path in this file is: "+path)
            new_line = "read path: "+ThisPath+"\n"
            new_lines.append(new_line)
        elif "write path: " in line:
            this_line = line.split(": ")
            path = this_line[1]
            #print("Path in this file is: "+path)
            new_line = "write path: "+ThisPath+"\n"
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    # Now print the new file
    file_for_output = open(FileName,'w')
    file_for_output.writelines(new_lines)
    file_for_output.close()
#=============================================================================



#=============================================================================
# This is just a welcome screen that is displayed if no arguments are provided.
#=============================================================================
def print_welcome():

    print("\n\n=======================================================================")
    print("Hello there, I am the going to adjust your LSDTT parameter files.")
    print("You will need to tell me what to do.")
    print("If you don't give me arguments I'll adjust every .driver or .param file in this directory.")
    print("If you give me one argument I'll adjust every .driver or .param file in the named directory.")
    print("If you give me two arguments I'll adjust a specific file in a specific directory.")
    print("=======================================================================\n\n ")
#=============================================================================

#=============================================================================
# This is the main function that runs the whole thing
#=============================================================================
def main(argv):

    print("The arguments are: ")
    print(argv)
    
    print("This has length " +str(len(sys.argv)))
    if not argv:
        print("The list is empty")
    
    
    # If there are no arguments, run in this directory
    if not argv:
        print_welcome()
        
        # get the current directory
        this_dir = os.getcwd()
        this_dir = this_dir+os.sep
        print("The directory is: "+this_dir)
               
        for file in glob( this_dir+"*.driver"):
            print("Im updating"+file)
            UpdatePathInParamfile(file,this_dir)
        for file in glob( this_dir+"*.param"):
            print("Im updating"+file)
            UpdatePathInParamfile(file,this_dir) 
        for file in glob( this_dir+"*.LSDTT_driver"):
            print("Im updating"+file)
            UpdatePathInParamfile(file,this_dir) 
            
    elif len(sys.argv) == 2:
        this_dir = sys.argv[1]
        print("I am going to try this directory: "+this_dir)
        
        # Add the seperator at the end. 
        if this_dir[-1] != os.sep:
            print("You forgot the slash at the end of your directory name. Adding.")
            this_dir = this_dir+os.sep
        
        print("The directory is: "+this_dir)  
        if not os.access(this_dir,os.F_OK):
            print("The path doesn't exist. Check your spelling. I am exiting without doing anything.")
            sys.exit()

        for file in glob( this_dir+"*.driver"):
            print("Im updating"+file)
            UpdatePathInParamfile(file,this_dir)
        for file in glob( this_dir+"*.param"):
            print("Im updating"+file)
            UpdatePathInParamfile(file,this_dir) 
        for file in glob( this_dir+"*.LSDTT_driver"):
            print("Im updating"+file)
            UpdatePathInParamfile(file,this_dir)     
        
    elif len(sys.argv) == 3:
        this_dir = sys.argv[1]
        print("I am going to try this directory: "+this_dir)
        
        # Add the seperator at the end. 
        if this_dir[-1] != os.sep:
            print("You forgot the slash at the end of your directory name. Adding.")
            this_dir = this_dir+os.sep
        
        print("The directory is: "+this_dir)  
        if not os.access(this_dir,os.F_OK):
            print("The path doesn't exist. Check your spelling. I am exiting without doing anything.")
            sys.exit()
            
        this_file = sys.argv[2]
        full_filename = this_dir+this_file
        print("Testing the file: "+this_file)
        if not os.access(full_filename,os.F_OK):
            print("The file doesn't exist. Check your spelling. I am exiting without doing anything.")
            sys.exit()  
        
        print("Okay, I am updating the file")
        print("The filename is: "+full_filename)
        print("The directory is: "+this_dir)
        UpdatePathInParamfile(full_filename,this_dir)
              
        
    else:
        this_dir = sys.argv[1]
        print("I am going to try this directory: "+this_dir)
        
        # Add the seperator at the end. 
        if this_dir[-1] != os.sep:
            print("You forgot the slash at the end of your directory name. Adding.")
            this_dir = this_dir+os.sep
        
        print("The directory is: "+this_dir)  
        if not os.access(this_dir,os.F_OK):
            print("The path doesn't exist. Check your spelling. I am exiting without doing anything.")
            sys.exit()
            
        this_file = sys.argv[2]
        full_filename = this_dir+this_file
        print("Testing the file: "+this_file)
        if not os.access(full_filename,os.F_OK):
            print("The file doesn't exist. Check your spelling. I am exiting without doing anything.")
            sys.exit()  
        
        print("Okay, I am updating the file")
        print("The filename is: "+full_filename)
        print("The directory is: "+this_dir)
        UpdatePathInParamfile(full_filename,this_dir)        
    
        
    
#=============================================================================

if __name__ == "__main__":
    main(sys.argv[1:])