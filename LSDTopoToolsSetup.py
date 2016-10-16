# This is a python script for setting up LSDTopoTools on your computer
# It creates a directory structure, clones the appropriate repositories
# And makes the programs. 
# @author Simon M Mudd
# @date 16-10-2016

import os

def LSDTopoToolsSetUp(WantHomeDirectory = True):
    
    # First, we need to find out if we are on vagrant
    home_dir = os.path.expanduser("~")
    this_dir = os.path.getcwd()
    
    print "You home directory is: "+home_dir
    
    vagrant_str = "vagrant"
    if vagrant_str in home_dir:
        print "You seem to be on a vagrant machine"
        vagrant_switch = True
    else:
        print "You don't seem to be using vagrant."
        if WantHomeDirectory == True:
            print "I am going to install on your home directory, which is here:"
            print home_dir
        else:
            print "You set the WantHomeDirectory to false, so I am going to install here:"
            print this_dir
        
        
    
    
if __name__ == "__main__":
    LSDTopoToolsSetUp() 