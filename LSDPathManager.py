# This is a python script for setting up LSDTopoTools on your computer
# It creates a directory structure, clones the appropriate repositories
# And makes the programs. 
# @author Simon M Mudd
# @date 16-10-2016

import os
import subprocess  
from glob import glob
 
def get_LSDTT_package_list():
    """
    This is just a list of the LSDTT release packages. It is later
    used to look for release pakages
    
    Author: SMM
    
    Date: 02/12/2017
    """
    
    LSDTT_release_list = []
    LSDTT_release_list.append("LSDTopoTools_AnalysisDriver/Analysis_driver")
    LSDTT_release_list.append("LSDTopoTools_ChannelExtraction/driver_functions_ChannelExtraction")
    LSDTT_release_list.append("LSDTopoTools_ChiMudd2014/driver_functions_ChiMudd2014")
    LSDTT_release_list.append("LSDTopoTools_CRNBasinwide/driver_functions_CRNBasinwide")

    return LSDTT_release_list
 
def find_base_directory():
    """
    This finds the base directory of LSDTopoTools. It looks for the home directory. 
    
    Author: SMM
    
    Date: 02/12/2017
    """
    # First, we need to find out if we are on vagrant
    home_dir = os.path.expanduser("~")
    this_dir = os.getcwd()
    the_base_directory = home_dir+"/"
    
    print "\n\nI am going to figure out where you have LSDTopoTools."
    print "Your home directory is: "+home_dir
    
    # Now we go through some logic that tests if we are in a vagrant machine
    vagrant_str = "vagrant"
    if vagrant_str in home_dir:
        print "You seem to be on a vagrant machine"
        vagrant_switch = True
        the_base_directory = "/"
    else:
        print "You don't seem to be using vagrant. \nI will assume LSDTopoTools is installed in your home directory."
        
    return the_base_directory

def Update_paths():
    """
    This loops through the differen LSDTT releases and updates the path for the session.  
    
    Author: SMM
    
    Date: 02/12/2017
    """   
    # First find the base directory
    the_base_directory = find_base_directory()
    print("The base directory is: "+ the_base_directory)
    
    # now get the list of paths
    LSDTT_release_list = get_LSDTT_package_list()

    # Loop through the releases. 
    for release_dir in LSDTT_release_list:
        
        # Get the release path
        this_path_to_release = the_base_directory+"LSDTopoTools/Git_projects/"+release_dir
        print("Checking to see if the path:")
        print(this_path_to_release)
        print("Exists")
        
        # See if the path exists
        if os.access(this_path_to_release,os.F_OK):
            print "Path exists. I will add it to the session path."
        
            path_command_1 = "PATH=$PATH:"+this_path_to_release
            path_command_2 = ["export", "PATH"]
            path_command_3 = ["echo", "$PATH"]
            
            print(path_command_1)
            print(path_command_2)
            print(path_command_3)
            
            subprocess.call(path_command_3)
        
        
            # Now call the subprocess
            subprocess.call(path_command_1) 
            subprocess.call(path_command_2)
            subprocess.call(path_command_3)
            
        else:
            print("This path doesn't exist")
    
    
if __name__ == "__main__":
    Update_paths() 