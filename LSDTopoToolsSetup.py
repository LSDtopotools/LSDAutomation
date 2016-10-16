# This is a python script for setting up LSDTopoTools on your computer
# It creates a directory structure, clones the appropriate repositories
# And makes the programs. 
# @author Simon M Mudd
# @date 16-10-2016

import os

def LSDTopoToolsSetUp():
    
    # First, we need to find out if we are on vagrant
    home_dir = os.path.expanduser("~")
